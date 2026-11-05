"""Tests for HGK_CONSUMER_RECEIPT@1 (stdlib unittest; no pytest in this environment)."""
import hashlib
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from hg_kseos.fhs import consumer_receipt as cr  # noqa: E402

RAW = b'{"policy":"demo","epoch":10}\n'


class BuildAndVerify(unittest.TestCase):
    def _receipt(self, **over):
        kw = dict(subject="SUBJ-R3-001", scope="W2/WP-FHS-06", policy_epoch=10,
                  consumer_id="hgk-policy-consumer", ack="ACK",
                  raw_bytes=RAW, raw_path="policy.raw.json",
                  policy_digest="a" * 64, loaded_digest="b" * 64,
                  observed_at="2026-11-05T23:00:00+0800")
        kw.update(over)
        return cr.build_receipt(**kw)

    def test_schema_and_leg_digest(self):
        r = self._receipt()
        self.assertEqual(r["schema"], "HGK_CONSUMER_RECEIPT@1")
        self.assertEqual(r["raw_sha256"], hashlib.sha256(RAW).hexdigest())

    def test_envelope_digest_is_recomputable(self):
        r = self._receipt()
        stripped = {k: v for k, v in r.items() if k != "receipt_sha256"}
        expect = hashlib.sha256(json.dumps(stripped, sort_keys=True, separators=(",", ":"),
                                           ensure_ascii=False).encode("utf-8")).hexdigest()
        self.assertEqual(r["receipt_sha256"], expect)

    def test_roundtrip_verifies(self):
        r = self._receipt()
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "receipt.json")
            digest = cr.write_receipt(p, r, raw_bytes=RAW)
            back = cr.load_receipt_file(p)
            self.assertEqual(cr.verify_receipt(back, base_dir=d), (True, None))
            with open(p, "rb") as fh:
                self.assertEqual(hashlib.sha256(fh.read()).hexdigest(), digest)

    def test_edited_subject_breaks_the_envelope(self):
        r = self._receipt()
        r["subject"] = "SUBJ-OTHER"
        ok, code = cr.verify_receipt(r)
        self.assertFalse(ok)
        self.assertEqual(code, cr.ERR_ENVELOPE)

    def test_raw_bytes_changed_after_sealing(self):
        r = self._receipt()
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "receipt.json")
            cr.write_receipt(p, r, raw_bytes=RAW)
            with open(os.path.join(d, "policy.raw.json"), "wb") as fh:
                fh.write(b'{"policy":"demo","epoch":11}\n')
            ok, code = cr.verify_receipt(r, base_dir=d)
            self.assertFalse(ok)
            self.assertEqual(code, cr.ERR_DIGEST)

    def test_missing_raw_is_unreadable_not_a_pass(self):
        r = self._receipt()
        with tempfile.TemporaryDirectory() as d:
            ok, code = cr.verify_receipt(r, base_dir=d)
            self.assertFalse(ok)
            self.assertTrue(str(code).startswith(cr.ERR_RAW_UNREADABLE))

    def test_wrong_schema_is_refused(self):
        r = self._receipt()
        r["schema"] = "HGK_CONSUMER_RECEIPT@0"
        self.assertEqual(cr.verify_receipt(r), (False, cr.ERR_SCHEMA))

    def test_bad_ack_is_refused(self):
        r = self._receipt()
        r["ack"] = "MAYBE"
        ok, code = cr.verify_receipt(r)
        self.assertFalse(ok)
        self.assertEqual(code, cr.ERR_ACK)

    def test_missing_field_is_refused(self):
        r = self._receipt()
        del r["consumer_id"]
        ok, code = cr.verify_receipt(r)
        self.assertFalse(ok)
        self.assertTrue(str(code).startswith(cr.ERR_REQUIRED))

    def test_deferral_requires_scope(self):
        with self.assertRaises(cr.ReceiptRejected) as ctx:
            self._receipt(ack="SCOPE_SPECIFIC_DEFERRED")
        self.assertEqual(ctx.exception.code, cr.ERR_SCOPE_DEFERRAL)

    def test_deferral_with_scope_is_accepted(self):
        r = self._receipt(ack="SCOPE_SPECIFIC_DEFERRED", deferred_operations=["DEV_REPO_WRITE"])
        with tempfile.TemporaryDirectory() as d:
            cr.write_receipt(os.path.join(d, "r.json"), r, raw_bytes=RAW)
            back = cr.load_receipt_file(os.path.join(d, "r.json"))
            self.assertEqual(cr.verify_receipt(back, base_dir=d), (True, None))

    def test_no_raw_bytes_is_refused(self):
        with self.assertRaises(cr.ReceiptRejected) as ctx:
            self._receipt(raw_bytes=None)
        self.assertEqual(ctx.exception.code, cr.ERR_RAW_UNREADABLE)

    def test_empty_subject_is_refused(self):
        with self.assertRaises(cr.ReceiptRejected) as ctx:
            self._receipt(subject="  ")
        self.assertEqual(ctx.exception.code, cr.ERR_REQUIRED)

    def test_write_is_lf_clean(self):
        r = self._receipt()
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "receipt.json")
            cr.write_receipt(p, r, raw_bytes=RAW)
            with open(p, "rb") as fh:
                raw = fh.read()
            self.assertNotIn(b"\r\n", raw)
            self.assertTrue(raw.endswith(b"\n") and not raw.endswith(b"\n\n"))

    def test_write_refuses_invalid_receipt(self):
        r = self._receipt()
        r["ack"] = "NOPE"
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "receipt.json")
            with self.assertRaises(cr.ReceiptRejected):
                cr.write_receipt(p, r, raw_bytes=RAW)
            self.assertFalse(os.path.exists(p))


if __name__ == "__main__":
    unittest.main(verbosity=2)
