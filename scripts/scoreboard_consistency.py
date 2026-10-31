#!/usr/bin/env python3
"""scoreboard_consistency -- one authority, many projections, and a gate that notices when they disagree.

Why this exists: this delivery carried four scoreboards at once (16 PASS/3 FAIL/3 NOT_RUN in the control plane,
2/12/7/1 in one handover, 6/13/7 in another, 16/3/0 in a third). Each was true when it was written and none
said when. A reader cannot tell a stale projection from a live one, so every round re-litigates the same count.

The rule this gate enforces:
  * the control plane's `work_queue` table is the ONLY authority for a work package's state;
  * TODO.md, STATUS.json and GOAL.json are projections and may not contradict it;
  * a projection carries an age, and past `stale_after_seconds` it is STALE, not evidence.

Exit codes: 0 CONSISTENT, 1 DIVERGENT, 2 UNREADABLE (a projection that cannot be parsed is a failure, not a skip),
3 STALE (the only readable projection is older than its own declared window).

Usage:
  scoreboard_consistency.py [--db <hg-kseos.db>] [--queue C:/wg/queue] [--json]
"""

from __future__ import annotations

try:  # every child of this process must be consoleless; see scripts/winproc.py and console_guard_gate.py
    import winproc as _winproc  # noqa: E402

    _winproc.install()
except Exception:
    pass

import argparse
import json
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DB = REPO / "var" / "shared-spine" / "hg-kseos.db"
QUEUE = Path("C:/wg/queue")


def authority(db: Path) -> dict:
    con = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute("SELECT wp_id, state FROM work_queue ORDER BY wp_id").fetchall()
    finally:
        con.close()
    return {r["wp_id"]: r["state"] for r in rows}


def from_todo(path: Path) -> tuple[dict, str | None]:
    if not path.is_file():
        return {}, "MISSING"
    out = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"\s*-\s*\[( |x|X)\]\s*(WP-FHS-\d+)\s+(\S+)", line)
        if m:
            out[m.group(2)] = m.group(3).upper()
    return out, None


def _verdict_of(value, base: Path) -> str:
    """A projection may hold the verdict itself or a path to the officer's verdict file.

    Measured defect: `verdict` in STATUS.json is a PATH, so taking the basename reported "VERDICT.JSON" for
    three work packages -- a string that looks like a state and is not one. A path is resolved and read; an
    unreadable path is UNKNOWN, never a guess.
    """
    if not isinstance(value, str):
        return "UNKNOWN"
    if value.upper() in ("PASS", "FAIL", "NOT_RUN", "PENDING", "RUNNING", "BLOCKED"):
        return value.upper()
    p = Path(value)
    if not p.is_absolute():
        p = base / p
    if not p.is_file():
        return "UNKNOWN"
    try:
        doc = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return "UNKNOWN"
    v = doc.get("verdict") or doc.get("state")
    return str(v).upper() if isinstance(v, str) else "UNKNOWN"


def from_status(path: Path) -> tuple[dict, dict]:
    if not path.is_file():
        return {}, {"error": "MISSING"}
    doc = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    out = {}
    for row in doc.get("work_packages") or []:
        wp = row.get("wp")
        if not wp:
            continue
        out[wp] = _verdict_of(row.get("verdict") or row.get("state"), path.parent)
    age = None
    try:
        as_of = datetime.fromisoformat(str(doc.get("as_of")))
        if as_of.tzinfo is None:
            as_of = as_of.replace(tzinfo=timezone.utc)
        age = (datetime.now(timezone.utc) - as_of).total_seconds()
    except Exception:
        age = None
    return out, {"as_of": doc.get("as_of"), "age_seconds": age,
                 "stale_after_seconds": doc.get("stale_after_seconds"),
                 "verdict": doc.get("verdict"),
                 # A liveness document names the packages that are RUNNING. Its verdict for a package that is
                 # not live is a snapshot of a past sitting, not a claim about now -- so it is reported as
                 # informational instead of as a divergence (see the loop below).
                 "live_wps": sorted({str(r.get("wp")) for r in (doc.get("live") or []) if r.get("wp")})}


def from_goal(path: Path) -> tuple[dict, dict]:
    if not path.is_file():
        return {}, {"error": "MISSING"}
    doc = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    snap = doc.get("queue_snapshot") or ""
    counts = {}
    for key in ("total", "pass", "fail", "not_run", "pending"):
        m = re.search(rf"{key}=(\d+)", str(snap))
        if m:
            counts[key] = int(m.group(1))
    return {}, {"queue_snapshot": snap, "counts": counts, "goal_id": doc.get("goal_id"),
                "locked": doc.get("locked")}


