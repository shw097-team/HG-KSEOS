"""C14: a checkpoint resume must not repeat a world effect.

What ``hg_kseos.recovery`` actually guarantees, read from the module and its behaviour before this
file was written:

* ``backup_database(database, backup_root)`` copies through SQLite's online backup API into
  ``<backup_root>/hg-kseos-<stamp>.db``, hashes the file that was *written* (not the source), and
  publishes a ``*.manifest.json`` sidecar carrying that digest with
  ``status: BACKUP_READBACK_PASS``. The return value is the manifest plus a ``manifest`` path key.
* ``restore_database(backup, expected_sha256, restore_target)`` is the resume surface, and it is a
  *gate* rather than an overwriting writer. It refuses a digest mismatch with
  ``ERR_BACKUP_DIGEST_MISMATCH`` before it touches the filesystem, and it refuses an existing target
  with ``ERR_RESTORE_TARGET_EXISTS``. That second refusal is how "a resume must not repeat a world
  effect" is enforced here: replaying a verified restore does not rewrite, merge into, or accumulate
  onto the target -- it is rejected, and the target's bytes stay byte-identical.
  The replay test therefore asserts the *refusal plus byte equality* guarantee that the code
  documents, not an in-place idempotent rewrite that ``restore_database`` does not implement. If the
  implementation ever learns to re-restore in place, that test fails loudly and the guarantee has to
  be restated deliberately instead of silently drifting.
* A successful restore returns ``RESTORE_READBACK_PASS`` with the sha256 it measured *after* the
  copy, and a copy that fails ``PRAGMA integrity_check`` is unlinked before
  ``ERR_RESTORE_INTEGRITY`` is raised -- so a failed restore cannot leave a half-written target
  standing in for a committed checkpoint.

Each test builds its own SQLite database under pytest's ``tmp_path``; there is no network, no repo
fixture, and no write outside the pytest temp root.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

recovery = pytest.importorskip(
    "hg_kseos.recovery",
    reason="HG-KSEOS src is not importable in this interpreter",
)
errors = pytest.importorskip(
    "hg_kseos.errors",
    reason="HG-KSEOS src is not importable in this interpreter",
)
InvariantViolation = errors.InvariantViolation

PAYLOADS = [f"effect-{index}" for index in range(5)]


def _sha256(path: Path) -> str:
    """Digest of a file on disk, independent of ``hg_kseos.util`` so the test cannot be fooled."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _seeded_database(root: Path) -> Path:
    """A real database with a handful of committed rows, i.e. a state worth checkpointing."""
    database = root / "live" / "spine.db"
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database)
    try:
        connection.execute(
            "CREATE TABLE checkpoint(id INTEGER PRIMARY KEY, payload TEXT NOT NULL)"
        )
        connection.executemany(
            "INSERT INTO checkpoint(payload) VALUES (?)",
            [(payload,) for payload in PAYLOADS],
        )
        connection.commit()
    finally:
        connection.close()
    return database


def _rows(database: Path) -> list[str]:
    connection = sqlite3.connect(database)
    try:
        return [row[0] for row in connection.execute("SELECT payload FROM checkpoint ORDER BY id")]
    finally:
        connection.close()


def test_backup_digest_is_accepted_by_restore(tmp_path):
    """A backup publishes the digest of the bytes it wrote, and a restore accepts that digest.

    The published digest is checked against the backup file itself, against the manifest sidecar,
    and against the bytes on disk after the restore. ``restore_database`` lowercases the expected
    digest before comparing, so an upper-cased copy of the same digest is accepted for a second,
    independent target -- that is a real guarantee of the module, not a convenience of this test.
    """
    database = _seeded_database(tmp_path)
    receipt = recovery.backup_database(database, tmp_path / "backups")

    backup = Path(receipt["backup"])
    assert backup.is_file(), "backup_database did not write a backup file"
    assert receipt["status"] == "BACKUP_READBACK_PASS"
    assert Path(receipt["source"]).resolve() == database.resolve()

    digest = _sha256(backup)
    assert receipt["sha256"] == digest, "the published digest is not the digest of the written file"

    manifest_path = Path(receipt["manifest"])
    assert manifest_path.is_file(), "backup_database did not write its manifest sidecar"
    published = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert published["sha256"] == digest
    assert Path(published["backup"]).resolve() == backup.resolve()
    assert published["status"] == "BACKUP_READBACK_PASS"

    target = tmp_path / "restore" / "spine.db"
    restored = recovery.restore_database(backup, receipt["sha256"], target)

    assert restored["status"] == "RESTORE_READBACK_PASS"
    assert restored["sha256"] == digest
    assert _sha256(target) == digest, "the restored file does not match the accepted backup digest"
    assert target.read_bytes() == backup.read_bytes()
    assert _rows(target) == PAYLOADS

    # The same digest with different casing resolves to the same backup, so a resumed checkpoint
    # whose digest was re-encoded by a caller is not treated as a mismatch.
    upper_target = tmp_path / "restore-upper" / "spine.db"
    upper = recovery.restore_database(backup, receipt["sha256"].upper(), upper_target)
    assert upper["status"] == "RESTORE_READBACK_PASS"
    assert _sha256(upper_target) == digest


