#!/usr/bin/env python3
"""Record a named blocker on a work unit: code, cause, and the one-line unblock.

Why this exists (measured 2026-10-31): `round_continuation_gate.py` refuses to close a round while units are not
PASS, and the only compliant exception is a unit that names a blocker AND its unblock. `work_queue` had no such
columns, so the gate could only ever answer OPEN_WORK -- the exception was unwritable, which makes a rule that
cannot be satisfied the same as no rule.

A blocker is code + cause + unblock. A row with a code and no unblock is a stop dressed as a status, and the gate
refuses it. That is deliberate: "blocked" without "here is what would unblock it" tells the next session nothing.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

DB = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/var/shared-spine/hg-kseos.db")
COLS = {"blocker_code": "TEXT", "blocker_cause": "TEXT", "blocker_unblock": "TEXT",
        "blocked_at": "TEXT"}


def ensure_columns(con: sqlite3.Connection) -> list[str]:
    have = {r[1] for r in con.execute("pragma table_info(work_queue)").fetchall()}
    added = []
    for name, typ in COLS.items():
        if name not in have:
            con.execute(f"alter table work_queue add column {name} {typ}")
            added.append(name)
    return added


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="record a named blocker on a work unit")
    ap.add_argument("--wp", required=True)
    ap.add_argument("--code", required=True)
    ap.add_argument("--cause", required=True)
    ap.add_argument("--unblock", required=True)
    ap.add_argument("--clear", action="store_true", help="remove the blocker instead of setting it")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if not args.unblock.strip() and not args.clear:
        print(json.dumps({"ok": False, "code": "BLOCKER_WITHOUT_UNBLOCK",
                          "why": "an unblock is required: a blocked unit that names no unblock is a stop, not a state"}))
        return 2

    con = sqlite3.connect(DB)
    try:
        added = ensure_columns(con)
        if args.clear:
            con.execute("update work_queue set blocker_code=null, blocker_cause=null, "
                        "blocker_unblock=null, blocked_at=null where wp_id=?", (args.wp,))
        else:
            import time
            con.execute("update work_queue set blocker_code=?, blocker_cause=?, blocker_unblock=?, blocked_at=? "
                        "where wp_id=?", (args.code, args.cause, args.unblock,
                                          time.strftime("%Y-%m-%dT%H:%M:%S%z"), args.wp))
        con.commit()
        row = con.execute("select wp_id, state, blocker_code, blocker_unblock from work_queue where wp_id=?",
                          (args.wp,)).fetchone()
    finally:
        con.close()
    out = {"ok": bool(row), "columns_added": added, "row": row}
    print(json.dumps(out, ensure_ascii=False) if args.json else out)
    return 0 if row else 1


if __name__ == "__main__":
    raise SystemExit(main())
