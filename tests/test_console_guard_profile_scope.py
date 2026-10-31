"""The console gate must catch the shape that actually popped windows, and must not cry wolf.

Measured 2026-10-31: minutes after the continuation supervisor was resumed the owner reported windows appearing
again. The supervisor re-execs itself under pythonw (no console) and then called

    subprocess.run([PY, *args], capture_output=True, text=True, timeout=timeout)

with no creationflags. On Windows a console program started from a console-less parent gets a NEW console, and a
new console is a window -- so hiding the parent made every child visible. The gate reported 32/33 OK because it
only ever scanned HG-KSEOS/scripts, and the tick body lives in the profile's scripts dir.

These tests pin: the pre-fix body is caught, the fixed body is not, and a local helper named `run` is not mistaken
for subprocess.run (flagging the wrapper that already passes the flag is how a gate earns the right to be ignored).
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import console_guard_gate as gate  # noqa: E402

PRE_FIX = '''
import subprocess

def run(args, timeout):
    return subprocess.run([PY, *args], capture_output=True, text=True, timeout=timeout)
'''

POST_FIX = '''
import os, subprocess

def run(args, timeout):
    kw = {}
    if os.name == "nt":
        kw["creationflags"] = 0x08000000
    return subprocess.run([PY, *args], capture_output=True, text=True, timeout=timeout, **kw)
'''

LOCAL_HELPER_ONLY = '''
import subprocess

def run(args, timeout):
    return subprocess.run([PY, *args], creationflags=0x08000000, timeout=timeout)

def main():
    return run(["--once"], 600)
'''


class TestSpawnSites(unittest.TestCase):
    def check(self, body: str):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "subject.py"
            p.write_text(body, encoding="utf-8")
            return gate.spawn_sites_without_flags(p)

    def test_the_body_that_popped_windows_is_caught(self):
        hits = self.check(PRE_FIX)
        self.assertEqual(len(hits), 1, hits)
        self.assertEqual(hits[0]["state"], "SPAWN_WITHOUT_CREATIONFLAGS")

    def test_the_fixed_body_passes(self):
        self.assertEqual(self.check(POST_FIX), [])

    def test_a_local_helper_named_run_is_not_subprocess_run(self):
        self.assertEqual(self.check(LOCAL_HELPER_ONLY), [])

    def test_the_profile_scripts_are_in_scope(self):
        dirs = gate.profile_script_dirs()
        self.assertTrue(dirs, "the tick body lives in a profile; scanning only HG-KSEOS/scripts is the blind spot")
        names = {p.name for d in dirs for p in d.glob("*.py")}
        self.assertIn("hgk_continuation.py", names)


if __name__ == "__main__":
    unittest.main()
