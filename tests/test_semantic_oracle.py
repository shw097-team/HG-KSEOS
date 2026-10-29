"""HG-KSEOS-side semantic checks against unmodified, source-owned PIPD fixtures."""
from __future__ import annotations

import importlib
import importlib.util
import json
import os
from pathlib import Path

import jsonschema
import pytest
import yaml

PIPD_ROOT = Path(os.environ.get("PIPD_ROOT", Path(__file__).resolve().parents[2] / "PIPD"))


def case(skill: str, case_id: str) -> dict:
    path = PIPD_ROOT / "skills" / skill / "tests" / "cases.yaml"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    return next(item for item in document["cases"] if item["id"] == case_id)


def schema_accepts(skill: str, payload: dict, side: str = "input") -> None:
    path = PIPD_ROOT / "skills" / skill / "schemas" / f"{side}.schema.json"
    jsonschema.Draft202012Validator(json.loads(path.read_text(encoding="utf-8"))).validate(payload)


def oracle():
    # Assert first so the RED phase reports the missing feature, not a collection error.
    assert importlib.util.find_spec("hg_kseos.semantic_oracle") is not None, "semantic oracle missing"
    return importlib.import_module("hg_kseos.semantic_oracle")


def test_distinct_real_positive():
    payload = case("pipd-assurance-tqaep", "POS-001")
    schema_accepts("pipd-assurance-tqaep", payload["input"])
    schema_accepts("pipd-assurance-tqaep", payload["output"], "output")
    result = oracle().check_distinct(payload["input"], payload["output"])
    assert result["predicate"] == "semantic.distinct"
    assert result["verdict"] == "SATISFIED"
    assert result["reasons"] and result["evidence"]


def test_distinct_real_negative_schema_accepts_oracle_refuses():
    payload = case("pipd-assurance-tqaep", "NEG-001")
    assert "output" not in payload  # Do not invent an output for this pre-emission refusal.
    schema_accepts("pipd-assurance-tqaep", payload["input"])
    result = oracle().check_distinct(payload["input"])
    assert result["verdict"] == "VIOLATED"
    assert result["evidence"]["identity_pairs"][0]["normalized"] == ["maker-a", "maker-a"]


def test_distinct_not_applicable_real_package_payload():
    payload = case("pipd-package-project", "POS-001")
    assert oracle().check_distinct(payload["input"], payload["output"])["verdict"] == "NOT_APPLICABLE"


def test_claim_gate_real_positive():
    payload = case("pipd-package-project", "POS-001")
    schema_accepts("pipd-package-project", payload["input"])
    schema_accepts("pipd-package-project", payload["output"], "output")
    assert hasattr(oracle(), "check_claim_gate"), "claim gate missing"
    result = oracle().check_claim_gate(payload["input"], payload["output"])
    assert result["predicate"] == "semantic.claim_gate"
    assert result["verdict"] == "SATISFIED"
    assert result["reasons"] and result["evidence"]


def test_claim_gate_real_negative_schema_accepts_oracle_refuses():
    payload = case("pipd-package-project", "NEG-001")
    assert "output" not in payload
    schema_accepts("pipd-package-project", payload["input"])
    assert hasattr(oracle(), "check_claim_gate"), "claim gate missing"
    result = oracle().check_claim_gate(payload["input"])
    assert result["verdict"] == "VIOLATED"
    assert set(result["evidence"]["missing_fields"]) == {
        "approval.checker_identity", "approval.approval_receipt"
    }


def test_claim_gate_not_applicable_real_lower_ceiling():
    payload = case("pipd-package-project", "POS-002")
    assert hasattr(oracle(), "check_claim_gate"), "claim gate missing"
    assert oracle().check_claim_gate(payload["input"], payload["output"])["verdict"] == "NOT_APPLICABLE"


@pytest.mark.parametrize("field", ["checker_identity", "approval_receipt"])
@pytest.mark.parametrize("value", [None, "", "   ", [], {}])
def test_claim_gate_supplemental_empty_evidence(field, value):
    # Explicit derived mutations; never stand in for the source NEG-001 test above.
    payload = case("pipd-package-project", "POS-001")["input"]
    payload["approval"][field] = value
    assert oracle().check_claim_gate(payload)["verdict"] == "VIOLATED"


@pytest.mark.parametrize("claim", ["LOCAL_QUALIFIED", "INDEPENDENT_PASS",
                                   "PUBLICATION_APPROVED", "RELEASED", "PRODUCTION_VERIFIED"])
def test_claim_gate_supplemental_emitted_escalation_without_approval(claim):
    payload = case("pipd-package-project", "POS-002")
    payload["output"]["allowed_claims"] = [claim]
    assert oracle().check_claim_gate(payload["input"], payload["output"])["verdict"] == "VIOLATED"


def test_claim_gate_supplemental_self_approval():
    payload = case("pipd-package-project", "POS-001")["input"]
    payload["approval"]["checker_identity"] = f" {payload['producer'].lower()} "
    assert oracle().check_claim_gate(payload)["verdict"] == "VIOLATED"


def test_distinct_real_downstream_self_acceptance():
    payload = case("pipd-assurance-tqaep", "SEC-001")
    assert oracle().check_distinct(payload["input"], payload["output"])["verdict"] == "VIOLATED"


@pytest.mark.parametrize("field", ["maker", "checker"])
def test_distinct_supplemental_empty_identity(field):
    payload = case("pipd-assurance-tqaep", "POS-001")["input"]
    payload[field] = "  "
    assert oracle().check_distinct(payload)["verdict"] == "VIOLATED"
