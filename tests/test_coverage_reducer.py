"""CoverageReducer (v2) focused tests — 指令-4 §13/§17 fail-closed contract."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from hg_kseos.release import CoverageEnvelope, CoverageReducer
from hg_kseos.spine import SharedSpine


def make_envelope(**overrides: object) -> CoverageEnvelope:
    base: dict[str, object] = {
        "coverage_domains_total": 30,
        "coverage_domains_terminal": 30,
        "canonical_requirements_total": 499,
        "requirements_reconciled": True,
        "orphan_requirements": 0,
        "unowned_mandatory_assets": 0,
        "tst_total": 92,
        "tst_independent_pass": 92,
        "semantic_depth_calibrated": True,
        "runtime_required_static_only_count": 0,
        "domains": {"memory": "RUNTIME_PASS", "knowledge_factory": "RUNTIME_PASS",
                    "retrieval_rag_kb": "RUNTIME_PASS", "knowledge_graph": "RUNTIME_PASS",
                    "graphrag": "DEFERRED_SOURCE_BACKED", "storage": "RUNTIME_PASS"},
        "knowledge_security_negative": "PASS",
        "domain_blocking_gaps": 0,
        "hermes_provider": "opencode-go",
        "hermes_model": "deepseek-v4-flash",
        "codex_cli_primary_executor": True,
        "opencodex_transport": True,
        "openai_model_fallback": False,
        "protected_identities_78_disposition_complete": True,
        "mandatory_default_active_providers_certified": True,
        "tst_054": "INDEPENDENT_CASE_PASS",
        "tst_092": "INDEPENDENT_CASE_PASS",
        "product_tests_all_pass": True,
        "hlpe_tests_all_pass": True,
        "security_blockers": 0,
        "blocking_tt": 0,
        "backup_restore_pass": True,
        "rollback_pass": True,
        "sbom_current": True,
        "user_guide_exists": True,
        "user_guide_runtime_consistent": True,
        "user_guide_sha256_verified": True,
        "package_exact_readback": True,
        "final_head_independently_checked": True,
        "final_evidence_md_exists": True,
        "final_evidence_md_readback_verified": True,
        "checker": "INDEPENDENT_CHECKER",
        "artifacts": ("evidence/review/HG-KSEOS_DOMAIN_COVERAGE_RECONCILIATION.json",),
    }
    base.update(overrides)
    return CoverageEnvelope.from_dict(base)


class CoverageReducerTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.spine = SharedSpine(Path(self._tmp.name) / "spine.db")
        self.spine.initialize()
        self.spine.create_project()
        self.reducer = CoverageReducer(self.spine)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_all_green_passes(self) -> None:
        decision = self.reducer.reduce(make_envelope())
        self.assertEqual("HG-KSEOS_LOCAL_DELIVERY_PASS", decision["verdict"])
        self.assertEqual([], decision["reasons"])
        self.assertEqual("2", decision["reducer_version"])

    def test_forbidden_domain_status_fails_closed(self) -> None:
        env = make_envelope(domains={"memory": "UNKNOWN"})
        decision = self.reducer.reduce(env)
        self.assertEqual("FAIL_CLOSED", decision["verdict"])
        self.assertTrue(any("DOMAIN_STATUS_FORBIDDEN" in r for r in decision["reasons"]))

    def test_openai_fallback_fails_closed(self) -> None:
        env = make_envelope(openai_model_fallback=True)
        decision = self.reducer.reduce(env)
        self.assertEqual("FAIL_CLOSED", decision["verdict"])
        self.assertIn("OPENAI_MODEL_FALLBACK_ENABLED", decision["reasons"])

    def test_deferred_not_impersonated_as_runtime(self) -> None:
        # DEFERRED_SOURCE_BACKED is a legal terminal status, distinct from RUNTIME_PASS
        env = make_envelope(domains={"graphrag": "DEFERRED_SOURCE_BACKED"})
        decision = self.reducer.reduce(env)
        self.assertEqual("HG-KSEOS_LOCAL_DELIVERY_PASS", decision["verdict"])

    def test_deferred_cannot_be_blank(self) -> None:
        env = make_envelope(domains={"graphrag": ""})
        decision = self.reducer.reduce(env)
        self.assertEqual("FAIL_CLOSED", decision["verdict"])
        self.assertTrue(any("DOMAIN_STATUS_NONTERMINAL" in r for r in decision["reasons"]))

    def test_route_mismatch_fails_closed(self) -> None:
        env = make_envelope(hermes_model="gpt-5.6-sol")
        decision = self.reducer.reduce(env)
        self.assertEqual("FAIL_CLOSED", decision["verdict"])
        self.assertIn("HERMES_ROUTE_MISMATCH", decision["reasons"])

    def test_tst_not_independent_fails_closed(self) -> None:
        env = make_envelope(tst_independent_pass=90)
        decision = self.reducer.reduce(env)
        self.assertEqual("FAIL_CLOSED", decision["verdict"])
        self.assertIn("ACCEPTANCE_NOT_INDEPENDENT_FULL", decision["reasons"])

    def test_missing_field_rejected(self) -> None:
        data = make_envelope().__dict__
        del data["checker"]
        with self.assertRaises(ValueError):
            CoverageEnvelope.from_dict(data)


if __name__ == "__main__":
    unittest.main()
