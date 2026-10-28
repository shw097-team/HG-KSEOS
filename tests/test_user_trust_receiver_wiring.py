"""Receiver wiring for the user-scoped trust profile (B1 r10 next-step 1).

The gap this closes: `user_trust` existed but nothing in `src/` read it, so the receiver could only ever
open the ProgramData machine root. These cases pin the resolver, the user-profile protection proof, the
scope/epoch binding and the signature path end to end.

Ceiling carried by every case: `USER_SCOPED_SOFTWARE_KEY`. A process running as the same Windows user can
ask DPAPI to unprotect the signer key, so this proves the issue/verify/revoke chain and key isolation by
storage - NOT maker/checker OS-principal separation.
"""
from __future__ import annotations

import json

import pytest

from hg_kseos import native_admission as n
from hg_kseos import user_trust as ut
from hg_kseos.errors import InvariantViolation

SID_OWNER = "S-1-5-21-111-222-333-1001"
SID_CHECKER = "S-1-5-21-111-222-333-1002"
SID_MAKER = "S-1-5-21-111-222-333-1003"
KIND = "B1_DOGFOOD"


@pytest.fixture(autouse=True)
def isolated_profile(tmp_path, monkeypatch):
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "localappdata"))
    monkeypatch.delenv("HGK_TRUST_PROFILE", raising=False)
    yield tmp_path


def scope_doc(root, *, epoch=34, head="a" * 40, kind=KIND):
    return {
        "schema": "HGK-USER-PROFILE-SCOPE/1",
        "mission_id": "FHS-MSC-B1-SELF-BOOTSTRAP-FOUR-PARTY-DOGFOOD",
        "source_manifest_sha256": "b" * 64,
        "policy_sha256": "c" * 64,
        "policy_epoch": epoch,
        "max_ttl_seconds": 300,
        "root": str(root),
        "approved_files": [],
        "task_kinds": {kind: {"state": "REGISTERED",
                              "operations": ["create_taskspec", "create_workorder"]}},
        "scope": {"head": head, "task_kind": kind, "lease_generation": 0,
                  "root_identity": "0:0", "database_path": str(root / "spine.db"),
                  "request_sha256": []},
    }


def enroll_with_scope(tmp_path, **kw):
    reg = ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER, **kw)
    ut.paths()["root"].joinpath(n.USER_SCOPE_FILENAME).write_text(
        json.dumps(scope_doc(tmp_path), indent=1), encoding="utf-8")
    ut.harden()
    return reg


# ------------------------------------------------------------------ resolver
def test_default_profile_is_machine_and_unchanged():
    assert n.trust_profile() == n.MACHINE_PROFILE
    assert n.registry_path() == n.REGISTRY
    assert isinstance(n.default_registry(), n.ProtectedRegistry)


def test_unknown_profile_is_refused_not_defaulted(monkeypatch):
    monkeypatch.setenv("HGK_TRUST_PROFILE", "usr")
    with pytest.raises(InvariantViolation, match="ERR_NATIVE_TRUST_PROFILE"):
        n.trust_profile()
    with pytest.raises(InvariantViolation, match="ERR_NATIVE_TRUST_PROFILE"):
        n.default_registry()


def test_user_profile_selects_the_user_root(monkeypatch):
    monkeypatch.setenv("HGK_TRUST_PROFILE", "user")
    assert n.trust_profile() == n.USER_PROFILE
    assert n.registry_path() == ut.paths()["registry"]
    assert isinstance(n.default_registry(), n.UserProfileRegistry)
    assert isinstance(n.NativeAdmission().registry, n.UserProfileRegistry)


# ------------------------------------------------------------------ positive path
def test_user_profile_normalizes_and_verifies_a_real_signature(tmp_path, monkeypatch):
    reg = enroll_with_scope(tmp_path)
    monkeypatch.setenv("HGK_TRUST_PROFILE", "user")
    snapshot = n.UserProfileRegistry().snapshot()
    assert snapshot["trust_profile"] == "user"
    assert snapshot["assurance_level"] == ut.ASSURANCE
    assert snapshot["policy_epoch"] == 34
    assert snapshot["task_kind"] == KIND
    assert snapshot["keys"][reg["key_id"]]["algorithm"] == "Ed25519"

    payload = {"operation": "create_taskspec", "subject_sha": "d" * 64}
    reference = ut.sign(payload)
    key = snapshot["keys"][reg["key_id"]]
    n.verify_signature(key, reference["signature"], n.canonical(reference["payload"]))  # no raise == verified

    tampered = json.loads(json.dumps(reference["payload"]))
    tampered["subject_sha"] = "e" * 64
    with pytest.raises(InvariantViolation, match="ERR_NATIVE_SIGNATURE"):
        n.verify_signature(key, reference["signature"], n.canonical(tampered))


