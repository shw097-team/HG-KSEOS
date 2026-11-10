#!/usr/bin/env python3
"""fhs_entry_guard.py — the MECHANICAL pre-dispatch entry gate for FHS lane work (EC-R26-001).

Why this file exists
--------------------
`fhs_3lm.py --bind/--assert` answers "may this arm be used at this epoch?" but nothing made another
session, a fresh PID or a spawned child CALL it before a dispatch. A line in `AGENTS.md` is a prompt,
not an interception. This module is the interception: a host that spawns a lane must pass
`assert-entry` (binding re-verified from bytes, arm checked against the retirement ledger, the SBL
binding reader consulted BY PATH) and then hold a one-shot run-scoped capability that the dispatcher
CONSUMES before it creates any child.

Division of labour (deliberate; do not grow this file into a router)
--------------------------------------------------------------------
* The **routing decision** is not made here. This module makes no selection, writes no registry and
  keeps no second copy of the pool. It reads `config/lane-routing-registry.yaml` and
  `config/lane-route-slots.candidate.json` for their BYTES (sha256, numeric epoch) and for the
  retirement ledger, and it reads one lane's ordered pool only to name the rank-1 arm when the caller
  did not name an arm.
* The **binding predicate** ("is this binding still admissible?") is NOT re-implemented here. It is
  executed by the single-source reader — `fhs_3lm.py --assert <binding>` — invoked by PATH
  (`--binding-reader`, else `$FHS_3LM_PATH`, else `config/fhs-3lm-path.txt`, else
  `var/fhs-entry/binding-reader-path.txt`). Its refusal codes are MAPPED into this gate's namespace
  (`READER_CODE_MAP`), never guessed.
* This module owns exactly four things the reader cannot be trusted to be complete about on every
  revision: the registry/pool DIGEST the binding was minted against (drift), the retirement ledger
  lookup for the arm about to be spawned, the arm the caller is actually asking for (the binding may
  name a different one), and expiry. Everything else is the reader's verdict, quoted.

Fail-closed codes (each with its own exit status; nothing falls through to a spawn)
----------------------------------------------------------------------------------
    20 FHS_ENTRY_ASSERT_REQUIRED    no --binding supplied, or the file is absent/unreadable
    21 FHS_ENTRY_BINDING_INVALID    not a binding record / tampered / reader refused it / wrong shape
    22 FHS_ENTRY_EPOCH_DRIFT        registry bytes (or its numeric epoch) moved since the binding
    23 FHS_ENTRY_POOL_DRIFT         pool bytes moved since the binding
    24 FHS_ENTRY_RETIRED_ARM        the requested arm is in the retirement ledger
    25 FHS_ENTRY_ARM_MISMATCH       the requested arm is not the bound arm (or the token's arm)
    26 FHS_ENTRY_BINDING_EXPIRED    the binding's own expires_at has passed
    27 FHS_ENTRY_GUARD_UNRESOLVED   the binding reader / HGK control plane could not be resolved
    28 FHS_ENTRY_TOKEN_REQUIRED     no one-shot capability for this run_id (absent or expired)
    29 FHS_ENTRY_TOKEN_CONSUMED     the capability was already spent (replay / re-mint)

Claim ceiling
-------------
A pass here proves that THIS host's declared dispatch path verified a binding and spent a run-scoped
capability before creating a child. It does not bind a desktop-app session and cannot be enforced on
another host that does not adopt this ABI; nothing here makes a model call or contacts a relay.

Exit codes: 0 ok; 2 bad usage (argparse); 20-29 as above.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import sys

SCHEMA = "FHS-ENTRY-GUARD/1"
CAPABILITY_SCHEMA = "FHS-ENTRY-CAPABILITY/1"
BINDING_SCHEMA_HINT = "FHS.3LM.Binding"
ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_ENTRY_DIR = ROOT / "var" / "fhs-entry"
DEFAULT_TTL_SECONDS = 300
READER_TIMEOUT_SECONDS = 180

EXIT_CODES = {
    "FHS_ENTRY_ASSERT_REQUIRED": 20,
    "FHS_ENTRY_BINDING_INVALID": 21,
    "FHS_ENTRY_EPOCH_DRIFT": 22,
    "FHS_ENTRY_POOL_DRIFT": 23,
    "FHS_ENTRY_RETIRED_ARM": 24,
    "FHS_ENTRY_ARM_MISMATCH": 25,
    "FHS_ENTRY_BINDING_EXPIRED": 26,
    "FHS_ENTRY_GUARD_UNRESOLVED": 27,
    "FHS_ENTRY_TOKEN_REQUIRED": 28,
    "FHS_ENTRY_TOKEN_CONSUMED": 29,
}

# The reader's own vocabulary -> this gate's namespace. A code that is not listed is NOT guessed: an
# unlisted refusal is recorded verbatim and becomes FHS_ENTRY_BINDING_INVALID (fail closed, quoted).
READER_CODE_MAP = {
    "EPOCH_DRIFT": "FHS_ENTRY_EPOCH_DRIFT",
    "POOL_DIGEST_DRIFT": "FHS_ENTRY_POOL_DRIFT",
    "HOLD_REGISTRY_POOL_DRIFT": "FHS_ENTRY_POOL_DRIFT",
    "RETIRED_ARM": "FHS_ENTRY_RETIRED_ARM",
    "BINDING_EXPIRED": "FHS_ENTRY_BINDING_EXPIRED",
    "ARM_LEFT_POOL": "FHS_ENTRY_BINDING_INVALID",
    "BINDING_TAMPERED": "FHS_ENTRY_BINDING_INVALID",
    "NOT_IN_LANE_POOL": "FHS_ENTRY_BINDING_INVALID",
    "UNKNOWN_LANE": "FHS_ENTRY_BINDING_INVALID",
    "UNKNOWN_SLOT": "FHS_ENTRY_BINDING_INVALID",
    "ERR_HGK_ROOT_UNRESOLVED": "FHS_ENTRY_GUARD_UNRESOLVED",
    "ERR_EPOCH_UNRESOLVED": "FHS_ENTRY_EPOCH_DRIFT",
}
# Reader exit statuses that are only trustworthy when the reader also printed a code (the legacy
# revision exits 7/6/9 without a `code` field). These make the mapping total for the shipped revisions.
READER_EXIT_MAP = {6: "FHS_ENTRY_BINDING_INVALID", 7: "FHS_ENTRY_EPOCH_DRIFT", 9: "FHS_ENTRY_RETIRED_ARM"}

TZ = datetime.timezone.utc


# ---------------------------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------------------------
def sha256_bytes(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def sha256_file(path) -> str | None:
    try:
        with open(path, "rb") as fh:
            h = hashlib.sha256()
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
            return h.hexdigest()
    except OSError:
        return None


def canonical_digest(body) -> str:
    """sha256 of the canonical form of a record body (sorted keys, no insignificant whitespace)."""
    return sha256_bytes(json.dumps(body, sort_keys=True, separators=(",", ":"),
                                   ensure_ascii=False).encode("utf-8"))


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(TZ)


def iso(dt: datetime.datetime) -> str:
    return dt.astimezone(TZ).isoformat(timespec="seconds")


def parse_iso(text) -> datetime.datetime | None:
    if not isinstance(text, str) or not text.strip():
        return None
    try:
        dt = datetime.datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=TZ)


def read_json(path) -> tuple[dict | None, str | None]:
    try:
        raw = pathlib.Path(path).read_bytes()
    except OSError as exc:
        return None, f"unreadable: {type(exc).__name__}: {exc}"
    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        return None, f"not JSON: {type(exc).__name__}: {exc}"
    if not isinstance(doc, dict):
        return None, f"top-level value is {type(doc).__name__}, not an object"
    return doc, None


# ---------------------------------------------------------------------------------------------
# control-plane bytes: registry (YAML, scanned) + pool (JSON)
# ---------------------------------------------------------------------------------------------
def scan_registry(path) -> dict:
    """Read the registry's BYTES and the few fields the gate owns.

    YAML is not parsed as a whole (PyYAML is not a stdlib dependency and a full parse would be a
    second, competing reader). Only top-level scalars and the two-space keys of the top-level
    `retired_arms:` block are picked up, which is exactly what this gate may decide on: the epoch,
    the status, and the retirement ledger.
    """
    out = {"path": str(path), "sha256": sha256_file(path), "epoch": None, "epoch_raw": None,
           "status": None, "contract_epoch": None, "retired": {}, "error": None}
    try:
        text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        out["error"] = f"unreadable: {type(exc).__name__}: {exc}"
        return out
    in_retired = False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            key, _, value = line.partition(":")
            key = key.strip()
            in_retired = key == "retired_arms"
            if key in ("epoch", "status", "contract_epoch"):
                out[key if key != "epoch" else "epoch_raw"] = value.strip().strip("'\"")
            continue
        if in_retired and line.startswith("  ") and not line.startswith("   ") and ":" in line:
            arm = line.strip().split(":", 1)[0].strip().strip("'\"")
            if arm:
                out["retired"][arm] = out["retired"].get(arm) or {}
    raw = out.pop("epoch_raw", None)
    if isinstance(raw, str) and raw.lstrip("-").isdigit():
        out["epoch"] = int(raw)
    elif raw is not None:
        out["error"] = out["error"] or f"epoch is not numeric: {raw!r}"
        out["epoch"] = raw
    return out


def scan_pool(path) -> dict:
    """Read the pool's BYTES, its numeric epoch, its lanes (rank order) and its retirement ledger."""
    out = {"path": str(path), "sha256": sha256_file(path), "epoch": None, "lanes": {},
           "retired": {}, "error": None}
    doc, err = read_json(path)
    if doc is None:
        out["error"] = err
        return out
    epoch = doc.get("epoch")
    out["epoch"] = epoch if isinstance(epoch, int) and not isinstance(epoch, bool) else None
    if out["epoch"] is None and epoch is not None:
        out["error"] = f"pool epoch is not an integer: {epoch!r}"
    retired = doc.get("retired_arms")
    if isinstance(retired, dict):
        out["retired"] = {str(k): (v if isinstance(v, dict) else {}) for k, v in retired.items()}
    for lane in doc.get("lanes") or []:
        if not isinstance(lane, dict):
            continue
        name = lane.get("lane")
        if not isinstance(name, str):
            continue
        rows = []
        for entry in lane.get("ordered_pool") or []:
            if not isinstance(entry, dict):
                continue
            arm = f"{entry.get('provider')}/{entry.get('model')}"
            rows.append({"arm": arm, "rank": entry.get("rank"),
                         "dispatchable": entry.get("dispatchable") is not False
                         and not str(entry.get("feasibility") or "").startswith(
                             ("UNREACHABLE", "CONFIG_COMPLETE_NOT_ACTIVATED"))})
        out["lanes"][name] = rows
    return out


