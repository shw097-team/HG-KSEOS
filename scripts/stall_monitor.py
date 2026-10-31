#!/usr/bin/env python3
"""stall_monitor -- does the running work look stuck, and if so, stop it instead of waiting.


try:  # keep every console child off the owner's desktop (see scripts/winproc.py)
    import winproc as _winproc  # noqa: E402  (same directory)
    _winproc.install()
except Exception:  # a missing helper must not stop a lane
    pass
The owner's rule, turned into a check: any task running longer than 10 minutes, and any task blocked more than
4 times by the same abnormal cause, must be diagnosed or paused immediately rather than left to grind.

Three findings, each measured, never inferred:

  * OVER_10_MIN     -- a live hgk-lane-dispatch process older than 10 minutes
  * REPEATED_BLOCK  -- the same failure code (or the same WP spawn) seen 4 or more times
  * NO_PROGRESS     -- a dispatch older than 10 minutes whose queue directory has gained no file in that window

`--pause` acts: it kills the offending dispatch tree and pauses the `hgk-continuation` cron job, so the loop
cannot immediately relaunch the same stuck unit. Without `--pause` it only reports, which is what the operator
should get from a cron notification.

Exit 0 = nothing stuck; 3 = at least one finding (the caller decides); 4 = --pause acted.
"""

from __future__ import annotations


try:  # every child of this process must be consoleless; see scripts/winproc.py and console_guard_gate.py
    import winproc as _winproc  # noqa: E402  (same directory)
    _winproc.install()
except Exception:  # a missing helper must not stop the tool
    pass


import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

QUEUE = Path(r"C:/wg/queue")
CRON_NAME = "hgk-continuation"
MAX_MINUTES = 10
MAX_REPEATS = 4
DEFAULT_WINDOW_MIN = 60   # repeats are judged inside the live window, never across the whole archive


def ps_dispatch() -> list[dict]:
    """Live dispatch processes with their start time, read through PowerShell CIM (wmic does not exist here)."""
    cmd = ("$p = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and "
           "$_.CommandLine -like '*hgk-lane-dispatch.py*' }; "
           "$p | ForEach-Object { '{0}|{1}|{2}' -f $_.ProcessId, $_.CreationDate.ToString('o'), "
           "($_.CommandLine -replace '\\s+',' ') }")
    done = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, timeout=90)
    text = (done.stdout or b"").decode("utf-8", errors="replace")
    out: list[dict] = []
    for line in text.splitlines():
        parts = line.split("|", 2)
        if len(parts) != 3 or not parts[0].strip().isdigit():
            continue
        pid, created, cl = int(parts[0]), parts[1], parts[2]
        try:
            started = datetime.fromisoformat(created)
            if started.tzinfo is None:
                started = started.astimezone()
        except ValueError:
            started = datetime.now().astimezone()
        nonce = (re.search(r"--nonce\s+(\S+)", cl) or [None, None])[1] if "--nonce" in cl else None
        wp = (re.search(r"(WP-FHS-\d\d)", cl) or [None, None])[1]
        out.append({"pid": pid, "started": started.isoformat(timespec="seconds"),
                    "minutes": round((datetime.now().astimezone() - started).total_seconds() / 60, 1),
                    "nonce": nonce, "wp": wp})
    # The launcher and the child share a start time; keep one row per (pid set) by nonce when possible.
    seen, uniq = set(), []
    for row in out:
        key = row["nonce"] or row["pid"]
        if key in seen:
            continue
        seen.add(key)
        uniq.append(row)
    return uniq


