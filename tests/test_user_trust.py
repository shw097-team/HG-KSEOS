"""RED/GREEN receipt for the user-scoped trust profile (no elevation, no machine key)."""
from __future__ import annotations

import json

import pytest

from hg_kseos import user_trust as ut

SID_OWNER = "S-1-5-21-111-222-333-1001"
SID_CHECKER = "S-1-5-21-111-222-333-1002"
SID_MAKER = "S-1-5-21-111-222-333-1003"


@pytest.fixture(autouse=True)
def isolated_profile(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "localappdata"))
    yield tmp_path


def test_enroll_creates_user_scoped_root_without_elevation():
    reg = ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER)
    p = ut.paths()
    assert p["registry"].exists() and p["key"].exists()
    assert str(p["root"]).startswith(str(p["root"].parents[2]))  # under the isolated profile
    assert reg["status"] == "ACTIVE" and reg["assurance_level"] == ut.ASSURANCE
    assert reg["algorithm"] == "Ed25519"
    # the private key never appears in the registry, and the key file is not plaintext PEM
    assert ut.private_key_is_not_in_registry()
    assert b"PRIVATE KEY" not in p["key"].read_bytes()


def test_principal_separation_is_refused_not_relaxed():
    with pytest.raises(ut.TrustRefusal, match="ERR_PRINCIPAL_SEPARATION"):
        ut.enroll(SID_OWNER, SID_OWNER, SID_MAKER)
    with pytest.raises(ut.TrustRefusal, match="ERR_PRINCIPAL_SEPARATION"):
        ut.enroll(SID_OWNER, SID_CHECKER, SID_CHECKER)


def test_sign_then_verify_readback():
    ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER)
    ref = ut.sign({"operation": "create_taskspec", "subject_sha": "a" * 64, "policy_epoch": 34})
    out = ut.verify(ref)
    assert out["verified"] is True
    assert out["assurance_level"] == "USER_SCOPED_SOFTWARE_KEY"
    assert out["owner_os_sid"] == SID_OWNER and out["checker_os_sid"] == SID_CHECKER
    assert json.dumps(ref).find("PRIVATE") == -1


def test_tampered_payload_is_refused():
    ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER)
    ref = ut.sign({"operation": "create_workorder", "subject_sha": "b" * 64})
    ref["payload"]["subject_sha"] = "c" * 64
    with pytest.raises(ut.TrustRefusal, match="ERR_SIGNATURE_INVALID"):
        ut.verify(ref)


def test_foreign_key_is_refused():
    ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER)
    ref = ut.sign({"operation": "x"})
    ref["key_id"] = "USR-someoneelse"
    with pytest.raises(ut.TrustRefusal, match="ERR_UNKNOWN_KEY_ID"):
        ut.verify(ref)


def test_expired_permit_is_refused():
    ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER)
    ref = ut.sign({"operation": "x"}, ttl_seconds=-5)
    with pytest.raises(ut.TrustRefusal, match="ERR_TTL_EXPIRED"):
        ut.verify(ref)


def test_revoke_ends_the_chain():
    reg = ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER)
    ref = ut.sign({"operation": "x"})
    assert ut.verify(ref)["verified"] is True
    out = ut.revoke("owner_end_of_round")
    assert out["revoked"] is True and out["key_id"] == reg["key_id"]
    with pytest.raises(ut.TrustRefusal, match="ERR_REGISTRY_NOT_ACTIVE"):
        ut.verify(ref)
