#!/usr/bin/env python3
"""Refuse to close a round while the task is still runnable.

MEASURED 2026-10-31, after the owner asked for the fourth time why the work stopped: the three mechanisms that
could have kept it moving were all absent at the same moment --

  * this session had no goal row at all (`load_goal` -> None), and Hermes only injects continuation turns while a
    goal row is active;
  * the cron supervisor `hgk-continuation-supervisor` existed but was **paused**;
  * there is no turn-end hook anywhere in HG-KSEOS.

So "keep going until done" was a sentence, not a state machine. A turn ends the moment tool calls stop, and nothing
is invoked at that instant. This gate is the missing piece: it makes "close the round" a decision that can FAIL.

It answers one question -- may this round be closed? -- and refuses on any of:

  NO_GOAL_ROW            no active goal object for the session (nothing will continue after the turn ends)
  SUPERVISOR_PAUSED      the continuation clock is paused (nothing will resume the loop)
  OPEN_WORK              work_queue still holds FAIL/NOT_RUN units
  BLOCKER_WITHOUT_UNBLOCK  a unit carries a blocker that names no unblock (that is a stop dressed as a status)
  NO_NEXT_ACTION         nothing is runnable and nothing is blocked -- an empty queue that is not empty

A round may close when every open unit carries a named blocker with a one-line unblock, or when the queue is fully
PASS. That is the only compliant stop: everything else is a report standing in for work.

Usage:
    python scripts/round_continuation_gate.py --session 20261031_201542_761b82
    python scripts/round_continuation_gate.py --session ... --json
    python scripts/round_continuation_gate.py --session ... --allow-close-because "owner asked to stop"
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

HGK = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS")
QUEUE_DB = HGK / "var" / "shared-spine" / "hg-kseos.db"

NO_GOAL_ROW = "NO_GOAL_ROW"
SUPERVISOR_PAUSED = "SUPERVISOR_PAUSED"
OPEN_WORK = "OPEN_WORK"
BLOCKER_WITHOUT_UNBLOCK = "BLOCKER_WITHOUT_UNBLOCK"
NO_NEXT_ACTION = "NO_NEXT_ACTION"
OK_TO_CLOSE = "OK_TO_CLOSE"


def goal_row(session: str) -> dict:
    """Read the goal the harness actually consults: state.db state_meta, key goal:<session>."""
    base = Path(os.path.expandvars(r"%LOCALAPPDATA%\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes"))
    hits = []
    for db in base.glob("profiles/*/state.db"):
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        except sqlite3.Error:
            continue
        try:
            rows = con.execute("select name from sqlite_master where type='table'").fetchall()
            if not any("state_meta" == r[0] for r in rows):
                continue
            row = con.execute("select value from state_meta where key=?", (f"goal:{session}",)).fetchone()
            if row:
                hits.append({"db": str(db), "value": row[0]})
        except sqlite3.Error:
            continue
        finally:
            con.close()
    if not hits:
        return {"present": False, "status": None, "db": None}
    raw = hits[0]["value"]
    status = None
    try:
        status = json.loads(raw).get("status")
    except (TypeError, ValueError):
        status = "UNPARSEABLE"
    return {"present": True, "status": status, "db": hits[0]["db"]}


def work_queue_rows() -> list[dict]:
    if not QUEUE_DB.is_file():
        return []
    con = sqlite3.connect(f"file:{QUEUE_DB}?mode=ro", uri=True)
    try:
        cols = [r[1] for r in con.execute("pragma table_info(work_queue)").fetchall()]
        if not cols:
            return []
        sel = ["wp_id", "state"] + [c for c in ("blocker_code", "blocker_unblock", "verdict") if c in cols]
        rows = con.execute(f"select {', '.join(sel)} from work_queue").fetchall()
        return [dict(zip(sel, r)) for r in rows]
    finally:
        con.close()


def supervisor_state() -> dict:
    """Is the continuation clock armed?

    Measured 2026-10-31: cron jobs are NOT in state.db -- they live in the profile's cron/jobs.json. A first version
    of this probe looked in state.db, found nothing, and reported "no supervisor exists at all" while `hermes cron
    list` was showing a paused one. A probe that cannot find its own input must not answer "absent": that is the
    same defect as a status surface that reports IDLE because its query crashed.
    """
    base = Path(os.path.expandvars(r"%LOCALAPPDATA%\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes"))
    found = []
    for jobs in base.glob("profiles/*/cron/jobs.json"):
        try:
            data = json.loads(jobs.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            return {"present": None, "paused": None, "name": None, "db": str(jobs),
                    "error": f"jobs.json unreadable: {exc}", "note": "UNREADABLE is not ABSENT"}
        items = data if isinstance(data, list) else (data.get("jobs") or [])
        for job in items:
            name = str(job.get("name") or "")
            if "continuation" in name.lower():
                found.append({"name": name, "paused": bool(job.get("paused") or job.get("enabled") is False),
                              "schedule": job.get("schedule"), "db": str(jobs)})
    if not found:
        return {"present": False, "paused": None, "name": None, "db": None,
                "note": "scanned every profile's cron/jobs.json"}
    return {"present": True, **found[0], "all": found}


def evaluate(session: str) -> dict:
    g = goal_row(session)
    sup = supervisor_state()
    rows = work_queue_rows()
    open_units = [r for r in rows if (r.get("state") or "").upper() not in ("PASS",)]

    def settled(r: dict) -> bool:
        """A unit may stay open at close only if it names a blocker AND the one-line unblock."""
        return bool((r.get("blocker_code") or "").strip()) and bool((r.get("blocker_unblock") or "").strip())

    unexplained = [r for r in open_units if not settled(r)]
    no_unblock = [r for r in open_units
                  if (r.get("blocker_code") or "").strip() and not (r.get("blocker_unblock") or "").strip()]

    findings: list[dict] = []
    if not g["present"]:
        findings.append({"code": NO_GOAL_ROW,
                         "why": "no goal row for this session: nothing injects a continuation turn once the turn ends",
                         "fix": f"save_goal({session!r}, GoalState(status='active', ...))"})
    elif (g["status"] or "").lower() != "active":
        findings.append({"code": NO_GOAL_ROW,
                         "why": f"goal row exists but status is {g['status']!r}, so it will not continue the task",
                         "fix": "set status='active' with a stop condition in the text"})
    if sup["present"] and sup["paused"]:
        findings.append({"code": SUPERVISOR_PAUSED,
                         "why": "the continuation supervisor exists but is paused: no clock will resume the loop",
                         "fix": "hermes cron resume hgk-continuation-supervisor"})
    if not sup["present"]:
        findings.append({"code": SUPERVISOR_PAUSED,
                         "why": "no continuation supervisor job exists at all",
                         "fix": "create the cron job before starting a multi-round task"})
    if unexplained:
        findings.append({"code": OPEN_WORK,
                         "why": f"{len(unexplained)} unit(s) not PASS and not properly blocked: "
                                f"{[r['wp_id'] for r in unexplained]}",
                         "fix": "dispatch the next runnable unit, or record blocker_code + blocker_unblock"})
    if no_unblock:
        findings.append({"code": BLOCKER_WITHOUT_UNBLOCK,
                         "why": f"blocked with no unblock named: {[r['wp_id'] for r in no_unblock]}",
                         "fix": "write the one-line unblock into the queue, not into a report"})
    if not open_units and not rows:
        findings.append({"code": NO_NEXT_ACTION,
                         "why": "the queue is empty, which is not the same as finished",
                         "fix": "seed the queue from the delivery DAG"})
    return {"schema": "HGK-ROUND-CONTINUATION-GATE/1", "session": session, "goal": g, "supervisor": sup,
            "work_queue": {"total": len(rows), "open": [r["wp_id"] for r in open_units]},
            "verdict": OK_TO_CLOSE if not findings else "REFUSED_TO_CLOSE",
            "findings": findings}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="may this round be closed?")
    ap.add_argument("--session", required=True)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--allow-close-because", default=None,
                    help="the owner's own words; a close is allowed only with a stated reason")
    args = ap.parse_args(argv)

    r = evaluate(args.session)
    if args.allow_close_because:
        r["owner_override"] = args.allow_close_because
        r["verdict"] = OK_TO_CLOSE
        r["findings"] = [f for f in r["findings"] if f["code"] not in (NO_GOAL_ROW, SUPERVISOR_PAUSED)]
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print(f"{r['verdict']}  (session {args.session})")
        print(f"  goal: {r['goal']}")
        print(f"  supervisor: {r['supervisor']}")
        print(f"  work_queue: {r['work_queue']['total']} rows, open {r['work_queue']['open']}")
        for f in r["findings"]:
            print(f"  - {f['code']}: {f['why']}\n      fix: {f['fix']}")
    return 0 if r["verdict"] == OK_TO_CLOSE else 1


if __name__ == "__main__":
    raise SystemExit(main())