def resolve_hgk_root(explicit=None) -> tuple[pathlib.Path | None, str]:
    """--hgk-root, then $HGK_ROOT, then config/hgk-root.txt, then this repo (which carries both files)."""
    candidates: list[tuple[pathlib.Path, str]] = []
    if explicit:
        candidates.append((pathlib.Path(explicit), "flag:--hgk-root"))
    env = os.environ.get("HGK_ROOT")
    if env:
        candidates.append((pathlib.Path(env), "env:HGK_ROOT"))
    discovery = ROOT / "config" / "hgk-root.txt"
    if discovery.is_file():
        for line in discovery.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                candidates.append((pathlib.Path(line), f"discovery:{discovery.name}"))
                break
    candidates.append((ROOT, "repo-root"))
    for path, source in candidates:
        if (path / "config" / "lane-routing-registry.yaml").is_file():
            return path.resolve(), source
    return None, "unresolved"


def resolve_reader(explicit=None) -> tuple[pathlib.Path | None, str]:
    """--binding-reader, then $FHS_3LM_PATH, then the two discovery files, else unresolved."""
    candidates: list[tuple[pathlib.Path, str]] = []
    if explicit:
        candidates.append((pathlib.Path(explicit), "flag:--binding-reader"))
    env = os.environ.get("FHS_3LM_PATH")
    if env:
        candidates.append((pathlib.Path(env), "env:FHS_3LM_PATH"))
    for rel in ("config/fhs-3lm-path.txt", "var/fhs-entry/binding-reader-path.txt"):
        path = ROOT / rel
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                candidates.append((pathlib.Path(line), f"discovery:{path.name}"))
                break
    for path, source in candidates:
        if path.is_file():
            return path.resolve(), source
    return None, "unresolved"


