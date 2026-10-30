"""The refusal gate must reject a guess wearing the form of a finding, and accept a real one."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys

import pytest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "refusal_gate.py"


def _load():
    spec = importlib.util.spec_from_file_location("refusal_gate", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["refusal_gate"] = mod
    spec.loader.exec_module(mod)
    return mod


GATE = _load()


def test_rejects_a_circumstance_dressed_as_a_finding():
    doc = {"refusals": [{"wp": "WP-X", "reason": "no host capability on this machine; only one host"}]}
    out = GATE.judge(doc)
    assert out["verdict"] == "REFUSAL_NOT_FALSIFIABLE"
    reasons = " ".join(out["failures"][0]["reasons"])
    assert "circumstance_not_object" in reasons
    assert "missing:cited_text" in reasons


def test_accepts_a_refusal_that_names_the_absent_object_and_shows_the_search():
    doc = {"refusals": [{
        "wp": "WP-FHS-02",
        "reason": "Fabric carries no policy epoch object",
        "cited_text": "Done: Source/Stage/Approve/Active/Loaded/Consumer each hash in the same scope",
        "absent_object": "Fabric policy epoch object",
        "reproduction": ["grep -rl POLICY_EPOCH FABRIC/ -> empty", "ls FABRIC/control | grep -i epoch -> empty"],
        "falsifier": "a declared epoch object appears in FABRIC/control",
        "expiry": "2026-12-31",
    }]}
    out = GATE.judge(doc)
    assert out["verdict"] == "REFUSALS_FALSIFIABLE", out


def test_a_refusal_resting_on_a_short_quote_is_not_a_quote():
    doc = {"refusals": [{
        "wp": "WP-X", "reason": "the object is missing",
        "cited_text": "HOST_OP", "absent_object": "epoch",
        "reproduction": ["search run"], "falsifier": "it exists", "expiry": "2026-12-31",
    }]}
    out = GATE.judge(doc)
    assert "cited_text_too_short_to_be_a_quote" in " ".join(out["failures"][0]["reasons"])


def test_missing_record_is_an_error_not_a_pass(tmp_path):
    missing = tmp_path / "nope.json"
    assert not missing.exists()
    rc = GATE.main.__wrapped__ if hasattr(GATE.main, "__wrapped__") else GATE.main
    sys.argv = ["refusal_gate", str(missing), "--json"]
    assert rc() == 3, "a missing record must be an error, not a pass"
