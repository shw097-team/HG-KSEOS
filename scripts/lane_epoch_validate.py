#!/usr/bin/env python3
"""lane_epoch_validate.py — fail-closed validator for the lane epoch and arm-retirement plane.

The owner order of 2026-11-09 admitted `opencode-go/mimo-v2.6-flash` to the PLAN pool at rank 4 and retired
`opencode-go/mimo-v2.6-pro`. A retirement that exists only as prose in `authorization_basis` is a suggestion:
the arm stays one copy-paste away from being selectable. This validator reads the three live control-plane
files and REFUSES when the epoch, the pools and the retirement disagree.

Inputs (relative to `--root`, default: the repository this script lives in):

    config/lane-routing-registry.yaml        authority  — epoch, status, contract_epoch, retired_arms, routes
    config/lane-route-slots.candidate.json   projection — lanes[].ordered_pool[]
    config/model-lane-assignment.json        projection — lane_chains{} and the source_of_routes digest pin

Standard library only. The registry is YAML, and this tool does NOT depend on PyYAML: it walks the file with a
restricted line grammar (top-level `key:` sections, the `routes:` route table, the `retired_arms:` map,
`source_of_routes:` scalars). A file whose `routes:` section cannot be read at all is refused as
REGISTRY_UNPARSEABLE rather than half-understood — silent partial parsing is how a validator becomes a
rubber stamp.

Refusal codes (each is named, and each exits 2):

    REGISTRY_UNPARSEABLE   schema is not HGK-LANE-ROUTING-REGISTRY/1, or the routes[] table is empty
    EPOCH_UNPARSEABLE      `epoch` (or `contract_epoch`) is not an integer literal — e.g. `forty-one`
    STATUS_INVALID         `status` is missing or outside {IN_FORCE, CANDIDATE}
    RETIRED_ARM_IN_POOL    the owner-ordered admission slot (PLAN rank 4) still holds a RETIRED arm
    RETIREMENT_DRIFT       a retired arm is live anywhere else: a route arm, a fallback, an ordered_pool
                           entry at another rank, or a lane_chain entry
    SLOT_CHAIN_DIVERGES    a projection's chain is not the registry's chain, rank for rank
    TRANSPORT_MISMATCH     an arm's transport token does not follow its provider's declared vocabulary
                           (openai-codex takes the bare model id; every other provider is provider/model)
    SOURCE_OF_ROUTES_PIN   source_of_routes does not pin the assignment bytes this tree carries, or the
                           pinned revision is not the assignment's revision

Only LIVE surfaces are scanned. `history:`, `change_log:`, `activation_state:`, probes and evidence prose are
records of what was true then, and a retired arm named there is not a drift.

Exit: 0 PASS, 2 REFUSED, 64 usage error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCHEMA = "HGK.LANE-EPOCH-VALIDATE/1"
REGISTRY_SCHEMA = "HGK-LANE-ROUTING-REGISTRY/1"
ALLOWED_STATUS = ("IN_FORCE", "CANDIDATE")
# The owner order of 2026-11-09 names this slot explicitly: PLAN rank 4 = the admitted replacement arm.
ADMISSION_SLOT = ("PLAN", 4)
INT_LITERAL = re.compile(r"^[0-9]+$")

ROUTES_SKIP_KEYS = {
    "lanes", "engine", "role_group", "canonical_identity", "auth", "oauth", "reasoning_effort",
    "selection_authority", "selected_arm", "selected_arm_identity", "admission_status",
    "admission_evidence", "admission_status_prior", "owner_order_20261021", "default",
}


def _unquote(value: str) -> str:
    """YAML scalar -> plain string, for the scalar shapes the control plane actually uses."""
    v = value.strip()
    if len(v) >= 2 and v[0] == "'" and v[-1] == "'":
        return v[1:-1].replace("''", "'")
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return v[1:-1].replace('\\"', '"')
    if v in ("null", "~", ""):
        return ""
    return v


def parse_registry(text: str) -> dict:
    """Read the registry's live surfaces with a restricted line grammar (no PyYAML)."""
    facts = {"scalars": {}, "routes": [], "retired_arms": {}, "source_of_routes": {}}
    section = None
    route = None
    list_key = None
    retired_arm = None

    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()

        # A top-level section header. Route items (`- lane: ...`) are also at column 0 and are not headers.
        if indent == 0 and not line.startswith("- "):
            key, _, value = line.partition(":")
            section = key.strip()
            route = None
            list_key = None
            retired_arm = None
            if section in ("schema", "status", "epoch", "contract_epoch", "claim_ceiling"):
                facts["scalars"][section] = _unquote(value)
            continue

        if section == "retired_arms":
            if indent == 2 and line.endswith(":") and not line.startswith("- "):
                retired_arm = _unquote(line[:-1])
                facts["retired_arms"][retired_arm] = {}
            elif indent >= 4 and retired_arm is not None and not line.startswith("- "):
                key, _, value = line.partition(":")
                facts["retired_arms"][retired_arm][key.strip()] = _unquote(value)
            continue

        if section == "source_of_routes":
            if indent == 2 and not line.startswith("- "):
                key, _, value = line.partition(":")
                facts["source_of_routes"][key.strip()] = _unquote(value)
            continue

        if section != "routes":
            continue

        if indent == 0 and line.startswith("- "):
            key, _, value = line[2:].partition(":")
            if key.strip() != "lane":
                route = None
                continue
            route = {"lane": _unquote(value), "provider": None, "model": None,
                     "transport_model": None, "arms": [], "fallbacks": []}
            facts["routes"].append(route)
            list_key = None
            continue

        if route is None:
            continue

        if indent == 2 and not line.startswith("- "):
            key, _, value = line.partition(":")
            key = key.strip()
            if key in ("provider", "model", "transport_model"):
                route[key] = _unquote(value)
                list_key = None
            elif key in ("arms", "fallbacks"):
                list_key = key
            else:
                list_key = None
            continue

        if indent == 2 and line.startswith("- ") and list_key:
            key, _, value = line[2:].partition(":")
            item = {"provider": None, "model": None}
            if key.strip() in item:
                item[key.strip()] = _unquote(value)
            route[list_key].append(item)
            continue

        if indent >= 4 and list_key and route[list_key] and not line.startswith("- "):
            key, _, value = line.partition(":")
            if key.strip() in ("provider", "model"):
                route[list_key][-1][key.strip()] = _unquote(value)
            continue

    return facts


