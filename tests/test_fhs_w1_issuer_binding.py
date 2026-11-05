"""WP-FHS-03 tests — a Permit is signed, an ECP intent is not a Permit, UNKNOWN is reconciled."""
from __future__ import annotations

import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: E402

from hg_kseos.fhs import issuer_binding as ib  # noqa: E402


def keypair():
    priv = Ed25519PrivateKey.generate()
    return priv, priv.public_key().public_bytes_raw().hex()


def permit(priv, **over):
    body = {
        "kind": "PERMIT",
        "permit_id": "PERMIT-FHS-W1-0001",
        "work_id": "WO-FHS-W1-WP03",
        "subject": "WP-FHS-03",
        "scope": "fhs-w1/wp03",
        "policy_epoch": 10,
        "issued_at": int(time.time()) - 30,
        "ttl_seconds": 600,
        "nonce": "nonce-0001",
        "receiver": "HGK-RECV-001",
        "receiver_abi": "HGK.Permit@2",
        "principal_sid": "S-1-5-21-1111111111-2222222222-3333333333-1001",
        "issuer_key_id": "OWNER-FHS-TEST",
    }
    body.update(over)
    sig = priv.sign(ib.canonical(body)).hex()
    return dict(body, signature_hex=sig)


def registry(**over):
    reg = {
        "registry_rev": 41,
        "policy_epoch": 10,
        "receivers": {
            "HGK-RECV-001": {"abi": "HGK.Permit@2", "status": "ACTIVE",
                             "principal_acl": ["S-1-5-21-1111111111-2222222222-3333333333-1001"]},
        },
        "used_nonces": [],
        "revoked_permits": [],
    }
    reg.update(over)
    return reg


class TestIssuerBindingPositive(unittest.TestCase):
    def setUp(self):
        self.priv, self.pub = keypair()

    def test_signed_permit_binds_to_its_receiver_in_one_revision(self):
        rec = ib.bind(permit(self.priv), registry(), issuer_public_hex=self.pub)
        self.assertEqual(rec["state"], "BOUND")
        self.assertEqual(rec["registry_rev"], 41)
        self.assertTrue(rec["signature"]["verified"])
        self.assertFalse(rec["issuer_permit_issued"])
        self.assertEqual(rec["claim_ceiling"], "AUTHOR_DESIGN_ONLY")
        self.assertEqual(rec["signature"]["original_issuer_receipt"], "NOT_OBSERVED")

    def test_binding_digest_is_replay_stable(self):
        p, r = permit(self.priv), registry()
        a = ib.bind(p, r, issuer_public_hex=self.pub)
        b = ib.bind(p, r, issuer_public_hex=self.pub)
        self.assertEqual(a["binding_sha256"], b["binding_sha256"])

    def test_revoke_is_requested_not_executed(self):
        out = ib.revoke(permit(self.priv), fence=11, reason="candidate rollback")
        self.assertEqual(out["state"], "REVOKE_REQUESTED")
        self.assertFalse(out["executed"])
        self.assertEqual(out["fence_epoch"], 11)


