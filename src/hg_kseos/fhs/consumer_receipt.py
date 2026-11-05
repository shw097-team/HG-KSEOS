"""HGK consumer ACK receipt — ``HGK_CONSUMER_RECEIPT@1``.

Why this module exists
----------------------
Fabric's policy binding has six independent legs; the sixth is ``consumer_ack`` with provenance
``HGK_CONSUMER_RECEIPT``. Before this module nothing in HG-KSEOS produced that artefact, so the leg
could only ever be satisfied by a caller-supplied fixture.

Contract (must match the Fabric reader ``FABRIC/fabric/consumers/hgk_consumer_receipt.py``)
-------------------------------------------------------------------------------------------
* ``raw_path``   — the bytes this acknowledgement is about, **relative to the receipt file**. The
  reader resolves it against the receipt's own directory and re-hashes those bytes.
* ``raw_sha256`` — sha256 of those bytes. Not a digest of this receipt: the leg's digest has to
  identify the acknowledged policy bytes, exactly like the other five legs.
* ``receipt_sha256`` — envelope integrity over the receipt body excluding this field, so a receipt
  whose subject/scope/epoch was edited in place is detectable on its own.

What it does NOT do
-------------------
* It does not decide that a policy is active. ``ack`` is supplied by the caller that consumed it.
* It does not invent subject/scope/epoch; all three are required and echoed byte-for-byte.
* It writes nothing unless :func:`write_receipt` is called with an explicit path.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from typing import Any, Dict, Tuple

SCHEMA = "HGK_CONSUMER_RECEIPT@1"
ALLOWED_ACK = ("ACK", "SCOPE_SPECIFIC_DEFERRED", "NACK")
REQUIRED = ("schema", "subject", "scope", "policy_epoch", "consumer_id", "ack",
            "raw_path", "raw_sha256")

ERR_SCHEMA = "HGK_RECEIPT_SCHEMA_MISMATCH"
ERR_REQUIRED = "HGK_RECEIPT_REQUIRED_FIELD_MISSING"
ERR_ACK = "HGK_RECEIPT_MISSING_ACK"
ERR_DIGEST = "HGK_RECEIPT_DIGEST_MISMATCH"
ERR_ENVELOPE = "HGK_RECEIPT_ENVELOPE_MISMATCH"
ERR_RAW_UNREADABLE = "HGK_RECEIPT_RAW_UNREADABLE"
ERR_SCOPE_DEFERRAL = "HGK_RECEIPT_DEFERRAL_WITHOUT_SCOPE"


class ReceiptRejected(ValueError):
    """Producer-side refusal (a reader returns codes instead of raising)."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


def canonical(obj: Dict[str, Any]) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def envelope_digest(body: Dict[str, Any]) -> str:
    stripped = {k: v for k, v in body.items() if k != "receipt_sha256"}
    return sha256_bytes(canonical(stripped))


def build_receipt(*, subject: str, scope: str, policy_epoch: Any, consumer_id: str,
                  ack: str, raw_bytes: bytes | None = None, raw_path: str | None = None,
                  policy_digest: str = "", loaded_digest: str = "",
                  observed_at: str | None = None, deferred_operations: list | None = None,
                  note: str = "") -> Dict[str, Any]:
    """Seal one observed consumption into a receipt.

    ``raw_bytes`` is authoritative: when given, ``raw_sha256`` is computed from it. ``raw_path``
    names where those bytes live, relative to the receipt file that :func:`write_receipt` writes.
    """
    for name, value in (("subject", subject), ("scope", scope), ("consumer_id", consumer_id),
                        ("raw_path", raw_path)):
        if not value or not str(value).strip():
            raise ReceiptRejected(ERR_REQUIRED, name)
    if ack not in ALLOWED_ACK:
        raise ReceiptRejected(ERR_ACK, str(ack))
    deferred = list(deferred_operations or [])
    if ack == "SCOPE_SPECIFIC_DEFERRED" and not deferred:
        raise ReceiptRejected(ERR_SCOPE_DEFERRAL, "deferred_operations is empty")
    if raw_bytes is None:
        raise ReceiptRejected(ERR_RAW_UNREADABLE, "raw_bytes are required to seal an acknowledgement")

    body: Dict[str, Any] = {
        "schema": SCHEMA,
        "subject": subject,
        "scope": scope,
        "policy_epoch": policy_epoch,
        "consumer_id": consumer_id,
        "policy_digest": policy_digest,
        "loaded_digest": loaded_digest,
        "raw_path": raw_path,
        "raw_sha256": sha256_bytes(raw_bytes),
        "observed_at": observed_at or time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "ack": ack,
        "deferred_operations": deferred,
        "note": note,
    }
    body["receipt_sha256"] = envelope_digest(body)
    return body


def verify_receipt(receipt: Dict[str, Any], *, base_dir: str | None = None) -> Tuple[bool, str | None]:
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
    if "receipt_sha256" in receipt and receipt["receipt_sha256"] != envelope_digest(receipt):
        return False, ERR_ENVELOPE
    raw_path = receipt.get("raw_path")
    if not raw_path:
        return False, ERR_REQUIRED + ":raw_path"
    candidate = raw_path if os.path.isabs(str(raw_path)) else os.path.join(base_dir or ".", str(raw_path))
    try:
        with open(candidate, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        return False, f"{ERR_RAW_UNREADABLE}:{exc.strerror or exc}"
    if sha256_bytes(raw) != receipt.get("raw_sha256"):
        return False, ERR_DIGEST
    return True, None


def write_receipt(path: str, receipt: Dict[str, Any], *, raw_bytes: bytes | None = None) -> str:
    """Write ``raw_bytes`` at ``base/raw_path`` and the receipt at ``path``; return receipt sha256.

    The receipt is UTF-8/LF with a single trailing newline (AGENTS.md: evidence must be
    reproducible). Raw bytes are written first so a reader can always resolve them.
    """
    base = os.path.dirname(os.path.abspath(path))
    raw_path = receipt.get("raw_path")
    if not raw_path:
        raise ReceiptRejected(ERR_REQUIRED, "raw_path")
    target = raw_path if os.path.isabs(str(raw_path)) else os.path.join(base, str(raw_path))
    if raw_bytes is not None:
        os.makedirs(os.path.dirname(os.path.abspath(target)) or base, exist_ok=True)
        with open(target, "wb") as fh:
            fh.write(raw_bytes)
    ok, code = verify_receipt(receipt, base_dir=base)
    if not ok:
        raise ReceiptRejected(code or ERR_DIGEST, "refusing to write an invalid receipt")
    os.makedirs(base, exist_ok=True)
    payload = json.dumps(receipt, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    data = payload.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    return sha256_bytes(data)


def load_receipt_file(path: str) -> Dict[str, Any]:
    with open(path, "rb") as fh:
        return json.loads(fh.read().decode("utf-8"))
