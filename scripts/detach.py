#!/usr/bin/env python3
"""detach — start a process outside Hermes' job tree so it survives the turn.

Why this exists
---------------
Measured 2026-10-31: three lane dispatches (WP-FHS-11 02:01:32, WP-FHS-20 02:17:47, WP-FHS-17 02:18:00) each wrote
their PRE_ATTEMPT receipt and then vanished with no attempt row, and the loop was silent from 02:18 to 07:39 -- five
hours twenty-one minutes -- with the watchdog dead as well. `CREATE_BREAKAWAY_FROM_JOB` does not break away when the
parent is already inside a nested job object, so a child spawned by `subprocess.Popen` still dies with the turn.

`Win32_Process.Create` (WMI) asks the service host for the process instead of forking it, so the new process has no
parent job to be killed with. That is the only launch path here that has survived a turn boundary.

Usage
-----
    python scripts/detach.py --out <logfile> -- <command> [args...]

Prints JSON: {"pid": N, "ok": true, "cmdline": "..."} and never raises for a child failure -- the caller decides.
"""
from __future__ import annotations


try:  # every child of this process must be consoleless; see scripts/winproc.py and console_guard_gate.py
    import winproc as _winproc  # noqa: E402  (same directory)
    _winproc.install()
except Exception:  # a missing helper must not stop the tool
    pass


import argparse
import json
import subprocess
import time
import sys
from pathlib import Path

CREATE_NO_WINDOW = 0x08000000


def _ps_quote(value: str) -> str:
    """PowerShell single-quoted literal: double the quote, nothing else is special."""
    return "'" + value.replace("'", "''") + "'"


def _consoleless(argv: list[str]) -> list[str]:
    """Swap a console interpreter for its windowless twin.

    `python.exe` started by the service host allocates a console; `pythonw.exe` never does. Same for the WScript host.
    """
    if argv and argv[0].lower().endswith("python.exe"):
        twin = Path(argv[0]).with_name("pythonw.exe")
        if twin.exists():
            argv = [str(twin), *argv[1:]]
    return argv


def create(cmdline: str, cwd: str) -> tuple[int, str]:
    ps = (
        "$r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{"
        f"CommandLine={_ps_quote(cmdline)}; CurrentDirectory={_ps_quote(cwd)}"
        "}; \"$($r.ProcessId)|$($r.ReturnValue)\""
    )
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True,
                       creationflags=CREATE_NO_WINDOW, timeout=120)
    out = (r.stdout or "").strip().splitlines()
    line = out[-1] if out else ""
    pid, _, rc = line.partition("|")
    if not pid.strip().isdigit():
        return 0, (r.stderr or r.stdout or "no pid").strip()[:300]
    if rc.strip() not in ("", "0"):
        return 0, f"Win32_Process.Create returned {rc.strip()}"
    return int(pid.strip()), ""


def _prove_alive(pid: int, expect_image: str, budget_s: float = 1.5) -> tuple[bool, str]:
    """Is that pid alive, and is it the program we asked for?

    MEASURED 2026-10-31: Win32_Process.Create returns `ok: true` with a pid for children that die in the same
    second -- 30 vanished dispatch attempts on one work package read as "dispatched" and produced no receipt at
    all. A launcher that cannot see its child is not a launcher: success must mean alive AND the expected image.
    """
    import ctypes
    import ctypes.wintypes as wt
    k32 = ctypes.windll.kernel32
    STILL_ACTIVE = 259
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    deadline = time.time() + budget_s
    last = "not sampled"
    while time.time() < deadline:
        h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
        if not h:
            last = "pid not found"
            time.sleep(0.05)
            continue
        try:
            code = wt.DWORD()
            if not k32.GetExitCodeProcess(h, ctypes.byref(code)) or code.value != STILL_ACTIVE:
                last = f"exited with {code.value}"
                return False, last
            buf = ctypes.create_unicode_buffer(1024)
            size = wt.DWORD(1024)
            image = ""
            if k32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
                image = Path(buf.value).name.lower()
            if image and expect_image:
                want = Path(expect_image).name.lower()
                # python.exe is swapped for pythonw.exe on purpose, so accept the windowless twin
                if image not in (want, want.replace(".exe", "w.exe")):
                    return False, f"image is {image}, expected {want}"
            return True, image or "alive"
        finally:
            k32.CloseHandle(h)
        time.sleep(0.05)
    return False, f"never observed alive ({last})"


def launch(argv: list[str], out: Path | None = None, cwd: str | None = None) -> dict:
    """Run argv outside the job tree. A log file is redirected by wrapping in cmd.exe when one is asked for."""
    cwd = cwd or str(Path.cwd())
    argv = _consoleless(argv)
    inner = subprocess.list2cmdline(argv)
    if out is not None:
        # Win32_Process.Create cannot pass handles, and `cmd /c ... >> log` would need a cmd.exe -- which the service
        # host starts WITH a console, i.e. a visible window on the owner's desktop (measured 07:41-07:44: ten cmd.exe
        # consoles and twenty Windows Terminal windows from exactly this wrapper). So no wrapper: the child logs itself.
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open("a", encoding="utf-8") as fh:
                fh.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} launched, no redirection (child logs itself): "
                         f"{inner}\n")
        except OSError:
            pass       # a note that cannot be written must not stop a launch
    pid, err = create(inner, cwd)
    if not pid:
        return {"ok": False, "pid": 0, "cmdline": inner, "error": err}
    alive, why = _prove_alive(pid, argv[0] if argv else "")
    if not alive:
        # Not a warning: a pid that is already gone means the caller must NOT record this as a dispatch.
        return {"ok": False, "pid": pid, "cmdline": inner,
                "error": f"CHILD_NOT_ALIVE_AFTER_LAUNCH: {why}"}
    return {"ok": True, "pid": pid, "cmdline": inner, "error": "", "liveness": why}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--cwd", default=None)
    ap.add_argument("command", nargs=argparse.REMAINDER)
    args = ap.parse_args(argv)
    cmd = [c for c in args.command if c != "--"]
    if not cmd:
        print(json.dumps({"ok": False, "error": "no command"}))
        return 2
    res = launch(cmd, Path(args.out) if args.out else None, args.cwd)
    print(json.dumps(res, ensure_ascii=False))
    return 0 if res["ok"] else 3


if __name__ == "__main__":
    sys.exit(main())
