"""A checker that must execute the subject cannot execute it in place.

Sitting E ran the WP-17 chain in the subject tree for 257 seconds, echoed its nonce, produced a real run -- and was
refused with ERR_CHECKER_MUTATED_SUBJECT, because build_evidence.py writes install roots, load receipts and
negatives into the tree it is judging. The refusal was correct: a checker that changes the subject has judged a
different subject than the one on record.

The fix is not to weaken the guard but to separate the two roles. `--guard-subject` is the workspace the checker
may write; `--guard-record` is the subject of record, which must stay byte-identical. And because a copy is only
evidence if it was faithful, the dispatcher compares the two BEFORE the sitting: a pre-tampered copy cannot pass
as a faithful one.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISPATCH = ROOT / "scripts" / "hgk-lane-dispatch.py"


def dispatch(*extra: str) -> dict:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "r.json"
        subprocess.run(
            [sys.executable, str(DISPATCH), "--lane", "VERIFY_SECURITY",
             "--prompt", "reply with: PROBE", "--nonce", "NONCE-TEST-GUARDRECORD",
             "--identity-source", "codex-rollout",
             "--codex-home", str(Path.home() / ".codex"), "--allow-human-home-transport",
             "--timeout", "20", "--json-out", str(out), *extra],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
        )
        if not out.exists():
            raise AssertionError("dispatcher wrote no receipt")
        return json.loads(out.read_text(encoding="utf-8"))


class TestGuardRecord(unittest.TestCase):
    def test_a_diverging_copy_is_refused_before_the_sitting(self):
        with tempfile.TemporaryDirectory() as td:
            record = Path(td) / "record"
            copy = Path(td) / "copy"
            record.mkdir()
            copy.mkdir()
            (record / "a.txt").write_text("the subject of record", encoding="utf-8")
            (copy / "a.txt").write_text("a different tree entirely", encoding="utf-8")
            r = dispatch("--guard-subject", str(copy), "--guard-record", str(record))
            self.assertFalse(r["ok"])
            self.assertEqual(r["code"], "ERR_SUBJECT_COPY_DIVERGES")
            self.assertTrue(r.get("differing_entries"), "the refusal must name what differs")
            self.assertEqual(r.get("attempts") or [], [], "a setup refusal must spend no model call")

    def test_an_identical_copy_is_accepted_as_a_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            record = Path(td) / "record"
            copy = Path(td) / "copy"
            record.mkdir()
            (record / "a.txt").write_text("the subject of record", encoding="utf-8")
            copy.mkdir()
            (copy / "a.txt").write_text("the subject of record", encoding="utf-8")
            r = dispatch("--guard-subject", str(copy), "--guard-record", str(record))
            # It will fail later for an unrelated reason (no model call is wanted here), but it must NOT be the
            # fidelity refusal: an identical copy is a legitimate workspace.
            self.assertNotEqual(r.get("code"), "ERR_SUBJECT_COPY_DIVERGES")


if __name__ == "__main__":
    unittest.main()
