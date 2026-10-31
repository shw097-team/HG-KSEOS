"""REQ-SEC-ROLLOUT-BINDING: the identity source must be able to say "this rollout is mine".

The officer's sitting-C probe found that `--identity-source codex-rollout` resolves the newest rollout in the
lane home without binding it to the spawn: a rollout written by an unrelated turn in the same directory was
accepted, while a rollout from a different cwd was refused. So the served identity is "the newest thing in this
directory", not "this child's turn".

That is a real impersonation surface, and it cannot be patched in this round without removing the only identity
source that currently serves all three lanes. So the guarantee is made *askable* instead: a run that demands it
is refused by name, before any spawn, and the refusal carries the requirement id. Asking for a guarantee that
does not exist must fail loudly; silently waiving it is how a known gap becomes an assumed property.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISPATCH = ROOT / "scripts" / "hgk-lane-dispatch.py"


def run(*extra: str) -> dict:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "r.json"
        subprocess.run(
            [sys.executable, str(DISPATCH), "--lane", "VERIFY_SECURITY",
             "--prompt", "reply with: PROBE", "--nonce", "NONCE-TEST-ROLLOUTBIND",
             "--identity-source", "codex-rollout",
             "--codex-home", str(Path.home() / ".codex"), "--allow-human-home-transport",
             "--timeout", "20", "--json-out", str(out), *extra],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
        )
        if not out.exists():
            raise AssertionError("dispatcher wrote no receipt")
        return json.loads(out.read_text(encoding="utf-8"))


class TestRolloutBindingIsAskable(unittest.TestCase):
    def test_asking_for_the_binding_is_refused_by_name(self):
        r = run("--require-rollout-binding")
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "ERR_ROLLOUT_BINDING_UNIMPLEMENTED")
        self.assertEqual(r.get("requirement"), "REQ-SEC-ROLLOUT-BINDING")

    def test_the_refusal_costs_no_spawn(self):
        r = run("--require-rollout-binding")
        self.assertEqual(r.get("attempts") or [], [],
                         "a refusal that spent a model call is the bug it exists to prevent")

    def test_the_refusal_says_how_to_proceed_without_it(self):
        r = run("--require-rollout-binding")
        self.assertIn("omit --require-rollout-binding", r.get("next_command") or "")


if __name__ == "__main__":
    unittest.main()
