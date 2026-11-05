"""WP-FHS-04 — Hermes durable runtime binding: WorkID, wake, queue item, lease, journal, checkpoint.

The contract's NEG list is precise: **no second SQLite queue**, **no PID held only in a chat/tool
call**, **no stale lease generation committing**. So this module never creates a queue. It binds to
the runtime the host already runs (Hermes: profile + Kanban + journal + checkpoint) and refuses:

* `ACTUAL_SERVED_NOT_OBSERVED` — a binding whose served profile/model was never written down;
* `SECOND_QUEUE_DENY` — a workspace that declares more than one queue root;
* `CROSS_PROFILE_SECRET_DENY` — a read reaching out of the bound profile;
* `RUNTIME_LEASE_BINDING_DENY` — a checkpoint committed by an older lease generation, or a
  non-monotonic journal cursor.

The journal and checkpoint files are plain append-only JSONL under the runtime root: they are the
*candidate* record of a real binding, never a second scheduler.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

SCHEMA = "HGK.WakeLeaseRuntimeBinding@design"
JOURNAL = "runtime-journal.jsonl"
CHECKPOINT = "runtime-checkpoint.json"
QUEUE_REGISTRY = "queue-roots.json"


class RuntimeRefusal(Exception):
    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code

    def as_dict(self) -> dict[str, Any]:
        return {"verdict": "REFUSED", "code": self.code, "message": str(self)}


def _sha(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def _sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ------------------------------------------------------------------ queue identity
def assert_single_queue(runtime_root: str | Path) -> dict[str, Any]:
    """One runtime root, one queue. A registry naming two live roots is refused, not merged."""
    root = Path(runtime_root)
    reg = root / QUEUE_REGISTRY
    if not reg.exists():
        return {"state": "SINGLE_QUEUE_ROOT", "roots": [str(root)], "registry": "ABSENT"}
    declared = json.loads(reg.read_text(encoding="utf-8"))
    roots = [str(r) for r in (declared.get("queue_roots") or [])]
    live = [r for r in roots if Path(r).exists()]
    if len({os.path.normcase(os.path.abspath(r)) for r in live}) > 1:
        raise RuntimeRefusal(
            "more than one live queue root is declared; this round may not create or merge a second "
            "queue: " + ", ".join(live), code="SECOND_QUEUE_DENY")
    return {"state": "SINGLE_QUEUE_ROOT", "roots": live or [str(root)], "registry": "PRESENT"}


# ------------------------------------------------------------------ binding
def bind(*, runtime_root: str | Path, work_id: str, profile: str, profile_sha: str,
         pid: int, actual_served: str, lease_generation: int,
         queue_item: str, wake_reason: str = "TURN_RESUME",
         native_reader: str = "hermes.kanban+journal") -> dict[str, Any]:
    """Bind one WorkID to one fresh process, one lease generation and one journal cursor."""
    root = Path(runtime_root)
    root.mkdir(parents=True, exist_ok=True)
    queue = assert_single_queue(root)
    if not str(actual_served).strip():
        raise RuntimeRefusal(
            "the profile that ACTUALLY served this turn was never recorded; a requested profile is "
            "not a served one", code="ACTUAL_SERVED_NOT_OBSERVED")
    if pid <= 0:
        raise RuntimeRefusal("a binding needs the fresh PID that serves it, not a stored one",
                             code="RUNTIME_LEASE_BINDING_DENY")
    journal = root / JOURNAL
    if not journal.exists():
        journal.write_text("", encoding="utf-8")
    cursor = len([l for l in journal.read_text(encoding="utf-8").splitlines() if l.strip()])
    ckpt = root / CHECKPOINT
    checkpoint_sha = _sha_file(ckpt) if ckpt.exists() else "ABSENT"
    record = {
        "schema": SCHEMA,
        "work_id": work_id,
        "profile": {"name": profile, "sha256": profile_sha},
        "actual_served": actual_served,
        "pid": int(pid),
        "lease_generation": int(lease_generation),
        "queue": {**queue, "item": queue_item},
        "journal": {"path": str(journal), "cursor": cursor},
        "checkpoint": {"path": str(ckpt), "sha256": checkpoint_sha},
        "wake": {"reason": wake_reason, "recoverable": cursor > 0},
        "native_reader": native_reader,
        "claim_ceiling": "AUTHOR_DESIGN_ONLY",
        "not_claimed": ["host install", "durable scheduler", "release"],
    }
    record["binding_sha256"] = _sha(record)
    return record


# ------------------------------------------------------------------ checkpoint / journal
def checkpoint(*, runtime_root: str | Path, work_id: str, lease_generation: int, state: str,
               checkpoint_seq: int, last_good: str) -> dict[str, Any]:
    """Append a checkpoint. A stale generation or a non-monotonic seq is refused."""
    root = Path(runtime_root)
    path = root / "runtime-checkpoints.jsonl"
    rows = ([json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
            if path.exists() else [])
    mine = [r for r in rows if r.get("work_id") == work_id]
    if mine:
        last = mine[-1]
        if int(checkpoint_seq) <= int(last["checkpoint_seq"]):
            raise RuntimeRefusal(
                f"checkpoint seq {checkpoint_seq} is not greater than the last ({last['checkpoint_seq']})",
                code="RUNTIME_LEASE_BINDING_DENY")
        if int(lease_generation) < int(last["lease_generation"]):
            raise RuntimeRefusal(
                f"lease generation {lease_generation} is older than {last['lease_generation']}; a "
                "stale worker may not commit", code="RUNTIME_LEASE_BINDING_DENY")
    rec = {"schema": "HGK.RuntimeCheckpoint@design", "work_id": work_id,
           "lease_generation": int(lease_generation), "checkpoint_seq": int(checkpoint_seq),
           "state": state, "last_good": last_good,
           "journal_cursor": len([l for l in (root / JOURNAL).read_text(encoding="utf-8").splitlines()
                                  if l.strip()]) if (root / JOURNAL).exists() else 0}
    rec["checkpoint_sha256"] = _sha(rec)
    root.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
    (root / CHECKPOINT).write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n",
                                   encoding="utf-8", newline="\n")
    return rec


def resume(*, runtime_root: str | Path, work_id: str, lease_generation: int) -> dict[str, Any]:
    """Resume from the last checkpoint; refuse when the caller's lease is older than the record."""
    root = Path(runtime_root)
    path = root / "runtime-checkpoints.jsonl"
    if not path.exists():
        raise RuntimeRefusal("no checkpoint to resume from", code="RUNTIME_LEASE_BINDING_DENY")
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    mine = [r for r in rows if r.get("work_id") == work_id]
    if not mine:
        raise RuntimeRefusal(f"no checkpoint for {work_id}", code="RUNTIME_LEASE_BINDING_DENY")
    last = mine[-1]
    if int(lease_generation) < int(last["lease_generation"]):
        raise RuntimeRefusal(
            f"resume lease {lease_generation} < recorded {last['lease_generation']}",
            code="RUNTIME_LEASE_BINDING_DENY")
    journal = root / JOURNAL
    cursor_now = len([l for l in journal.read_text(encoding="utf-8").splitlines() if l.strip()]) \
        if journal.exists() else 0
    return {"state": "RESUMABLE", "work_id": work_id, "from_checkpoint": last["checkpoint_sha256"],
            "last_good": last["last_good"], "checkpoint_seq": last["checkpoint_seq"],
            "journal_cursor_then": last["journal_cursor"], "journal_cursor_now": cursor_now,
            "replay_from": last["journal_cursor"], "replay_required": cursor_now > last["journal_cursor"],
            "claim_ceiling": "AUTHOR_DESIGN_ONLY"}


def journal_append(*, runtime_root: str | Path, work_id: str, kind: str, detail: dict[str, Any]) -> dict[str, Any]:
    """Append one journal event and return its cursor."""
    root = Path(runtime_root)
    root.mkdir(parents=True, exist_ok=True)
    path = root / JOURNAL
    if not path.exists():
        path.write_text("", encoding="utf-8")
    cursor = len([l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()])
    rec = {"schema": "HGK.RuntimeJournalEvent@design", "work_id": work_id, "kind": kind,
           "detail": detail, "cursor": cursor + 1}
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
    return rec


def assert_profile_scope(requested_path: str | Path, *, profile_root: str | Path) -> dict[str, Any]:
    """A read must stay inside the bound profile; crossing it is a secret-scope denial."""
    target = Path(requested_path).resolve()
    root = Path(profile_root).resolve()
    try:
        target.relative_to(root)
    except ValueError:
        raise RuntimeRefusal(
            f"{target} is outside the bound profile {root}: a cross-profile read is refused",
            code="CROSS_PROFILE_SECRET_DENY") from None
    return {"state": "IN_PROFILE", "path": str(target), "profile_root": str(root)}