# ---------------------------------------------------------------------------------------------
# the binding reader (single-source predicate; called by path only)
# ---------------------------------------------------------------------------------------------
def call_reader(reader: pathlib.Path, binding: pathlib.Path, hgk_root: pathlib.Path) -> dict:
    """Run `<reader> --assert <binding>` and return its raw verdict.

    The reader resolves its own control plane from `--hgk-root` then `$HGK_ROOT`; this gate hands the
    RESOLVED root through `$HGK_ROOT` so the two can never disagree about which bytes are authority
    (and so a reader revision that has no `--hgk-root` flag is not fed an argument it would reject).
    """
    import subprocess

    env = dict(os.environ)
    env["HGK_ROOT"] = str(hgk_root)
    argv = [sys.executable, str(reader), "--assert", str(binding)]
    rec = {"path": str(reader), "argv": argv[1:], "hgk_root_env": str(hgk_root)}
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", env=env, stdin=subprocess.DEVNULL,
                              timeout=READER_TIMEOUT_SECONDS)
    except (OSError, subprocess.SubprocessError) as exc:
        rec.update(exit=None, ok=False, code="FHS_ENTRY_GUARD_UNRESOLVED",
                   detail=f"the binding reader could not be executed: {type(exc).__name__}: {exc}")
        return rec
    rec["exit"] = proc.returncode
    rec["stdout_sha256"] = sha256_bytes((proc.stdout or "").encode("utf-8"))
    body = None
    try:
        body = json.loads(proc.stdout or "")
    except ValueError:
        body = None
    rec["stdout"] = (proc.stdout or "")[:4000]
    if proc.returncode == 0:
        rec.update(ok=True, code=None, detail=None, body=body)
        return rec
    reader_code = None
    if isinstance(body, dict):
        reader_code = body.get("code") or body.get("error") or body.get("first_fail")
    guard_code = READER_CODE_MAP.get(str(reader_code)) or READER_EXIT_MAP.get(proc.returncode)
    if not guard_code:
        # The reader did not REFUSE the binding -- it failed to produce a verdict at all (a traceback, a
        # usage error, an unusable revision). That is a resolution failure in THIS gate's inputs, not
        # evidence about the binding, so it must not be reported as "your binding is invalid".
        rec.update(ok=False, code="FHS_ENTRY_GUARD_UNRESOLVED", reader_code=reader_code,
                   detail=(f"the binding reader at {reader} produced no usable verdict (exit "
                           f"{proc.returncode}, no recognised refusal code); a reader that cannot "
                           f"decide cannot authorize a spawn: "
                           f"{(proc.stderr or proc.stdout or '').strip()[-600:]}"),
                   stderr=(proc.stderr or "")[:2000])
        return rec
    rec.update(ok=False, code=guard_code, reader_code=reader_code,
               detail=(f"the binding reader refused this binding: exit {proc.returncode}, "
                       f"reader code {reader_code!r} -> {guard_code}"),
               stderr=(proc.stderr or "")[:2000])
    return rec


