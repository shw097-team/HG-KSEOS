#!/usr/bin/env python3
"""console_window_gate — did this dispatch put a window on the owner's desktop?

FAR-20261031-028, fix F3. The class under investigation is "a console-subsystem process started from a
context with no console gets a new console, and on a Windows Terminal host that console is a visible
window". A hiding flag cannot be verified by reading code; it has to be observed. `scripts/window_watch.py`
is the only sensor with the resolution to see it (20 ms), so this gate reads its ledger for the dispatch
window and answers with a number.

Verdicts (three-valued, never a vacuous pass):

* ``PASS``     — the ledger covers the window and no console window was observed.
* ``FAIL``     — console windows were observed during the window; the owners are named.
* ``INCONCLUSIVE`` — the ledger does not cover the window (watcher not running, or the window predates the
  first event). This is the honest answer when nothing was measured, and it is NOT a pass.

Usage
-----
    python scripts/console_window_gate.py --receipt <dispatch.json>
    python scripts/console_window_gate.py --since 2026-10-31T10:44:00 --until 2026-10-31T10:52:00
    python scripts/console_window_gate.py --since ... --assert-zero     # exit 1 on FAIL, 3 on INCONCLUSIVE
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EVENTS = ROOT / "var" / "console-window-events.jsonl"


def _parse(stamp: str) -> datetime:
    stamp = stamp.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(stamp).replace(tzinfo=None)
    except ValueError:
        return datetime.strptime(stamp[:19], "%Y-%m-%dT%H:%M:%S")


def window_from_receipt(receipt: Path) -> tuple[datetime, datetime]:
    d = json.loads(receipt.read_text(encoding="utf-8"))
    attempts = d.get("attempts") or []
    stamps = [a.get("at") or a.get("started_at") for a in attempts if a.get("at") or a.get("started_at")]
    start = d.get("started_at") or d.get("at") or (stamps[0] if stamps else None)
    end = d.get("ended_at") or d.get("finished_at")
    if not start:
        raise SystemExit("ERR_RECEIPT_NO_TIMESTAMP: the receipt carries no start time; pass --since/--until")
    t0 = _parse(start)
    t1 = _parse(end) if end else t0 + timedelta(seconds=float(d.get("duration_s") or 1800))
    return t0, t1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipt", default=None)
    ap.add_argument("--since", default=None)
    ap.add_argument("--until", default=None)
    ap.add_argument("--events", default=str(DEFAULT_EVENTS))
    ap.add_argument("--assert-zero", action="store_true",
                    help="exit non-zero on FAIL (1) or INCONCLUSIVE (3)")
    ap.add_argument("--json-out", default=None)
    args = ap.parse_args(argv)

    if args.receipt:
        t0, t1 = window_from_receipt(Path(args.receipt))
        if args.since:
            t0 = _parse(args.since)
        if args.until:
            t1 = _parse(args.until)
    elif args.since:
        t0 = _parse(args.since)
        t1 = _parse(args.until) if args.until else datetime.now()
    else:
        print("ERR_NO_WINDOW: pass --receipt or --since", file=sys.stderr)
        return 2

    path = Path(args.events)
    if not path.is_file():
        result = {"verdict": "INCONCLUSIVE", "reason": "no window ledger", "events_path": str(path),
                  "window": {"since": t0.isoformat(), "until": t1.isoformat()}}
        print(json.dumps(result, ensure_ascii=False, indent=1))
        if args.json_out:
            Path(args.json_out).write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
        return 3 if args.assert_zero else 0

    rows, covered_from = [], None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        stamp = row.get("at")
        if not stamp:
            continue
        when = _parse(stamp)
        covered_from = when if covered_from is None or when < covered_from else covered_from
        if t0 <= when <= t1:
            rows.append(row)

    by_exe: dict[str, int] = {}
    for row in rows:
        by_exe[str(row.get("exe"))] = by_exe.get(str(row.get("exe")), 0) + 1

    if rows:
        # An observed window is a fact regardless of when the ledger started: coverage can only decide whether
        # "nothing was seen" means PASS or INCONCLUSIVE, never whether a seen window is a pass.
        verdict, reason = "FAIL", "console windows were observed inside the dispatch window"
    elif covered_from is None or covered_from > t0:
        verdict = "INCONCLUSIVE"
        reason = ("the ledger starts after the dispatch window opened; nothing was measured for it"
                  if covered_from else "the ledger is empty")
    else:
        verdict, reason = "PASS", "no console window observed inside a window the ledger covers"

    result = {
        "schema": "CONSOLE-WINDOW-GATE/1",
        "verdict": verdict,
        "reason": reason,
        "window": {"since": t0.isoformat(), "until": t1.isoformat()},
        "observed": len(rows),
        "by_exe": by_exe,
        "owners": [{"at": r.get("at"), "pid": r.get("pid"), "exe": r.get("exe"), "title": (r.get("title") or "")[:60]}
                   for r in rows[:20]],
        "ledger_covers_from": covered_from.isoformat() if covered_from else None,
        "events_path": str(path),
        "note": "INCONCLUSIVE is not a pass: an unmeasured dispatch has not been shown to be windowless.",
    }
    text = json.dumps(result, ensure_ascii=False, indent=1)
    print(text)
    if args.json_out:
        Path(args.json_out).write_text(text, encoding="utf-8")
    if args.assert_zero:
        return {"PASS": 0, "FAIL": 1, "INCONCLUSIVE": 3}[verdict]
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
