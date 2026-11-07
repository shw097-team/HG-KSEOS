"""WP-FHS-07 — Native PLAN Commander A / B / C and the PLAN revision CAS.

A = read-only guide view (no write, no queue touch).
B = an ISOLATED `PlanRevisionProposal` (a file outside any repo/queue).
C = the original PLAN writer's compare-and-swap: `expected_revision` must equal the current one.

The refusal this module exists for is the bootstrap inversion: a plan may be drafted without first
holding a WorkOrder Permit, so a caller that makes planning conditional on a Permit is refused with

    WP-FHS-07.FIRST_FAIL:COMMANDER_BOOTSTRAP_INVERSION

A stale CAS is `PLAN_CAS_STALE` (the caller re-reads the current revision; the store is never
force-overwritten), and a proposal from another WorkID is `CROSS_WORK_PLAN_AUTH_DENY`.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

SCHEMA = "HGK.PlanRevision@design"
PROPOSAL_SCHEMA = "HGK.PlanRevisionProposal@design"


class PlanRefusal(Exception):
    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code

    def as_dict(self) -> dict[str, Any]:
        return {"verdict": "REFUSED", "code": self.code, "message": str(self)}


def _sha(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


class PlanStore:
    """Append-only plan revision log: one JSONL per WorkID, revision = number of accepted rows.

    This is a FILE store for the candidate path only. It is deliberately not a database, not a
    scheduler and not a second queue: the production writer is the original HGK PLAN writer.
    """

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, work_id: str) -> Path:
        safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in work_id)
        return self.root / f"{safe}.revisions.jsonl"

    def revisions(self, work_id: str) -> list[dict[str, Any]]:
        p = self._path(work_id)
        if not p.exists():
            return []
        return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]

    def current_revision(self, work_id: str) -> int:
        rows = self.revisions(work_id)
        return int(rows[-1]["revision"]) if rows else 0

    def append(self, work_id: str, record: dict[str, Any]) -> None:
        p = self._path(work_id)
        with p.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def _proposal_digest(proposal: dict[str, Any]) -> str:
    """Digest over the proposal body; identity fields (digest, id) are excluded by construction."""
    return _sha({k: v for k, v in proposal.items() if k not in ("sha256", "proposal_id")})


# ------------------------------------------------------------------ A: read-only
def readonly_view(store: PlanStore, work_id: str) -> dict[str, Any]:
    """Commander A. Reads the current revision and returns a guide view; never writes."""
    rows = store.revisions(work_id)
    return {"role": "A", "work_id": work_id, "current_revision": len(rows) and rows[-1]["revision"] or 0,
            "revisions": [{"revision": r["revision"], "sha256": r["sha256"]} for r in rows],
            "writes": 0, "isolated": True, "claim_ceiling": "AUTHOR_DESIGN_ONLY"}


# ------------------------------------------------------------------ B: isolated proposal
def propose(*, store: PlanStore, work_id: str, base_revision: int, goal: str,
            specs: dict[str, str], body: dict[str, Any], require_permit: bool = False,
            permit: dict[str, Any] | None = None) -> dict[str, Any]:
    """Commander B. Produces an isolated proposal.

    `require_permit=True`, or presenting a permit as the *precondition* for planning, is the
    bootstrap inversion the W1 contract forbids.
    """
    if require_permit:
        raise PlanRefusal(
            "planning must not be gated on a WorkOrder Permit: "
            "WP-FHS-07.FIRST_FAIL:COMMANDER_BOOTSTRAP_INVERSION",
            code="WP-FHS-07.FIRST_FAIL:COMMANDER_BOOTSTRAP_INVERSION")
    if permit is not None and str(permit.get("gate") or "").upper() == "PLANNING":
        raise PlanRefusal(
            "a permit gating PLANNING is the bootstrap inversion: "
            "WP-FHS-07.FIRST_FAIL:COMMANDER_BOOTSTRAP_INVERSION",
            code="WP-FHS-07.FIRST_FAIL:COMMANDER_BOOTSTRAP_INVERSION")
    current = store.current_revision(work_id)
    if int(base_revision) != current:
        raise PlanRefusal(f"base_revision {base_revision} != current {current}: re-read Commander A "
                          "before proposing", code="PLAN_CAS_STALE")
    if not goal.strip():
        raise PlanRefusal("a proposal needs a goal", code="PLAN_PROPOSAL_EMPTY")

    proposal = {
        "schema": PROPOSAL_SCHEMA,
        "work_id": work_id,
        "base_revision": int(base_revision),
        "goal": goal,
        "specs": dict(specs),
        "body": body,
        "isolated": True,
        "touches_repo": False,
        "touches_queue": False,
        "created_by": "COMMANDER_B",
        "claim_ceiling": "AUTHOR_DESIGN_ONLY",
    }
    proposal["sha256"] = _proposal_digest(proposal)
    proposal["proposal_id"] = "PLAN-PROP-" + proposal["sha256"][:16]
    return proposal


# ------------------------------------------------------------------ C: CAS accept
CANDIDATE_REQUESTER = "LOCAL_CANDIDATE_REQUESTER"
# The original identities are *process* identities held by the original writer/reader. A string
# that merely spells one of them is a claim, not an identity; accepting it is how a maker-forged
# ACK gets minted (same defect class as Fabric #31). The literal is therefore never emitted here.
_SELF_CLAIMABLE_IDENTITIES = ("ORIGINAL_HGK_PLAN_WRITER", "ORIGINAL_HGK_PLAN_CAS_READER")


def commit(*, store: PlanStore, proposal: dict[str, Any], expected_revision: int,
           requester: str = CANDIDATE_REQUESTER, work_id: str | None = None,
           reader: Any | None = None) -> dict[str, Any]:
    """Commander C. Compare-and-swap against the store's current revision.

    The candidate store can append a revision, but it can only return ``ACK`` when a caller-supplied
    ``reader`` object produces a receipt that is *bound to this record's digest*. Without one, the
    verdict is ``CANDIDATE_APPENDED_NO_ORIGINAL_READER`` — a candidate append is not an acceptance,
    and no field of this function's output may claim the original reader's identity.
    """
    if str(requester).strip().upper() in _SELF_CLAIMABLE_IDENTITIES:
        raise PlanRefusal(
            f"{requester!r} is the original principal's identity spelled as a string: a caller cannot "
            "claim it, and minting an ACK from it is the forged-reader defect",
            code="PLAN_WRITER_SELF_CLAIM_DENY")
    target = str(work_id or proposal.get("work_id") or "")
    if work_id is not None and str(proposal.get("work_id")) != str(work_id):
        raise PlanRefusal(
            f"proposal belongs to {proposal.get('work_id')!r}, not {work_id!r}: a plan may not be "
            "committed under another WorkID", code="CROSS_WORK_PLAN_AUTH_DENY")
    work_id = target
    if _proposal_digest(proposal) != proposal.get("sha256"):
        raise PlanRefusal("proposal body does not match its digest (edited after proposal)",
                          code="PLAN_PROPOSAL_TAMPERED")
    current = store.current_revision(work_id)
    if int(expected_revision) != current:
        raise PlanRefusal(f"CAS stale: expected {expected_revision}, current {current}",
                          code="PLAN_CAS_STALE")
    if int(proposal["base_revision"]) != current:
        raise PlanRefusal(f"proposal was written against revision {proposal['base_revision']}, "
                          f"store is at {current}", code="PLAN_CAS_STALE")

    record = {
        "schema": SCHEMA,
        "work_id": work_id,
        "revision": current + 1,
        "base_revision": current,
        "proposal_id": proposal["proposal_id"],
        "sha256": proposal["sha256"],
        "requester": requester,
        "cas": {"expected_revision": int(expected_revision), "matched": True},
        "claim_ceiling": "AUTHOR_DESIGN_ONLY",
        "original_reader_ack": False,
        "note": "candidate revision in a file store; the original PLAN writer owns the real CAS",
    }
    record_sha = _sha(record)

    if reader is None:
        store.append(work_id, record)
        return {"verdict": "CANDIDATE_APPENDED_NO_ORIGINAL_READER", "role": "C",
                "work_id": work_id, "revision": record["revision"],
                "proposal_id": proposal["proposal_id"], "proposal_sha256": proposal["sha256"],
                "reader": None, "original_reader_receipt": "ABSENT",
                "claim_ceiling": "AUTHOR_DESIGN_ONLY", "appended": True,
                "receipt_sha256": record_sha}

    receipt = reader.verify(record)
    if not isinstance(receipt, dict):
        raise PlanRefusal("reader returned no receipt object", code="PLAN_READER_RECEIPT_UNBOUND")
    if str(receipt.get("record_sha256") or "") != record_sha:
        raise PlanRefusal(
            "the reader receipt is not bound to this record's digest: a receipt for another record "
            "cannot acknowledge this one", code="PLAN_READER_RECEIPT_UNBOUND")
    identity = str(receipt.get("reader_identity") or "").strip()
    if not identity:
        raise PlanRefusal("the reader receipt names no reader identity",
                          code="PLAN_READER_RECEIPT_UNBOUND")
    verdict = str(receipt.get("verdict") or "").upper()
    if verdict not in {"ACK", "NACK"}:
        raise PlanRefusal(f"reader verdict {verdict!r} is outside ACK/NACK",
                          code="PLAN_READER_RECEIPT_UNBOUND")
    if verdict == "NACK":
        return {"verdict": "NACK", "role": "C", "work_id": work_id,
                "revision": record["revision"], "proposal_id": proposal["proposal_id"],
                "proposal_sha256": proposal["sha256"], "reader": identity,
                "original_reader_receipt": receipt, "claim_ceiling": "AUTHOR_DESIGN_ONLY",
                "appended": False, "receipt_sha256": record_sha}

    record["original_reader_ack"] = True
    record["reader_receipt_sha256"] = _sha(receipt)
    store.append(work_id, record)
    return {"verdict": "ACK", "role": "C", "work_id": work_id, "revision": record["revision"],
            "proposal_id": proposal["proposal_id"], "proposal_sha256": proposal["sha256"],
            "reader": identity, "original_reader_receipt": receipt,
            "claim_ceiling": "AUTHOR_DESIGN_ONLY", "appended": True,
            "receipt_sha256": _sha(record)}


def rollback(*, store: PlanStore, work_id: str, to_revision: int) -> dict[str, Any]:
    """Discarding a proposal is a no-op; a real rollback needs the original writer's CAS."""
    if to_revision > store.current_revision(work_id):
        raise PlanRefusal("cannot roll forward to a revision that does not exist",
                          code="PLAN_CAS_STALE")
    return {"state": "DISCARD_ISOLATED_PROPOSAL_ONLY", "work_id": work_id,
            "at_revision": store.current_revision(work_id),
            "note": "the candidate store is append-only; production rollback is the original writer's"}
