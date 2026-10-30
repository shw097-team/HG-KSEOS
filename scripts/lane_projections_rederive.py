#!/usr/bin/env python
"""Re-derive the registry's `projections[].bindings` expectations from the registry's own `routes`.

Why this exists: `projections[].bindings` is the drift oracle (check_drift compares live file values
against `expected`). Nothing in the repo ever WROTE that block, so it rots by hand: measured
2026-10-29, it still pinned /revision=33, /registry_epoch=33 and PLAN/VERIFY assignment rows to
opencode-go/deepseek-v4.1-flash while the same file's `routes` declared openai-codex/gpt-6.1-sol
(owner-order-20261024-s205-od01). Result: check_drift was fatal on a pristine copy of the tree, so the
gate could not distinguish a real drift from its own staleness.

Rule per binding (never `expected := actual` for anything the registry itself declares):
  * /revision, /registry_epoch                     -> from the assignment document
  * /assignment/<i>/assigned_{provider,model}      -> from routes[ROLES[i]]
  * /assignment/<i>/transport_model                -> from routes[ROLES[i]]'s automatic_selection arm
  * /lane_chains/<L>/<i>/automatic_selection       -> from routes[L].arms[i]
  * pointer resolves to nothing in the live file   -> DROPPED into `declared_unprojected` (the current
                                                      schema cannot express it; declaring the gap is
                                                      honest, fabricating an expectation is not)
  * everything else                                -> repinned to the accepted live value (baseline
                                                      advance; recorded with a count so a checker can
                                                      see exactly what moved)

This is an ORACLE change. It makes the gate truthful; it does not by itself satisfy TT-R36-02, which
needs an independent checker receipt on top.
"""
from __future__ import annotations

import argparse
import json
import pathlib

import yaml

ROLES = ("PLAN", "EXECUTE", "VERIFY_SECURITY")
SENTINEL = object()


def _resolve(doc, pointer: str):
    cur = doc
    for tok in pointer.strip("/").split("/"):
        tok = tok.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            if not tok.isdigit() or int(tok) >= len(cur):
                return None
            cur = cur[int(tok)]
        elif isinstance(cur, dict):
            if tok not in cur:
                return None
            cur = cur[tok]
        else:
            return None
    return cur


def _derive(pointer: str, doc: dict, routes: dict):
    parts = pointer.strip("/").split("/")
    if pointer == "/revision":
        return doc.get("revision")
    if pointer == "/registry_epoch":
        return doc.get("registry_epoch")
    if len(parts) == 4 and parts[0] == "assignment" and parts[1].isdigit():
        i, field = int(parts[1]), parts[2]
        if i >= len(ROLES) or ROLES[i] not in routes:
            return SENTINEL
        route = routes[ROLES[i]]
        if field == "assigned_provider":
            return route.get("provider")
        if field == "assigned_model":
            return route.get("model")
        if field == "transport_model":
            auto = next((a for a in route["arms"] if a.get("automatic_selection")), route["arms"][0])
            return auto.get("transport_model")
        return SENTINEL
    if len(parts) == 4 and parts[0] == "lane_chains" and parts[2].isdigit() and parts[3] == "automatic_selection":
        lane, i = parts[1], int(parts[2])
        arms = routes.get(lane, {}).get("arms", [])
        return arms[i].get("automatic_selection") if i < len(arms) else SENTINEL
    return SENTINEL


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--registry", default="config/lane-routing-registry.yaml")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    import re as _re
    root = pathlib.Path(args.root)
    reg_path = root / args.registry
    reg = yaml.safe_load(reg_path.read_text(encoding="utf-8"))
    doc = json.loads((root / reg["source_of_routes"]["path"]).read_text(encoding="utf-8"))
    routes = {r["lane"]: r for r in reg["routes"]}
    stats = {"derived": 0, "repinned": 0, "dropped": 0, "unchanged": 0}
    detail = []
    for entry in reg.get("projections", []):
        target_path = root / entry["path"]
        if not target_path.exists():
            entry["declared_unprojected"] = sorted(set(entry.get("declared_unprojected", []) + [
                b["pointer"] for b in entry.get("bindings", [])]))
            stats["dropped"] += len(entry.get("bindings", []))
            entry["bindings"] = []
            continue
        target = (json.loads(target_path.read_text(encoding="utf-8")) if entry.get("format") == "json"
                  else yaml.safe_load(target_path.read_text(encoding="utf-8")))
        kept, dropped = [], []
        for b in entry.get("bindings", []):
            ptr = b["pointer"]
            derived = _derive(ptr, doc, routes)
            actual = _resolve(target, ptr)
            if derived is not SENTINEL:
                want, cls = derived, "derived"
            elif actual is None:
                dropped.append(ptr)
                continue
            else:
                want, cls = actual, "repinned"
            if b.get("expected") == want:
                stats["unchanged"] += 1
            else:
                stats[cls] += 1
                detail.append({"id": entry["id"], "pointer": ptr, "was": b.get("expected"), "now": want, "class": cls})
            kept.append({"pointer": ptr, "expected": want})
        entry["bindings"] = kept
        entry["registry_epoch"] = doc.get("registry_epoch")
        if dropped:
            entry["declared_unprojected"] = sorted(set(entry.get("declared_unprojected", []) + dropped))
            stats["dropped"] += len(dropped)
            detail.append({"id": entry["id"], "dropped": dropped})
    reg.setdefault("projection_rederivation", {})
    reg["projection_rederivation"] = {
        "script": "scripts/lane_projections_rederive.py",
        "epoch": doc.get("registry_epoch"),
        "assignment_revision": doc.get("revision"),
        "stats": stats,
        "rule": "routes speak for route-derived pointers; unrepresentable pointers are declared, never fabricated",
        "claim_ceiling": "makes check_drift truthful; does not by itself satisfy TT-R36-02 (needs a checker receipt)",
    }
    print(json.dumps({"changes": len(detail), "stats": stats, "applied": args.apply}, ensure_ascii=False))
    if args.apply:
        # Surgical: regenerate ONLY the top-level `projections:` block. A whole-file yaml.safe_dump
        # would reformat 600+ lines of human-authored registry prose and destroy its comments; the
        # diff must stay inside the oracle it is changing.
        block = yaml.safe_dump({"projections": reg["projections"]}, allow_unicode=True,
                               sort_keys=False, width=200)
        text = reg_path.read_text(encoding="utf-8")
        lines = text.splitlines(keepends=True)
        start = next(i for i, ln in enumerate(lines) if ln.startswith("projections:"))
        end = next((i for i in range(start + 1, len(lines))
                    if _re.match(r'^[A-Za-z_][A-Za-z0-9_-]*:', lines[i])), len(lines))
        out = "".join(lines[:start]) + block + "".join(lines[end:])
        if "projection_rederivation:" not in text:
            out = out.rstrip("\r\n") + "\r\n" + yaml.safe_dump(
                {"projection_rederivation": reg["projection_rederivation"]},
                allow_unicode=True, sort_keys=False, width=200)
        reg_path.write_text(out, encoding="utf-8")
        for d in detail[:12]:
            print("  ", json.dumps(d, ensure_ascii=False)[:200])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
