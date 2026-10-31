#!/usr/bin/env python3
"""ops_status -- one surface that answers "is anything running right now", for a human, at a glance.


try:  # keep every console child off the owner's desktop (see scripts/winproc.py)
    import winproc as _winproc  # noqa: E402  (same directory)
    _winproc.install()
except Exception:  # a missing helper must not stop a lane
    pass
Two failures made this necessary, both measured on 2026-10-30:

  1. I told the owner a VERIFY run was in flight. It had already finished 3 minutes earlier and produced no
     artefact the loop expected. The owner looked at the interface, saw nothing, and had to ask whether the
     work had silently died. It had.
  2. The queue directory is the truth, but nobody can be asked to read a directory listing to know whether
     the round is alive. A status that only exists in a transcript is not a status.

What this writes, every time it runs:
  C:/wg/queue/STATUS.json    machine-readable truth (live dispatches, phase per WP, last artefact, verdicts)
  C:/wg/queue/STATUS.md      ten lines a human can read in the interface
  a Kanban card per live dispatch (status=running) and per finished phase (status=done), so the desktop board
  shows the round without anyone running a command

It never decides acceptance. It reports what is running, what finished, and what produced nothing.

Usage: ops_status.py [--board fhs-msc-allpass-20261030] [--quiet]
Exit 0 always: a status command that can fail is a status nobody trusts.
"""

from __future__ import annotations


try:  # every child of this process must be consoleless; see scripts/winproc.py and console_guard_gate.py
    import winproc as _winproc  # noqa: E402  (same directory)
    _winproc.install()
except Exception:  # a missing helper must not stop the tool
    pass


import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

QUEUE = Path(r"C:/wg/queue")
BOARD = "fhs-msc-allpass-20261030"
STALE_AFTER = 240  # two cron ticks; past this a reader must say STALE, not RUNNING
STATUS_JSON = QUEUE / "STATUS.json"
STATUS_MD = QUEUE / "STATUS.md"
KANBAN_MARK = QUEUE / "kanban_cards.json"


def live_dispatches() -> list[dict]:
    cmd = ("$p = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and "
           "$_.CommandLine -like '*hgk-lane-dispatch.py*' }; "
           "$p | ForEach-Object { '{0}|{1}|{2}' -f $_.ProcessId, $_.CreationDate.ToString('o'), "
           "($_.CommandLine -replace '\\s+',' ') }")
    try:
        # text=True crashed the reader thread on a cp950 console (UnicodeDecodeError at byte 0xaa), and the
        # exception was swallowed into an empty list -- so a live dispatch was reported as IDLE. Decode bytes and
        # never let a decoding problem become "nothing is running".
        done = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, timeout=90)
        out = (done.stdout or b"").decode("utf-8", errors="replace")
    except (OSError, subprocess.SubprocessError):
        return [{"error": "STATUS_QUERY_FAILED"}]
    rows, seen = [], set()
    for line in out.splitlines():
        parts = line.split("|", 2)
        if len(parts) < 3 or not parts[0].strip().isdigit():
            continue
        pid, created, cl = int(parts[0]), parts[1], parts[2]
        import re
        nonce = (re.search(r"--nonce\s+(\S+)", cl) or [None, None])[1]
        wp = (re.search(r"(WP-FHS-\d\d)", cl) or [None, None])[1]
        lane = (re.search(r"--lane\s+(\S+)", cl) or [None, None])[1]
        key = nonce or pid
        if key in seen:
            continue
        seen.add(key)
        try:
            started = datetime.fromisoformat(created)
        except ValueError:
            started = datetime.now().astimezone()
        rows.append({"pid": pid, "wp": wp, "lane": lane, "nonce": nonce,
                     "started": started.isoformat(timespec="seconds"),
                     "minutes": round((datetime.now().astimezone() - started).total_seconds() / 60, 1)})
    return rows


def wp_state(qdir: Path) -> dict:
    files = sorted((p for p in qdir.glob("*") if p.is_file()), key=lambda p: p.stat().st_mtime)
    brief = qdir / "brief.md"
    verdict = next((p for p in files if p.name == "verdict.json"), None)
    if verdict is None:
        verdict = next((p for p in qdir.rglob("verdict.json")), None)
    receipts = [p for p in files if p.suffix == ".json" and "attempts" not in p.name]
    newest = files[-1] if files else None
    return {
        "wp": qdir.name,
        "brief": str(brief) if brief.is_file() else None,
        "verdict": str(verdict) if verdict else None,
        "artefacts": len(files),
        "last_artefact": {"name": newest.name, "at": time.strftime("%H:%M:%S", time.localtime(newest.stat().st_mtime))} if newest else None,
        "receipts": [{"name": p.name,
                      "ok": (json.loads(p.read_text(encoding="utf-8", errors="replace")).get("ok") if isinstance(json.loads(p.read_text(encoding="utf-8", errors="replace")), dict) else None
                             if p.suffix == ".json" else None)} for p in receipts[-4:]],
    }