class TestIssuerBindingNegative(unittest.TestCase):
    def setUp(self):
        self.priv, self.pub = keypair()

    def test_ecp_intent_cannot_be_a_permit(self):
        doc = {"kind": "ECP", "permit_id": "PERMIT-X", "work_id": "WO-FHS-W1-WP03"}
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.admit_permit(doc)
        self.assertEqual(ctx.exception.code, "WP-FHS-03.FIRST_FAIL:ISSUER_BINDING_INVALID")

    def test_plan_and_repofile_are_candidate_material(self):
        for kind in ("PLAN", "REPO_FILE", "TASKSPEC"):
            with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
                ib.admit_permit({"kind": kind, "work_id": "WO-FHS-W1-WP03"})
            self.assertEqual(ctx.exception.code, "WP-FHS-03.FIRST_FAIL:ISSUER_BINDING_INVALID")

    def test_missing_binding_field_refuses(self):
        doc = permit(self.priv)
        doc.pop("nonce")
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.admit_permit(doc)
        self.assertIn("nonce", str(ctx.exception))

    def test_non_workid_refuses(self):
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.admit_permit(permit(self.priv, work_id="whatever-1"))
        self.assertEqual(ctx.exception.code, "WP-FHS-03.FIRST_FAIL:ISSUER_BINDING_INVALID")

    def test_tampered_body_breaks_the_signature(self):
        doc = permit(self.priv)
        doc["scope"] = "fhs-w1/somewhere-else"
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.bind(doc, registry(), issuer_public_hex=self.pub)
        self.assertEqual(ctx.exception.code, "WP-FHS-03.FIRST_FAIL:ISSUER_BINDING_INVALID")

    def test_signature_by_another_key_refuses(self):
        other, _ = keypair()
        with self.assertRaises(ib.IssuerBindingRefusal):
            ib.bind(permit(other), registry(), issuer_public_hex=self.pub)

    def test_epoch_mismatch_refuses(self):
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.bind(permit(self.priv), registry(policy_epoch=11), issuer_public_hex=self.pub)
        self.assertEqual(ctx.exception.code, "ISSUER_WORK_BINDING_NACK")

    def test_unknown_receiver_refuses(self):
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.bind(permit(self.priv, receiver="HGK-RECV-999"), registry(),
                    issuer_public_hex=self.pub)
        self.assertEqual(ctx.exception.code, "ISSUER_WORK_BINDING_NACK")

    def test_inactive_receiver_refuses(self):
        reg = registry()
        reg["receivers"]["HGK-RECV-001"]["status"] = "RETIRED"
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.bind(permit(self.priv), reg, issuer_public_hex=self.pub)
        self.assertEqual(ctx.exception.code, "ISSUER_WORK_BINDING_NACK")

    def test_abi_mismatch_refuses(self):
        reg = registry()
        reg["receivers"]["HGK-RECV-001"]["abi"] = "HGK.Permit@1"
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.bind(permit(self.priv), reg, issuer_public_hex=self.pub)
        self.assertEqual(ctx.exception.code, "ISSUER_WORK_BINDING_NACK")

    def test_replayed_nonce_refuses(self):
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.bind(permit(self.priv), registry(used_nonces=["nonce-0001"]),
                    issuer_public_hex=self.pub)
        self.assertEqual(ctx.exception.code, "ISSUER_WORK_BINDING_NACK")

    def test_expired_permit_refuses(self):
        old = permit(self.priv, issued_at=int(time.time()) - 3600, ttl_seconds=60)
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.bind(old, registry(), issuer_public_hex=self.pub)
        self.assertIn("expired", str(ctx.exception))

    def test_revoked_permit_refuses(self):
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.bind(permit(self.priv), registry(revoked_permits=["PERMIT-FHS-W1-0001"]),
                    issuer_public_hex=self.pub)
        self.assertEqual(ctx.exception.code, "ISSUER_WORK_BINDING_NACK")

    def test_foreign_sid_refuses(self):
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.bind(permit(self.priv, principal_sid="S-1-5-21-9999-9999-9999-1009"),
                    registry(), issuer_public_hex=self.pub)
        self.assertEqual(ctx.exception.code, "ISSUER_PRINCIPAL_ACL_DENY")

    def test_unknown_effect_cannot_be_blind_retried(self):
        with self.assertRaises(ib.IssuerBindingRefusal) as ctx:
            ib.reconcile("UNKNOWN")
        self.assertEqual(ctx.exception.code, "UNKNOWN_BLIND_RETRY_DENY")
        out = ib.reconcile("UNKNOWN", world_readback={"reader": "ORIGINAL_WORLD_READER",
                                                      "observed": "no residue"})
        self.assertEqual(out["state"], "RECONCILED")

    def test_known_effect_needs_no_reconcile(self):
        self.assertEqual(ib.reconcile("APPLIED")["action"], "NO_RECONCILE_REQUIRED")


if __name__ == "__main__":
    unittest.main()
