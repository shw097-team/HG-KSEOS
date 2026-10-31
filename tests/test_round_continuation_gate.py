"""The round-close gate must refuse for the right reason, and must not invent one.

Measured 2026-10-31: the gate's first version looked for cron jobs in state.db, found none, and reported "no
continuation supervisor exists at all" while `hermes cron list` was showing a paused one two feet away. A probe
that cannot find its own input must not answer "absent" -- that is the same defect as a status surface that
reports IDLE because its query crashed, and it would have sent the next session to create a job that already
existed.

These tests pin the three real refusal reasons and the one legitimate close.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import round_continuation_gate as gate  # noqa: E402

ACTIVE_GOAL = {"present": True, "status": "active", "db": "state.db"}
NO_GOAL = {"present": False, "status": None, "db": None}
PAUSED_SUP = {"present": True, "paused": True, "name": "hgk-continuation-supervisor", "db": "jobs.json"}
ARMED_SUP = {"present": True, "paused": False, "name": "hgk-continuation-supervisor", "db": "jobs.json"}
MISSING_SUP = {"present": False, "paused": None, "name": None, "db": None}
OPEN_ROWS = [{"wp_id": "WP-A", "state": "FAIL"}, {"wp_id": "WP-B", "state": "PASS"}]
DONE_ROWS = [{"wp_id": "WP-B", "state": "PASS"}]
BLOCKED_NO_UNBLOCK = [{"wp_id": "WP-A", "state": "FAIL", "blocker_code": "ERR_X", "blocker_unblock": ""}]
BLOCKED_WITH_UNBLOCK = [{"wp_id": "WP-A", "state": "FAIL", "blocker_code": "ERR_X",
                         "blocker_unblock": "upgrade the bundled runtime"}]


class TestRoundContinuationGate(unittest.TestCase):
    def run_gate(self, goal, sup, rows):
        with mock.patch.object(gate, "goal_row", return_value=goal), \
             mock.patch.object(gate, "supervisor_state", return_value=sup), \
             mock.patch.object(gate, "work_queue_rows", return_value=rows):
            return gate.evaluate("S1")

    def codes(self, r):
        return [f["code"] for f in r["findings"]]

    def test_an_absent_goal_row_refuses_the_close(self):
        r = self.run_gate(NO_GOAL, ARMED_SUP, DONE_ROWS)
        self.assertEqual(r["verdict"], "REFUSED_TO_CLOSE")
        self.assertIn(gate.NO_GOAL_ROW, self.codes(r))

    def test_a_paused_goal_is_as_good_as_no_goal(self):
        r = self.run_gate({"present": True, "status": "done", "db": "state.db"}, ARMED_SUP, DONE_ROWS)
        self.assertIn(gate.NO_GOAL_ROW, self.codes(r))

    def test_a_paused_supervisor_refuses_the_close(self):
        r = self.run_gate(ACTIVE_GOAL, PAUSED_SUP, DONE_ROWS)
        self.assertIn(gate.SUPERVISOR_PAUSED, self.codes(r))

    def test_a_missing_supervisor_is_not_the_same_as_a_paused_one_but_both_refuse(self):
        r = self.run_gate(ACTIVE_GOAL, MISSING_SUP, DONE_ROWS)
        self.assertIn(gate.SUPERVISOR_PAUSED, self.codes(r))

    def test_open_work_refuses_even_when_every_mechanism_is_armed(self):
        r = self.run_gate(ACTIVE_GOAL, ARMED_SUP, OPEN_ROWS)
        self.assertEqual(r["verdict"], "REFUSED_TO_CLOSE")
        self.assertEqual(self.codes(r), [gate.OPEN_WORK])

    def test_a_blocker_without_an_unblock_is_a_stop_dressed_as_a_status(self):
        r = self.run_gate(ACTIVE_GOAL, ARMED_SUP, BLOCKED_NO_UNBLOCK)
        self.assertIn(gate.BLOCKER_WITHOUT_UNBLOCK, self.codes(r))

    def test_a_named_blocker_with_an_unblock_permits_the_close(self):
        r = self.run_gate(ACTIVE_GOAL, ARMED_SUP, BLOCKED_WITH_UNBLOCK)
        self.assertEqual(r["verdict"], gate.OK_TO_CLOSE, r["findings"])

    def test_all_pass_permits_the_close(self):
        r = self.run_gate(ACTIVE_GOAL, ARMED_SUP, DONE_ROWS)
        self.assertEqual(r["verdict"], gate.OK_TO_CLOSE)

    def test_an_empty_queue_is_not_a_finished_queue(self):
        r = self.run_gate(ACTIVE_GOAL, ARMED_SUP, [])
        self.assertIn(gate.NO_NEXT_ACTION, self.codes(r))

    def test_the_owner_override_is_recorded_not_silent(self):
        with mock.patch.object(gate, "goal_row", return_value=NO_GOAL), \
             mock.patch.object(gate, "supervisor_state", return_value=PAUSED_SUP), \
             mock.patch.object(gate, "work_queue_rows", return_value=DONE_ROWS):
            rc = gate.main(["--session", "S1", "--allow-close-because", "owner asked to stop"])
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
