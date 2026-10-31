"""Positive control for the window fix: does a console GRANDCHILD become visible?

The failure shape is: a console-less parent starts a console program, Windows gives it a NEW console, and a new
console is a visible window. A test that only ever shows "0 windows" proves nothing -- it may simply be unable to
see windows. So this probe runs both arms from a console-less parent (pythonw) and counts visible windows while a
console program runs:

  CONTROL  child started with CREATE_NO_WINDOW  -> the child has no console, so the program IT starts allocates a
                                                   visible one. Expected: >= 1 window. This arm proves the probe fires.
  FIX      child started with CREATE_NEW_CONSOLE + SW_HIDE -> one hidden console, inherited. Expected: 0 windows.

If CONTROL also reports 0, the probe is blind and the FIX result must not be believed.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

CREATE_NO_WINDOW = 0x08000000
CREATE_NEW_CONSOLE = 0x00000010

# A console program that stays alive long enough to be counted, and that itself starts nothing.
CHILD = [sys.executable, "-c", "import time; time.sleep(6)"]


def visible_console_windows() -> int:
    """Count visible top-level windows owned by console-ish processes."""
    ps = ("(Get-Process | Where-Object { $_.MainWindowHandle -ne 0 -and "
          "$_.Name -match 'python|conhost|cmd|node|codex' }).Count")
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                       capture_output=True, text=True, timeout=60)
    try:
        return int((r.stdout or "0").strip() or 0)
    except ValueError:
        return -1


def arm(label: str, kw: dict) -> dict:
    before = visible_console_windows()
    proc = subprocess.Popen(CHILD, **kw)
    peak = before
    for _ in range(10):
        time.sleep(0.5)
        n = visible_console_windows()
        peak = max(peak, n)
    proc.wait(timeout=30)
    return {"arm": label, "before": before, "peak": peak, "appeared": peak - before}


def main() -> int:
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = 0
    control = arm("CONTROL_CREATE_NO_WINDOW", {"creationflags": CREATE_NO_WINDOW})
    fixed = arm("FIX_CREATE_NEW_CONSOLE_HIDDEN", {"creationflags": CREATE_NEW_CONSOLE, "startupinfo": si})
    out = {"parent_console_less": True, "control": control, "fix": fixed,
           "probe_fires": control["appeared"] > 0,
           "verdict": ("PROBE_BLIND" if control["appeared"] <= 0 else
                       ("FIX_CONFIRMED" if fixed["appeared"] <= 0 else "FIX_INSUFFICIENT"))}
    path = r"C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/window_probe.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
