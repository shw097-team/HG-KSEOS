#!/usr/bin/env python3
"""set_goal — open the desktop /goal the way `/goal` itself opens it, from outside the chat.

Measured correction, 2026-10-30: I told the owner "`/goal` is a desktop slash command, so I cannot set it".
The first half is true and the second half was false. `hermes_cli.goals` exposes `load_goal`, `save_goal` and
`GoalState`, and `/goal` is only a thin command over them: the state lives in `state_meta` of the profile's
`state.db`, keyed by the session id. Writing that row opens the goal exactly as the slash command would, and
`/goal status` then reads it back.

So this tool does the same thing through the same API -- no new store, no parallel truth:

  set_goal.py show   [--session ID]
  set_goal.py set    --goal TEXT [--max-turns N] [--subgoal TEXT ...] [--session ID]
  set_goal.py clear  [--session ID]

Session defaults to the most recently active desktop session in the profile's state.db, which is the session a
human is looking at; pass --session to target another. Exit 2 if the goal store or the session cannot be resolved.
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
import time
from pathlib import Path

HERMES_HOME = Path(os.environ.get(
    "HERMES_HOME",
    r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/profiles/hgk-governed",
))


def newest_desktop_session() -> str | None:
    db = HERMES_HOME / "state.db"
    if not db.is_file():
        return None
    con = sqlite3.connect(str(db))
    try:
        row = con.execute(
            "SELECT id FROM sessions WHERE source='desktop' ORDER BY last_activity_at DESC, rowid DESC LIMIT 1"
        ).fetchone()
        return row[0] if row else None
    except sqlite3.Error:
        return None
    finally:
        con.close()


def cmd_resume(args) -> int:
    """Re-open a paused goal without rewriting it. A goal that can be paused by anything and noticed by nothing is
    the same defect as a status file without an age: the owner believes a lock is on while it is off."""
    g = load_goal(args.session)
    if not g:
        print("NO_GOAL")
        return 3
    g.status = "active"
    g.paused_at = None
    save_goal(args.session, g)
    print(f"GOAL_RESUMED session={args.session} status={g.status} max_turns={g.max_turns}")
    return 0


def main(argv=None) -> int:
    os.environ.setdefault("HERMES_HOME", str(HERMES_HOME))
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("show", "set", "clear", "resume"):
        p = sub.add_parser(name)
        p.add_argument("--session", default=None)
        if name == "set":
            p.add_argument("--goal", required=True)
            p.add_argument("--max-turns", type=int, default=200)
            p.add_argument("--subgoal", action="append", default=[])
    args = ap.parse_args(argv or sys.argv[1:])

    try:
        from hermes_cli.goals import GoalState, clear_goal, load_goal, save_goal  # type: ignore
    except Exception as exc:  # noqa: BLE001
        print(f"GOAL_STORE_UNAVAILABLE: {exc}")
        return 2

    session = args.session or newest_desktop_session()
    if not session:
        print("SESSION_UNRESOLVED: no desktop session in state.db (pass --session)")
        return 2

    if args.cmd == "show":
        state = load_goal(session)
        print(f"session={session} " + ("NO_GOAL" if state is None else
              f"status={state.status} turns={state.turns_used}/{state.max_turns} goal={state.goal[:160]}"))
        return 0

    if args.cmd == "resume":
        state = load_goal(session)
        if state is None:
            print("NO_GOAL")
            return 3
        state.status = "active"
        state.paused_at = None
        save_goal(session, state)
        back = load_goal(session)
        print(f"{'GOAL_RESUMED' if back and back.status == 'active' else 'GOAL_RESUME_UNVERIFIED'} "
              f"session={session} max_turns={back.max_turns if back else '?'}")
        return 0 if back and back.status == "active" else 3

    if args.cmd == "clear":
        clear_goal(session)
        print(f"cleared session={session}")
        return 0

    state = GoalState(goal=args.goal, status="active", max_turns=args.max_turns,
                      created_at=time.time(), last_turn_at=0.0)
    state.subgoals = list(args.subgoal)
    save_goal(session, state)
    back = load_goal(session)
    ok = back is not None and back.status == "active" and back.goal == args.goal
    print(f"{'GOAL_SET' if ok else 'GOAL_WRITE_UNVERIFIED'} session={session} "
          f"max_turns={args.max_turns} subgoals={len(args.subgoal)}")
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
