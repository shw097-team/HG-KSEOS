#!/usr/bin/env python3
"""winproc_tree_probe — does a consoleless root still put windows on the desktop?

Measures the exact failing shape: a root started with NO console (the shape detach.py creates by
swapping python.exe -> pythonw.exe), which then starts console programs that themselves start more
console programs (cmd -> git, python -> cmd -> git). Counts the visible console windows that appear
while it runs, so the answer is a number and not an impression.

Usage:  python scripts/winproc_tree_probe.py [--legacy]
        --legacy reproduces the pre-patch behaviour (CREATE_NO_WINDOW on the direct child only).
"""
from __future__ import annotations

import argparse
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


def visible_console_windows() -> list[dict]:
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    out: list[dict] = []
    CONSOLE_CLASSES = {"ConsoleWindowClass", "CASCADIA_HOSTING_WINDOW_CLASS", "PseudoConsoleWindow"}

    @ctypes.WINFUNCTYPE(ctypes.c_bool, wt.HWND, wt.LPARAM)
    def cb(hwnd, _lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        cls = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(hwnd, cls, 256)
        if cls.value not in CONSOLE_CLASSES:
            return True
        pid = wt.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        h = kernel32.OpenProcess(0x1000, False, pid.value)
        exe = ""
        if h:
            buf = ctypes.create_unicode_buffer(1024)
            size = wt.DWORD(1024)
            if kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
                exe = Path(buf.value).name
            kernel32.CloseHandle(h)
        out.append({"pid": pid.value, "exe": exe, "class": cls.value})
        return True

    user32.EnumWindows(cb, 0)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--legacy", action="store_true", help="reproduce CREATE_NO_WINDOW-on-the-direct-child only")
    ap.add_argument("--out", default=None, help="write the JSON result here (a pythonw root has no stdout)")
    args = ap.parse_args()

    if args.legacy:
        flags = winproc.CREATE_NO_WINDOW
        si = None
    else:
        winproc.install()
        flags = winproc.hidden_flags()
        si = winproc.hidden_startupinfo()

    before = {w["pid"] for w in visible_console_windows()}
    spawns = []

    def run(argv):
        kw = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL,
              "stdin": subprocess.DEVNULL, "creationflags": flags}
        if si is not None:
            kw["startupinfo"] = si
        p = subprocess.Popen(argv, **kw)
        p.wait(timeout=90)
        spawns.append({"argv": argv, "rc": p.returncode})

    # 1: direct child, 2: child -> grandchild, 3: child -> grandchild -> great-grandchild
    run(["cmd", "/c", "git --version"])
    run([sys.executable, "-c",
         "import subprocess;subprocess.run(['cmd','/c','git --version'],stdout=subprocess.DEVNULL)"])
    run([sys.executable, "-c",
         "import subprocess;subprocess.run([__import__('sys').executable,'-c',"
         "\"import subprocess;subprocess.run(['cmd','/c','git --version'],stdout=subprocess.DEVNULL)\"],"
         "stdout=subprocess.DEVNULL)"])
    time.sleep(1.5)

    after = visible_console_windows()
    new = [w for w in after if w["pid"] not in before]
    result = {"mode": "legacy" if args.legacy else "patched",
              "spawns": spawns, "new_console_windows": len(new),
              "windows": new[:10],
              "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
    text = json.dumps(result, ensure_ascii=False, indent=1)
    print(text)
    # A pythonw root has no stdout: the result must land on disk or the measurement is lost.
    out = args.out or os.environ.get("WINPROC_PROBE_OUT")
    if out:
        Path(out).write_text(text, encoding="utf-8")
    return 0 if (args.legacy or not new) else 2


if __name__ == "__main__":
    raise SystemExit(main())
