"""Focused tests for UserExperienceReducer v1 (task-006 §16)."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hg_kseos.release import UserExperienceEnvelope, UserExperienceReducer
from hg_kseos.spine import SharedSpine


def make_envelope(**overrides: object) -> UserExperienceEnvelope:
    base: dict[str, object] = {
        "uecx_source_expectations": 16,
        "uecx_rows": 15,
        "uecx_orphans": 0,
        "uecx_unknown": 0,
        "p0_required_user_journeys_open": 0,
        "p0_required_user_journeys_static_only": 0,
        "p0_required_user_journeys_maker_only": 0,
        "required_vertical_slices_total": 15,
        "required_vertical_slices_applicable": 13,
        "required_vertical_slices_pass": 13,
        "required_vertical_slices_deferred_source_backed": 2,
        "required_negative_tests_total": 12,
        "required_negative_tests_pass": 12,
        "natural_task_auto_route": "PASS",
        "skill_auto_select": "PASS",
        "memory_route_positive": "PASS",
        "memory_route_negative": "PASS",
        "rag_auto_route": "PASS",
        "kg_route_positive": "PASS",
        "kg_route_negative": "PASS",
        "unnecessary_hitl": 0,
        "unnecessary_multi_agent": 0,
        "unnecessary_tool_activation": 0,
        "self_promotion": 0,
        "authority_mutation": 0,
        "controlled_learning_scope_resolved": True,
        "obsidian_scope_resolved": True,
        "all_deferred_items_source_backed": True,
        "blocking_user_experience_tt": 0,
        "coverage_reducer_v2_exit": 0,
        "checker": "INDEPENDENT_CHECKER",
        "artifacts": ("UECX", "U7", "U8", "U9"),
    }
    base.update(overrides)
    return UserExperienceEnvelope.from_dict(base)


class UserExperienceReducerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.spine = SharedSpine(Path(self.tmp.name) / "spine.db")
        self.spine.initialize()
        self.spine.create_project()
        self.reducer = UserExperienceReducer(self.spine)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_full_pass(self) -> None:
        decision = self.reducer.reduce(make_envelope())
        self.assertEqual(decision["verdict"], "HG-KSEOS_USER_EXPECTED_CAPABILITY_EXPERIENCE_PASS")
        self.assertEqual(decision["reasons"], [])
        self.assertEqual(decision["exit_code"], 0)
        self.assertEqual(decision["schema"], "HGK-USER-EXPERIENCE-REDUCER/1")

    def test_open_p0_journey_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(p0_required_user_journeys_open=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("P0_USER_JOURNEYS_OPEN", decision["reasons"])

    def test_vertical_slice_incomplete_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(required_vertical_slices_pass=12))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("VERTICAL_SLICES_INCOMPLETE", decision["reasons"])

    def test_negative_tests_incomplete_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(required_negative_tests_pass=11))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("NEGATIVE_OPERATIONAL_TESTS_INCOMPLETE", decision["reasons"])

    def test_auto_route_fail(self) -> None:
        decision = self.reducer.reduce(make_envelope(natural_task_auto_route="FAIL"))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("NATURAL_TASK_AUTO_ROUTE_FAIL", decision["reasons"])

    def test_unnecessary_hitl_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(unnecessary_hitl=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("UNNECESSARY_HITL_NONZERO", decision["reasons"])

    def test_self_promotion_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(self_promotion=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("SELF_PROMOTION_NONZERO", decision["reasons"])

    def test_coverage_reducer_not_pass_fails(self) -> None:
        decision = self.reducer.reduce(make_envelope(coverage_reducer_v2_exit=1))
        self.assertEqual(decision["verdict"], "FAIL_CLOSED")
        self.assertIn("COVERAGE_REDUCER_V2_NOT_PASS", decision["reasons"])

    def test_missing_field_rejected(self) -> None:
        data = make_envelope().__dict__
        del data["checker"]
        with self.assertRaises(ValueError):
            UserExperienceEnvelope.from_dict(data)


if __name__ == "__main__":
    unittest.main()
