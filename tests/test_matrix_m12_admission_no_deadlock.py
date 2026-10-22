"""M12 — a legitimate bootstrap read and a legitimate admission do not deadlock.

Acceptance matrix row 12 (``var/LANE-ENFORCEMENT-APPLY-20261015/ACCEPTANCE_MATRIX.json``):
「合法 bootstrap read／admission 不死鎖」 over the full repaired runtime path.

Liveness is the assertion here: every exercised path runs in a real subprocess with an
explicit ``timeout=``, so a hang surfaces as a failing test instead of a stalled run.
``signal.alarm`` is not used (not portable on Windows).

Measured 2026-10-23 on this host (Windows, CPython 3.12.13, repo ``.venv``): child
interpreter start + real module import + the exercised path completes in ~0.5-0.8 s.
The bound is ``max(30 s, 20 x measured)`` — a small multiple of the measured normal
runtime with headroom for cold file cache / AV scanning on this host.

Claim ceiling: the legitimate bootstrap read and admission paths terminate within the
bound on this host under these fixtures. It does NOT prove absence of deadlock under
real load, real network, or a contended spine.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
SCRATCH_ROOT = Path("C:/Projects/Agent_Workspace/TEST_RESULTS")

BOUND_FLOOR_S = 30.0
BOUND_MULTIPLE = 20.0

_MEASURE_CHILD = """
import hg_kseos.bootstrap  # noqa: F401
import hg_kseos.lane_admission  # noqa: F401
print("ok")
"""


class MatrixM12LivenessTests(unittest.TestCase):
    """M12: legitimate bootstrap read + admission terminate under a hard bound."""

    bound: float = BOUND_FLOOR_S

    @classmethod
    def setUpClass(cls) -> None:
        SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
        # Measure the normal (non-hanging) child runtime, then bound a small multiple of it.
        measured = cls._spawn(_MEASURE_CHILD, timeout=BOUND_FLOOR_S * 4)
        cls.bound = max(BOUND_FLOOR_S, BOUND_MULTIPLE * measured)
        print(f"\nM12 measured child runtime {measured:.3f}s -> liveness bound {cls.bound:.1f}s")

    # -- plumbing ---------------------------------------------------------------------------
    @classmethod
    def _spawn(cls, body: str, *, timeout: float) -> float:
        env = dict(os.environ)
        existing = env.get("PYTHONPATH")
        env["PYTHONPATH"] = str(SRC_ROOT) + ((os.pathsep + existing) if existing else "")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        started = time.perf_counter()
        completed = subprocess.run(
            [sys.executable, "-c", textwrap.dedent(body)],
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            cwd=str(REPO_ROOT),
        )
        elapsed = time.perf_counter() - started
        if completed.returncode != 0:
            raise AssertionError(
                "child failed (exit "
                f"{completed.returncode}): {completed.stderr.strip()[-2000:]}"
            )
        return elapsed

    def run_child(self, body: str, *, label: str) -> tuple[float, dict]:
        env = dict(os.environ)
        existing = env.get("PYTHONPATH")
        env["PYTHONPATH"] = str(SRC_ROOT) + ((os.pathsep + existing) if existing else "")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        started = time.perf_counter()
        try:
            completed = subprocess.run(
                [sys.executable, "-c", textwrap.dedent(body)],
                capture_output=True,
                text=True,
                timeout=self.bound,
                env=env,
                cwd=str(REPO_ROOT),
            )
        except subprocess.TimeoutExpired:
            self.fail(
                f"M12 LIVENESS VIOLATION [{label}]: child did not terminate within "
                f"{self.bound:.1f}s on {sys.platform} — treated as a deadlock, not slowness"
            )
        elapsed = time.perf_counter() - started
        self.assertEqual(
            completed.returncode,
            0,
            f"M12 [{label}] child exit {completed.returncode}: {completed.stderr.strip()[-2000:]}",
        )
        self.assertLessEqual(
            elapsed,
            self.bound,
            f"M12 LIVENESS VIOLATION [{label}]: completed in {elapsed:.2f}s > bound {self.bound:.1f}s",
        )
        lines = [line for line in completed.stdout.splitlines() if line.strip()]
        self.assertTrue(
            lines,
            f"M12 [{label}] vacuous pass guard: child produced no output payload "
            f"(stdout empty, stderr={completed.stderr.strip()[-500:]!r})",
        )
        return elapsed, json.loads(lines[-1])

    def scratch_child(self, body: str, *, label: str) -> tuple[float, dict]:
        """Run a child whose body is handed a private scratch dir via ``SCRATCH``."""
        scratch = tempfile.mkdtemp(prefix="m12-", dir=str(SCRATCH_ROOT))
        self.addCleanup(lambda: __import__("shutil").rmtree(scratch, ignore_errors=True))
        return self.run_child(body.replace("__SCRATCH__", scratch.replace("\\", "/")), label=label)

    # -- 1. bootstrap read, positive --------------------------------------------------------
    def test_legitimate_bootstrap_read_terminates_with_expected_bindings(self) -> None:
        body = """
        import json
        from pathlib import Path
        from hg_kseos.bootstrap import configured_workspace_bindings

        root = Path("__SCRATCH__") / "bootstrap"
        canonical = root / "canonical"
        source = root / "source"
        maker = root / "maker"
        for directory in (canonical, source, maker):
            directory.mkdir(parents=True, exist_ok=True)

        single = configured_workspace_bindings(canonical, canonical)
        companion = configured_workspace_bindings(maker, source)
        print(json.dumps({
            "canonical": [[b[0], b[1], str(b[2]), b[3]] for b in single],
            "companion": [[b[0], b[1], str(b[2]), b[3]] for b in companion],
            "canonical_root": str(canonical.resolve()),
            "source_root": str(source.resolve()),
            "maker_root": str(maker.resolve()),
        }))
        """
        elapsed, payload = self.scratch_child(body, label="bootstrap_read")

        self.assertEqual(len(payload["canonical"]), 1, f"payload={payload}")
        workspace_id, project_id, path, mode = payload["canonical"][0]
        self.assertEqual(workspace_id, "WS-CANONICAL")
        self.assertEqual(project_id, "HGK-P0")
        self.assertEqual(path, payload["canonical_root"])
        self.assertEqual(mode, "WRITABLE_CANONICAL_WITH_FROZEN_INPUT_SUBTREES")

        self.assertEqual([row[0] for row in payload["companion"]], ["WS-SOURCE", "WS-MAKER"])
        self.assertEqual([row[3] for row in payload["companion"]], ["READ_ONLY_SOURCE", "WRITABLE_MAKER"])
        self.assertEqual(payload["companion"][0][2], payload["source_root"])
        self.assertEqual(payload["companion"][1][2], payload["maker_root"])

    # -- 2. admission, positive -------------------------------------------------------------
    def test_legitimate_admission_terminates_and_receipt_is_byte_deterministic(self) -> None:
        body = """
        import hashlib
        import json
        from pathlib import Path
        from hg_kseos import lane_admission as la

        arm = {"provider": "opencode-go", "model": "deepseek-v4.1-flash", "engine": "codex-cli"}
        out = Path("__SCRATCH__") / "admission"

        key = la.admission_key(lane="EXECUTE", arm=arm)
        record = la.LaneAdmission(lane="EXECUTE", arm=arm, policy_epoch=25)
        record.record_start()
        record.record_lane_exercise(
            completed_model_calls=1,
            completed_tools=1,
            served_provider="opencode-go",
            served_model="opencode-go/deepseek-v4.1-flash",
            served_engine="codex-cli",
        )
        decided = la.decide_status(record)
        persisted = record.decide()
        first = la.write_receipt(record, out / "a" / f"{key}.json")
        second = la.write_receipt(record, out / "b" / f"{key}.json")
        loaded = la.load_receipt(first)
        print(json.dumps({
            "key": key,
            "key_is_path_safe": not (set(key) & set("/\\\\")) and ".." not in key,
            "key_inside_root": str(first.resolve()).startswith(str(out.resolve())),
            "decide_status": decided,
            "persisted_status": persisted,
            "receipt_status": loaded["status"],
            "receipt_schema": loaded["schema"],
            "receipt_key": loaded["admission_key"],
            "digest_a": hashlib.sha256(first.read_bytes()).hexdigest(),
            "digest_b": hashlib.sha256(second.read_bytes()).hexdigest(),
            "bytes_identical": first.read_bytes() == second.read_bytes(),
            "trailing_newline": first.read_bytes().endswith(b"\\n"),
            "size": len(first.read_bytes()),
            "loaded_arm": loaded["arm"],
            "loaded_served": loaded["served"],
            "loaded_failure_code": loaded["failure_code"],
            "top_level_keys": sorted(loaded.keys()),
        }))
        """
        _elapsed, payload = self.scratch_child(body, label="admission")

        self.assertEqual(payload["key"], "EXECUTE__opencode-go__deepseek-v4.1-flash__codex-cli")
        self.assertTrue(payload["key_is_path_safe"], payload["key"])
        self.assertTrue(payload["key_inside_root"], payload["key"])
        self.assertEqual(payload["decide_status"], "ADMITTED")
        self.assertEqual(payload["persisted_status"], "ADMITTED")
        self.assertEqual(payload["receipt_status"], "ADMITTED")
        self.assertEqual(payload["receipt_schema"], "HGK-LANE-ADMISSION/1")
        self.assertEqual(payload["receipt_key"], payload["key"])
        self.assertTrue(payload["bytes_identical"], "receipt bytes differ between identical writes")
        self.assertEqual(payload["digest_a"], payload["digest_b"])
        self.assertTrue(payload["trailing_newline"])
        self.assertGreater(payload["size"], 0)
        self.assertEqual(payload["loaded_arm"]["model"], "deepseek-v4.1-flash")
        self.assertEqual(payload["loaded_served"]["provider"], "opencode-go")
        self.assertIsNone(payload["loaded_failure_code"])
        self.assertIn("claim_ceiling", payload["top_level_keys"])

    # -- 3. negative control ----------------------------------------------------------------
    def test_non_legitimate_admission_inputs_refuse_promptly_and_typed(self) -> None:
        body = """
        import json
        from pathlib import Path
        from hg_kseos import lane_admission as la

        out = Path("__SCRATCH__") / "negative"
        hostile_lane = "../../etc/passwd"
        hostile_arm = {"provider": "..\\\\..", "model": "..\\\\..\\\\secret", "engine": "/abs"}
        hostile_key = la.admission_key(lane=hostile_lane, arm=hostile_arm)
        target = out / f"{hostile_key}.json"

        # wrong served identity for the requested arm: a definitive, typed refusal
        arm = {"provider": "opencode-go", "model": "deepseek-v4.1-flash", "engine": "codex-cli"}
        mismatch = la.LaneAdmission(lane="VERIFY_SECURITY", arm=arm)
        mismatch.record_start()
        mismatch.record_lane_exercise(
            completed_model_calls=1,
            completed_tools=1,
            served_provider="opencode-go",
            served_model="opencode-go/glm-5.3-flash",
            served_engine="codex-cli",
        )

        # nothing measured: must never become ADMITTED
        unmeasured = la.LaneAdmission(lane="PLAN", arm=arm)
        unmeasured.record_direct_completion(ok=True, http_status=200, content_present=True)

        # exercised then definitively failed
        failed = la.LaneAdmission(lane="EXECUTE", arm=arm)
        failed.record_lane_exercise(
            completed_model_calls=0,
            completed_tools=0,
            served_provider=None,
            served_model=None,
            served_engine=None,
        )
        failed.set_failure("ERR_LANE_TIMEOUT")

        print(json.dumps({
            "hostile_key": hostile_key,
            "hostile_key_has_separator": ("/" in hostile_key) or ("\\\\" in hostile_key),
            "hostile_key_escapes_root": not str(target.resolve()).startswith(str(out.resolve())),
            "hostile_receipt_path": str(target.resolve()),
            "root": str(out.resolve()),
            "mismatch_status": mismatch.decide(),
            "mismatch_code": mismatch.failure_code,
            "mismatch_receipt_status": la.load_receipt(
                la.write_receipt(mismatch, out / "mismatch.json")
            )["status"],
            "unmeasured_status": unmeasured.decide(),
            "unmeasured_code": unmeasured.failure_code,
            "failed_status": failed.decide(),
            "failed_code": failed.failure_code,
        }))
        """
        _elapsed, payload = self.scratch_child(body, label="negative_control")

        self.assertEqual(payload["hostile_key"], "etc-passwd__unknown__secret__abs")
        self.assertFalse(payload["hostile_key_has_separator"], payload["hostile_key"])
        self.assertFalse(payload["hostile_key_escapes_root"], payload["hostile_receipt_path"])
        self.assertIn(payload["root"], payload["hostile_receipt_path"])

        self.assertEqual(payload["mismatch_status"], "REFUSED")
        self.assertEqual(payload["mismatch_code"], "ERR_LANE_IDENTITY_MODEL_MISMATCH")
        self.assertEqual(payload["mismatch_receipt_status"], "REFUSED")

        self.assertEqual(payload["unmeasured_status"], "UNPROVEN")
        self.assertIsNone(payload["unmeasured_code"])

        self.assertEqual(payload["failed_status"], "REFUSED")
        self.assertEqual(payload["failed_code"], "ERR_LANE_TIMEOUT")


if __name__ == "__main__":
    unittest.main()
