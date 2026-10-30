#!/usr/bin/env python3
"""relay_daemon — start, check and stop the ocx relay without putting a console on the owner's screen.

Measured 2026-10-31: the relay was alive and healthy while a `cmd.exe /K "ocx.cmd start --port 10101"` window sat on
the desktop. Killing the `cmd` wrapper did not help — `node.exe` had **inherited** that console, so the window simply
changed owner. Two conclusions, both acted on here:

1. A console window is attached at spawn time; it cannot be removed by killing the parent. It must either be hidden
   with `ShowWindow(SW_HIDE)` or, correctly, never created: `CREATE_NO_WINDOW` on a detached spawn.
2. `ocx start` is a foreground launcher. Anything that calls it from a headless driver inherits a window, so this
   module is the only sanctioned way to bring the relay up.

  relay_daemon.py status
  relay_daemon.py start [--port 10101]     # detached, no console, waits for /healthz
  relay_daemon.py hide                     # hides a console that already exists (does not restart the proxy)
  relay_daemon.py stop

Exit: 0 healthy · 3 not healthy · 2 bad usage
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

CREATE_NO_WINDOW = 0x08000000
DETACHED = 0x00000008

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import winproc
    winproc.install()
except Exception:
    pass


def health(port: int = 10101, timeout: float = 3.0) -> int:
    try:
        r = subprocess.run(["curl", "-s", "-o", os.devnull, "-w", "%{http_code}",
                            f"http://127.0.0.1:{port}/healthz"], capture_output=True, timeout=timeout)
        return int((r.stdout or b"0").decode().strip() or 0)
    except Exception:
        return 0


def ocx_pids() -> list[dict]:
    cmd = (r"Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*opencodex*' } | "
           r"ForEach-Object { '{0}|{1}|{2}' -f $_.ProcessId,$_.Name,(Get-Process -Id $_.ProcessId -ErrorAction SilentlyContinue).MainWindowHandle }")
    r = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True)
    out = []
    for line in (r.stdout or b"").decode("utf-8", "replace").splitlines():
        parts = line.strip().split("|")
        if len(parts) == 3 and parts[0].isdigit():
            out.append({"pid": int(parts[0]), "name": parts[1], "main_window": parts[2]})
    return out


def ocx_argv() -> list[str] | None:
    from shutil import which
    exe = which("ocx") or which("opencodex")
    if not exe:
        return None
    if os.name == "nt" and not exe.lower().endswith(".exe"):
        # npm shims (.cmd) need cmd, but cmd is a console program: launching it is exactly how the window appeared.
        # The real server is the .mjs, so run that under node instead.
        cand = Path(os.environ.get("APPDATA", "")) / "npm/node_modules/@bitkyc08/opencodex/bin/ocx.mjs"
        node = which("node")
        if cand.is_file() and node:
            return [node, str(cand)]
        return ["cmd", "/c", exe]
    return [exe]


def start(port: int = 10101) -> dict:
    if health(port) == 200:
        return {"started": False, "why": "already healthy", "port": port}
    argv = ocx_argv()
    if not argv:
        return {"started": False, "why": "ocx not found"}
    argv = [*argv, "start", "--port", str(port)]
    log = Path(r"C:/wg/relay/ocx.log")
    log.parent.mkdir(parents=True, exist_ok=True)
    fh = open(log, "ab")
    p = subprocess.Popen(argv, stdout=fh, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                         creationflags=CREATE_NO_WINDOW | DETACHED, close_fds=True)
    for _ in range(40):
        time.sleep(0.5)
        if health(port) == 200:
            return {"started": True, "pid": p.pid, "argv": argv, "port": port, "health": 200,
                    "console": "none (CREATE_NO_WINDOW|DETACHED)"}
    return {"started": True, "pid": p.pid, "argv": argv, "port": port, "health": health(port),
            "note": "spawned but /healthz not answering yet; see " + str(log)}


def hide_existing() -> dict:
    code = r'''
$sig = @"
using System; using System.Runtime.InteropServices;
public class W { [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
                 [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h); }
"@
Add-Type -TypeDefinition $sig
$rows = @()
foreach ($p in Get-Process | Where-Object { $_.MainWindowHandle -ne 0 -and ($_.ProcessName -match 'node|bun|cmd|ocx') }) {
  $h = $p.MainWindowHandle
  [void][W]::ShowWindow($h, 0)
  $rows += ('{0}|{1}|{2}' -f $p.Id, $p.ProcessName, [W]::IsWindowVisible($h))
}
if ($rows.Count -eq 0) { 'none' } else { $rows -join "`n" }
'''
    r = subprocess.run(["powershell", "-NoProfile", "-Command", code], capture_output=True)
    return {"hidden": (r.stdout or b"").decode("utf-8", "replace").strip()}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["status", "start", "hide", "stop"])
    ap.add_argument("--port", type=int, default=10101)
    a = ap.parse_args(argv or sys.argv[1:])
    if a.action == "status":
        procs = ocx_pids()
        visible = [p for p in procs if p["main_window"] != "0"]
        print(json.dumps({"health": health(a.port), "port": a.port, "procs": procs,
                          "visible_windows": visible,
                          "verdict": "RELAY_OK" if health(a.port) == 200 and not visible else
                                     ("RELAY_VISIBLE" if visible else "RELAY_DOWN")}, ensure_ascii=False))
        return 0 if health(a.port) == 200 and not visible else 3
    if a.action == "hide":
        print(json.dumps(hide_existing(), ensure_ascii=False))
        return 0
    if a.action == "start":
        print(json.dumps(start(a.port), ensure_ascii=False))
        return 0 if health(a.port) == 200 else 3
    if a.action == "stop":
        killed = []
        for p in ocx_pids():
            subprocess.run(["taskkill", "/PID", str(p["pid"]), "/T", "/F"], capture_output=True)
            killed.append(p["pid"])
        print(json.dumps({"stopped": killed}, ensure_ascii=False))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