def repeated_blocks(extra_roots: list[Path] | None = None, window_min: int = DEFAULT_WINDOW_MIN) -> list[dict]:
    """Same failure code 4+ times, or same WP spawned 4+ times, across receipts and the driver log.

    Scope matters: the queue alone knows nothing about the sittings that ran before the queue existed, and the
    five voided VERIFY sittings (ERR_CHECKER_MUTATED_SUBJECT) live in C:/wg/ao*. A monitor that only reads the
    queue would have declared "no repeats" while the same block had happened five times one directory away.
    """
    codes: dict[str, list[str]] = {}
    receipts = list(QUEUE.rglob("*.json"))
    for root in extra_roots or []:
        if root.is_dir():
            receipts += list(root.rglob("*.json"))
    for receipt in receipts:
        if receipt.name.endswith("driver_state.json"):
            continue
        try:
            body = json.loads(receipt.read_text(encoding="utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(body, dict):
            continue
        # A defect that was diagnosed and fixed must stop counting, or the gate becomes a permanent brake:
        # the first run of this monitor paused the loop because of six ERR_CHECKER_MUTATED_SUBJECT failures
        # that review_lock had already cured. Only recent occurrences inside the live window are evidence.
        if time.time() - receipt.stat().st_mtime > window_min * 60:
            continue
        code = body.get("code") or ("OK" if body.get("ok") else None)
        if not code:
            continue
        codes.setdefault(str(code), []).append(receipt.name)

    spawns: dict[str, list[str]] = {}
    log = QUEUE / "driver.log"
    if log.is_file():
        for line in log.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("action") in ("spawn", "spawned") and ev.get("wp") or ev.get("action") == "spawn":
                key = ev.get("wp") or (re.search(r"(WP-FHS-\d\d)", str(ev.get("nonce"))) or [None, "UNKNOWN"])[1]
                spawns.setdefault(str(key), []).append(ev.get("at", ""))

    findings = [{"kind": "REPEATED_BLOCK", "key": k, "count": len(v), "examples": v[:5]}
                for k, v in codes.items() if len(v) >= MAX_REPEATS and k != "OK"]
    findings += [{"kind": "REPEATED_SPAWN", "key": k, "count": len(v), "examples": v[-5:]}
                 for k, v in spawns.items() if len(v) >= MAX_REPEATS]
    return findings


def no_progress(row: dict) -> bool:
    """A long dispatch that has written nothing into its queue directory in that window is not working."""
    if not row.get("wp"):
        return False
    d = QUEUE / row["wp"]
    if not d.is_dir():
        return True
    newest = max((p.stat().st_mtime for p in d.glob("*")), default=0)
    return (time.time() - newest) > MAX_MINUTES * 60


def pause_everything(row: dict | None) -> dict:
    acted = {"killed": None, "cron": None}
    if row:
        subprocess.run(["taskkill", "/PID", str(row["pid"]), "/T", "/F"], capture_output=True, text=True, timeout=60)
        acted["killed"] = row["pid"]
    done = subprocess.run(["hermes", "cron", "pause", CRON_NAME], capture_output=True, text=True, timeout=120)
    acted["cron"] = (done.stdout or done.stderr).strip()[:200]
    return acted


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pause", action="store_true", help="kill the stuck dispatch and pause the cron job")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--window-min", type=int, default=DEFAULT_WINDOW_MIN)
    args = ap.parse_args(argv or sys.argv[1:])

    live = ps_dispatch()
    long_running = [r for r in live if r["minutes"] > MAX_MINUTES]
    stalled = [r for r in long_running if no_progress(r)]
    findings = []
    for r in long_running:
        findings.append({"kind": "OVER_10_MIN", **r})
    for r in stalled:
        findings.append({"kind": "NO_PROGRESS", **r})
    findings += repeated_blocks([Path(r"C:/wg/ao4"), Path(r"C:/wg/ao5"), Path(r"C:/wg/ao6"),
                                  Path(r"C:/wg/ao7"), Path(r"C:/wg/ao8"), Path(r"C:/wg/ao9"),
                                  Path(r"C:/wg/ao12"), Path(r"C:/wg/ao13")], window_min=args.window_min)

    report = {"checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "live_dispatches": live, "findings": findings,
              "thresholds": {"minutes": MAX_MINUTES, "repeats": MAX_REPEATS}}

    if findings and args.pause:
        report["action"] = pause_everything((stalled or long_running or [None])[0])
    print(json.dumps(report, ensure_ascii=False, indent=None if args.json else 2))
    if findings and args.pause:
        return 4
    return 3 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
