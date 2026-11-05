"""HGK consumer ACK receipt — ``HGK_CONSUMER_RECEIPT@1``.

Why this module exists
----------------------
Fabric's policy binding has six independent legs; the sixth is ``consumer_ack`` with provenance
``HGK_CONSUMER_RECEIPT``. Before this module nothing in HG-KSEOS produced that artefact, so the leg
could only ever be satisfied by a caller-supplied fixture, and ``build_binding`` would still answer
``BOUND`` (design-level internal consistency, ``claim_ceiling=AUTHOR_DESIGN_ONLY``).

What it does NOT do
-------------------
* It does not decide that a policy is active. ``ack`` is supplied by the caller that actually
  consumed the policy; this module only packages and seals the observation.
* It does not fabricate a subject, scope or epoch: all three are required arguments and are echoed
  byte-for-byte into the receipt.
* It writes nothing by itself — ``write_receipt`` is an explicit call with an explicit path.

Digest rule
-----------
``raw_sha256`` covers the canonical JSON of the receipt **without** the ``raw_sha256`` field itself,
so a verifier can recompute it from the file. The file is written as UTF-8 with LF endings and a
single trailing newline (``AGENTS.md`` rule 3: evidence must be reproducible).
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any, Dict, Tuple

SCHEMA = "HGK_CONSUMER_RECEIPT@1"
ALLOWED_ACK = ("ACK", "SCOPE_SPECIFIC_DEFERRED", "NACK")
REQUIRED = ("schema", "subject", "scope", "policy_epoch", "consumer_id",
            "policy_digest", "loaded_digest", "observed_at", "ack")

ERR_SCHEMA = "HGK_RECEIPT_SCHEMA_MISMATCH"
ERR_REQUIRED = "HGK_RECEIPT_REQUIRED_FIELD_MISSING"
ERR_ACK = "HGK_RECEIPT_MISSING_ACK"
ERR_DIGEST = "HGK_RECEIPT_DIGEST_MISMATCH"
ERR_SCOPE_DEFERRAL = "HGK_RECEIPT_DEFERRAL_WITHOUT_SCOPE"


class ReceiptRejected(ValueError):
    """Raised by the producer for programmer errors (a reader returns codes instead)."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def canonical(obj: Dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def body_digest(body: Dict[str, Any]) -> str:
    """digest over the receipt body with ``raw_sha256`` removed."""
    stripped = {k: v for k, v in body.items() if k != "raw_sha256"}
    return hashlib.sha256(canonical(stripped)).hexdigest()


def build_receipt(*, subject: str, scope: str, policy_epoch: Any, consumer_id: str,
                  policy_digest: str, loaded_digest: str, ack: str,
                  observed_at: str | None = None, deferred_operations: list | None = None,
                  note: str = "") -> Dict[str, Any]:
    """Seal one observed consumption into a receipt.

    ``ack`` must be one of :data:`ALLOWED_ACK`; a ``SCOPE_SPECIFIC_DEFERRED`` ack must name the
    deferred operations, because a deferral without a scope is indistinguishable from a refusal.
    """
    for name, value in (("subject", subject), ("scope", scope), ("consumer_id", consumer_id),
                        ("policy_digest", policy_digest), ("loaded_digest", loaded_digest)):
        if not value or not str(value).strip():
            raise ReceiptRejected(ERR_REQUIRED, name)
    if ack not in ALLOWED_ACK:
        raise ReceiptRejected(ERR_ACK, str(ack))
    deferred = list(deferred_operations or [])
    if ack == "SCOPE_SPECIFIC_DEFERRED" and not deferred:
        raise ReceiptRejected(ERR_SCOPE_DEFERRAL, "deferred_operations is empty")

    body: Dict[str, Any] = {
        "schema": SCHEMA,
        "subject": subject,
        "scope": scope,
        "policy_epoch": policy_epoch,
        "consumer_id": consumer_id,
        "policy_digest": policy_digest,
        "loaded_digest": loaded_digest,
        "observed_at": observed_at or time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "ack": ack,
        "deferred_operations": deferred,
        "note": note,
    }
    body["raw_sha256"] = body_digest(body)
    return body


def verify_receipt(receipt: Dict[str, Any]) -> Tuple[bool, str | None]:
    """Return ``(ok, code)``; never raises on bad data."""
    if not isinstance(receipt, dict):
        return False, ERR_SCHEMA
    if receipt.get("schema") != SCHEMA:
        return False, ERR_SCHEMA
    missing = [k for k in REQUIRED if receipt.get(k) in (None, "")]
    if missing:
        return False, f"{ERR_REQUIRED}:{','.join(missing)}"
    if receipt.get("ack") not in ALLOWED_ACK:
        return False, ERR_ACK
    if receipt.get("ack") == "SCOPE_SPECIFIC_DEFERRED" and not receipt.get("deferred_operations"):
        return False, ERR_SCOPE_DEFERRAL
    if receipt.get("raw_sha256") != body_digest(receipt):
        return False, ERR_DIGEST
    return True, None


def write_receipt(path: str, receipt: Dict[str, Any]) -> str:
    """Write the receipt as UTF-8/LF with one trailing newline; return its sha256."""
    ok, code = verify_receipt(receipt)
    if not ok:
        raise ReceiptRejected(code or ERR_DIGEST, "refusing to write an invalid receipt")
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)
    payload = json.dumps(receipt, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    data = payload.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    return hashlib.sha256(data).hexdigest()


def load_receipt_file(path: str) -> Dict[str, Any]:
    with open(path, "rb") as fh:
        return json.loads(fh.read().decode("utf-8"))
