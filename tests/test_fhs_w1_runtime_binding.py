"""WP-FHS-04 tests — one queue, a fresh PID, monotonic checkpoints, a real resume."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hg_kseos.fhs import runtime_binding as rb  # noqa: E402


class TestRuntimeBinding(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_bind_records_fresh_pid_lease_and_cursor(self):
        rec = rb.bind(runtime_root=self.root, work_id="WO-FHS-W1-WP04", profile="hgk-governed",
                      profile_sha="d" * 64, pid=4242, actual_served="deepseek-v4.1-flash",
                      lease_generation=7, queue_item="card-1")
        self.assertEqual(rec["pid"], 4242)
        self.assertEqual(rec["lease_generation"], 7)
        self.assertEqual(rec["queue"]["state"], "SINGLE_QUEUE_ROOT")
        self.assertEqual(rec["journal"]["cursor"], 0)
        self.assertEqual(rec["claim_ceiling"], "AUTHOR_DESIGN_ONLY")
        self.assertRegex(rec["binding_sha256"], r"^[0-9a-f]{64}$")

    def test_unobserved_actual_served_is_refused(self):
        with self.assertRaises(rb.RuntimeRefusal) as ctx:
            rb.bind(runtime_root=self.root, work_id="WO-1", profile="p", profile_sha="0" * 64,
                    pid=1, actual_served="  ", lease_generation=1, queue_item="c")
        self.assertEqual(ctx.exception.code, "ACTUAL_SERVED_NOT_OBSERVED")

    def test_second_live_queue_root_is_refused(self):
        other = self.root / "second-queue"
        other.mkdir()
        (self.root / rb.QUEUE_REGISTRY).write_text(json.dumps(
            {"queue_roots": [str(self.root), str(other)]}), encoding="utf-8")
        with self.assertRaises(rb.RuntimeRefusal) as ctx:
            rb.assert_single_queue(self.root)
        self.assertEqual(ctx.exception.code, "SECOND_QUEUE_DENY")

    def test_one_live_queue_root_is_accepted(self):
        (self.root / rb.QUEUE_REGISTRY).write_text(json.dumps(
            {"queue_roots": [str(self.root), str(self.root / "gone")]}), encoding="utf-8")
        self.assertEqual(rb.assert_single_queue(self.root)["state"], "SINGLE_QUEUE_ROOT")

    def test_checkpoints_are_monotonic_and_resumable(self):
        rb.journal_append(runtime_root=self.root, work_id="WO-1", kind="START", detail={})
        first = rb.checkpoint(runtime_root=self.root, work_id="WO-1", lease_generation=1,
                              state="READY", checkpoint_seq=1, last_good="none")
        self.assertEqual(first["journal_cursor"], 1)
        rb.journal_append(runtime_root=self.root, work_id="WO-1", kind="STEP", detail={"n": 1})
        second = rb.checkpoint(runtime_root=self.root, work_id="WO-1", lease_generation=2,
                              state="IMPLEMENT", checkpoint_seq=2, last_good=first["checkpoint_sha256"])
        self.assertNotEqual(first["checkpoint_sha256"], second["checkpoint_sha256"])
        out = rb.resume(runtime_root=self.root, work_id="WO-1", lease_generation=2)
        self.assertEqual(out["state"], "RESUMABLE")
        self.assertEqual(out["checkpoint_seq"], 2)
        self.assertEqual(out["from_checkpoint"], second["checkpoint_sha256"])
        self.assertEqual(out["journal_cursor_now"], 2)

    def test_stale_lease_may_not_commit(self):
        rb.checkpoint(runtime_root=self.root, work_id="WO-1", lease_generation=3,
                      state="READY", checkpoint_seq=1, last_good="none")
        with self.assertRaises(rb.RuntimeRefusal) as ctx:
            rb.checkpoint(runtime_root=self.root, work_id="WO-1", lease_generation=2,
                          state="STALE", checkpoint_seq=2, last_good="x")
        self.assertEqual(ctx.exception.code, "RUNTIME_LEASE_BINDING_DENY")

    def test_non_monotonic_checkpoint_seq_is_refused(self):
        rb.checkpoint(runtime_root=self.root, work_id="WO-1", lease_generation=1,
                      state="READY", checkpoint_seq=2, last_good="none")
        with self.assertRaises(rb.RuntimeRefusal) as ctx:
            rb.checkpoint(runtime_root=self.root, work_id="WO-1", lease_generation=1,
                          state="AGAIN", checkpoint_seq=2, last_good="x")
        self.assertEqual(ctx.exception.code, "RUNTIME_LEASE_BINDING_DENY")

    def test_stale_lease_may_not_resume(self):
        rb.checkpoint(runtime_root=self.root, work_id="WO-1", lease_generation=5,
                      state="READY", checkpoint_seq=1, last_good="none")
        with self.assertRaises(rb.RuntimeRefusal) as ctx:
            rb.resume(runtime_root=self.root, work_id="WO-1", lease_generation=4)
        self.assertEqual(ctx.exception.code, "RUNTIME_LEASE_BINDING_DENY")

    def test_resume_without_a_checkpoint_is_refused(self):
        with self.assertRaises(rb.RuntimeRefusal):
            rb.resume(runtime_root=self.root, work_id="WO-NONE", lease_generation=1)

    def test_cross_profile_read_is_refused(self):
        inside = self.root / "profiles" / "p1" / "note.json"
        inside.parent.mkdir(parents=True)
        inside.write_text("{}", encoding="utf-8")
        self.assertEqual(rb.assert_profile_scope(inside, profile_root=self.root / "profiles" / "p1")["state"],
                         "IN_PROFILE")
        with self.assertRaises(rb.RuntimeRefusal) as ctx:
            rb.assert_profile_scope(inside, profile_root=self.root / "profiles" / "other")
        self.assertEqual(ctx.exception.code, "CROSS_PROFILE_SECRET_DENY")


if __name__ == "__main__":
    unittest.main()
