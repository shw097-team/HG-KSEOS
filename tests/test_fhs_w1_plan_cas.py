"""WP-FHS-07 tests — Commander A/B/C, the CAS, and the bootstrap inversion."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hg_kseos.fhs import plan_cas as pc  # noqa: E402

SPECS = {"product": "a" * 64, "architecture": "b" * 64, "program": "c" * 64}


class PlanReaderStub:
    """A stand-in reader. It is NOT the original PLAN reader: it proves only that the ACK path is
    gated on a receipt bound to the record digest, and that the reader's identity comes from the
    object rather than from a literal inside the module."""

    def __init__(self, module, *, identity: str, verdict: str = "ACK",
                 bind_to: str | None = None) -> None:
        self._m = module
        self.identity = identity
        self.verdict = verdict
        self.bind_to = bind_to

    def verify(self, record: dict[str, Any]) -> dict[str, Any]:
        return {"verdict": self.verdict, "reader_identity": self.identity,
                "record_sha256": self.bind_to if self.bind_to is not None else self._m._sha(record)}


class TestPlanCas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = pc.PlanStore(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def proposal(self, **over: Any):
        kw: dict[str, Any] = {"work_id": "WO-FHS-W1-WP07", "base_revision": 0,
                              "goal": "W1 PLAN 提案", "specs": SPECS,
                              "body": {"steps": ["wire", "test"]}}
        kw.update(over)
        return pc.propose(store=self.store, **kw)

    def test_a_reads_without_writing(self):
        view = pc.readonly_view(self.store, "WO-FHS-W1-WP07")
        self.assertEqual(view["current_revision"], 0)
        self.assertEqual(view["writes"], 0)
        self.assertTrue(view["isolated"])

    def test_b_proposes_in_isolation(self):
        p = self.proposal()
        self.assertTrue(p["isolated"])
        self.assertFalse(p["touches_repo"])
        self.assertFalse(p["touches_queue"])
        self.assertEqual(p["claim_ceiling"], "AUTHOR_DESIGN_ONLY")
        self.assertEqual(self.store.current_revision("WO-FHS-W1-WP07"), 0)

    def test_c_accepts_with_matching_revision(self):
        p = self.proposal()
        ack = pc.commit(store=self.store, proposal=p, expected_revision=0)
        # A candidate append is NOT an acceptance: no original reader was involved.
        self.assertEqual(ack["verdict"], "CANDIDATE_APPENDED_NO_ORIGINAL_READER")
        self.assertIsNone(ack["reader"])
        self.assertEqual(ack["original_reader_receipt"], "ABSENT")
        self.assertEqual(ack["revision"], 1)
        self.assertEqual(self.store.current_revision("WO-FHS-W1-WP07"), 1)

    # ---- forged-reader defect class (Fabric #31 analogue) -------------------
    def test_ack_requires_a_reader_receipt_bound_to_the_record(self):
        p = self.proposal()
        reader = PlanReaderStub(pc, identity="HGK-PLAN-READER-TEST")
        ack = pc.commit(store=self.store, proposal=p, expected_revision=0, reader=reader)
        self.assertEqual(ack["verdict"], "ACK")
        self.assertEqual(ack["reader"], "HGK-PLAN-READER-TEST")
        self.assertTrue(ack["appended"])
        row = self.store.revisions("WO-FHS-W1-WP07")[-1]
        self.assertTrue(row["original_reader_ack"])
        self.assertIn("reader_receipt_sha256", row)

    def test_receipt_for_another_record_is_refused(self):
        p = self.proposal()
        reader = PlanReaderStub(pc, identity="HGK-PLAN-READER-TEST", bind_to="0" * 64)
        with self.assertRaises(pc.PlanRefusal) as ctx:
            pc.commit(store=self.store, proposal=p, expected_revision=0, reader=reader)
        self.assertEqual(ctx.exception.code, "PLAN_READER_RECEIPT_UNBOUND")
        self.assertEqual(self.store.current_revision("WO-FHS-W1-WP07"), 0)

    def test_reader_without_identity_is_refused(self):
        p = self.proposal()
        reader = PlanReaderStub(pc, identity="   ")
        with self.assertRaises(pc.PlanRefusal) as ctx:
            pc.commit(store=self.store, proposal=p, expected_revision=0, reader=reader)
        self.assertEqual(ctx.exception.code, "PLAN_READER_RECEIPT_UNBOUND")

    def test_reader_nack_does_not_advance_the_revision(self):
        p = self.proposal()
        reader = PlanReaderStub(pc, identity="HGK-PLAN-READER-TEST", verdict="NACK")
        out = pc.commit(store=self.store, proposal=p, expected_revision=0, reader=reader)
        self.assertEqual(out["verdict"], "NACK")
        self.assertFalse(out["appended"])
        self.assertEqual(self.store.current_revision("WO-FHS-W1-WP07"), 0)

    def test_self_claimed_original_writer_identity_is_refused(self):
        p = self.proposal()
        with self.assertRaises(pc.PlanRefusal) as ctx:
            pc.commit(store=self.store, proposal=p, expected_revision=0,
                      requester="ORIGINAL_HGK_PLAN_WRITER")
        self.assertEqual(ctx.exception.code, "PLAN_WRITER_SELF_CLAIM_DENY")

    def test_an_arbitrary_requester_gets_a_candidate_append_not_an_ack(self):
        p = self.proposal()
        out = pc.commit(store=self.store, proposal=p, expected_revision=0,
                        requester="NOT_THE_ORIGINAL_WRITER")
        self.assertEqual(out["verdict"], "CANDIDATE_APPENDED_NO_ORIGINAL_READER")
        self.assertEqual(self.store.revisions("WO-FHS-W1-WP07")[-1]["requester"],
                         "NOT_THE_ORIGINAL_WRITER")
        self.assertFalse(self.store.revisions("WO-FHS-W1-WP07")[-1]["original_reader_ack"])

    def test_no_output_ever_names_the_original_reader_as_the_reader(self):
        p = self.proposal()
        out = pc.commit(store=self.store, proposal=p, expected_revision=0)
        self.assertNotEqual(out.get("reader"), "ORIGINAL_HGK_PLAN_CAS_READER")
        self.assertIsNone(out.get("reader"))

    def test_second_revision_requires_the_new_base(self):
        ack = pc.commit(store=self.store, proposal=self.proposal(), expected_revision=0)
        self.assertEqual(ack["revision"], 1)
        p2 = self.proposal(base_revision=1, body={"steps": ["revise"]})
        ack2 = pc.commit(store=self.store, proposal=p2, expected_revision=1)
        self.assertEqual(ack2["revision"], 2)

    def test_stale_cas_is_refused(self):
        pc.commit(store=self.store, proposal=self.proposal(), expected_revision=0)
        p2 = self.proposal(base_revision=1)
        with self.assertRaises(pc.PlanRefusal) as ctx:
            pc.commit(store=self.store, proposal=p2, expected_revision=0)
        self.assertEqual(ctx.exception.code, "PLAN_CAS_STALE")
        self.assertEqual(self.store.current_revision("WO-FHS-W1-WP07"), 1)

    def test_proposal_against_a_stale_base_is_refused(self):
        with self.assertRaises(pc.PlanRefusal) as ctx:
            self.proposal(base_revision=5)
        self.assertEqual(ctx.exception.code, "PLAN_CAS_STALE")

    def test_cross_work_commit_is_refused(self):
        p = self.proposal()
        with self.assertRaises(pc.PlanRefusal) as ctx:
            pc.commit(store=self.store, proposal=p, expected_revision=0, work_id="WO-FHS-W1-OTHER")
        self.assertEqual(ctx.exception.code, "CROSS_WORK_PLAN_AUTH_DENY")

    def test_tampered_proposal_is_refused(self):
        p = self.proposal()
        p["body"] = {"steps": ["different"]}
        with self.assertRaises(pc.PlanRefusal) as ctx:
            pc.commit(store=self.store, proposal=p, expected_revision=0)
        self.assertEqual(ctx.exception.code, "PLAN_PROPOSAL_TAMPERED")

    def test_requiring_a_permit_to_plan_is_the_bootstrap_inversion(self):
        with self.assertRaises(pc.PlanRefusal) as ctx:
            self.proposal(require_permit=True)
        self.assertEqual(ctx.exception.code, "WP-FHS-07.FIRST_FAIL:COMMANDER_BOOTSTRAP_INVERSION")

    def test_a_planning_gate_permit_is_refused(self):
        with self.assertRaises(pc.PlanRefusal) as ctx:
            self.proposal(permit={"gate": "PLANNING", "permit_id": "PERMIT-1"})
        self.assertIn("COMMANDER_BOOTSTRAP_INVERSION", ctx.exception.code)

    def test_empty_goal_is_refused(self):
        with self.assertRaises(pc.PlanRefusal) as ctx:
            self.proposal(goal="   ")
        self.assertEqual(ctx.exception.code, "PLAN_PROPOSAL_EMPTY")

    def test_rollback_is_a_discard_not_a_rewrite(self):
        pc.commit(store=self.store, proposal=self.proposal(), expected_revision=0)
        out = pc.rollback(store=self.store, work_id="WO-FHS-W1-WP07", to_revision=1)
        self.assertEqual(out["state"], "DISCARD_ISOLATED_PROPOSAL_ONLY")
        self.assertEqual(self.store.current_revision("WO-FHS-W1-WP07"), 1)


if __name__ == "__main__":
    unittest.main()
