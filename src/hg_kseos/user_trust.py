"""User-scoped native trust profile (B1 r10 §0/§2B).

The r5 candidate bound every trust operation to `Administrator + LocalMachine/My + machine CNG key +
ProgramData ACL`. That was an implementation choice, not a DOC-00..08 obligation: a normal coding
factory WorkOrder does not need machine-wide OS authority. This module adds the minimal, versioned,
NON-admin alternative the OWNER authorised:

  * trust root lives under %LOCALAPPDATA%\\HG-KSEOS\\native-admission (user profile, not a repo file)
  * the signer key is Ed25519, stored DPAPI-protected (CurrentUser scope) - never in the registry,
    never in a repo, never in an env var
  * the registry keeps only the PUBLIC key plus the principal separation fields the receiver checks

Honest ceiling: `USER_SCOPED_SOFTWARE_KEY`. The key is protected from other users and from disk
theft, but a process running as the SAME user can ask DPAPI to unprotect it. That is why
`assurance_level` is recorded and why the high-assurance gates stay HOLD: this profile proves the
issue/verify/revoke chain and key isolation-by-storage, not maker/checker OS-principal separation.
"""
from __future__ import annotations

import base64
import ctypes
import json
import os
import uuid
from ctypes import wintypes
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

ASSURANCE = "USER_SCOPED_SOFTWARE_KEY"
SCHEMA = "HGK-USER-TRUST-REGISTRY/1"


class TrustRefusal(Exception):
    """Typed refusal - never a silent False."""


def _home() -> Path:
    base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    return Path(base) / "HG-KSEOS" / "native-admission"


def paths() -> dict[str, Path]:
    h = _home()
    return {"root": h, "registry": h / "registry.json", "key": h / "user-signer.key.dpapi"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ----------------------------------------------------------------- DPAPI (no third-party dependency)
class _Blob(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]


def _dpapi(data: bytes, protect: bool) -> bytes:
    buf_in = _Blob(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_char)))
    buf_out = _Blob()
    fn = ctypes.windll.crypt32.CryptProtectData if protect else ctypes.windll.crypt32.CryptUnprotectData
    if not fn(ctypes.byref(buf_in), None, None, None, None, 0, ctypes.byref(buf_out)):
        raise TrustRefusal("ERR_DPAPI_" + ("PROTECT" if protect else "UNPROTECT"))
    try:
        return ctypes.string_at(buf_out.pbData, buf_out.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree(buf_out.pbData)


# ----------------------------------------------------------------- registry
def _read() -> dict:
    p = paths()["registry"]
    if not p.exists():
        raise TrustRefusal("ERR_USER_REGISTRY_ABSENT")
    return json.loads(p.read_text(encoding="utf-8"))


def _write(data: dict) -> None:
    p = paths()
    p["root"].mkdir(parents=True, exist_ok=True)
    tmp = p["registry"].with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, p["registry"])


def enroll(owner_sid: str, checker_sid: str, maker_sid: str, *, policy_epoch: int = 34) -> dict:
    """Create the user-scoped root. Refuses to collapse the three principals into one SID."""
    if not (owner_sid and checker_sid and maker_sid):
        raise TrustRefusal("ERR_PRINCIPAL_MISSING")
    if len({owner_sid.casefold(), checker_sid.casefold(), maker_sid.casefold()}) != 3:
        raise TrustRefusal("ERR_PRINCIPAL_SEPARATION")
    p = paths()
    p["root"].mkdir(parents=True, exist_ok=True)
    priv = Ed25519PrivateKey.generate()
    pem = priv.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                             serialization.NoEncryption())
    p["key"].write_bytes(_dpapi(pem, True))
    pub = priv.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    reg = {"schema": SCHEMA, "status": "ACTIVE", "assurance_level": ASSURANCE,
           "key_id": "USR-" + uuid.uuid4().hex[:12], "algorithm": "Ed25519",
           "public_key": base64.b64encode(pub).decode("ascii"),
           "owner_os_sid": owner_sid, "checker_os_sid": checker_sid, "maker_os_sid": maker_sid,
           "policy_epoch": policy_epoch, "created_at": now(), "revoked_at": None,
           "private_key_location": "DPAPI(CurrentUser) outside any repo"}
    _write(reg)
    return reg


def _private_key() -> Ed25519PrivateKey:
    p = paths()["key"]
    if not p.exists():
        raise TrustRefusal("ERR_USER_KEY_ABSENT")
    pem = _dpapi(p.read_bytes(), False)
    return serialization.load_pem_private_key(pem, password=None)


def canonical(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign(payload: dict, *, ttl_seconds: int = 300) -> dict:
    reg = _read()
    if reg.get("status") != "ACTIVE":
        raise TrustRefusal("ERR_REGISTRY_NOT_ACTIVE")
    body = dict(payload)
    body["issued_at"] = now()
    body["expires_at"] = (datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds)).isoformat()
    body["nonce"] = uuid.uuid4().hex
    sig = _private_key().sign(canonical(body))
    return {"key_id": reg["key_id"], "payload": body,
            "signature": base64.b64encode(sig).decode("ascii")}


def verify(reference: dict) -> dict:
    reg = _read()
    if reg.get("status") != "ACTIVE":
        raise TrustRefusal("ERR_REGISTRY_NOT_ACTIVE")
    for field in ("key_id", "payload", "signature"):
        if field not in reference:
            raise TrustRefusal("ERR_REFERENCE_SHAPE")
    if reference["key_id"] != reg["key_id"]:
        raise TrustRefusal("ERR_UNKNOWN_KEY_ID")
    payload = reference["payload"]
    exp = payload.get("expires_at")
    if not exp or datetime.fromisoformat(exp) <= datetime.now(timezone.utc):
        raise TrustRefusal("ERR_TTL_EXPIRED")
    try:
        pub = Ed25519PublicKey.from_public_bytes(base64.b64decode(reg["public_key"]))
        pub.verify(base64.b64decode(reference["signature"]), canonical(payload))
    except Exception as e:  # noqa: BLE001
        raise TrustRefusal(f"ERR_SIGNATURE_INVALID:{type(e).__name__}") from e
    return {"verified": True, "key_id": reg["key_id"], "assurance_level": reg["assurance_level"],
            "owner_os_sid": reg["owner_os_sid"], "checker_os_sid": reg["checker_os_sid"],
            "policy_epoch": reg["policy_epoch"], "payload_sha256": base64.b16encode(
                __import__("hashlib").sha256(canonical(payload)).digest()).decode().lower()}


def revoke(reason: str = "owner_revoked") -> dict:
    reg = _read()
    reg["status"] = "REVOKED"
    reg["revoked_at"] = now()
    reg["revoke_reason"] = reason
    _write(reg)
    return {"revoked": True, "key_id": reg["key_id"], "revoked_at": reg["revoked_at"], "reason": reason}


def private_key_is_not_in_registry() -> bool:
    """The registry must never carry private material."""
    raw = paths()["registry"].read_text(encoding="utf-8")
    # the registry legitimately describes WHERE the key lives ("private_key_location"); what it must
    # never carry is key material itself.
    return "PRIVATE KEY" not in raw and '"private_key":' not in raw and "BEGIN OPENSSH" not in raw
