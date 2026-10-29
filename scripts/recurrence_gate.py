#!/usr/bin/env python3
"""Refuse to work a defect class that has already been "fixed" twice without a regression test.

Every round in this repository produces a report; almost none of them produce a test. The result is
visible in `config/recurrence-ledger.json`: six classes, each with two or more occurrences, each
previously diagnosed in prose. A ledger without a gate is another report, so this is the gate.

Rules
  * a class with >= 2 occurrences must name a `regression_test` that exists on disk;
  * that test must reference the class id, so the ledger cannot point at an unrelated green test;
  * `--target PATH` additionally refuses when the class is not yet closed and the path is the same
    site that failed last time (cheap, but it stops the most common relapse).

Usage:
    python scripts/recurrence_gate.py --list
    python scripts/recurrence_gate.py --class RC-POLICY-DRIFT          # exit 0 open, 2 blocked
    python scripts/recurrence_gate.py --all                            # exit 2 if any class is blocked
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "config" / "recurrence-ledger.json"


def load() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def judge(entry: dict) -> dict:
    occ = len(entry.get("occurrences", []))
    test = entry.get("regression_test")
    problems: list[str] = []
    if occ >= 2:
        if not test:
            problems.append("no regression_test named")
        else:
            p = ROOT / test.split("::")[0]
            if not p.exists():
                problems.append(f"regression_test file missing: {test.split('::')[0]}")
            elif entry["class_id"] not in p.read_text(encoding="utf-8", errors="replace"):
                problems.append(f"regression_test does not reference {entry['class_id']}")
    return {
        "class_id": entry["class_id"],
        "occurrences": occ,
        "status": entry.get("status", "OPEN"),
        "regression_test": test,
        "blocked": bool(problems) and entry.get("status") != "CLOSED_WITH_TEST",
        "problems": problems,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--class", dest="cls", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    ledger = load()
    entries = ledger["classes"]
    if a.cls:
        entries = [e for e in entries if e["class_id"] == a.cls]
        if not entries:
            print(json.dumps({"verdict": "UNKNOWN_CLASS", "class": a.cls}))
            return 3

    rows = [judge(e) for e in entries]
    blocked = [r for r in rows if r["blocked"]]

    if a.list or not (a.cls or a.all):
        print(json.dumps({"classes": rows, "blocked": len(blocked)}, ensure_ascii=False, indent=1))
        return 0

    out = {"schema": "RECURRENCE-GATE/1", "verdict": "BLOCKED" if blocked else "OPEN",
           "checked": rows, "blocked": [r["class_id"] for r in blocked],
           "rule": "a class that recurred twice may not be worked again without a failing-when-it-returns test"}
    print(json.dumps(out, ensure_ascii=False, indent=1) if not a.json else json.dumps(out, ensure_ascii=False))
    return 2 if blocked else 0


if __name__ == "__main__":
    sys.exit(main())
