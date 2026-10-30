"""M18 -- rollback restores the pre-state AND does not delete pre-existing evidence.

Acceptance matrix row M18: 「rollback 恢復且不刪舊證據」, scope *full repaired runtime path, not helper
alone*. The subject under test is the REAL shipped script
``var/LANE-ENFORCEMENT-APPLY-20261015/APPLY_P6/rollback.py`` executed as a subprocess against the
REAL shipped ``apply_manifest.json`` and ``backup/`` tree.

Safety by construction (asserted, not merely intended): ``rollback.py`` derives its destinations
from the absolute ``canonical`` values in the manifest, so running it as shipped would revert the
LIVE applied control. This test therefore copies the artefact directory into a temp sandbox,
rewrites every absolute path in the COPIED manifest to a sandbox location, verifies that every
destination now resolves inside the sandbox, and only then spawns the byte-identical script copy
(sha256 asserted equal to the shipped file). The live repo, the live config and the recorder's
AppData path are never touched; nothing is written under ``APPLY_P6/``.

What is established:

1. RESTORES -- every ``pre_state`` entry ends in its recorded pre-state bytes (digest equals the
   manifest's recorded ``sha256`` for non-new files) and every ``new_file`` entry is gone.
2. PRESERVES -- sandbox files NOT named in ``pre_state`` and NOT created by the apply (raw receipts,
   lane stdout, the copied apply receipt) still exist with an UNCHANGED sha256.
3. NEGATIVE CONTROL -- a sandbox whose backup was tampered with does NOT silently produce a green
   restore. The shipped script carries no digest guard (it is a bare ``shutil.copy2``), so the
   failure mode it can offer is a detectable digest mismatch; the test asserts exactly that and
   names the missing guard instead of pretending to a guard the product does not have.

Claim ceiling: the shipped rollback logic restores pre-state and preserves unlisted evidence on a
SANDBOXED COPY of the manifest. Execution against canonical is deliberately out of scope and
remains unexecuted.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRATCH_ROOT = pathlib.Path("C:/Projects/Agent_Workspace/TEST_RESULTS")
PY = ROOT / ".venv" / "Scripts" / "python.exe"
APPLY = ROOT / "var" / "LANE-ENFORCEMENT-APPLY-20261015" / "APPLY_P6"
ROLLBACK = APPLY / "rollback.py"
MANIFEST = APPLY / "apply_manifest.json"
BACKUP = APPLY / "backup"

TIMEOUT = 120


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    return sha256_bytes(path.read_bytes())


class MatrixM18Rollback(unittest.TestCase):
    """Row M18: rollback restores and keeps old evidence (sandboxed execution of the real script)."""

    @classmethod
    def setUpClass(cls) -> None:
        missing = [str(p) for p in (ROLLBACK, MANIFEST, BACKUP) if not p.exists()]
        if missing:
            raise unittest.SkipTest(
                "M18: APPLY_P6 artefact directory is absent, cannot exercise the shipped rollback: "
                + ", ".join(missing)
            )
        cls.shipped = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.shipped_rollback_digest = sha256_file(ROLLBACK)

    # ------------------------------------------------------------------ sandbox builders
    def _make_sandbox(self, label: str) -> dict:
        """Copy the artefact dir into a fresh temp tree and point every manifest path inside it."""
        SCRATCH_ROOT.mkdir(parents=True, exist_ok=True)
        root = pathlib.Path(tempfile.mkdtemp(prefix=f"m18_{label}_", dir=str(SCRATCH_ROOT)))
        apply_dir = root / "APPLY_P6"
        apply_dir.mkdir()
        shutil.copy2(ROLLBACK, apply_dir / "rollback.py")
        shutil.copy2(APPLY / "APPLY_RECEIPT.json", apply_dir / "APPLY_RECEIPT.json")
        shutil.copytree(BACKUP, apply_dir / "backup")

        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        canonical_dir = root / "canonical"
        canonical_dir.mkdir()
        targets: dict[str, pathlib.Path] = {}
        for rel, entry in manifest["pre_state"].items():
            dst = canonical_dir / rel.replace("/", "__")
            dst.parent.mkdir(parents=True, exist_ok=True)
            entry["canonical"] = str(dst)
            targets[rel] = dst
        e_config = root / "canonical" / "hermes-codex-lane.json"
        manifest["e_config_pre"]["path"] = str(e_config)
        (apply_dir / "apply_manifest.json").write_text(
            json.dumps(manifest, indent=1, sort_keys=False), encoding="utf-8"
        )

        # Every destination must live inside the sandbox, and the sandbox must be outside the repo's
        # live paths. This is the construction that makes "never run against live" checkable.
        root_resolved = root.resolve()
        all_paths = [p for p in targets.values()] + [e_config]
        for path in all_paths:
            self.assertTrue(
                path.resolve().is_relative_to(root_resolved),
                f"M18: rewritten manifest path escapes the sandbox: {path}",
            )
        for path in all_paths:
            self.assertFalse(
                path.resolve().is_relative_to(ROOT.resolve()),
                f"M18: rewritten manifest path points into the live repository: {path}",
            )
        live_root = str(ROOT.resolve()).lower()
        rewritten_paths = [e["canonical"] for e in manifest["pre_state"].values()]
        rewritten_paths.append(manifest["e_config_pre"]["path"])
        for raw in rewritten_paths:
            self.assertNotIn(
                live_root,
                str(raw).lower(),
                f"M18: a residual live repository path survived the rewrite: {raw}",
            )

        return {
            "root": root,
            "apply_dir": apply_dir,
            "canonical_dir": canonical_dir,
            "targets": targets,
            "e_config": e_config,
            "manifest": manifest,
        }

    def _seed_post_apply_state(self, box: dict) -> dict:
        """Materialise the post-apply world: changed files present, new files present, evidence too."""
        recorded: dict[str, str | None] = {}
        for rel, entry in box["manifest"]["pre_state"].items():
            dst = box["targets"][rel]
            dst.parent.mkdir(parents=True, exist_ok=True)
            if entry["new_file"]:
                dst.write_bytes(f"# created by APPLY_P6 for {rel}\n".encode("utf-8"))
            else:
                dst.write_bytes(f"# POST-APPLY CONTENT for {rel}\n".encode("utf-8") * 3)
            recorded[rel] = entry["sha256"]
        box["e_config"].write_bytes(b'{"post": "apply", "hermes-codex-lane": true}\n')

        evidence = {
            "raw/receipt.json": b'{"receipt": "pre-existing evidence", "nonce": "M18"}\n',
            "lanes/20261016_lane/stdout.txt": b"lane stdout that must survive rollback\n",
            "lanes/20261016_lane/stderr.txt": b"",
            "APPLY_P6/APPLY_RECEIPT.json": (box["apply_dir"] / "APPLY_RECEIPT.json").read_bytes(),
        }
        for rel, data in evidence.items():
            path = box["root"] / rel
            if rel == "APPLY_P6/APPLY_RECEIPT.json":
                continue  # copied with the artefact dir; hashed in place
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        box["evidence"] = {rel: sha256_file(box["root"] / rel) for rel in evidence}
        box["recorded"] = recorded
        return box

    def _run_rollback(self, box: dict) -> subprocess.CompletedProcess:
        script = box["apply_dir"] / "rollback.py"
        self.assertEqual(
            sha256_file(script),
            self.shipped_rollback_digest,
            "M18: the executed copy is not byte-identical to the shipped rollback.py",
        )
        self.assertTrue(
            script.resolve().is_relative_to(box["root"].resolve()),
            "M18: refusing to spawn a rollback script outside the sandbox",
        )
        return subprocess.run(
            [str(PY), str(script)],
            cwd=str(box["root"]),
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
        )

    # ------------------------------------------------------------------ 1. restore
    def test_m18_rollback_restores_recorded_pre_state(self) -> None:
        box = self._seed_post_apply_state(self._make_sandbox("restore"))
        proc = self._run_rollback(box)
        self.assertEqual(
            proc.returncode,
            0,
            f"M18: rollback exited {proc.returncode}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
        )
        self.assertIn("ROLLBACK COMPLETE", proc.stdout, "M18: rollback did not report completion")

        for rel, entry in box["manifest"]["pre_state"].items():
            dst = box["targets"][rel]
            if entry["new_file"]:
                self.assertFalse(
                    dst.exists(),
                    f"M18: file created by the apply was not removed by rollback: {rel}",
                )
                continue
            self.assertTrue(dst.exists(), f"M18: pre-existing file missing after rollback: {rel}")
            expected = entry["sha256"]
            self.assertIsNotNone(expected, f"M18: non-new entry has no recorded digest: {rel}")
            self.assertEqual(
                sha256_file(dst),
                expected,
                f"M18: restored bytes of {rel} do not match the recorded pre-state digest",
            )
            backup = box["apply_dir"] / "backup" / rel.replace("/", "__")
            self.assertEqual(
                dst.read_bytes(),
                backup.read_bytes(),
                f"M18: restored {rel} is not byte-equal to its backup",
            )

        self.assertEqual(
            sha256_file(box["e_config"]),
            box["manifest"]["e_config_pre"]["sha256"],
            "M18: the e_config restore does not match its recorded pre-state digest",
        )

    # ------------------------------------------------------------------ 2. evidence survives
    def test_m18_rollback_preserves_unlisted_evidence(self) -> None:
        box = self._seed_post_apply_state(self._make_sandbox("evidence"))
        listed = {
            box["targets"][rel].resolve() for rel in box["manifest"]["pre_state"]
        } | {box["e_config"].resolve()}
        for rel, digest in box["evidence"].items():
            path = box["root"] / rel
            self.assertNotIn(path.resolve(), listed, f"M18: evidence fixture is manifest-listed: {rel}")
            self.assertTrue(path.exists(), f"M18: seeded evidence missing before rollback: {rel}")
            self.assertEqual(sha256_file(path), digest, f"M18: evidence seed digest drifted: {rel}")

        proc = self._run_rollback(box)
        self.assertEqual(proc.returncode, 0, f"M18: rollback failed\nstdout:\n{proc.stdout}\n{proc.stderr}")

        removed = [line for line in proc.stdout.splitlines() if line.startswith("removed new file")]
        new_files = [rel for rel, e in box["manifest"]["pre_state"].items() if e["new_file"]]
        self.assertEqual(
            len(removed),
            len(new_files),
            f"M18: rollback reported {len(removed)} removals for {len(new_files)} new_file entries "
            f"-- it may be deleting more than the apply created\nstdout:\n{proc.stdout}",
        )

        for rel, digest in box["evidence"].items():
            path = box["root"] / rel
            self.assertTrue(
                path.exists(),
                f"M18: rollback DELETED pre-existing evidence that the manifest does not list: {rel}",
            )
            self.assertEqual(
                sha256_file(path),
                digest,
                f"M18: rollback MUTATED pre-existing evidence: {rel}",
            )

    # ------------------------------------------------------------------ 3. negative control
    def test_m18_tampered_backup_is_not_a_silent_green(self) -> None:
        """A tampered backup must surface as a mismatch, never as an unnoticed clean restore.

        The shipped rollback.py contains no digest guard (bare shutil.copy2), so the only honest
        oracle is the test's own post-run digest comparison. This round is otherwise a
        should-have-passed round: every other entry still restores correctly, so the observed
        mismatch is attributable to the tamper alone.
        """
        box = self._seed_post_apply_state(self._make_sandbox("tamper"))
        victim = next(
            rel
            for rel, entry in box["manifest"]["pre_state"].items()
            if not entry["new_file"] and entry["sha256"]
        )
        backup_path = box["apply_dir"] / "backup" / victim.replace("/", "__")
        tampered = b"# TAMPERED BACKUP -- forged restoration payload\n"
        backup_path.write_bytes(tampered)
        self.assertEqual(sha256_file(backup_path), sha256_bytes(tampered))
        recorded = box["manifest"]["pre_state"][victim]["sha256"]
        self.assertNotEqual(sha256_bytes(tampered), recorded)

        proc = self._run_rollback(box)
        victim_dst = box["targets"][victim]
        observed = sha256_file(victim_dst) if victim_dst.exists() else None

        self.assertFalse(
            proc.returncode == 0 and observed == recorded,
            "M18 negative control: a tampered backup produced a GREEN restore "
            f"(exit {proc.returncode}, digest equal to recorded) -- the oracle is broken",
        )
        if proc.returncode == 0:
            # Documented gap: the shipped rollback.py performs a bare shutil.copy2 with no digest
            # verification, so a tampered backup is copied verbatim. The guard belongs in the
            # product and is deliberately NOT added here (this slice is test-only); the oracle is
            # the post-run digest comparison, which must be able to see the divergence.
            self.assertNotEqual(
                observed,
                recorded,
                "M18: shipped rollback.py has NO digest guard; the tampered backup must at least "
                "leave a digest the test can detect",
            )
            self.assertEqual(
                observed,
                sha256_bytes(tampered),
                "M18: the tampered backup was not even used, so this round proves nothing",
            )
            self.assertIn("restored", proc.stdout)
        else:
            combined = (proc.stdout + proc.stderr).lower()
            self.assertTrue(
                "sha256" in combined or "digest" in combined or "mismatch" in combined
                or victim.lower() in combined or "restored" in combined,
                "M18: rollback failed without naming the tampered subject or a digest mismatch:\n"
                f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}",
            )

        # Non-vacuity: the untouched entries still restore, so the tamper is the only divergence.
        for rel, entry in box["manifest"]["pre_state"].items():
            if rel == victim or entry["new_file"]:
                continue
            self.assertEqual(
                sha256_file(box["targets"][rel]),
                entry["sha256"],
                f"M18: collateral damage -- an untampered entry failed to restore: {rel}",
            )


if __name__ == "__main__":
    unittest.main()
