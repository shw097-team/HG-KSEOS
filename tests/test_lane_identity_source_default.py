"""The identity source must be the honest default, and the frozen failure classification must not move.

Two separate things are pinned here:

1. `--identity-source` defaults to `codex-rollout`. Measured on this host, the old default `relay-usage` can
   never obtain a usage row for an OAuth-direct turn, so a perfectly serving arm was reported as
   `ERR_LANE_ALL_ROUTES_EXHAUSTED` -- a dead lane that was not dead. The default is what an unattended round
   uses, so leaving the wrong value there means every future round rediscovers the same false conclusion.

2. `failure_disposition()` keeps its frozen vocabulary. The fix above is a DEFAULT change, not a
   reclassification: a run with no acceptable turn still reports `ERR_LANE_ALL_ROUTES_EXHAUSTED`, and a run
   that answered without a nonce still reports `ERR_NO_ARM_EMITTED_NONCE`. If a future edit makes the honest
   case "pass" by weakening this function, these tests fail.

Run: python -m unittest tests.test_lane_identity_source_default -v
"""
from __future__ import annotations

import ast
import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DISPATCH = REPO / "scripts" / "hgk-lane-dispatch.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("hgk_lane_dispatch_under_test", DISPATCH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


class IdentitySourceDefault(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tree = ast.parse(DISPATCH.read_text(encoding="utf-8"))
        cls.mod = _load_module()

    def _identity_source_defaults(self):
        """Every default= that a --identity-source argument declares, and every getattr fallback for it."""
        arg_defaults, getattr_fallbacks = [], []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                fname = getattr(node.func, "attr", getattr(node.func, "id", ""))
                if fname == "add_argument":
                    names = [a.value for a in node.args
                             if isinstance(a, ast.Constant) and isinstance(a.value, str)]
                    if "--identity-source" in names:
                        for kw in node.keywords:
                            if kw.arg == "default" and isinstance(kw.value, ast.Constant):
                                arg_defaults.append(kw.value.value)
                if fname == "getattr" and len(node.args) >= 3:
                    a1, a2 = node.args[1], node.args[2]
                    if (isinstance(a1, ast.Constant) and a1.value == "identity_source"
                            and isinstance(a2, ast.Constant)):
                        getattr_fallbacks.append(a2.value)
        return arg_defaults, getattr_fallbacks

    def test_argument_default_is_codex_rollout(self):
        arg_defaults, _ = self._identity_source_defaults()
        self.assertEqual(arg_defaults, ["codex-rollout"],
                         "the declared default must be the source that can actually resolve an OAuth turn")

    def test_every_fallback_agrees_with_the_declared_default(self):
        arg_defaults, fallbacks = self._identity_source_defaults()
        self.assertTrue(fallbacks, "expected at least one getattr fallback to be pinned")
        self.assertEqual(set(fallbacks), set(arg_defaults),
                         f"getattr fallbacks {sorted(set(fallbacks))} disagree with the declared default "
                         f"{arg_defaults}: a call path without the flag would silently use a different source")

    def test_the_flag_still_offers_both_sources(self):
        # Narrowing the choices would make the measured negative (relay-usage) impossible to reproduce.
        choices = None
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "add_argument":
                names = [a.value for a in node.args if isinstance(a, ast.Constant)]
                if "--identity-source" in names:
                    for kw in node.keywords:
                        if kw.arg == "choices" and isinstance(kw.value, ast.Tuple):
                            choices = [e.value for e in kw.value.elts]
        self.assertEqual(choices, ["relay-usage", "codex-rollout"])


class FrozenFailureClassification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_no_acceptable_turn_is_still_exhausted(self):
        attempts = [{"rank": 1, "provider": "openai-codex", "model": "gpt-6.1-sol",
                     "exit": 1, "usage_receipt_ok": False, "nonce_present": False}]
        self.assertEqual(self.mod.failure_disposition(attempts)["code"],
                         "ERR_LANE_ALL_ROUTES_EXHAUSTED")

    def test_answered_without_nonce_is_named(self):
        attempts = [{"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash",
                     "exit": 0, "usage_receipt_ok": True, "nonce_present": False}]
        self.assertEqual(self.mod.failure_disposition(attempts)["code"], "ERR_NO_ARM_EMITTED_NONCE")

    def test_answered_with_nonce_is_not_a_failure(self):
        attempts = [{"rank": 1, "provider": "opencode-go", "model": "deepseek-v4.1-flash",
                     "exit": 0, "usage_receipt_ok": True, "nonce_present": True}]
        self.assertEqual(self.mod.failure_disposition(attempts)["code"], "ERR_LANE_ALL_ROUTES_EXHAUSTED")


if __name__ == "__main__":
    unittest.main()