# ---------------------------------------------------------------------------------------------
# binding record access (field LOCATION tolerance only; no predicate here)
# ---------------------------------------------------------------------------------------------
def binding_arm(rec: dict) -> str | None:
    provider, model = rec.get("provider"), rec.get("model")
    if isinstance(provider, str) and isinstance(model, str) and provider and model:
        return f"{provider}/{model}"
    return None


def binding_field(rec: dict, name: str):
    """Read `name` where the shipped binding revisions put it (top level, or nested under `epoch`)."""
    if name in rec:
        return rec[name]
    nested = rec.get("epoch")
    if isinstance(nested, dict) and name in nested:
        return nested[name]
    return None


def binding_id_of(rec: dict) -> str:
    """The record's own binding_id when it declares one, else the digest of its body."""
    declared = rec.get("binding_id")
    if isinstance(declared, str) and len(declared) == 64:
        return declared
    body = {k: v for k, v in rec.items() if k != "binding_id"}
    return canonical_digest(body)


def arm_retirement(arm: str, registry: dict, pool: dict) -> dict | None:
    """The retirement ledger entry for `arm`, if ANY ledger declares it (registry or pool).

    Both ledgers are merged FIELD BY FIELD (registry first, then pool filling gaps): the registry scan
    records the arm names of its `retired_arms:` block without parsing the nested prose, so a field
    the registry copy omits is taken from the pool copy rather than reported as absent.
    """
    hits = []
    for name, ledger in (("registry", registry.get("retired")), ("pool", pool.get("retired"))):
        if isinstance(ledger, dict) and arm in ledger:
            hits.append({"ledger": name, "entry": ledger[arm] if isinstance(ledger[arm], dict) else {}})
    if not hits:
        return None
    merged: dict = {}
    for hit in hits:
        for key, value in (hit["entry"] or {}).items():
            if merged.get(key) in (None, "", {}) and value not in (None, ""):
                merged[key] = value
    return {"arm": arm, "ledgers": hits, "replacement": merged.get("replacement"),
            "reason": merged.get("reason"), "retired_epoch": merged.get("retired_epoch"),
            "ordered_by": merged.get("ordered_by")}


