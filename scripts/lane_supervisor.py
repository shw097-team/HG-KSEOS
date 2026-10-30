#!/usr/bin/env python3
"""lane_supervisor — dispatch every READY unit, in parallel, as soon as it is ready.

Why this exists (measured 2026-10-31):

  The first version of the continuation loop advanced **one unit per cron tick**, and the tick was 15 minutes. A single
  EXECUTE run on this host takes 15-30 minutes (measured: WP-FHS-17 EXECUTE needed >900 s and was still writing
  files when the old budget cut it). So one unit cost 15 min of dispatch latency + 20 min of work, and six units were
  serialised behind a timer whose period was chosen for a different job (status refresh), not for throughput.

  The delivery text also says what a loop must not be: `11_WORKPACKAGES_AND_DAG.md` -- "依賴原服務，不創第二
  Scheduler", and `REPAIR_CLOSURE_REPORT.md` -- "未造第二 Queue、Scheduler、Issuer、Checker 或 Canonical Writer".
  A 15-minute timer that decides *when* work may start is a second scheduler by any reading. What the package allows
  is a reader of the DAG's typed edges that dispatches through the ORIGINAL lane runtime (`hgk-lane-dispatch.py`) and
  records in the original registry (`acceptances`).

  So this file is deliberately not a scheduler: it holds no queue, no cadence policy, and no ordering of its own.
  Readiness comes from `work_queue.py next --wp` (the DAG projection), dispatch goes through
  `continuation_driver.py` (which owns the lane call), and the only thing added here is **concurrency**: several
  independent units may be in flight, because the DAG says they are independent.

Usage:
  python scripts/lane_supervisor.py                 # one pass over ready units, then report
  python scripts/lane_supervisor.py --watch         # keep watching until nothing is ready and nothing runs
  python scripts/lane_supervisor.py --watch --interval 5 --max-parallel 4
  python scripts/lane_supervisor.py --status        # what is in flight right now
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import winproc  # noqa: E402  -- every child of this process is headless

winproc.install()

K = Path(__file__).resolve().parent.parent
QUEUE = Path(r"C:/wg/queue")
LOCKS = K / "var" / "review-locks"
DB = K / "var" / "shared-spine" / "hg-kseos.db"
LOG = QUEUE / "supervisor.log"


def log(event: dict) -> None:
    event["at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")


def all_wps() -> list[str]:
    import sqlite3

    con = sqlite3.connect(str(DB))
    rows = [r[0] for r in con.execute("select wp_id from work_queue order by wp_id")]
    con.close()
    return rows


def ready(wp: str) -> dict | None:
    """Ask the DAG projection, not my own copy of it."""
    r = subprocess.run([sys.executable, str(K / "scripts" / "work_queue.py"), "next", "--wp", wp],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0 or not r.stdout.strip():
        return None
    try:
        item = json.loads(r.stdout.strip().splitlines()[-1])
    except json.JSONDecodeError:
        return None
    return item if item.get("wp") == wp else None


def inflight(wp: str) -> bool:
    """A unit is in flight while its lock is held by a live process, or its newest receipt is a fresh PRE_ATTEMPT."""
    for lock in LOCKS.glob(f"NONCE-{wp}-*.json"):
        try:
            d = json.loads(lock.read_text(encoding="utf-8", errors="replace"))
        except (json.JSONDecodeError, OSError):
            continue
        pid = d.get("pid")
        if not pid:
            continue
        probe = subprocess.run(["powershell", "-NoProfile", "-Command",
                                f"Get-Process -Id {int(pid)} -ErrorAction SilentlyContinue | "
                                f"Select-Object -ExpandProperty Id"],
                               capture_output=True, text=True, timeout=60)
        if probe.stdout.strip():
            return True
    # A live dispatch process for this unit is the strongest signal there is; the receipt can lag it by seconds.
    probe = subprocess.run(["powershell", "-NoProfile", "-Command",
                            "$p = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and "
                            "$_.CommandLine -like '*hgk-lane-dispatch.py*' -and "
                            f"$_.CommandLine -like '*-{wp}-*' }}; ($p | Measure-Object).Count"],
                           capture_output=True, text=True, timeout=60)
    digits = "".join(ch for ch in (probe.stdout or "").strip() if ch.isdigit())
    if digits and int(digits) > 0:
        return True

    q = QUEUE / wp
    if q.is_dir():
        for rec in sorted(q.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:2]:
            try:
                d = json.loads(rec.read_text(encoding="utf-8", errors="replace"))
            except (json.JSONDecodeError, OSError):
                continue
            if not isinstance(d, dict):   # a receipt may legitimately be a list; only dicts carry a phase
                continue
            # Seconds, not an hour. A PRE_ATTEMPT receipt with no live process is a DEAD attempt: measured 01:07-01:35,
            # WP-FHS-17's round-2 receipt kept the unit "in flight" for 28 minutes while nothing ran, and the
            # supervisor stopped dispatching anything for it.
            if d.get("phase") == "PRE_ATTEMPT" and time.time() - rec.stat().st_mtime < 120:
                return True
    return False


def dispatch(item: dict) -> subprocess.Popen:
    """One unit, one lane, through the driver that owns the lane call."""
    cmd = [sys.executable, str(K / "scripts" / "continuation_driver.py"),
           "--once", "--auto-record", "--wp", item["wp"]]
    return subprocess.Popen(cmd, cwd=str(K), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            creationflags=winproc.CREATE_NO_WINDOW, text=True, encoding="utf-8", errors="replace")


def status() -> int:
    wps = all_wps()
    rows = [(wp, inflight(wp)) for wp in wps]
    live = [wp for wp, f in rows if f]
    print(json.dumps({"in_flight": live, "checked": len(wps)}, ensure_ascii=False))
    return 0


def refresh_status() -> None:
    """The status surface must be rewritten by whoever is actually acting, not only by the 3-minute watchdog."""
    try:
        subprocess.run([sys.executable, str(K / "scripts" / "ops_status.py")], capture_output=True, timeout=180)
    except (OSError, subprocess.SubprocessError):
        pass


def one_pass(max_parallel: int, verbose: bool) -> list:
    """Dispatch up to `max_parallel` ready units and hand the child handles back.

    Returning the handles matters: a child spawned from a process that exits immediately is killed with the tree on
    this host (measured: two dispatches reported pid 7596/7896 and neither wrote a receipt). The caller must keep them
    alive -- by waiting in a single pass, or by staying alive itself while watching.
    """
    started = []
    for wp in all_wps():
        if len(started) >= max_parallel:
            break
        if inflight(wp):
            continue
        item = ready(wp)
        if not item:
            continue
        p = dispatch(item)
        started.append((item["wp"], p))
        log({"action": "dispatch", "wp": wp, "phase": item.get("phase"), "pid": p.pid})
        if verbose:
            print(json.dumps({"dispatched": wp, "phase": item.get("phase"), "pid": p.pid}, ensure_ascii=False))
        time.sleep(0.4)
    refresh_status()
    return started


def main(argv=None) -> int:
    PID = K / "var" / "lane_supervisor.pid"
    PID.parent.mkdir(parents=True, exist_ok=True)
    # Single instance, enforced by the process that would be duplicated. Measured twice: one spawn produced two
    # supervisors, and they dispatched the same unit twice. A pid file that only records is not a lock.
    if PID.exists():
        try:
            other = int(PID.read_text(encoding="utf-8").strip() or 0)
        except (OSError, ValueError):
            other = 0
        if other and other != os.getpid():
            probe = subprocess.run(["powershell", "-NoProfile", "-Command",
                                    f"if (Get-Process -Id {other} -ErrorAction SilentlyContinue) {{ 1 }} else {{ 0 }}"],
                                   capture_output=True, text=True, timeout=60)
            if probe.stdout.strip().endswith("1"):
                print(json.dumps({"verdict": "SUPERVISOR_ALREADY_RUNNING", "pid": other}, ensure_ascii=False))
                return 0
    PID.write_text(str(os.getpid()), encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", action="store_true", help="keep dispatching until nothing is ready and nothing runs")
    ap.add_argument("--interval", type=float, default=5.0, help="seconds between passes while watching")
    ap.add_argument("--max-parallel", type=int, default=4, help="units allowed in flight at once")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv or sys.argv[1:])

    if args.status:
        return status()

    if not args.watch:
        started = one_pass(args.max_parallel, not args.quiet)
        results = []
        for wp, proc in started:
            try:
                out = proc.communicate(timeout=2700)[0] or ""
            except subprocess.TimeoutExpired:
                proc.kill()
                out = "TIMEOUT"
            results.append({"wp": wp, "rc": proc.returncode, "tail": out.strip().splitlines()[-1:] or [""]})
        log({"action": "pass_complete", "results": results})
        print(json.dumps({"pass": "complete", "results": results}, ensure_ascii=False))
        return 0

    idle_passes = 0
    running: list = []
    while True:
        running = [(wp, pr) for wp, pr in running if pr.poll() is None]
        started = one_pass(max(0, args.max_parallel - len(running)), not args.quiet)
        running.extend(started)
        n = len(started)
        live = [wp for wp in all_wps() if inflight(wp)]
        if not args.quiet:
            print(json.dumps({"dispatched": n, "in_flight": live, "at": time.strftime("%H:%M:%S")},
                             ensure_ascii=False), flush=True)
        if n == 0 and not live and not running:
            idle_passes += 1
            # Two consecutive quiet passes: the clock is not doing anything the work needs, so stop being a clock.
            if idle_passes >= 2:
                log({"action": "supervisor_idle_exit"})
                print(json.dumps({"verdict": "NOTHING_READY", "detail": "no unit is ready and none is in flight"},
                                 ensure_ascii=False))
                return 0
        else:
            idle_passes = 0
        time.sleep(args.interval)


if __name__ == "__main__":
    sys.exit(main())