def transport_for(provider: str, model: str) -> str:
    """The transport token follows the provider's declared vocabulary, never a remembered string."""
    return model if provider == "openai-codex" else f"{provider}/{model}"


def arm_id(provider: str, model: str) -> str:
    return transport_for(provider, model)


def registry_chain(route: dict) -> list[tuple[str, str]]:
    chain = [(route.get("provider") or "", route.get("model") or "")]
    chain += [(a.get("provider") or "", a.get("model") or "") for a in route.get("fallbacks", [])]
    return chain


def digests(blob: bytes) -> dict[str, str]:
    lf = blob.replace(b"\r\n", b"\n")
    crlf = lf.replace(b"\n", b"\r\n")
    return {
        "raw": hashlib.sha256(blob).hexdigest(),
        "lf": hashlib.sha256(lf).hexdigest(),
        "crlf": hashlib.sha256(crlf).hexdigest(),
    }


class Result:
    def __init__(self) -> None:
        self.findings: list[dict] = []
        self.reported_sites: set[tuple[str, str | int]] = set()

    def add(self, code: str, detail: str, site: str = "") -> None:
        self.findings.append({"code": code, "detail": detail, "site": site})

    def codes(self) -> list[str]:
        out: list[str] = []
        for f in self.findings:
            if f["code"] not in out:
                out.append(f["code"])
        return out


