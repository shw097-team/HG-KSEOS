"""The emit-time gate, exercised where it is actually called.

TS13's residual was not that the oracle was wrong, but that nothing on the acceptance path called it: `run_acceptance`
could emit MAKER_CASE_PASS for a case whose input aliases maker as checker. These tests drive `_semantic_gate` through
real fixture files so the wiring, not just the predicate, is pinned.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import run_acceptance  # noqa: E402


def _write_fixture(root: Path, case_id: str, payload: dict) -> None:
    fixtures = root / "eval" / "fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    (fixtures / f"{case_id}.yaml").write_text(json.dumps(payload), encoding="utf-8")


def test_an_aliased_maker_and_checker_is_refused_at_emit_time():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_fixture(root, "TST-001", {"input": {"maker": "Maker-A", "checker": " maker-a "}})
        gate = run_acceptance._semantic_gate({"case_id": "TST-001"}, root, {})
    assert gate["verdict"] == "VIOLATED", gate
    assert gate["predicate"] == "semantic.distinct"


def test_a_distinct_pair_passes_the_gate():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_fixture(root, "TST-002", {"input": {"maker": "Maker-A", "checker": "Maker-B"}})
        gate = run_acceptance._semantic_gate({"case_id": "TST-002"}, root, {})
    assert gate["verdict"] == "SATISFIED", gate


def test_a_gated_claim_without_a_receipt_is_refused_at_emit_time():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_fixture(root, "TST-003", {"input": {
            "maker": "Maker-A",
            "checker": "Maker-B",
            "allowed_claims": ["LOCAL_QUALIFIED"],
            "producer": "Maker-A",
            "approval": {"checker_identity": "Maker-B"},
        }})
        gate = run_acceptance._semantic_gate({"case_id": "TST-003"}, root, {})
    assert gate["verdict"] == "VIOLATED", gate
    assert gate["predicate"] == "semantic.claim_gate"


def test_a_case_without_an_input_is_not_applicable_and_says_so():
    with tempfile.TemporaryDirectory() as tmp:
        gate = run_acceptance._semantic_gate({"case_id": "TST-404"}, Path(tmp), {})
    assert gate["verdict"] == "NOT_APPLICABLE", gate
    assert gate["reasons"] == ["no case input to judge"]


def test_the_gate_is_reached_from_the_emission_loop():
    """A grep-level guard: the loop that writes evidence must call the gate before writing."""
    source = (TOOLS / "run_acceptance.py").read_text(encoding="utf-8")
    assert "_semantic_gate(row, root, details)" in source, "the emission loop no longer calls the gate"
    loop_at = source.index("_semantic_gate(row, root, details)")
    evidence_at = source.index('"schema": "HGK-CASE-EVIDENCE/2"', loop_at)
    assert loop_at < evidence_at, "the gate must run before the evidence document is assembled"