def test_replaying_a_verified_restore_does_not_repeat_the_effect(tmp_path):
    """A second restore of the same verified backup leaves the target byte-identical.

    ``restore_database`` enforces this by refusing to write over an existing target
    (``ERR_RESTORE_TARGET_EXISTS``), so the replay has no chance to duplicate, re-apply, or
    truncate anything. The assertions pin both halves: the typed refusal, and the fact that the
    target's sha256 and bytes are unchanged after the attempt. The restore directory is also
    required to hold exactly one artifact -- a replay that "succeeded" into a new filename would be
    a repeated world effect wearing a different name.
    """
    database = _seeded_database(tmp_path)
    receipt = recovery.backup_database(database, tmp_path / "backups")
    backup = Path(receipt["backup"])
    target = tmp_path / "restore" / "spine.db"

    first = recovery.restore_database(backup, receipt["sha256"], target)
    first_digest = _sha256(target)
    first_bytes = target.read_bytes()
    assert first["sha256"] == first_digest == receipt["sha256"]

    with pytest.raises(InvariantViolation) as caught:
        recovery.restore_database(backup, receipt["sha256"], target)

    assert str(caught.value) == "ERR_RESTORE_TARGET_EXISTS"
    assert target.is_file()
    assert _sha256(target) == first_digest, "the refused replay changed the target's digest"
    assert target.read_bytes() == first_bytes, "the refused replay changed the target's bytes"
    assert sorted(entry.name for entry in target.parent.iterdir()) == ["spine.db"]
    assert _rows(target) == PAYLOADS, "the refused replay duplicated or dropped rows"


def test_resume_with_mismatched_digest_is_refused_and_target_untouched(tmp_path):
    """A resume whose expected digest disagrees with the backup is refused and writes nothing.

    Two cases are pinned, because "untouched" means different things for each: a pre-existing target
    keeps its exact bytes (the digest gate fires before the overwrite gate), and a missing target
    stays missing (the module does not create an empty file or a parent directory on the way to
    rejecting the resume).
    """
    database = _seeded_database(tmp_path)
    receipt = recovery.backup_database(database, tmp_path / "backups")
    backup = Path(receipt["backup"])
    wrong_digest = "0" * 64
    assert wrong_digest != receipt["sha256"]

    target = tmp_path / "restore" / "spine.db"
    target.parent.mkdir(parents=True, exist_ok=True)
    sentinel = b"checkpoint state that must survive a refused resume\n"
    target.write_bytes(sentinel)
    before_digest = _sha256(target)

    with pytest.raises(InvariantViolation) as caught:
        recovery.restore_database(backup, wrong_digest, target)

    assert str(caught.value) == "ERR_BACKUP_DIGEST_MISMATCH"
    assert target.read_bytes() == sentinel, "a refused resume overwrote the existing target"
    assert _sha256(target) == before_digest
    assert target.read_bytes() != backup.read_bytes()

    # A missing target stays missing: refusal happens before the parent directory is created.
    absent = tmp_path / "never-created" / "spine.db"
    with pytest.raises(InvariantViolation) as caught:
        recovery.restore_database(backup, wrong_digest, absent)
    assert str(caught.value) == "ERR_BACKUP_DIGEST_MISMATCH"
    assert not absent.exists(), "a refused resume created the restore target"
    assert not absent.parent.exists(), "a refused resume created the restore directory"

    # The backup itself was never the thing being written to, so it is still the accepted digest.
    assert _sha256(backup) == receipt["sha256"]


def test_resume_after_interrupted_restore_reproduces_the_backup_exactly(tmp_path):
    """After an interrupted restore, resuming from the intact backup reproduces its bytes exactly.

    The interruption is modelled the way the module's own failure path leaves the world: the target
    is gone (a crashed copy, or an integrity failure that unlinked the bad copy) while the backup is
    untouched. Resuming writes the bytes the backup holds -- equality is asserted on the raw bytes,
    not just on the digest -- and the reproduced checkpoint carries each row once, so the resume
    reconciles to the backup's state instead of layering a second application on top of it.
    """
    database = _seeded_database(tmp_path)
    receipt = recovery.backup_database(database, tmp_path / "backups")
    backup = Path(receipt["backup"])
    backup_digest = _sha256(backup)
    backup_bytes = backup.read_bytes()
    target = tmp_path / "restore" / "spine.db"

    completed = recovery.restore_database(backup, receipt["sha256"], target)
    assert completed["status"] == "RESTORE_READBACK_PASS"
    assert _sha256(target) == backup_digest

    # Interruption: the target does not survive, the backup does.
    target.unlink()
    assert not target.exists()
    assert backup.is_file(), "the interrupted restore damaged the backup"
    assert _sha256(backup) == backup_digest == receipt["sha256"]

    resumed = recovery.restore_database(backup, backup_digest, target)

    assert resumed["status"] == "RESTORE_READBACK_PASS"
    assert resumed["sha256"] == backup_digest
    assert target.read_bytes() == backup_bytes, "the resumed restore is not byte-identical to the backup"
    assert _sha256(target) == backup_digest

    connection = sqlite3.connect(target)
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    finally:
        connection.close()
    assert integrity == "ok"
    assert _rows(target) == PAYLOADS, "the resumed checkpoint re-applied rows instead of reproducing them"
    assert len(_rows(target)) == len(PAYLOADS)

    # Resuming did not consume or rewrite the backup either.
    assert _sha256(backup) == backup_digest
    assert backup.read_bytes() == backup_bytes
