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
* An interrupted restore is modelled the way a killed copy really leaves the world: the target path
  is *occupied* by what the dead attempt produced -- a truncated file, or a directory wearing the
  target's name -- and the module reports it as ``ERR_RESTORE_TARGET_EXISTS`` instead of writing
  through it. That is a different situation from an absent target, and the resume test pins it.
* The module has no ``operation_id``, no readback after a timeout, and no UNKNOWN/PARTIAL
  reconciliation (KB ``SBL_HGK_FABRIC_PIPD_LS_PKG_R15_1...#1418``).
  ``test_resume_requires_operation_identity`` states that contract and is marked
  ``xfail(strict=True)``: it fails today, so the gap stays visible, and it turns XPASS -- and
  therefore a failing build -- the moment ``recovery`` grows the identity, so the rule cannot be
  quietly satisfied by a weaker reading later.

Each test builds its own SQLite database under pytest's ``tmp_path``; there is no network, no repo
fixture, and no write outside the pytest temp root.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import shutil
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

    The interruption is not "the target never existed". A copy that dies part-way leaves the target
    path *occupied* by its own debris, and this test produces both shapes of that debris: a file
    holding a strict prefix of the backup (a killed ``copy2``), and a directory sitting on the
    target name with a partial payload inside (a crashed extraction). In each case the module
    reports the occupied destination -- ``ERR_RESTORE_TARGET_EXISTS`` -- and leaves the debris
    byte-identical, so the resume cannot merge into it, append to it, or silently treat a
    half-written file as a checkpoint. Once the failed attempt's debris is cleared, the resume has
    to reproduce the backup: the load-bearing assertions are byte equality with the backup file,
    its digest, ``PRAGMA integrity_check``, and each row present exactly once -- not any message.
    """
    database = _seeded_database(tmp_path)
    receipt = recovery.backup_database(database, tmp_path / "backups")
    backup = Path(receipt["backup"])
    backup_digest = _sha256(backup)
    backup_bytes = backup.read_bytes()
    assert backup_digest == receipt["sha256"]

    # --- interruption 1: a copy killed mid-file leaves a truncated target behind ------------------
    target = tmp_path / "restore" / "spine.db"
    target.parent.mkdir(parents=True, exist_ok=True)
    interrupted_bytes = backup_bytes[: len(backup_bytes) // 2]
    assert 0 < len(interrupted_bytes) < len(backup_bytes), (
        "the interruption is not a truncated copy"
    )
    assert backup_bytes.startswith(interrupted_bytes), (
        "the interruption is not a prefix of the backup"
    )
    target.write_bytes(interrupted_bytes)

    with pytest.raises(InvariantViolation) as caught:
        recovery.restore_database(backup, backup_digest, target)
    assert str(caught.value).startswith("ERR_RESTORE_TARGET_EXISTS"), (
        "the product did not report the interrupted attempt's leftover; a resume that writes "
        "through it would be the repeated world effect this test exists to catch"
    )
    assert target.read_bytes() == interrupted_bytes, (
        "the refused resume wrote through the interrupted copy"
    )
    assert _sha256(target) != backup_digest, (
        "the interrupted target already looks like a finished restore"
    )

    # The dead attempt's artifact is cleared; the resume now has to reproduce the checkpoint.
    target.unlink()
    assert not target.exists()
    assert backup.is_file(), "the interrupted restore damaged the backup"
    assert _sha256(backup) == backup_digest

    resumed = recovery.restore_database(backup, backup_digest, target)

    assert resumed["status"] == "RESTORE_READBACK_PASS"
    assert resumed["sha256"] == backup_digest
    assert target.read_bytes() == backup_bytes, (
        "the resumed restore is not byte-identical to the backup"
    )
    assert _sha256(target) == backup_digest

    connection = sqlite3.connect(target)
    try:
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    finally:
        connection.close()
    assert integrity == "ok"
    assert _rows(target) == PAYLOADS, (
        "the resumed checkpoint re-applied rows instead of reproducing them"
    )
    assert len(_rows(target)) == len(PAYLOADS)

    # --- interruption 2: the crashed attempt left a directory on the target name ------------------
    blocked = tmp_path / "restore-dir" / "spine.db"
    blocked.mkdir(parents=True)
    leftover = blocked / "partial.tmp"
    leftover_bytes = backup_bytes[: 1024]
    leftover.write_bytes(leftover_bytes)

    with pytest.raises(InvariantViolation) as caught:
        recovery.restore_database(backup, backup_digest, blocked)
    assert str(caught.value).startswith("ERR_RESTORE_TARGET_EXISTS")
    assert blocked.is_dir(), "the refused resume replaced the interrupted target"
    assert leftover.read_bytes() == leftover_bytes, (
        "the refused resume wrote into the interrupted target"
    )

    shutil.rmtree(blocked)
    resumed_dir_target = recovery.restore_database(backup, backup_digest, blocked)
    assert resumed_dir_target["status"] == "RESTORE_READBACK_PASS"
    assert blocked.is_file()
    assert blocked.read_bytes() == backup_bytes, (
        "the resumed restore is not byte-identical to the backup"
    )
    assert _sha256(blocked) == backup_digest
    assert _rows(blocked) == PAYLOADS

    # Resuming did not consume or rewrite the backup either.
    assert _sha256(backup) == backup_digest
    assert backup.read_bytes() == backup_bytes


@pytest.mark.xfail(
    strict=True,
    reason="R15_1#1418 operation_id / readback reconciliation absent",
)
def test_resume_requires_operation_identity(tmp_path):
    """A resume has to be addressed by the ``operation_id`` of the attempt it continues.

    Citation: KB ``SBL_HGK_FABRIC_PIPD_LS_PKG_R15_1...#1418`` -- an effect that timed out or lost
    its transport must not be blindly re-sent; ``operation_id`` is the unique idempotency key and a
    Native state readback comes first. ``CONFIRMED_EFFECT`` continues with verification only,
    ``CONFIRMED_NO_EFFECT`` re-requests under the owner's policy, and ``UNKNOWN_EFFECT`` /
    ``PARTIAL_EFFECT`` pause the affected operation into reconciliation/compensation.

    ``hg_kseos.recovery`` currently has none of that: ``restore_database`` takes no ``operation_id``
    and its receipts carry no identity, so a caller cannot say which attempt a resume belongs to,
    cannot read the target back to classify a timed-out restore, and therefore cannot tell a
    confirmed effect from an unknown one. This test states the contract so the gap is a named
    failure rather than an unwritten expectation; it is ``xfail(strict=True)`` because the product
    rule is absent, and it will XPASS -- failing loudly -- as soon as the rule arrives, at which
    point the marker must be removed deliberately.
    """
    database = _seeded_database(tmp_path)
    receipt = recovery.backup_database(database, tmp_path / "backups")
    assert "operation_id" in receipt, (
        "a checkpoint that can be resumed is not addressed by an operation_id"
    )
    backup = Path(receipt["backup"])
    target = tmp_path / "restore" / "spine.db"
    operation_id = "op-resume-0001"

    parameters = inspect.signature(recovery.restore_database).parameters
    assert "operation_id" in parameters, (
        "restore_database cannot be told which operation it resumes, so a timed-out restore can "
        "only be classified by guessing; #1418 requires the operation_id and a readback first"
    )

    first = recovery.restore_database(
        backup, receipt["sha256"], target, operation_id=operation_id
    )
    assert first.get("operation_id") == operation_id, (
        "the restore receipt does not record the operation it served"
    )

    # A readback under the same operation continues a CONFIRMED_EFFECT; it must not become a
    # second application of it.
    readback = recovery.restore_database(
        backup, receipt["sha256"], target, operation_id=operation_id
    )
    assert readback["status"] == "RESTORE_READBACK_PASS"
    assert readback.get("operation_id") == operation_id
    assert readback["sha256"] == receipt["sha256"]
    assert _sha256(target) == receipt["sha256"]
    assert _rows(target) == PAYLOADS

    # A different operation against a target another operation already owns is UNKNOWN/PARTIAL
    # reconciliation territory, not a silent overwrite.
    with pytest.raises(InvariantViolation) as caught:
        recovery.restore_database(
            backup, receipt["sha256"], target, operation_id="op-resume-0002"
        )
    assert str(caught.value).startswith(
        ("ERR_RESUME_OPERATION_MISMATCH", "ERR_RESTORE_TARGET_EXISTS")
    )
    assert _rows(target) == PAYLOADS
