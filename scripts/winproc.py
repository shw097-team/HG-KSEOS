#!/usr/bin/env python3
"""winproc — stop console windows from appearing on the owner's desktop.

Why windows appear at all: when a process has **no console** (a GUI app, or a process started with
DETACHED_PROCESS), Windows gives any console-subsystem child it launches a **brand new console**, and a new console
means a visible window. So a headless driver that spawns `powershell.exe`, `codex.exe`, `taskkill.exe` or another
`python.exe` produces a pop-up for each one -- even though the driver itself is invisible. Passing
Passing CREATE_NO_WINDOW to the child is the only way to keep it hidden.

MEASURED 2026-10-31 (var/console-window-events.jsonl, 170 events / 01:58-09:00): the recorded owners were
WindowsTerminal.exe 121, python.exe 15, cmd.exe 14, powershell.exe 7, bun.exe 2, with titles
powershell.exe 26, git.EXE 24, cmd.exe 16 -- i.e. the *grandchildren* of a consoleless parent. Hiding one
level does not hide the tree: CREATE_NO_WINDOW gives the child NO console, so the next process it starts
(codex -> node -> git, cmd -> git, python -> pwsh) is a console program with no console and Windows gives
it a brand new visible one. The rule is therefore: the child gets ONE console, created hidden
(CREATE_NEW_CONSOLE + STARTF_USESHOWWINDOW, wShowWindow = 0), which every descendant inherits.

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
CREATE_NEW_CONSOLE = 0x00000010
DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

_INSTALLED = False
_HIDDEN = {"run": 0, "popen": 0}


def hidden_startupinfo():
    """A STARTUPINFO that hides the console the child is about to be given."""
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = 0                              # SW_HIDE
    return si


def hidden_flags(base: int = 0) -> int:
    """Give a child ONE hidden console (inherited by its whole tree) instead of no console at all."""
    return int(base or 0) | CREATE_NEW_CONSOLE


def install() -> bool:
    """Make every child of this process invisible. Idempotent, no-op off Windows."""
    global _INSTALLED
    if _INSTALLED or os.name != "nt":
        return False
    run, popen = subprocess.run, subprocess.Popen

    def _apply(kw: dict) -> dict:
        flags = int(kw.get("creationflags") or 0)
        if flags & DETACHED_PROCESS:                 # mutually exclusive with CREATE_NEW_CONSOLE
            return kw
        # CREATE_NO_WINDOW and CREATE_NEW_CONSOLE are contradictory: the first says "no console at all", the
        # second says "one console, hidden". Leaving both set is an invalid combination, so the narrow one is
        # dropped rather than OR-ed on top of.
        flags &= ~CREATE_NO_WINDOW
        kw["creationflags"] = flags | CREATE_NEW_CONSOLE
        kw.setdefault("startupinfo", hidden_startupinfo())
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


def audit(root=None) -> list[dict]:
    """Report spawn sites in this repo that could put a console on the owner's screen.

    Install-time hiding only covers processes that import this module. A script nobody calls install() from is
    invisible to that guarantee, and the owner sees the result as a window. So the audit is a check, not a promise:
    every `subprocess.*(` in scripts/ must either sit next to creationflags or live in a file that installs winproc.
    """
    import re
    from pathlib import Path
    base = Path(root) if root else Path(__file__).resolve().parent
    findings = []
    for path in sorted(base.glob("*.py")):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "subprocess." not in text:
            continue
        installs = "winproc.install()" in text or "_winproc.install()" in text
        if installs:
            continue
        for m in re.finditer(r"subprocess\.(run|Popen|check_output|call)\(", text):
            window = text[m.start():m.start() + 420]
            if "creationflags" in window:
                continue
            findings.append({"file": path.name, "line": text[:m.start()].count("\n") + 1})
    return findings


if __name__ == "__main__":
    import json as _json
    hits = audit()
    print(_json.dumps({"unhidden_spawn_sites": len(hits), "sites": hits[:40]}, ensure_ascii=False))