def validate(root: Path, registry_path: Path, pool_path: Path, assignment_path: Path) -> dict:
    res = Result()
    inputs: dict[str, str] = {}

    def blob(path: Path) -> bytes | None:
        if not path.exists():
            res.add("REGISTRY_UNPARSEABLE", f"missing input file: {path}", str(path))
            return None
        data = path.read_bytes()
        inputs[str(path)] = hashlib.sha256(data).hexdigest()
        return data

    registry_bytes = blob(registry_path)
    pool_bytes = blob(pool_path)
    assignment_bytes = blob(assignment_path)
    if registry_bytes is None or pool_bytes is None or assignment_bytes is None:
        return {"schema": SCHEMA, "verdict": "REFUSED", "primary_code": "REGISTRY_UNPARSEABLE",
                "codes": res.codes(), "findings": res.findings, "inputs": inputs}

    reg = parse_registry(registry_bytes.decode("utf-8-sig"))
    try:
        pool = json.loads(pool_bytes.decode("utf-8-sig"))
        assignment = json.loads(assignment_bytes.decode("utf-8-sig"))
    except json.JSONDecodeError as exc:
        res.add("SLOT_CHAIN_DIVERGES", f"projection file is not parseable JSON: {exc}")
        return {"schema": SCHEMA, "verdict": "REFUSED", "primary_code": res.codes()[0],
                "codes": res.codes(), "findings": res.findings, "inputs": inputs}

    epoch_raw = reg["scalars"].get("epoch", "")
    contract_raw = reg["scalars"].get("contract_epoch", "")

    # ---- C1 registry shape -------------------------------------------------------------------
    if reg["scalars"].get("schema") != REGISTRY_SCHEMA:
        res.add("REGISTRY_UNPARSEABLE",
                f"schema is {reg['scalars'].get('schema')!r}, expected {REGISTRY_SCHEMA}")
    if not reg["routes"]:
        res.add("REGISTRY_UNPARSEABLE", "routes[] table is empty or unreadable; refusing to guess")

    # ---- C2 epoch must be a number -----------------------------------------------------------
    if not epoch_raw:
        res.add("EPOCH_UNPARSEABLE", "registry declares no `epoch` field")
    elif not INT_LITERAL.match(epoch_raw):
        res.add("EPOCH_UNPARSEABLE", f"epoch {epoch_raw!r} is not an integer literal", "epoch")
    if contract_raw and not INT_LITERAL.match(contract_raw):
        res.add("EPOCH_UNPARSEABLE", f"contract_epoch {contract_raw!r} is not an integer literal",
                "contract_epoch")

    # ---- C3 status ---------------------------------------------------------------------------
    status = reg["scalars"].get("status", "")
    if status not in ALLOWED_STATUS:
        res.add("STATUS_INVALID", f"status {status!r} outside {list(ALLOWED_STATUS)}", "status")

    retired = {k: v for k, v in reg["retired_arms"].items() if k}
    pool_lanes = {lane.get("lane"): lane for lane in pool.get("lanes", []) or []}
    reg_lanes = {r["lane"]: r for r in reg["routes"]}
    chains = (assignment.get("lane_chains") or {})

    # ---- C4 the owner-ordered admission slot -------------------------------------------------
    slot_lane, slot_rank = ADMISSION_SLOT
    slot_entry = None
    for entry in (pool_lanes.get(slot_lane, {}) or {}).get("ordered_pool", []) or []:
        if entry.get("rank") == slot_rank:
            slot_entry = entry
            break
    if slot_entry is None:
        res.add("SLOT_CHAIN_DIVERGES", f"{slot_lane} rank {slot_rank} is absent from the ordered pool",
                f"pool:{slot_lane}[{slot_rank}]")
    else:
        slot_arm = arm_id(slot_entry.get("provider") or "", slot_entry.get("model") or "")
        if slot_arm in retired:
            res.add("RETIRED_ARM_IN_POOL",
                    f"{slot_lane} rank {slot_rank} holds {slot_arm}, which the registry RETIRES "
                    f"(retired_epoch {retired[slot_arm].get('retired_epoch')}, "
                    f"replacement {retired[slot_arm].get('replacement')})",
                    f"pool:{slot_lane}[{slot_rank}]")
            res.reported_sites.add((slot_lane, slot_rank))

    # ---- C5 a retired arm must not be live anywhere else -------------------------------------
    def scan_live(sites: list[tuple[str, str, object]]) -> None:
        for site, lane, rank in sites:
            provider, model = (rank or ("", "")) if isinstance(rank, tuple) else ("", "")
            arm = arm_id(provider, model) if provider or model else ""
            if not arm or arm not in retired:
                continue
            key = (lane, rank if isinstance(rank, int) else -1)
            if key in res.reported_sites:
                continue
            res.reported_sites.add(key)
            res.add("RETIREMENT_DRIFT",
                    f"{arm} is live at {site} but the registry retires it "
                    f"(ordered_by {retired[arm].get('ordered_by')} on {retired[arm].get('ordered_at')})",
                    site)

    sites: list[tuple[str, str, object]] = []
    for lane, route in reg_lanes.items():
        sites.append((f"registry:{lane}:rank1", lane, (route.get("provider") or "", route.get("model") or "")))
        for field in ("arms", "fallbacks"):
            for i, arm in enumerate(route.get(field, []) or []):
                sites.append((f"registry:{lane}:{field}[{i}]", lane,
                              (arm.get("provider") or "", arm.get("model") or "")))
    scan_live(sites)
    for lane, node in pool_lanes.items():
        for entry in node.get("ordered_pool", []) or []:
            arm = arm_id(entry.get("provider") or "", entry.get("model") or "")
            rank = entry.get("rank")
            if arm in retired and (lane, rank) not in res.reported_sites:
                res.reported_sites.add((lane, rank))
                res.add("RETIREMENT_DRIFT",
                        f"{arm} is live at ordered_pool rank {rank} of {lane} but the registry retires it "
                        f"(ordered_by {retired[arm].get('ordered_by')} on {retired[arm].get('ordered_at')})",
                        f"pool:{lane}[{rank}]")
    for lane, chain in chains.items():
        for i, entry in enumerate(chain or []):
            arm = arm_id(entry.get("provider") or "", entry.get("model") or "")
            if arm in retired:
                res.add("RETIREMENT_DRIFT",
                        f"{arm} is live in lane_chains[{lane}][{i}] but the registry retires it",
                        f"assignment:{lane}[{i}]")

    # ---- C6 projections must be the registry's chain, rank for rank ---------------------------
    slots_total = 0
    slots_admitted = 0
    by_lane: dict[str, int] = {}
    distinct: set[str] = set()
    for lane, route in reg_lanes.items():
        want = registry_chain(route)
        got_node = pool_lanes.get(lane)
        if got_node is None:
            res.add("SLOT_CHAIN_DIVERGES", f"{lane} is absent from the ordered slot pool", f"pool:{lane}")
            continue
        got = [(e.get("provider") or "", e.get("model") or "") for e in got_node.get("ordered_pool", []) or []]
        by_lane[lane] = len(got)
        slots_total += len(got)
        for i, arm in enumerate(got):
            distinct.add(arm_id(*arm))
        if got != want:
            first = next((i for i in range(min(len(got), len(want))) if got[i] != want[i]),
                         min(len(got), len(want)))
            res.add("SLOT_CHAIN_DIVERGES",
                    f"{lane} pool is {len(got)} arm(s) and the registry chain is {len(want)}; first difference "
                    f"at rank {first + 1}: pool={got[first] if first < len(got) else None} "
                    f"registry={want[first] if first < len(want) else None}",
                    f"pool:{lane}[{first + 1}]")
        asg = [(e.get("provider") or "", e.get("model") or "") for e in (chains.get(lane) or [])]
        if chains.get(lane) is not None and asg != want:
            res.add("SLOT_CHAIN_DIVERGES",
                    f"lane_chains[{lane}] does not carry the registry chain "
                    f"({len(asg)} arm(s) vs {len(want)})", f"assignment:{lane}")

    # ---- C7 transport token must follow the provider vocabulary ------------------------------
    for lane, node in pool_lanes.items():
        for entry in node.get("ordered_pool", []) or []:
            provider = entry.get("provider") or ""
            model = entry.get("model") or ""
            expected = transport_for(provider, model)
            actual = entry.get("transport_model")
            if actual != expected:
                res.add("TRANSPORT_MISMATCH",
                        f"{lane} rank {entry.get('rank')} declares transport_model {actual!r} for "
                        f"{provider}/{model}; the declared vocabulary requires {expected!r}",
                        f"pool:{lane}[{entry.get('rank')}]")

    # ---- C8 the digest pin behind source_of_routes -------------------------------------------
    sor = reg["source_of_routes"]
    if sor:
        pin = (sor.get("sha256") or "").lower()
        pin_lf = (sor.get("sha256_lf") or "").lower()
        actual_digests = digests(assignment_bytes)
        if pin and pin not in actual_digests.values() and pin != pin_lf:
            res.add("SOURCE_OF_ROUTES_PIN",
                    f"source_of_routes.sha256 {pin[:16]}... pins none of the assignment digests this tree "
                    f"carries (raw {actual_digests['raw'][:16]}..., lf {actual_digests['lf'][:16]}..., "
                    f"crlf {actual_digests['crlf'][:16]}...)", "source_of_routes.sha256")
        elif pin_lf and pin_lf not in actual_digests.values():
            res.add("SOURCE_OF_ROUTES_PIN",
                    f"source_of_routes.sha256_lf {pin_lf[:16]}... pins none of the assignment digests "
                    f"(raw {actual_digests['raw'][:16]}..., lf {actual_digests['lf'][:16]}..., "
                    f"crlf {actual_digests['crlf'][:16]}...)", "source_of_routes.sha256_lf")
        revision = sor.get("revision")
        if revision and str(revision) != str(assignment.get("revision")):
            res.add("SOURCE_OF_ROUTES_PIN",
                    f"source_of_routes.revision {revision!r} != assignment revision "
                    f"{assignment.get('revision')!r}", "source_of_routes.revision")

    codes = res.codes()
    named_sites = {f["site"] for f in res.findings}
    for lane, node in pool_lanes.items():
        for entry in node.get("ordered_pool", []) or []:
            if f"pool:{lane}[{entry.get('rank')}]" not in named_sites:
                slots_admitted += 1

    verdict = "REFUSED" if codes else "PASS"
    return {
        "schema": SCHEMA,
        "verdict": verdict,
        "primary_code": codes[0] if codes else None,
        "codes": codes,
        "epoch": int(epoch_raw) if INT_LITERAL.match(epoch_raw or "") else epoch_raw,
        "contract_epoch": int(contract_raw) if INT_LITERAL.match(contract_raw or "") else contract_raw,
        "status": status,
        "retired_arms": sorted(retired),
        "lanes": sorted(reg_lanes),
        "slots": {
            "total": slots_total,
            "admitted": slots_admitted,
            "by_lane": by_lane,
            "distinct_arms": len(distinct),
        },
        "findings": res.findings,
        "inputs": inputs,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Fail-closed lane epoch + arm retirement validator.")
    ap.add_argument("--root", default=None, help="tree to read (default: this script's repository)")
    ap.add_argument("--registry", default=None, help="override config/lane-routing-registry.yaml")
    ap.add_argument("--pool", default=None, help="override config/lane-route-slots.candidate.json")
    ap.add_argument("--assignment", default=None, help="override config/model-lane-assignment.json")
    ap.add_argument("--json-out", default=None, help="also write the result JSON here")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    registry_path = Path(args.registry) if args.registry else root / "config" / "lane-routing-registry.yaml"
    pool_path = Path(args.pool) if args.pool else root / "config" / "lane-route-slots.candidate.json"
    assignment_path = (Path(args.assignment) if args.assignment
                       else root / "config" / "model-lane-assignment.json")

    if not root.is_dir():
        print(f"root is not a directory: {root}", file=sys.stderr)
        return 64

    result = validate(root, registry_path, pool_path, assignment_path)
    text = json.dumps(result, ensure_ascii=False, indent=1)
    print(text)
    if args.json_out:
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
    if result["verdict"] != "PASS":
        print(f"REFUSED {result['primary_code']}: {len(result['codes'])} code(s) {result['codes']}",
              file=sys.stderr)
        return 2
    print(f"PASS epoch={result['epoch']} slots={result['slots']['admitted']}/{result['slots']['total']} "
          f"retired={result['retired_arms']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
