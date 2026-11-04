# -*- coding: utf-8 -*-
"""Tests for the read-only HGK consumer gate over an FHS W0 implementation result."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
for cand in HERE.parents:
    if (cand / "src" / "hg_kseos").is_dir():
        sys.path.insert(0, str(cand / "src"))
        break
else:  # pragma: no cover
    raise RuntimeError("src/hg_kseos not found above " + str(HERE))

from hg_kseos.fhs_w0_consumer import evaluate  # noqa: E402

GOOD = {
    "work_packages": {
        "WP-FHS-00": {"status": "DONE"},
        "WP-FHS-01": {"status": "DONE"},
        "WP-FHS-15": {"status": "DONE"},
        "WP-FHS-16": {"status": "PARTIAL"},
        "WP-FHS-19": {"status": "PARTIAL"},
        "WP-FHS-21": {"status": "DONE"},
    },
    "trace": {"scope": "AUTHOR_STATIC"},
    "specs": {
        "product": {"sha256": "a" * 64},
        "architecture": {"sha256": "b" * 64},
        "program": {"sha256": "c" * 64},
    },
    "claim_ceiling": "AUTHOR_LOCAL_TEST",
}


class ConsumerGateTests(unittest.TestCase):
    def _run(self, payload):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "result.json"
            p.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            return evaluate(p)

    def test_positive_candidate_ready(self):
        v = self._run(GOOD)
        self.assertEqual(v.verdict, "CANDIDATE_READY_FOR_HGK_REVIEW")
        self.assertIsNone(v.first_fail)
        self.assertEqual(v.claim_ceiling, "CANDIDATE_ONLY")
        self.assertIn("NOT_AN_HGK_PERMIT", v.non_claims)

    def test_missing_artifact(self):
        v = evaluate(Path(tempfile.gettempdir()) / "definitely-absent-w0-result.json")
        self.assertEqual(v.first_fail, "MISSING_ARTIFACT")

    def test_native_claim_refused(self):
        bad = json.loads(json.dumps(GOOD))
        bad["hgk_permit"] = True
        v = self._run(bad)
        self.assertEqual(v.first_fail, "NATIVE_CLAIM_REFUSED")
        self.assertEqual(v.verdict, "REFUSED")

    def test_missing_work_package(self):
        bad = json.loads(json.dumps(GOOD))
        bad["work_packages"].pop("WP-FHS-16")
        v = self._run(bad)
        self.assertEqual(v.first_fail, "WP_NOT_IMPLEMENTED")
        self.assertEqual(v.findings, ["WP-FHS-16"])

    def test_trace_scope_invalid(self):
        bad = json.loads(json.dumps(GOOD))
        bad["trace"]["scope"] = "NATIVE_E2E"
        v = self._run(bad)
        self.assertEqual(v.first_fail, "TRACE_SCOPE_INVALID")

    def test_spec_unbound(self):
        bad = json.loads(json.dumps(GOOD))
        bad["specs"]["program"] = {}
        v = self._run(bad)
        self.assertEqual(v.first_fail, "SPEC_UNBOUND")
        self.assertEqual(v.findings, ["program"])


if __name__ == "__main__":
    unittest.main()
