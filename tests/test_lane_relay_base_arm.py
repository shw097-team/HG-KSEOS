"""An arm's provider and the relay base must agree, and the disagreement must be named before any spawn.

Measured defect (this round, D-16 as first stated and then corrected): `EXECUTE --require-arm
opencode-go/deepseek-v4.1-flash` was reported unroutable. It was not the pin. The same pinned run returns
ok:true in 2.7 s against the default loopback relay, and fails in 2.8 s with

    The 'opencode-go/deepseek-v4.1-flash' model is not supported when using Codex with a ChatGPT account.

when it carries `--relay-base https://chatgpt.com/backend-api/codex` -- the OAuth upstream, which will not serve
a non-OpenAI model to a ChatGPT account. A three-second refusal that names the model reads as a dead arm, and
that is what three separate investigations concluded before this was measured.

So the combination is refused by name, before any spawn, and the refusal carries the remedy. This test runs the
real CLI (the refusal happens pre-spawn, so no model call is made and the test is fast).
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
UPSTREAM = "https://chatgpt.com/backend-api/codex"
LOOPBACK = "http://127.0.0.1:10101/v1"


def run(*extra: str) -> dict:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "r.json"
        subprocess.run(
            [sys.executable, str(DISPATCH), "--lane", "EXECUTE",
             "--prompt", "reply with: PROBE", "--nonce", "NONCE-TEST-RELAYBASE",
             "--require-arm", "opencode-go/deepseek-v4.1-flash",
             "--identity-source", "codex-rollout",
             "--codex-home", str(Path.home() / ".codex"), "--allow-human-home-transport",
             "--timeout", "20", "--json-out", str(out), *extra],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
        )
        if not out.exists():
            raise AssertionError("dispatcher wrote no receipt")
        return json.loads(out.read_text(encoding="utf-8"))


class TestRelayBaseMustMatchArmProvider(unittest.TestCase):
    def test_opencode_arm_with_oauth_upstream_is_refused_by_name(self):
        r = run("--relay-base", UPSTREAM)
        self.assertFalse(r["ok"])
        self.assertEqual(r["code"], "ERR_RELAY_BASE_INCOMPATIBLE_WITH_ARM")
        self.assertEqual(r.get("arm_provider"), "opencode-go")
        # The refusal must carry the remedy, not just the diagnosis.
        self.assertIn("drop --relay-base", r.get("next_command") or "")
        self.assertIn("10101", r.get("next_command") or "")

    def test_the_refusal_happens_before_any_spawn(self):
        """No attempt may exist: a refusal that spent a model call would be the bug it is preventing."""
        r = run("--relay-base", UPSTREAM)
        self.assertEqual(r.get("attempts") or [], [])

    def test_the_default_relay_is_not_refused(self):
        """The same arm on the loopback relay must get past this gate -- the gate is about the base, not the arm."""
        r = run("--relay-base", LOOPBACK)
        self.assertNotEqual(r.get("code"), "ERR_RELAY_BASE_INCOMPATIBLE_WITH_ARM")


if __name__ == "__main__":
    unittest.main()
