"""R14-TS08 oracle — the typed capability delta must refuse replay, expiry, and partial effect.

These are the four negative cases the command document names. They are asserted against the module, not against a
document, because "we documented the semantics" is exactly the claim this round is trying to stop accepting.
"""
from __future__ import annotations

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from hg_kseos import capability_delta as cd

ROOT = Path(__file__).resolve().parent.parent


def _delta(**over):
    d = {
        "schema": cd.SCHEMA,
        "delta_id": "DELTA-TEST-001",
        "nonce": "NONCE-TEST-001",
        "expires_at": "2099-01-01T00:00:00Z",
        "items": [
            {"item_id": "I1", "capability": "lane_routing", "state": cd.REUSE_AS_IS},
            {"item_id": "I2", "capability": "workorder_spine", "state": cd.REUSE_AS_IS},
            {"item_id": "I3", "capability": "knowledge_repoint", "state": cd.NEEDS_NATIVE_UPGRADE},
        ],
    }
    d.update(over)
    return d


class DeltaComputationTests(unittest.TestCase):
    def test_every_capability_is_classified_with_evidence(self) -> None:
        doc = cd.compute(ROOT)
        self.assertEqual(doc["schema"], cd.SCHEMA)
        self.assertTrue(doc["rows"])
        self.assertTrue(doc["adapter_is_not_a_native_upgrade"])
        for row in doc["rows"]:
            self.assertIn(row["state"], {cd.REUSE_AS_IS, cd.REUSE_WITH_ADAPTER, cd.MISSING, cd.NEEDS_NATIVE_UPGRADE})
            self.assertTrue(row["evidence"], f"{row['capability']} must carry evidence, not a verdict")
        known = {r["capability"] for r in doc["rows"]}
        self.assertIn("lane_routing", known)
        self.assertIn("workorder_spine", known)


class DeltaApplicationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name) / "spine.db"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_apply_is_atomic_and_reports_a_rollback_pointer(self) -> None:
        r = cd.apply_delta(self.db, _delta())
        self.assertTrue(r["applied"])
        self.assertEqual(r["items_applied"], ["I1", "I2", "I3"])
        self.assertEqual(r["rollback_pointer"], "RB-DELTA-TEST-001")
        self.assertTrue(r["evidence_digest"].startswith("sha256:"))
        con = sqlite3.connect(self.db)
        self.assertEqual(con.execute("SELECT COUNT(*) FROM capability_delta_items").fetchone()[0], 3)
        con.close()
        back = cd.rollback(self.db, "DELTA-TEST-001")
        self.assertTrue(back["rolled_back"])
        self.assertEqual(sorted(back["items_removed"]), ["I1", "I2", "I3"])
        con = sqlite3.connect(self.db)
        self.assertEqual(con.execute("SELECT COUNT(*) FROM capability_delta_items").fetchone()[0], 0)
        con.close()

    def test_replay_is_refused(self) -> None:
        cd.apply_delta(self.db, _delta())
        with self.assertRaises(cd.DeltaRefused) as ctx:
            cd.apply_delta(self.db, _delta())
        self.assertEqual(ctx.exception.code, "ERR_DELTA_REPLAY")
        self.assertFalse(ctx.exception.receipt()["applied"])

    def test_expiry_is_refused(self) -> None:
        with self.assertRaises(cd.DeltaRefused) as ctx:
            cd.apply_delta(self.db, _delta(expires_at="2000-01-01T00:00:00Z"))
        self.assertEqual(ctx.exception.code, "ERR_DELTA_EXPIRED")

    def test_partial_effect_leaves_nothing_behind(self) -> None:
        with self.assertRaises(cd.DeltaRefused) as ctx:
            cd.apply_delta(self.db, _delta(), fail_item="I3")
        self.assertEqual(ctx.exception.code, "ERR_DELTA_PARTIAL_EFFECT")
        self.assertIn("rolled back 2", ctx.exception.detail)
        con = sqlite3.connect(self.db)
        try:
            items = con.execute("SELECT COUNT(*) FROM capability_delta_items").fetchone()[0]
            deltas = con.execute("SELECT COUNT(*) FROM capability_deltas").fetchone()[0]
        finally:
            con.close()
        self.assertEqual((items, deltas), (0, 0), "a refused delta must not leave a half-applied spine")

    def test_bad_schema_and_empty_delta_are_refused(self) -> None:
        with self.assertRaises(cd.DeltaRefused) as ctx:
            cd.apply_delta(self.db, _delta(schema="SOMETHING/2"))
        self.assertEqual(ctx.exception.code, "ERR_DELTA_SCHEMA")
        with self.assertRaises(cd.DeltaRefused) as ctx:
            cd.apply_delta(self.db, _delta(items=[]))
        self.assertEqual(ctx.exception.code, "ERR_DELTA_EMPTY")

    def test_denied_receipt_is_typed_and_serialisable(self) -> None:
        cd.apply_delta(self.db, _delta())
        with self.assertRaises(cd.DeltaRefused) as ctx:
            cd.apply_delta(self.db, _delta())
        payload = json.loads(json.dumps(ctx.exception.receipt()))
        self.assertEqual(payload["schema"], "HGK-DELTA-DENIED/1")
        self.assertEqual(payload["code"], "ERR_DELTA_REPLAY")


if __name__ == "__main__":
    unittest.main()
