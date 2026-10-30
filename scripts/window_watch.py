#!/usr/bin/env python3
"""window_watch — record any console window that appears, with the process that owns it.

Why: the owner reported windows appearing on screen while the loop runs. Three attempts to reproduce it in steady
state (300 s with three lanes and a cron tick, plus two terminal calls) recorded only Chrome's own windows. That does
not mean the owner was wrong; it means the events are short-lived and my sampling missed them, or they come from a
process I never suspected.

So this does not fix anything by itself. It is the instrument that names the culprit next time: every new visible
top-level window whose class or executable looks like a console is appended to var/console-window-events.jsonl with
its pid and executable, at 20 ms resolution.

Start it hidden:
    python scripts/window_watch.py --start        # detached, no console of its own
    python scripts/window_watch.py --status
    python scripts/window_watch.py --stop
    python scripts/window_watch.py --report
"""
from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import winproc  # noqa: E402

winproc.install()

K = Path(__file__).resolve().parent.parent
OUT = K / "var" / "console-window-events.jsonl"
PIDF = K / "var" / "window_watch.pid"

k32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

CONSOLE_CLASSES = {"ConsoleWindowClass", "CASCADIA_HOSTING_WINDOW_CLASS", "PseudoConsoleWindow",
                   "VSCodeConsoleWindowClass"}
SUSPECT_EXES = {"python.exe", "pythonw.exe", "powershell.exe", "pwsh.exe", "cmd.exe", "conhost.exe",
                "codex.exe", "node.exe", "bun.exe", "ocx.exe", "git.exe", "icacls.exe", "taskkill.exe"}


def exe_name(pid: int) -> str:
    h = k32.OpenProcess(0x1000, False, pid)
    if not h:
        return "?"
    buf = ctypes.create_unicode_buffer(512)
    size = wt.DWORD(512)
    ok = k32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size))
    k32.CloseHandle(h)
    return buf.value.split("\\")[-1] if ok else "?"


def snapshot() -> set:
    out = set()

    @ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
    def cb(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            pid = wt.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            cls = ctypes.create_unicode_buffer(64)
            user32.GetClassNameW(hwnd, cls, 64)
            title = ctypes.create_unicode_buffer(256)
            user32.GetWindowTextW(hwnd, title, 256)
            out.add((int(hwnd), pid.value, cls.value, title.value[:60]))
        return True

    user32.EnumWindows(cb, 0)
    return out


def interesting(pid: int, cls: str) -> str | None:
    exe = exe_name(pid)
    if cls in CONSOLE_CLASSES:
        return exe
    if exe.lower() in SUSPECT_EXES:
        return exe
    return None


def loop(seconds: float = 0) -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    base = snapshot()
    deadline = time.time() + seconds if seconds else None
    with OUT.open("a", encoding="utf-8") as fh:
        while True:
            cur = snapshot()
            for hwnd, pid, cls, title in cur - base:
                who = interesting(pid, cls)
                if who:
                    fh.write(json.dumps({"at": time.strftime("%Y-%m-%dT%H:%M:%S"), "exe": who, "pid": pid,
                                         "class": cls, "title": title}, ensure_ascii=False) + "\n")
                    fh.flush()
                base.add((hwnd, pid, cls, title))
            for gone in base - cur:
                base.discard(gone)
            if deadline and time.time() > deadline:
                return 0
            time.sleep(0.02)


def alive() -> int:
    if not PIDF.exists():
        return 0
    try:
        pid = int(PIDF.read_text(encoding="utf-8").strip() or 0)
    except ValueError:
        return 0
    if not pid:
        return 0
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ 1 }} else {{ 0 }}"],
                       capture_output=True, text=True, timeout=60)
    return pid if r.stdout.strip().endswith("1") else 0


def main(argv=None) -> int:
    args = argv or sys.argv[1:]
    cmd = args[0] if args else "--start"
    if cmd == "--start":
        if alive():
            print(json.dumps({"window_watch": "ALREADY", "pid": alive()}, ensure_ascii=False))
            return 0
        flags = winproc.CREATE_NO_WINDOW | 0x00000008 | 0x01000000
        proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "--loop"], close_fds=True,
                                creationflags=flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        PIDF.write_text(str(proc.pid), encoding="utf-8")
        print(json.dumps({"window_watch": "STARTED", "pid": proc.pid}, ensure_ascii=False))
        return 0
    if cmd == "--status":
        print(json.dumps({"window_watch": "alive" if alive() else "not running", "events_file": str(OUT),
                          "events": sum(1 for _ in OUT.open(encoding="utf-8")) if OUT.exists() else 0},
                         ensure_ascii=False))
        return 0
    if cmd == "--stop":
        pid = alive()
        if pid:
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True, timeout=60)
        print(json.dumps({"window_watch": "stopped" if pid else "was not running"}, ensure_ascii=False))
        return 0
    if cmd == "--report":
        if not OUT.exists():
            print("no events recorded")
            return 0
        for line in OUT.read_text(encoding="utf-8").splitlines()[-40:]:
            print(line)
        return 0
    if cmd == "--loop":
        return loop(0)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
