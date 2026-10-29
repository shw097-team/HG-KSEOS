#!/usr/bin/env python3
"""Obligation-ledger driver for R15.

Prints exactly ONE actionable item, or ONLY_BLOCKERS with every blocked id named,
or DONE. Exit 0 = work exists, 3 = only blockers, 0 with DONE = finished.

    r15_ledger.py                show
    r15_ledger.py --evidence O10 path/to/receipt.json
    r15_ledger.py --set O05 DONE --evidence O05 var/.../gstack.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "var" / "R15-MODEL-FALLBACK-20261023" / "LEDGER_R15.json"


def load() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    LEDGER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence", nargs=2, metavar=("ID", "PATH"))
    ap.add_argument("--set", nargs=2, metavar=("ID", "STATE"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    data = load()
    rows = {r["id"]: r for r in data["rows"]}

    if args.set:
        rid, state = args.set
        if rid not in rows:
            print(f"ERR unknown id {rid}", file=sys.stderr)
            return 2
        rows[rid]["state"] = state

    if args.evidence:
        rid, path = args.evidence
        if rid not in rows:
            print(f"ERR unknown id {rid}", file=sys.stderr)
            return 2
        p = Path(path)
        if not p.is_absolute():
            p = ROOT / p
        if not p.exists():
            print(f"ERR evidence file does not exist: {p}", file=sys.stderr)
            return 2
        rows[rid]["evidence"].append(str(p.relative_to(ROOT)).replace("\\", "/"))
        if rows[rid]["state"] == "OPEN":
            rows[rid]["state"] = "DONE"

    save(data)

    done = [r for r in data["rows"] if r["state"] == "DONE"]
    open_rows = [r for r in data["rows"] if r["state"] != "DONE"]
    blocked = [r for r in open_rows if any(rows[d]["state"] != "DONE" for d in r["depends_on"])]
    actionable = [r for r in open_rows if r not in blocked]

    if args.json:
        print(json.dumps({"done": len(done), "total": len(data["rows"]),
                          "actionable": actionable, "blocked": blocked}, indent=2))
    else:
        print(f"LEDGER: {len(done)}/{len(data['rows'])} done")
        if actionable:
            r = actionable[0]
            print(f"NEXT: {r['id']} — {r['title']}")
            print(f"      action: {r['next_action']}")
            for d in r["depends_on"]:
                print(f"      dep {d}: {rows[d]['state']}")
        if blocked:
            print("ONLY_BLOCKERS: " + ", ".join(f"{r['id']}(dep {','.join(d for d in r['depends_on'] if rows[d]['state'] != 'DONE')})" for r in blocked))
        if not open_rows:
            print("DONE")

    if not open_rows:
        return 0
    return 0 if actionable else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