# ---------------------------------------------------------------------------------------------
# the gate
# ---------------------------------------------------------------------------------------------
def gate_entry(binding=None, lane: str = "", arm=None, hgk_root=None, reader=None,
               require_bound: bool = False, now: datetime.datetime | None = None) -> tuple[int, dict]:
    """Re-verify the binding for `lane` and decide whether `arm` may enter. Returns (exit, record).

    `exit == 0` is the ONLY value on which a caller may create a child. Every other value carries a
    named code from EXIT_CODES plus the check list that produced it.
    """
    now = now or utc_now()
    rec: dict = {"schema": SCHEMA, "ok": False, "code": None, "detail": None,
                 "generated_utc": iso(now), "lane": lane, "arm": arm, "checks": []}

    def fail(code: str, detail: str, **extra) -> tuple[int, dict]:
        rec.update(ok=False, code=code, detail=detail, **extra)
        rec["check"] = code
        return EXIT_CODES[code], rec

    def note(cid: str, ok: bool, **extra) -> None:
        rec["checks"].append({"id": cid, "ok": ok, **extra})

    # 1. the binding must exist ---------------------------------------------------------------
    if not binding:
        note("binding_present", False, reason="no --binding supplied")
        return fail("FHS_ENTRY_ASSERT_REQUIRED",
                    "no --binding was supplied; a fresh process has no session binding, and an "
                    "unbound run must not reach a spawn")
    bpath = pathlib.Path(binding)
    if not bpath.is_file():
        note("binding_present", False, reason=f"absent: {bpath}")
        return fail("FHS_ENTRY_ASSERT_REQUIRED", f"the binding file is absent: {bpath}")
    brec, berr = read_json(bpath)
    if brec is None:
        note("binding_parse", False, reason=berr)
        return fail("FHS_ENTRY_BINDING_INVALID", f"{bpath}: {berr}")
    rec["binding_path"] = str(bpath)
    rec["binding_sha256"] = sha256_file(bpath)
    rec["binding_id"] = binding_id_of(brec)
    rec["binding_run_id"] = binding_field(brec, "run_id")
    rec["binding_session_id"] = binding_field(brec, "session_id")
    note("binding_parse", True, binding_id=rec["binding_id"], run_id=rec.get("binding_run_id"))

    # 2. the control plane (registry + pool) must resolve -------------------------------------
    root, root_source = resolve_hgk_root(hgk_root)
    if root is None:
        note("hgk_root", False, reason="unresolved")
        return fail("FHS_ENTRY_GUARD_UNRESOLVED",
                    "the HGK control plane could not be resolved (no --hgk-root, no $HGK_ROOT, no "
                    "config/hgk-root.txt, and this repo carries no config/lane-routing-registry.yaml)")
    registry = scan_registry(root / "config" / "lane-routing-registry.yaml")
    pool = scan_pool(root / "config" / "lane-route-slots.candidate.json")
    rec.update(hgk_root=str(root), hgk_root_source=root_source,
               registry={k: registry[k] for k in ("path", "sha256", "epoch", "status",
                                                  "contract_epoch", "error")},
               pool={k: pool[k] for k in ("path", "sha256", "epoch", "error")})
    if not registry["sha256"] or not pool["sha256"]:
        note("control_plane_readable", False, registry=registry["error"], pool=pool["error"])
        return fail("FHS_ENTRY_GUARD_UNRESOLVED",
                    f"the control plane at {root} is unreadable: registry={registry['error']!r} "
                    f"pool={pool['error']!r}")
    note("control_plane_readable", True, epoch=registry["epoch"], pool_epoch=pool["epoch"])

    # 3. arm under test: the caller's, else the lane's rank-1 pool arm ------------------------
    arm_source = "flag:--arm"
    if not arm:
        rank1 = next((r for r in pool["lanes"].get(lane, []) if r["dispatchable"]), None)
        arm = rank1["arm"] if rank1 else None
        arm_source = "derived:pool-rank-1"
    rec["arm_source"] = arm_source
    if not arm:
        note("arm_resolved", False, reason=f"no arm for lane {lane}")
        return fail("FHS_ENTRY_ARM_MISMATCH",
                    f"no arm was named and lane {lane!r} has no dispatchable pool arm at {pool['path']}")
    rec["arm"] = arm
    note("arm_resolved", True, arm=arm, arm_source=arm_source)

    # 4. epoch drift: registry bytes (and numeric epoch) the binding was minted against --------
    bound_registry_sha = binding_field(brec, "registry_sha256")
    if not bound_registry_sha:
        note("registry_digest_present", False, reason="the binding records no registry_sha256")
        return fail("FHS_ENTRY_BINDING_INVALID",
                    f"the binding {bpath} records no registry_sha256, so no epoch can be verified; "
                    f"a binding that cannot name its epoch is not evidence")
    if bound_registry_sha != registry["sha256"]:
        note("registry_digest", False, bound=bound_registry_sha, now=registry["sha256"])
        return fail("FHS_ENTRY_EPOCH_DRIFT",
                    f"the registry bytes moved since the binding was minted: bound "
                    f"{bound_registry_sha[:16]}..., now {registry['sha256'][:16]}... "
                    f"({registry['path']})")
    bound_epoch = binding_field(brec, "policy_epoch")
    if bound_epoch is None:
        bound_epoch = binding_field(brec, "epoch")
    # a binding that nests its epoch record under `epoch` also names its numeric epoch there
    if isinstance(bound_epoch, dict):
        bound_epoch = bound_epoch.get("policy_epoch")
    if bound_epoch is not None and registry["epoch"] is not None and bound_epoch != registry["epoch"]:
        note("registry_epoch", False, bound=bound_epoch, now=registry["epoch"])
        return fail("FHS_ENTRY_EPOCH_DRIFT",
                    f"the binding was minted at epoch {bound_epoch!r} but the registry declares "
                    f"{registry['epoch']!r}")
    note("registry_digest", True, sha256=registry["sha256"], epoch=registry["epoch"])

    # 5. pool drift: the pool bytes the binding was minted against -----------------------------
    bound_pool_sha = binding_field(brec, "pool_sha256")
    if not bound_pool_sha:
        note("pool_digest_present", False, reason="the binding records no pool_sha256")
        return fail("FHS_ENTRY_BINDING_INVALID",
                    f"the binding {bpath} records no pool_sha256, so the pool it was admitted "
                    f"against cannot be identified")
    if bound_pool_sha != pool["sha256"]:
        note("pool_digest", False, bound=bound_pool_sha, now=pool["sha256"])
        return fail("FHS_ENTRY_POOL_DRIFT",
                    f"the pool bytes moved since the binding was minted: bound "
                    f"{bound_pool_sha[:16]}..., now {pool['sha256'][:16]}... ({pool['path']})")
    note("pool_digest", True, sha256=pool["sha256"])

    # 6. the requested arm must not be retired (registry ledger AND pool ledger) --------------
    retired = arm_retirement(arm, registry, pool)
    if retired:
        note("retirement_ledger", False, **retired)
        return fail("FHS_ENTRY_RETIRED_ARM",
                    f"the arm {arm} is RETIRED ({retired['reason'] or 'no reason recorded'}); "
                    f"replacement is {retired['replacement']!r}; a retired arm is never selectable",
                    retirement=retired)
    note("retirement_ledger", True, arm=arm)

    # 7. expiry -------------------------------------------------------------------------------
    expires_at = parse_iso(binding_field(brec, "expires_at"))
    if expires_at is not None and expires_at <= now:
        note("binding_expiry", False, expires_at=iso(expires_at), now=iso(now))
        return fail("FHS_ENTRY_BINDING_EXPIRED",
                    f"the binding expired at {iso(expires_at)} (now {iso(now)}); a binding is a "
                    f"time-bounded fact, not a standing permission")
    note("binding_expiry", True, expires_at=iso(expires_at) if expires_at else None)

    # 8. the arm actually being entered must be the bound arm ---------------------------------
    bound_arm = binding_arm(brec)
    if bound_arm is None:
        note("bound_arm_present", False, reason="the binding names no provider/model")
        return fail("FHS_ENTRY_BINDING_INVALID",
                    f"the binding {bpath} names no provider/model, so no arm can be matched")
    if bound_arm.strip().lower() != str(arm).strip().lower():
        note("arm_match", False, bound=bound_arm, requested=arm)
        return fail("FHS_ENTRY_ARM_MISMATCH",
                    f"the binding authorizes {bound_arm} but this entry asks for {arm}; the token "
                    f"must name the arm that will be spawned")
    note("arm_match", True, arm=bound_arm)

    # 9. --require-bound: the record must carry what makes it a HARD-entry binding ------------
    if require_bound:
        missing = [f for f in ("run_id", "session_id") if not binding_field(brec, f)]
        if not isinstance(brec.get("binding_id"), str):
            missing.append("binding_id")
        if missing:
            note("require_bound", False, missing=missing)
            return fail("FHS_ENTRY_BINDING_INVALID",
                        f"--require-bound is set and the binding omits {missing}; a lane-wide "
                        f"default is not a run-scoped binding")
        note("require_bound", True, run_id=binding_field(brec, "run_id"))
    else:
        note("require_bound", True, enforced=False)

    # 10. the single-source predicate: the SBL binding reader, by PATH ------------------------
    reader_path, reader_source = resolve_reader(reader)
    rec["reader_source"] = reader_source
    if reader_path is None:
        note("reader_resolved", False, reason="unresolved")
        return fail("FHS_ENTRY_GUARD_UNRESOLVED",
                    "--binding-reader was not supplied and no discovery file / $FHS_3LM_PATH "
                    "names the SBL reader; this gate will not re-implement the binding predicate")
    verdict = call_reader(reader_path, bpath, root)
    rec["reader"] = verdict
    note("reader_resolved", True, path=str(reader_path), source=reader_source)
    if not verdict.get("ok"):
        return fail(verdict.get("code") or "FHS_ENTRY_BINDING_INVALID",
                    verdict.get("detail") or "the binding reader refused this binding",
                    reader=verdict)
    note("reader_assert", True, exit=verdict.get("exit"))

    rec.update(ok=True, code=None, detail=None, check="PASS")
    return 0, rec


