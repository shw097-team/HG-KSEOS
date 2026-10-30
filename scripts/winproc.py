#!/usr/bin/env python3
"""winproc — stop console windows from appearing on the owner's desktop.

Why windows appear at all: when a process has **no console** (a GUI app, or a process started with
DETACHED_PROCESS), Windows gives any console-subsystem child it launches a **brand new console**, and a new console
means a visible window. So a headless driver that spawns `powershell.exe`, `codex.exe`, `taskkill.exe` or another
`python.exe` produces a pop-up for each one -- even though the driver itself is invisible. Passing
CREATE_NO_WINDOW to the child is the only way to keep it hidden.

`install()` wraps `subprocess.run` / `subprocess.Popen` for the whole process (children inherit the intent, so it
only has to be done once per process tree root) and ORs in CREATE_NO_WINDOW. Nothing else changes: same arguments,
same return values, still fully logged -- invisible is not the same as unattended.

Verification that does not rely on the owner watching the screen: launch a long-lived console child and check
`MainWindowHandle == 0` (and that the child is alive). See `probe()`.
"""

from __future__ import annotations

import os
import subprocess
import sys

CREATE_NO_WINDOW = 0x08000000
DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

_INSTALLED = False
_HIDDEN = {"run": 0, "popen": 0}


def hidden_flags(base: int = 0) -> int:
    """Flags that keep a child off the desktop without detaching it from our handle."""
    return base | CREATE_NO_WINDOW


def install() -> bool:
    """Make every child of this process invisible. Idempotent, no-op off Windows."""
    global _INSTALLED
    if _INSTALLED or os.name != "nt":
        return False
    run, popen = subprocess.run, subprocess.Popen

    def _apply(kw: dict) -> dict:
        kw["creationflags"] = int(kw.get("creationflags") or 0) | CREATE_NO_WINDOW
        return kw

    def run_hidden(*args, **kwargs):
        if kwargs.pop("_visible", False):      # explicit escape hatch for a genuinely interactive child
            return run(*args, **kwargs)
        _HIDDEN["run"] += 1
        return run(*args, **_apply(kwargs))

    def popen_hidden(*args, **kwargs):
        if kwargs.pop("_visible", False):
            return popen(*args, **kwargs)
        _HIDDEN["popen"] += 1
        return popen(*args, **_apply(kwargs))

    subprocess.run, subprocess.Popen = run_hidden, popen_hidden
    _INSTALLED = True
    return True


def stats() -> dict:
    """How many children were launched without a console. A count of 0 after real work means the wrapper was never
    installed at this entry point -- which is exactly the defect that put 96 windows on the owner's desktop."""
    return dict(_HIDDEN, installed=_INSTALLED)


def probe(python_exe: str, seconds: int = 20) -> dict:
    """Start a console child hidden and report whether Windows gave it a main window."""
    cmd = (f"$p = Get-CimInstance Win32_Process | Where-Object {{ $_.CommandLine -like '*winproc_probe*' }}; "
           f"if($p){{ $p | ForEach-Object {{ '{{0}}|{{1}}' -f $_.ProcessId,$_.ProcessId }} }} else {{ 'NONE' }}")
    child = subprocess.Popen([python_exe, "-c",
                              "import time,sys; time.sleep(" + str(seconds) + ")  # winproc_probe"],
                             creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS, close_fds=True)
    import time
    time.sleep(2)
    out = subprocess.run(["powershell", "-NoProfile", "-Command",
                          f"(Get-Process -Id {child.pid}).MainWindowHandle"],
                         capture_output=True)
    handle = (out.stdout or b"").decode("utf-8", "replace").strip()
    alive = child.poll() is None
    return {"pid": child.pid, "alive": alive, "main_window_handle": handle,
            "invisible": handle == "0" and alive, "probe_cmd": cmd}


if __name__ == "__main__":
    install()
    print(probe(sys.executable))
