"""The front door must follow exactly one named active policy, or refuse to start.

W02/C02. Two configs used to claim authority over the same decision and neither was marked active
(TT-R15.2-FRONTDOOR-SANCTIONED-DRIFT). `check_active_policy` makes the designation load-bearing:

  ABSENT            -> reported in the start banner, nothing refused (the pre-existing state)
  BOUND             -> the designation names the digest of the declaration actually loaded
  digest mismatch   -> refuse to start (a front door following a stale policy is the defect)

The negative control has to forge the very thing that is checked: a designation whose digest is not the
declaration's bytes. Without it the positive case proves only that a file can be read.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

_FRONTDOOR = Path(__file__).resolve().parent.parent / "scripts" / "hgk-exec-model-frontdoor.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("hgk_frontdoor_under_test", _FRONTDOOR)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def frontdoor():
    return _load_module()


def _declaration(tmp_path: Path, body: dict | None = None) -> Path:
    path = tmp_path / "hermes-codex-lane.json"
    path.write_text(json.dumps(body or {"provider": "opencode-go", "model": "deepseek-v4.1-flash"}),
                    encoding="utf-8")
    return path


def test_missing_designation_refuses_to_start(frontdoor, tmp_path):
    """Deleting the designation used to be a silent bypass (found by the challenge, 2026-10-23)."""
    dec = _declaration(tmp_path)
    with pytest.raises(ValueError) as exc:
        frontdoor.check_active_policy({"path": str(dec)}, tmp_path / "missing.json")
    assert "ERR_EXEC_FRONTDOOR_ACTIVE_POLICY_ABSENT" in str(exc.value)


def test_missing_designation_can_be_allowed_by_an_explicit_flag(frontdoor, tmp_path):
    dec = _declaration(tmp_path)
    result = frontdoor.check_active_policy({"path": str(dec)}, tmp_path / "missing.json", allow_absent=True)
    assert result["state"] == "ABSENT_ALLOWED_BY_FLAG"
    assert result["actual_digest"] == hashlib.sha256(dec.read_bytes()).hexdigest()


def test_designation_naming_another_policy_is_refused(frontdoor, tmp_path):
    """A digest that matches the loaded file but names a different policy_path is still a lie."""
    dec = _declaration(tmp_path)
    other = tmp_path / "another-lane.json"
    other.write_text("{}", encoding="utf-8")
    digest = hashlib.sha256(dec.read_bytes()).hexdigest()
    designation = tmp_path / "active-policy.json"
    designation.write_text(json.dumps({"policy_path": str(other), "policy_digest": digest}), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        frontdoor.check_active_policy({"path": str(dec)}, designation)
    assert "ERR_EXEC_FRONTDOOR_ACTIVE_POLICY_MISMATCH" in str(exc.value)


def test_designation_bound_to_exact_bytes(frontdoor, tmp_path):
    dec = _declaration(tmp_path)
    digest = hashlib.sha256(dec.read_bytes()).hexdigest()
    designation = tmp_path / "active-policy.json"
    designation.write_text(json.dumps({"policy_digest": digest, "declared_by": "test",
                                       "declared_at": "2026-10-23T00:00:00+00:00"}), encoding="utf-8")
    result = frontdoor.check_active_policy({"path": str(dec)}, designation)
    assert result["state"] == "BOUND"
    assert result["declared_digest"] == result["actual_digest"] == digest


def test_stale_designation_refuses_to_start(frontdoor, tmp_path):
    dec = _declaration(tmp_path)
    stale = hashlib.sha256(b"a policy that is not the loaded one").hexdigest()
    designation = tmp_path / "active-policy.json"
    designation.write_text(json.dumps({"policy_digest": stale}), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        frontdoor.check_active_policy({"path": str(dec)}, designation)
    assert "ERR_EXEC_FRONTDOOR_POLICY_DIGEST_MISMATCH" in str(exc.value)


def test_policy_edited_after_designation_is_refused(frontdoor, tmp_path):
    """The real drift: the file is designated, then someone edits it."""
    dec = _declaration(tmp_path)
    digest = hashlib.sha256(dec.read_bytes()).hexdigest()
    designation = tmp_path / "active-policy.json"
    designation.write_text(json.dumps({"policy_digest": digest}), encoding="utf-8")
    assert frontdoor.check_active_policy({"path": str(dec)}, designation)["state"] == "BOUND"
    _declaration(tmp_path, {"provider": "opencode-go", "model": "some-other-arm"})
    with pytest.raises(ValueError):
        frontdoor.check_active_policy({"path": str(dec)}, designation)


def test_malformed_designation_is_typed_not_ignored(frontdoor, tmp_path):
    dec = _declaration(tmp_path)
    designation = tmp_path / "active-policy.json"
    designation.write_text(json.dumps({"policy_digest": "not-a-digest"}), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        frontdoor.check_active_policy({"path": str(dec)}, designation)
    assert "ERR_EXEC_FRONTDOOR_ACTIVE_POLICY_INVALID" in str(exc.value)