# ---------------------------------------------------------------------------------------------
# one-shot run-scoped capability
# ---------------------------------------------------------------------------------------------
def capability_path(entry_dir, run_id: str) -> pathlib.Path:
    return pathlib.Path(entry_dir or DEFAULT_ENTRY_DIR) / f"{run_id}.json"


def spent_marker(entry_dir, run_id: str) -> pathlib.Path:
    return pathlib.Path(entry_dir or DEFAULT_ENTRY_DIR) / f"{run_id}.spent"


def mint_capability(run_id: str, token: str, lane: str, arm: str, gate: dict,
                    entry_dir=None, ttl: int = DEFAULT_TTL_SECONDS,
                    now: datetime.datetime | None = None) -> tuple[int, dict]:
    """Write `var/fhs-entry/<run_id>.json` with O_CREAT|O_EXCL. One run_id, one capability."""
    now = now or utc_now()
    if not run_id:
        return 28, {"schema": CAPABILITY_SCHEMA, "ok": False, "code": "FHS_ENTRY_TOKEN_REQUIRED",
                    "detail": "--guard-token needs --run-id: the capability is keyed by the run it "
                              "authorizes, and a token nobody can look up authorizes nothing"}
    path = capability_path(entry_dir, run_id)
    if path.exists():
        return 29, {"schema": CAPABILITY_SCHEMA, "ok": False, "code": "FHS_ENTRY_TOKEN_CONSUMED",
                    "detail": f"a capability already exists for run_id {run_id!r} at {path}; a "
                              f"second mint would be a replay of a spent run scope",
                    "path": str(path)}
    path.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "schema": CAPABILITY_SCHEMA,
        "run_id": run_id, "token": token,
        "lane": lane, "arm": arm,
        "binding_path": gate.get("binding_path"), "binding_id": gate.get("binding_id"),
        "binding_sha256": gate.get("binding_sha256"),
        "registry_sha256": (gate.get("registry") or {}).get("sha256"),
        "pool_sha256": (gate.get("pool") or {}).get("sha256"),
        "minted_by_pid": os.getpid(), "minted_at": iso(now),
        "expires_at": iso(now + datetime.timedelta(seconds=int(ttl))),
        "ttl_seconds": int(ttl), "spent": False,
        "scope": "one dispatch run; consumed by scripts/hgk-lane-dispatch.py before any child",
    }
    body["capability_id"] = canonical_digest(body)
    payload = (json.dumps(body, indent=1, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        return 29, {"schema": CAPABILITY_SCHEMA, "ok": False, "code": "FHS_ENTRY_TOKEN_CONSUMED",
                    "detail": f"the capability for run_id {run_id!r} appeared while minting "
                              f"(O_EXCL); refusing a replay", "path": str(path)}
    except OSError as exc:
        return 27, {"schema": CAPABILITY_SCHEMA, "ok": False, "code": "FHS_ENTRY_GUARD_UNRESOLVED",
                    "detail": f"the capability file could not be created at {path}: {exc}",
                    "path": str(path)}
    try:
        os.write(fd, payload)
    finally:
        os.close(fd)
    return 0, {"schema": CAPABILITY_SCHEMA, "ok": True, "code": None, "path": str(path),
               "capability": body}


def consume_capability(run_id=None, lane=None, arm=None, entry_dir=None, binding_path=None,
                       now: datetime.datetime | None = None) -> tuple[int, dict]:
    """Spend the run's capability. A second spend is refused: the `.spent` marker is the atomic claim."""
    now = now or utc_now()
    if not run_id:
        return 28, {"schema": CAPABILITY_SCHEMA, "ok": False, "code": "FHS_ENTRY_TOKEN_REQUIRED",
                    "detail": "no --fhs-entry-token was supplied for this run; the dispatcher does "
                              "not spawn without a one-shot capability minted by assert-entry",
                    "entry_dir": str(entry_dir or DEFAULT_ENTRY_DIR)}
    path = capability_path(entry_dir, run_id)
    rec: dict = {"schema": CAPABILITY_SCHEMA, "path": str(path), "run_id": run_id}
    if not path.is_file():
        return 28, {**rec, "ok": False, "code": "FHS_ENTRY_TOKEN_REQUIRED",
                    "detail": f"no capability exists for run_id {run_id!r} at {path}; the entry "
                              f"was never asserted for this run"}
    body, err = read_json(path)
    if body is None:
        return 21, {**rec, "ok": False, "code": "FHS_ENTRY_BINDING_INVALID",
                    "detail": f"the capability file is not a readable record: {err}"}
    rec["capability"] = body
    marker = spent_marker(entry_dir, run_id)
    if body.get("spent") is True or marker.exists():
        return 29, {**rec, "ok": False, "code": "FHS_ENTRY_TOKEN_CONSUMED",
                    "detail": f"the capability for run_id {run_id!r} was already spent "
                              f"(spent_at={body.get('consumed_at')!r}, "
                              f"by_pid={body.get('consumer_pid')!r}); a capability is one-shot"}
    if str(body.get("lane") or "") != str(lane or ""):
        return 25, {**rec, "ok": False, "code": "FHS_ENTRY_ARM_MISMATCH",
                    "detail": f"the capability authorizes lane {body.get('lane')!r}, this run is "
                              f"{lane!r}"}
    if arm and str(body.get("arm") or "").strip().lower() != str(arm).strip().lower():
        return 25, {**rec, "ok": False, "code": "FHS_ENTRY_ARM_MISMATCH",
                    "detail": f"the capability authorizes arm {body.get('arm')!r}, this run would "
                              f"spawn {arm!r}"}
    expires_at = parse_iso(body.get("expires_at"))
    if expires_at is None or expires_at <= now:
        return 28, {**rec, "ok": False, "code": "FHS_ENTRY_TOKEN_REQUIRED",
                    "detail": f"the capability expired at {body.get('expires_at')!r} (now "
                              f"{iso(now)}); an expired capability is not a permission",
                    "reason": "token_expired"}
    if binding_path is not None:
        live_sha = sha256_file(binding_path)
        if live_sha is not None and body.get("binding_sha256") != live_sha:
            return 21, {**rec, "ok": False, "code": "FHS_ENTRY_BINDING_INVALID",
                        "detail": f"the binding changed after the capability was minted "
                                  f"(minted {str(body.get('binding_sha256'))[:16]}..., now "
                                  f"{live_sha[:16]}...); the capability does not cover these bytes"}
    # the one-shot claim: whoever creates the marker first wins, atomically
    try:
        fd = os.open(str(marker), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        return 29, {**rec, "ok": False, "code": "FHS_ENTRY_TOKEN_CONSUMED",
                    "detail": f"the capability for run_id {run_id!r} was claimed concurrently "
                              f"({marker}); a capability is one-shot"}
    except OSError as exc:
        return 27, {**rec, "ok": False, "code": "FHS_ENTRY_GUARD_UNRESOLVED",
                    "detail": f"the spent marker could not be claimed at {marker}: {exc}"}
    try:
        os.write(fd, f"{iso(now)} pid={os.getpid()}\n".encode("utf-8"))
    finally:
        os.close(fd)
    body.update(spent=True, consumed_at=iso(now), consumer_pid=os.getpid())
    try:
        path.write_text(json.dumps(body, indent=1, ensure_ascii=False, sort_keys=True) + "\n",
                        encoding="utf-8")
    except OSError:
        pass  # the marker is the claim of record; a failed pretty-print must not unspend it
    return 0, {**rec, "ok": True, "code": None, "consumed_at": iso(now),
               "capability": body}


# ---------------------------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------------------------
def _emit(rec: dict, json_out=None) -> None:
    if json_out:
        out = pathlib.Path(json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rec, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(rec, indent=2, ensure_ascii=False))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="fhs_entry_guard.py",
                                 description="FHS mechanical pre-dispatch entry gate (EC-R26-001)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("assert-entry", help="re-verify a session binding for one lane/arm")
    a.add_argument("--binding", default=None, help="path to the SBL SessionBinding record")
    a.add_argument("--lane", required=True)
    a.add_argument("--arm", default=None,
                   help="provider/model about to be spawned (default: the lane's rank-1 pool arm)")
    a.add_argument("--require-bound", action="store_true",
                   help="also require a run-scoped record (run_id/session_id/binding_id)")
    a.add_argument("--guard-token", default=None,
                   help="mint a one-shot run-scoped capability bound to this nonce")
    a.add_argument("--run-id", default=None, help="the run the capability authorizes")
    a.add_argument("--ttl", type=int, default=DEFAULT_TTL_SECONDS)
    a.add_argument("--hgk-root", default=None)
    a.add_argument("--binding-reader", default=None)
    a.add_argument("--entry-dir", default=None)
    a.add_argument("--json-out", default=None)

    c = sub.add_parser("consume-token", help="spend the run's one-shot capability (dispatcher side)")
    c.add_argument("--run-id", default=None)
    c.add_argument("--lane", default=None)
    c.add_argument("--arm", default=None)
    c.add_argument("--entry-dir", default=None)
    c.add_argument("--binding", default=None, help="the binding this run will use (bytes re-checked)")
    c.add_argument("--json-out", default=None)

    p = sub.add_parser("paths", help="print how this gate resolved its control plane and reader")
    p.add_argument("--hgk-root", default=None)
    p.add_argument("--binding-reader", default=None)
    p.add_argument("--json-out", default=None)

    args = ap.parse_args(argv)

    if args.cmd == "assert-entry":
        code, rec = gate_entry(binding=args.binding, lane=args.lane, arm=args.arm,
                               hgk_root=args.hgk_root, reader=args.binding_reader,
                               require_bound=args.require_bound)
        if code == 0 and args.guard_token:
            # A run-scoped binding and a run-scoped capability must name the SAME run; otherwise the
            # capability authorizes a run the binding was never minted for.
            bound_run = rec.get("binding_run_id")
            if bound_run and args.run_id and str(bound_run) != str(args.run_id):
                _emit({**rec, "ok": False, "code": "FHS_ENTRY_BINDING_INVALID", "check":
                       "FHS_ENTRY_BINDING_INVALID",
                       "detail": f"the binding was minted for run {bound_run!r} but this capability "
                                 f"is for run {args.run_id!r}; a run-scoped binding does not cover "
                                 f"another run"}, args.json_out)
                return 21
            mint_code, mint = mint_capability(args.run_id, args.guard_token, args.lane,
                                              rec.get("arm") or args.arm or "", rec,
                                              entry_dir=args.entry_dir, ttl=args.ttl)
            rec["capability"] = mint
            if mint_code != 0:
                rec.update(ok=False, code=mint.get("code"), detail=mint.get("detail"),
                           check=mint.get("code"))
                code = mint_code
        _emit(rec, args.json_out)
        return code

    if args.cmd == "consume-token":
        code, rec = consume_capability(run_id=args.run_id, lane=args.lane, arm=args.arm,
                                      entry_dir=args.entry_dir, binding_path=args.binding)
        _emit(rec, args.json_out)
        return code

    root, root_source = resolve_hgk_root(args.hgk_root)
    reader, reader_source = resolve_reader(args.binding_reader)
    _emit({"schema": SCHEMA, "hgk_root": str(root) if root else None,
           "hgk_root_source": root_source,
           "registry": str((root / "config" / "lane-routing-registry.yaml")) if root else None,
           "pool": str((root / "config" / "lane-route-slots.candidate.json")) if root else None,
           "binding_reader": str(reader) if reader else None,
           "binding_reader_source": reader_source,
           "entry_dir": str(DEFAULT_ENTRY_DIR)}, args.json_out)
    return 0 if (root and reader) else 27


if __name__ == "__main__":
    raise SystemExit(main())
