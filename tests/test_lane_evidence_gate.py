"""The lane gate must accept a receipt that proves what it claims and refuse one that does not."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "lane_evidence_gate.py"


def _load():
    spec = importlib.util.spec_from_file_location("lane_evidence_gate", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lane_evidence_gate"] = mod
    spec.loader.exec_module(mod)
    return mod


GATE = _load()


def _receipt(**over):
    r = {"lane": "PLAN", "ok": True, "usage_receipt_ok": True,
         "used_transport_model": "gpt-6.1-sol",
         "attempts": [{"rank": 1, "model": "gpt-6.1-sol", "provider": "desktop_router",
                       "exit": 0, "seconds": 55.5}]}
    r.update(over)
    return r


def test_accepts_a_receipt_where_the_served_model_is_the_asked_one():
    out = GATE.judge(_receipt(), "PLAN")
    assert out["verdict"] == "LANE_SERVED_AS_CLAIMED", out


def test_refuses_a_silent_substitution():
    r = _receipt()
    r["attempts"][0]["model"] = "opencode-go/mimo-v2.6-flash"
    out = GATE.judge(r, "PLAN")
    assert out["verdict"] == "LANE_CLAIM_UNSUPPORTED"
    assert any("silent_substitution" in p for p in out["problems"]), out


def test_refuses_a_fallback_arm_masquerading_as_primary():
    r = _receipt()
    r["attempts"][0]["rank"] = 2
    out = GATE.judge(r, "PLAN")
    assert any("rank_not_primary" in p for p in out["problems"]), out


def test_refuses_a_round_claiming_the_wrong_lane():
    out = GATE.judge(_receipt(), "EXECUTE")
    assert any("lane_mismatch" in p for p in out["problems"]), out


def test_refuses_a_dispatch_that_did_not_succeed():
    out = GATE.judge(_receipt(ok=False, usage_receipt_ok=False), "PLAN")
    problems = " ".join(out["problems"])
    assert "dispatch_not_ok" in problems and "usage_receipt_not_ok" in problems


def test_a_receipt_with_no_attempt_is_not_a_lane_use():
    out = GATE.judge({"lane": "PLAN", "attempts": []}, "PLAN")
    assert out["verdict"] == "NO_ATTEMPT"


def test_a_provisional_receipt_proves_the_arm_but_not_the_finish(tmp_path):
    """Falling back to a provisional receipt must weaken the claim, not silently satisfy it."""
    receipt = {"lane": "VERIFY_SECURITY", "receipt_complete": False,
               "attempts": [{"rank": 1, "provider": "openai-codex", "model": "gpt-6.1-sol",
                             "exit": 0, "seconds": 131.7}]}
    v = GATE.judge(receipt, "VERIFY_SECURITY")
    assert v["verdict"] == "LANE_SERVED_PROVISIONAL"
    assert v["receipt_complete"] is False
    assert v["served"] == "gpt-6.1-sol"


def test_a_provisional_receipt_with_a_bad_attempt_is_refused():
    receipt = {"lane": "VERIFY_SECURITY", "receipt_complete": False,
               "attempts": [{"rank": 1, "provider": "openai-codex", "model": "gpt-6.1-sol", "exit": 3}]}
    assert GATE.judge(receipt, "VERIFY_SECURITY")["verdict"] == "LANE_CLAIM_UNSUPPORTED"

    receipt["attempts"][0]["exit"] = 0
    receipt["attempts"][0]["model"] = None
    assert GATE.judge(receipt, "VERIFY_SECURITY")["verdict"] == "LANE_CLAIM_UNSUPPORTED"


def test_the_gate_judges_the_attempt_the_run_ended_on():
    """Reporting attempts[0] flattered sitting 6: the first attempt served gpt-6.1-sol, the run fell
    through to rank 4 and exited 1. The gate must read the attempt the run actually ended on."""
    receipt = {"lane": "VERIFY_SECURITY", "receipt_complete": False,
               "attempts": [
                   {"rank": 1, "provider": "openai-codex", "model": "gpt-6.1-sol", "exit": 0},
                   {"rank": 2, "provider": "opencode-go", "model": "glm-5.3-flash", "exit": 1},
                   {"rank": 4, "provider": "nvidia", "model": "deepseek-ai/deepseek-v4.1-flash", "exit": 1},
               ]}
    v = GATE.judge(receipt, "VERIFY_SECURITY")
    assert v["verdict"] == "LANE_CLAIM_UNSUPPORTED"
    assert v["rank"] == 4
    assert v["served"] == "deepseek-ai/deepseek-v4.1-flash"
    assert any("fallthrough" in p for p in v["problems"])