def test_full_receiver_shaped_reference_verifies_end_to_end(tmp_path, monkeypatch):
    """The exact payload shape `authorize()` verifies - not just a toy dict."""
    reg = enroll_with_scope(tmp_path)
    monkeypatch.setenv("HGK_TRUST_PROFILE", "user")
    snapshot = n.UserProfileRegistry().snapshot()
    payload = {
        "profile": n.PROFILE, "reference_kind": "source_freeze",
        "mission_id": snapshot["mission_id"],
        "source_manifest_sha256": snapshot["source_manifest_sha256"],
        "subject_sha256": "f" * 64, "policy_sha256": snapshot["policy_sha256"],
        "policy_epoch": snapshot["policy_epoch"], "operation": "create_taskspec",
        "purpose": n.PURPOSES["create_taskspec"], "lease_generation": 0,
        "root_identity": "0:0", "head": snapshot["scope"]["head"],
        "task_kind": snapshot["task_kind"], "evidence_ref": "E-USER-TRUST-PROFILE",
    }
    reference = ut.sign(payload)
    assert set(reference["payload"]) == set(payload) | {"nonce", "issued_at", "expires_at"}
    n.verify_signature(snapshot["keys"][reg["key_id"]], reference["signature"],
                       n.canonical(reference["payload"]))
    with pytest.raises(ut.TrustRefusal, match="ERR_SIGNATURE_INVALID"):
        bad = json.loads(json.dumps(reference))
        bad["payload"]["head"] = "b" * 40
        ut.verify(bad)


def test_registry_and_key_live_outside_any_repo(tmp_path, monkeypatch):
    enroll_with_scope(tmp_path)
    paths = ut.paths()
    for p in (paths["registry"], paths["key"]):
        assert str(p).casefold().startswith(str(tmp_path).casefold())
    assert ut.private_key_is_not_in_registry()


# ------------------------------------------------------------------ audience/scope gates
def test_missing_scope_sidecar_is_refused(tmp_path, monkeypatch):
    reg = ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER)
    monkeypatch.setenv("HGK_TRUST_PROFILE", "user")
    with pytest.raises(InvariantViolation, match="ERR_NATIVE_USER_PROFILE_SCOPE_REQUIRED"):
        n.UserProfileRegistry().snapshot()
    assert reg["status"] == "ACTIVE"


def test_epoch_conflict_between_anchor_and_scope_is_refused(tmp_path):
    anchor = ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER, policy_epoch=34)
    with pytest.raises(InvariantViolation, match="ERR_NATIVE_USER_PROFILE_EPOCH_CONFLICT"):
        n.normalize_user_registry(anchor, scope_doc(tmp_path, epoch=33))


def test_unregistered_task_kind_is_refused(tmp_path):
    anchor = ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER)
    doc = scope_doc(tmp_path)
    doc["task_kinds"] = {"SOMETHING_ELSE": {"state": "REGISTERED", "operations": []}}
    with pytest.raises(InvariantViolation, match="ERR_NATIVE_UNREGISTERED_KIND"):
        n.normalize_user_registry(anchor, doc)


def test_collapsed_principals_are_refused(tmp_path):
    anchor = ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER)
    anchor["checker_os_sid"] = anchor["owner_os_sid"]
    with pytest.raises(InvariantViolation, match="ERR_NATIVE_PRINCIPAL_SEPARATION"):
        n.normalize_user_registry(anchor, scope_doc(tmp_path))


def test_private_key_material_in_registry_is_refused(tmp_path):
    anchor = ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER)
    anchor["leak"] = "-----BEGIN PRIVATE KEY-----"
    with pytest.raises(InvariantViolation, match="ERR_NATIVE_USER_KEY_MATERIAL_IN_REGISTRY"):
        n.normalize_user_registry(anchor, scope_doc(tmp_path))


def test_revoked_user_root_stops_the_chain(tmp_path, monkeypatch):
    enroll_with_scope(tmp_path)
    monkeypatch.setenv("HGK_TRUST_PROFILE", "user")
    assert n.UserProfileRegistry().snapshot()["status"] == "ACTIVE"
    ut.revoke("owner_end_of_round")
    with pytest.raises(InvariantViolation, match="ERR_NATIVE_REGISTRY_INACTIVE"):
        n.UserProfileRegistry().snapshot()


# ------------------------------------------------------------------ the protection proof itself
def test_unhardened_root_is_refused(tmp_path, monkeypatch):
    """A registry whose DACL is merely INHERITED is not proof: another principal may rewrite it."""
    reg = ut.enroll(SID_OWNER, SID_CHECKER, SID_MAKER)
    ut.paths()["root"].joinpath(n.USER_SCOPE_FILENAME).write_text(
        json.dumps(scope_doc(tmp_path), indent=1), encoding="utf-8")
    reg_path = ut.paths()["registry"]
    import subprocess
    subprocess.run(["icacls", str(reg_path), "/inheritance:e"], capture_output=True,
                   encoding="utf-8", errors="replace")
    monkeypatch.setenv("HGK_TRUST_PROFILE", "user")
    with pytest.raises(InvariantViolation, match="ERR_NATIVE_USER_TRUST_ACL_UNPROTECTED"):
        n.UserProfileRegistry().snapshot()
    assert reg["status"] == "ACTIVE"


def test_assert_user_protected_accepts_the_hardened_root(tmp_path):
    reg = enroll_with_scope(tmp_path)
    n.assert_user_protected(ut.paths()["registry"])  # no raise
    assert reg["assurance_level"] == "USER_SCOPED_SOFTWARE_KEY"