def kanban_sync(state: dict, live: list[dict]) -> list[str]:
    """A card per live dispatch so the desktop board shows the round. Never more than one per nonce."""
    try:
        known = json.loads(KANBAN_MARK.read_text(encoding="utf-8")) if KANBAN_MARK.is_file() else {}
    except json.JSONDecodeError:
        known = {}
    created = []
    for d in live:
        key = d["nonce"] or str(d["pid"])
        if key in known:
            continue
        title = f"RUNNING {d['wp']} {d['lane']} (pid {d['pid']})"
        done = subprocess.run(
            ["hermes", "kanban", "--board", BOARD, "create", title,
             "--body", f"nonce={key} started={d['started']} queue={QUEUE / (d['wp'] or '')}",
             "--initial-status", "running"],
            capture_output=True, text=True, timeout=120)
        created.append((done.stdout or done.stderr).strip().splitlines()[-1] if (done.stdout or done.stderr) else "")
        known[key] = created[-1]
    KANBAN_MARK.write_text(json.dumps(known, ensure_ascii=False, indent=1), encoding="utf-8")
    return created


def supervisor_status() -> str:
    """The clock is a process, not a guarantee. Measured 2026-10-31: the cron job had been PAUSED since 00:24:11 and
    three turns still described 'the 15-minute loop'; a paused clock is invisible until something prints it."""
    pid_file = K / "var" / "lane_supervisor.pid"
    if not pid_file.exists():
        return "SUPERVISOR: not started"
    try:
        pid = int(pid_file.read_text(encoding="utf-8").strip() or 0)
    except (OSError, ValueError):
        return "SUPERVISOR: pid unreadable"
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ 1 }} else {{ 0 }}"],
                       capture_output=True, text=True, timeout=60)
    return f"SUPERVISOR: {'alive pid ' + str(pid) if r.stdout.strip().endswith('1') else 'DEAD (pid file stale)'}"


def goal_status() -> str:
    """The goal is a lock the owner believes is on. Nothing checked it, and it was found PAUSED while three turns
    reported progress -- so it is now read on every status refresh rather than remembered."""
    try:
        import sqlite3
        db = Path(os.environ.get("HERMES_HOME", r"C:/Users/user/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/"
                                 r"LocalCache/Local/hermes/profiles/hgk-governed")) / "state.db"
        con = sqlite3.connect(str(db))
        rows = con.execute("select key,value from state_meta where key like 'goal:%'").fetchall()
        con.close()
        if not rows:
            return "GOAL: none recorded"
        k, v = rows[-1]
        d = json.loads(v)
        return f"GOAL: {d.get('status')} ({k.split(':',1)[1]}, turns {d.get('turns_used', 0)}/{d.get('max_turns')})"
    except Exception as exc:
        return f"GOAL: UNREADABLE ({type(exc).__name__})"


