#!/usr/bin/env python3
"""lane_watchdog — keep exactly one lane supervisor alive, and get out of the way.

The 15-minute cron that used to pace the loop was doing two jobs badly: it was the *clock* (deciding when work may
start) and the *liveness check* (noticing that nothing runs). Those need opposite periods. The clock has to react in
seconds -- one EXECUTE run takes 15-30 min and six units were being serialised behind a timer -- while liveness only
needs to be checked every few minutes.

So the split is:

  * the supervisor (scripts/lane_supervisor.py) is the clock: it dispatches every ready unit, in parallel, within
    seconds of readiness, and exits when there is nothing left to start;
  * this watchdog is the liveness check: a short, cheap cron body that starts the supervisor if it is not already
    alive, then exits. It never decides what work may run.

The supervisor is started detached (BREAKAWAY_FROM_JOB | DETACHED_PROCESS | CREATE_NO_WINDOW) so that it outlives
this cron invocation and never puts a console on the owner's screen. Two other dispositions were measured and
rejected: a child of the cron process (killed with the job tree, receipts never written) and `cmd /c start` (a visible
window per dispatch).
"""
from __future__ import annotations

import json
import os
import subprocess
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import winproc  # noqa: E402

K = Path(__file__).resolve().parent.parent
PID = K / "var" / "lane_supervisor.pid"
OUT = Path(r"C:/wg/queue/supervisor.out")

DETACHED_PROCESS = 0x00000008
CREATE_BREAKAWAY_FROM_JOB = 0x01000000


def alive(pid: int) -> bool:
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command",
                            f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ 1 }} else {{ 0 }}"],
                           capture_output=True, text=True, timeout=60,
                           creationflags=winproc.CREATE_NO_WINDOW)
        return r.stdout.strip().endswith("1")
    except (OSError, subprocess.SubprocessError):
        return True          # unreadable answer: assume alive rather than start a second supervisor


def main() -> int:
    if PID.exists():
        try:
            pid = int(PID.read_text(encoding="utf-8").strip() or 0)
        except ValueError:
            pid = 0
        if pid and alive(pid):
            print(json.dumps({"watchdog": "ALIVE", "pid": pid}, ensure_ascii=False))
            return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    flags = winproc.CREATE_NO_WINDOW | CREATE_BREAKAWAY_FROM_JOB   # no DETACHED_PROCESS: see winproc.window_origin
    with OUT.open("a", encoding="utf-8") as fh:
        proc = subprocess.Popen(
            [sys.executable, str(K / "scripts" / "lane_supervisor.py"),
             "--watch", "--interval", "5", "--max-parallel", "3"],
            cwd=str(K), stdout=fh, stderr=subprocess.STDOUT, creationflags=flags, close_fds=True)
    # The supervisor writes its OWN pid on start. Writing it from here made the two disagree, and the next watchdog
    # found the stale value, spawned another supervisor, and the loop filled with duplicates (measured: three).
    for _ in range(20):
        time.sleep(0.5)
        if PID.exists():
            try:
                written = int(PID.read_text(encoding="utf-8").strip() or 0)
            except ValueError:
                continue
            if written and alive(written):
                print(json.dumps({"watchdog": "SPAWNED", "pid": written}, ensure_ascii=False))
                return 0
    print(json.dumps({"watchdog": "SPAWNED_UNCONFIRMED", "pid": proc.pid}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
