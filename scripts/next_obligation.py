#!/usr/bin/env python
"""Print the single next obligation for this round. The round may not end while this returns work.

Why this exists
---------------
Measured failure mode (FAR_R14_4): the round kept ending its turn on a milestone ("18 reds -> 0,
independent PASS") although the command prompt has 31 TS items, 4 milestones and 14 DOC volumes.
The cause was not permission - it was that "what remains" lived only in prose, so the last green
artefact silently became the definition of "done". This script makes the remainder computable: it
prints exactly one actionable item, or refuses to print work only when nothing actionable is left.

Rules encoded here
------------------
* BLOCKED_HARD / BLOCKED_SOFT items are skipped, but they are NAMED in the output so they cannot be
  forgotten; a skip is not a completion.
* An item is actionable when its state is OPEN/PARTIAL/BLOCKED_MEASURE and every dependency is DONE.
* Ordering is by id, so the round always walks the command document in its own order unless a
  dependency forces otherwise.
* Exit code 0 = there is work (JSON on stdout). Exit code 3 = nothing actionable, but blockers remain.
  Exit code 0 with state DONE = the ledger is empty; only then may the round report completion.

Usage: python next_obligation.py [--file OBLIGATIONS.json] [--set <id> <state>] [--evidence <id> <path>]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT = HERE / "OBLIGATIONS.json"
ACTIONABLE = {"OPEN", "PARTIAL", "BLOCKED_MEASURE"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")


def next_item(doc: dict) -> dict:
    items = {i["id"]: i for i in doc["items"]}
    done = {i for i, v in items.items() if v["state"] == "DONE"}
    blocked = [i for i, v in items.items() if v["state"].startswith("BLOCKED")]
    for ident in sorted(items):
        it = items[ident]
        if it["state"] not in ACTIONABLE:
            continue
        if all(d in done for d in it.get("depends_on", [])):
            return {"state": "WORK", "item": it, "blocked_named": blocked,
                    "progress": f"{len(done)}/{len(items)} DONE"}
    if blocked:
        return {"state": "ONLY_BLOCKERS", "blocked": [items[b] for b in blocked],
                "progress": f"{len(done)}/{len(items)} DONE"}
    return {"state": "DONE", "progress": f"{len(done)}/{len(items)} DONE"}


WS = Path(r"C:/Projects/Agent_Workspace")
EVIDENCE_ROOTS = [WS / "_r14_packet", WS / "_r14_ev", WS / "_r14_ev/_governance/round-20261022-r14",
                  WS / "HG-KSEOS", WS]


def resolve(ev: str) -> Path | None:
    """Evidence strings are written by humans under time pressure; resolve the three shapes actually used:
    a path relative to the round evidence root, a '<repo> <relpath>' pair, or a workspace-relative path."""
    parts = ev.split(" ", 1)
    if len(parts) == 2 and parts[0] in {"HG-KSEOS", "PIPD", "SBL", "Fabric"}:
        cand = WS / parts[0] / parts[1]
        if cand.exists():
            return cand
    for root in EVIDENCE_ROOTS:
        cand = root / ev
        if cand.exists():
            return cand
    return None


def audit(doc: dict) -> dict:
    """Every DONE row must point at bytes. A ledger whose evidence paths do not resolve is a claim, not a record."""
    broken, checked = [], 0
    for it in doc["items"]:
        if it["state"] != "DONE":
            continue
        for ev in it.get("evidence", []):
            checked += 1
            if resolve(ev) is None:
                broken.append({"id": it["id"], "evidence": ev})
    return {"checked": checked, "broken": broken, "ok": not broken}


def main(argv: list[str]) -> int:
    path = DEFAULT
    if "--file" in argv:
        path = Path(argv[argv.index("--file") + 1])
    doc = load(path)
    if "--audit" in argv:
        out = audit(doc)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if out["ok"] else 4
    if "--set" in argv:
        i = argv.index("--set")
        ident, state = argv[i + 1], argv[i + 2]
        for it in doc["items"]:
            if it["id"] == ident:
                it["state"] = state
        save(path, doc)
        print(json.dumps({"updated": ident, "state": state}, ensure_ascii=False))
        return 0
    if "--evidence" in argv:
        i = argv.index("--evidence")
        ident, ev = argv[i + 1], argv[i + 2]
        for it in doc["items"]:
            if it["id"] == ident:
                it.setdefault("evidence", []).append(ev)
                it["state"] = "DONE"
        save(path, doc)
        print(json.dumps({"closed": ident, "evidence": ev}, ensure_ascii=False))
        return 0
    out = next_item(doc)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if out["state"] == "WORK":
        return 0
    return 0 if out["state"] == "DONE" else 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