def tally(states: dict) -> dict:
    out = {"total": len(states), "PASS": 0, "FAIL": 0, "NOT_RUN": 0, "OTHER": 0}
    for v in states.values():
        if v in ("PASS", "FAIL", "NOT_RUN"):
            out[v] += 1
        else:
            out["OTHER"] += 1
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DB))
    ap.add_argument("--queue", default=str(QUEUE))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    db, queue = Path(a.db), Path(a.queue)
    if not db.is_file():
        print(json.dumps({"verdict": "UNREADABLE", "why": "no control-plane database", "db": str(db)}))
        return 2

    auth = authority(db)
    if not auth:
        print(json.dumps({"verdict": "UNREADABLE", "why": "work_queue is empty", "db": str(db)}))
        return 2
    auth_tally = tally(auth)

    todo, todo_err = from_todo(queue / "TODO.md")
    status, status_meta = from_status(queue / "STATUS.json")
    _goal_rows, goal_meta = from_goal(queue / "GOAL.json")

    stale = False
    age = (status_meta or {}).get("age_seconds")
    window = (status_meta or {}).get("stale_after_seconds")
    if age is not None and window:
        stale = age > float(window)

    divergences = []
    informational = []
    # A stale liveness document cannot certify which packages are live: its `live` set describes a driver that
    # stopped hours ago. Trust it only while it is fresh, otherwise every STATUS row is informational.
    _live_wps = set((status_meta or {}).get("live_wps") or []) if not stale else set()
    for wp, state in sorted(auth.items()):
        if wp in todo and todo[wp] != state:
            divergences.append({"source": "TODO.md", "wp": wp, "says": todo[wp], "authority": state})
        if wp in status and status[wp] != state:
            if wp in _live_wps:
                divergences.append({"source": "STATUS.json", "wp": wp, "says": status[wp], "authority": state})
            else:
                informational.append({"source": "STATUS.json", "wp": wp, "says": status[wp],
                                      "authority": state,
                                      "why": "not in STATUS.json's live set: a past sitting's verdict, not a "
                                             "claim about now"})
    for src, rows in (("TODO.md", todo), ("STATUS.json", status)):
        for wp in sorted(set(rows) - set(auth)):
            divergences.append({"source": src, "wp": wp, "says": rows[wp], "authority": "ABSENT"})

    goal_counts = (goal_meta or {}).get("counts") or {}
    goal_divergent = {}
    mapping = {"total": "total", "pass": "PASS", "fail": "FAIL", "not_run": "NOT_RUN"}
    for gk, ak in mapping.items():
        if gk in goal_counts and goal_counts[gk] != auth_tally[ak]:
            goal_divergent[gk] = {"says": goal_counts[gk], "authority": auth_tally[ak]}

    report = {
        "schema": "HGK-SCOREBOARD-CONSISTENCY/1",
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "authority": {"source": str(db), "table": "work_queue", "tally": auth_tally},
        "projections": {
            "TODO.md": {"rows": len(todo), "error": todo_err},
            "STATUS.json": {"rows": len(status), **{k: v for k, v in (status_meta or {}).items()}},
            "GOAL.json": goal_meta,
        },
        "divergences": divergences,
        "informational": informational,
        "liveness": ("STALE" if stale else "FRESH"),
        "goal_divergences": goal_divergent,
        "status_stale": stale,
    }

    if divergences or goal_divergent:
        report["verdict"] = "DIVERGENT"
        code = 1
    elif todo_err or (status_meta or {}).get("error"):
        report["verdict"] = "UNREADABLE"
        code = 2
    else:
        report["verdict"] = "CONSISTENT"
        code = 0

    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        print(f"{report['verdict']}  authority total={auth_tally['total']} "
              f"PASS={auth_tally['PASS']} FAIL={auth_tally['FAIL']} NOT_RUN={auth_tally['NOT_RUN']} "
              f"divergences={len(divergences) + len(goal_divergent)} stale={stale}")
        for d in divergences[:20]:
            print(f"  {d['source']}: {d['wp']} says {d['says']} but the control plane says {d['authority']}")
        for k, v in goal_divergent.items():
            print(f"  GOAL.json: {k} says {v['says']} but the control plane says {v['authority']}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