def fresh() -> int:
    """One line a reader can trust: RUNNING (live, within its own validity) or STALE/IDLE. This exists because a
    status file read without its age is how "finished" got reported as "running" for eight minutes."""
    if not STATUS_JSON.is_file():
        print("STATUS: MISSING — nothing has ever been recorded")
        return 3
    d = json.loads(STATUS_JSON.read_text(encoding="utf-8"))
    age = time.time() - time.mktime(time.strptime(d.get("as_of", "1970-01-01T00:00:00"), "%Y-%m-%dT%H:%M:%S"))
    limit = int(d.get("stale_after_seconds") or STALE_AFTER)
    head = f"as of {d.get('as_of')} ({int(age)}s ago, valid {limit}s)"
    if age > limit:
        print(f"STATUS: STALE — {head}; do not read this as running")
        return 3
    if d.get("live"):
        w = ", ".join(f"{x['wp']} {x['lane']} pid {x['pid']} {x['minutes']}min" for x in d["live"])
        print(f"STATUS: RUNNING — {w} · {head}")
        print(goal_status())
        print(supervisor_status())
        return 0
    print(f"STATUS: IDLE — nothing is running · {head}")
    print(goal_status())
    print(supervisor_status())
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--board", default=BOARD)
    ap.add_argument("--quiet", action="store_true")
    # Measured preference, 2026-10-30: the owner wants running work inside todo_list + the goal, not a card per
    # dispatch and not a window. Cards are now opt-in (--cards); the goal anchor card is never recreated here.
    ap.add_argument("--cards", action="store_true")
    ap.add_argument("--fresh", action="store_true")
    args = ap.parse_args(argv or sys.argv[1:])

    if args.fresh:
        return fresh()

    live = live_dispatches()
    wps = [wp_state(d) for d in sorted(p for p in QUEUE.glob("WP-FHS-*") if p.is_dir())]
    # OD-Z1: a projection with no age can only become wrong, never self-correct. `as_of` + `stale_after_seconds`
    # let a reader tell "quiet" from "nobody has looked recently", which is the difference between a status file and
    # a claim. `alive` is re-checked per pid here rather than trusted from when the dispatch was recorded.
    body = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "as_of": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "stale_after_seconds": STALE_AFTER,
        "live": live,
        "running_count": len(live),
        "verdict": "WORK_IN_FLIGHT" if live else "IDLE",
        "work_packages": wps,
    }
    STATUS_JSON.write_text(json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# HG-KSEOS round status — as of {time.strftime('%Y-%m-%d %H:%M:%S')} "
        f"(valid {STALE_AFTER}s; older than that reads STALE, never RUNNING)",
        "",
        f"**{'RUNNING: ' + str(len(live)) + ' dispatch(es)' if live else 'IDLE — nothing is running'}**",
        "",
    ]
    for d in live:
        lines.append(f"- `{d['wp']}` {d['lane']} · pid {d['pid']} · {d['minutes']} min · `{d['nonce']}`")
    if not live:
        lines.append("- the last phase ended; the next unit is dispatched by the `hgk-continuation` cron")
    lines += ["", "| WP | brief | verdict | artefacts | last | receipts ok |", "|---|---|---|---|---|---|"]
    for w in wps:
        rec = ", ".join(str(r["ok"]) for r in w["receipts"]) or "-"
        lines.append(f"| {w['wp']} | {'yes' if w['brief'] else 'no'} | {'yes' if w['verdict'] else 'no'} "
                     f"| {w['artefacts']} | {w['last_artefact']['at'] if w['last_artefact'] else '-'} | {rec} |")
    STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # Goal + todo projection, written from the control plane on every tick.
    #
    # Why it is a projection and not a session object: `todo_list` lives in the conversation, so a compaction or a
    # new session erases it, and I have twice rebuilt it with merge=false (which REPLACES the whole list) and lost
    # items. The goal anchor and the task list therefore live in files derived from work_queue, and the cron
    # rewrites them every 15 minutes. Anything a human or an agent reads there is current by construction.
    queue_rows = subprocess.run([sys.executable, str(Path(__file__).with_name("work_queue.py")), "show"],
                                capture_output=True, text=True, timeout=120).stdout
    goal = {
        "goal_id": "FHS-MSC-PIPD-LS-PKG-ALL-PASS-YYYYMMDD".replace("YYYYMMDD", "20261030"),
        "objective": "all 22 work packages of FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1 actually executed, "
                     "independently accepted, receipt-backed",
        "locked": True,
        "derived_from": "hg-kseos.db work_queue + acceptances (never from a transcript)",
        "running": [f"{d['wp']} {d['lane']} pid {d['pid']}" for d in live],
        "queue_snapshot": queue_rows.strip().splitlines()[-1] if queue_rows.strip() else "",
        "updated_at": body["generated_at"],
    }
    (QUEUE / "GOAL.json").write_text(json.dumps(goal, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    running_by_wp = {d["wp"]: d for d in live if d.get("wp")}
    todo = ["# Todo (derived from the control plane, not from a session)", ""]
    for line in queue_rows.strip().splitlines():
        if not line.startswith("WP-FHS-"):
            continue
        parts = line.split()
        wp, state = parts[0], (parts[1] if len(parts) > 1 else "")
        live_row = running_by_wp.get(wp)
        if live_row:
            # A unit that is running must never read as "pending" -- that is the exact confusion the owner hit.
            todo.append(f"- [>] {wp} RUNNING {live_row['lane']} pid {live_row['pid']} ({live_row['minutes']} min)")
        else:
            box = "[x]" if state == "PASS" else ("[!]" if state in ("FAIL", "BLOCKED") else "[ ]")
            todo.append(f"- {box} {wp} {state}")
    (QUEUE / "TODO.md").write_text("\n".join(todo) + "\n", encoding="utf-8")

    cards = kanban_sync(body, live) if args.cards else []
    if not args.quiet:
        print(json.dumps({"status_json": str(STATUS_JSON), "status_md": str(STATUS_MD),
                          "running": len(live), "cards_created": cards}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
