"""Three-level window probe: does a console GRANDCHILD become visible, and does the hidden-console fix stop it?

A two-level probe misses this shape. The chain that pops a window is:

    console-less parent (pythonw)  ->  child with CREATE_NO_WINDOW (still console-less)
        ->  grandchild console program  ->  Windows gives IT a fresh console  ->  visible window

  CONTROL  grandchild under a CREATE_NO_WINDOW child            -> expected >= 1 console window
  FIX      grandchild under a CREATE_NEW_CONSOLE+SW_HIDE child  -> expected 0

Both arms run from a console-less parent so the comparison is honest. If CONTROL is 0 the harness is blind and the
FIX result must not be believed -- that is the mistake this file exists to prevent, having made it once already.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

CREATE_NO_WINDOW = 0x08000000
CREATE_NEW_CONSOLE = 0x00000010

# The child stays alive, gives its own child no console, and that grandchild is a console program.
# The grandchild must be a CONSOLE program. A first version spawned sys.executable, which under pythonw is
# pythonw.exe -- a GUI program with no console -- so the control arm produced nothing and the probe declared itself
# blind. cmd.exe is the real shape: a console program started by a console-less parent.
CHILD = (
    "import subprocess,time;"
    "subprocess.run(['cmd','/c','ping -n 6 127.0.0.1 >nul']);"
    "time.sleep(1)"
)


def arm(label: str, flags: int, hide_si: bool) -> dict:
    si = subprocess.STARTUPINFO()
    if hide_si:
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0                      # SW_HIDE
    kw: dict = {"creationflags": flags}
    if hide_si:
        kw["startupinfo"] = si
    before = os.path.getsize(LOG) if os.path.exists(LOG) else 0
    proc = subprocess.Popen([sys.executable, "-c", CHILD], **kw)
    proc.wait(timeout=60)
    time.sleep(1.0)
    after = os.path.getsize(LOG) if os.path.exists(LOG) else 0
    events = []
    if after > before:
        with open(LOG, encoding="utf-8") as fh:
            fh.seek(before)
            for line in fh:
                try:
                    events.append(json.loads(line))
                except ValueError:
                    pass
    return {"arm": label, "flags": hex(flags), "hide_startupinfo": hide_si,
            "events": len(events),
            "examples": [{"exe": e.get("exe"), "class": e.get("class"), "title": (e.get("title") or "")[:50]}
                         for e in events[:5]]}


LOG = r"C:/Projects/Agent_Workspace/HG-KSEOS/var/console-window-events.jsonl"


def main() -> int:
    if not os.path.exists(LOG):
        print(json.dumps({"verdict": "NO_INSTRUMENT",
                          "why": "start it first: python scripts/window_watch.py --start"}))
        return 2
    control = arm("CONTROL_GRANDCHILD_OF_CREATE_NO_WINDOW", CREATE_NO_WINDOW, False)
    fixed = arm("FIX_GRANDCHILD_OF_HIDDEN_CONSOLE", CREATE_NEW_CONSOLE, True)
    out = {"parent_console_less": True, "instrument": LOG, "control": control, "fix": fixed,
           "probe_fires": control["events"] > 0,
           "verdict": ("PROBE_BLIND" if control["events"] <= 0 else
                       ("FIX_CONFIRMED" if fixed["events"] == 0 else "FIX_INSUFFICIENT"))}
    path = r"C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/window_probe.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
