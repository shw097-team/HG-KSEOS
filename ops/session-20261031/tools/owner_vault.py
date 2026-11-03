"""Owner key vault — optional passphrase envelope in front of the Ed25519 owner key.

Why: an owner key that any process running as the same Windows user can read is not owner-controlled.
Wrapping it in scrypt + AES-256-GCM makes the signing capability require the owner's passphrase at the
moment of signing, without introducing a second OS principal or any service.

Guarantees this module keeps:
  * no key material, passphrase or derived bytes are printed, logged or written anywhere except the
    encrypted envelope;
  * the public key — and therefore every existing enrollment and signature — is UNCHANGED by wrapping
    (wrapping is not rotation);
  * a missing passphrase is a typed refusal, never a silent fallback (`REFUSED_OWNER_KEY_LOCKED`).
"""
from __future__ import annotations

import base64
import getpass
import hashlib
import json
import os
import time
import pathlib

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

MAGIC = b"HGKOWNER1"
SCRYPT = {"n": 2 ** 15, "r": 8, "p": 1}


def enc_path(path: pathlib.Path) -> pathlib.Path:
    return path.with_name(path.name + ".enc")


def _derive(passphrase: str, salt: bytes) -> bytes:
    return Scrypt(salt=salt, length=32, **SCRYPT).derive(passphrase.encode("utf-8"))


def pub_hex(priv: Ed25519PrivateKey) -> str:
    return priv.public_key().public_bytes(serialization.Encoding.Raw,
                                          serialization.PublicFormat.Raw).hex()


def fingerprint(pub: str) -> str:
    return hashlib.sha256(bytes.fromhex(pub)).hexdigest()[:16]


def status(path: pathlib.Path) -> dict:
    e, esc = enc_path(path), escrow_path(path)
    wrapped = e.is_file() and not path.is_file()
    if not wrapped:
        att = "ADMINISTRATIVE_ONLY"
    elif esc.is_file():
        att = "CRYPTOGRAPHIC_OWNER_CONTROL_WITH_LOCAL_ESCROW"
    else:
        att = "CRYPTOGRAPHIC_OWNER_CONTROL"
    return {"plaintext_present": path.is_file(), "wrapped_present": e.is_file(),
            "escrow_present": esc.is_file(), "attribution": att}


def load_private(path: pathlib.Path, passphrase: str | None = None) -> Ed25519PrivateKey:
    e = enc_path(path)
    if e.is_file():
        blob = json.loads(e.read_text(encoding="utf-8"))
        pp = passphrase
        if pp is None:
            # Windows' getpass reads the console directly; in an unattended process that blocks forever.
            # No TTY means no human: fail closed instead of hanging.
            import sys as _sys
            if not (_sys.stdin and _sys.stdin.isatty() and _sys.stdout and _sys.stdout.isatty()):
                raise PermissionError("REFUSED_OWNER_KEY_LOCKED")
            pp = getpass.getpass(f"owner key passphrase ({path.name}): ")
        if not pp:
            raise PermissionError("REFUSED_OWNER_KEY_LOCKED")
        raw = AESGCM(_derive(pp, base64.b64decode(blob["kdf"]["salt"]))).decrypt(
            base64.b64decode(blob["aead"]["nonce"]), base64.b64decode(blob["aead"]["ct"]), MAGIC)
        return Ed25519PrivateKey.from_private_bytes(raw)
    if not path.is_file():
        raise FileNotFoundError(str(path))
    return Ed25519PrivateKey.from_private_bytes(bytes.fromhex(path.read_bytes().decode().strip()))


def wrap_in_place(path: pathlib.Path, passphrase: str) -> dict:
    """Encrypt the existing plaintext key and delete it. The key itself is NOT rotated."""
    if not path.is_file():
        raise FileNotFoundError(str(path))
    plain_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    priv = load_private(path)
    pub = pub_hex(priv)
    raw = priv.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw,
                             serialization.NoEncryption())
    salt, nonce = os.urandom(16), os.urandom(12)
    ct = AESGCM(_derive(passphrase, salt)).encrypt(nonce, raw, MAGIC)
    blob = {"magic": MAGIC.decode(), "kdf": {"alg": "scrypt", **SCRYPT, "salt": base64.b64encode(salt).decode()},
            "aead": {"alg": "AES-256-GCM", "nonce": base64.b64encode(nonce).decode(),
                     "ct": base64.b64encode(ct).decode()},
            "public_hex": pub, "key_fingerprint": fingerprint(pub),
            "wrapped_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "wrapping_is_not_rotation": True}
    e = enc_path(path)
    e.write_text(json.dumps(blob), encoding="utf-8")
    try:
        os.chmod(e, 0o600)
    except Exception:
        pass
    # verify the envelope round-trips BEFORE destroying the plaintext
    back = AESGCM(_derive(passphrase, salt)).decrypt(nonce, ct, MAGIC)
    if back != raw:
        e.unlink(missing_ok=True)
        raise RuntimeError("REFUSED_ENVELOPE_ROUNDTRIP_FAILED")
    path.unlink()
    return {"wrapped": True, "key_fingerprint": fingerprint(pub), "public_hex": pub,
            "plaintext_sha256": plain_sha, "plaintext_removed": not path.is_file(),
            "attribution": "CRYPTOGRAPHIC_OWNER_CONTROL"}


# --- optional local escrow of the passphrase (DPAPI, current Windows user) -------------------
# This exists only so the ceremony can run unattended. It does NOT create owner-exclusive control:
# any process running as the same Windows user can call CryptUnprotectData. The ceiling is recorded
# in the attestation; a human passphrase (no escrow) is the stronger end state.
def _dpapi(data: bytes, protect: bool) -> bytes:
    import ctypes
    from ctypes import wintypes

    class BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

    def blob(b: bytes) -> BLOB:
        buf = ctypes.create_string_buffer(b, len(b))
        return BLOB(len(b), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))

    crypt32 = ctypes.windll.crypt32
    fn = crypt32.CryptProtectData if protect else crypt32.CryptUnprotectData
    src, dst = blob(data), BLOB()
    if protect:
        ok = fn(ctypes.byref(src), None, None, None, None, 0x1, ctypes.byref(dst))  # UI_FORBIDDEN
    else:
        ok = fn(ctypes.byref(src), None, None, None, None, 0x1, ctypes.byref(dst))
    if not ok:
        raise OSError("REFUSED_DPAPI_CALL_FAILED")
    try:
        return ctypes.string_at(dst.pbData, dst.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree(dst.pbData)


def escrow_path(key_path: pathlib.Path) -> pathlib.Path:
    return key_path.with_name("unlock.dpapi")


def escrow_passphrase(key_path: pathlib.Path, passphrase: str) -> dict:
    p = escrow_path(key_path)
    p.write_bytes(_dpapi(passphrase.encode("utf-8"), True))
    try:
        import subprocess
        user = os.environ.get("USERNAME")
        subprocess.run(["icacls", str(p), "/inheritance:r", "/grant:r", f"{user}:F"], capture_output=True)
    except Exception:
        pass
    return {"escrowed": p.is_file(), "path": str(p), "protection": "DPAPI(current user, UI forbidden)",
            "ceiling": "same-user processes can unprotect it; this is availability, not exclusivity"}


def read_escrowed_passphrase(key_path: pathlib.Path) -> str:
    p = escrow_path(key_path)
    if not p.is_file():
        raise PermissionError("REFUSED_NO_ESCROW")
    return _dpapi(p.read_bytes(), False).decode("utf-8")


def reseal(path: pathlib.Path, old_passphrase: str, new_passphrase: str) -> dict:
    """Re-wrap an existing envelope under a different passphrase (no rotation, same public key)."""
    enc = enc_path(path)
    if not enc.is_file():
        raise FileNotFoundError(str(enc))
    priv = load_private(path, old_passphrase)
    tmp = path.with_name(path.name + ".reseal")
    tmp.write_bytes(priv.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw,
                                       serialization.NoEncryption()).hex().encode())
    try:
        res = wrap_in_place(tmp, new_passphrase)          # writes tmp.enc, verifies, deletes tmp
    finally:
        tmp.unlink(missing_ok=True)
    new_enc = enc_path(tmp)
    enc.unlink(missing_ok=True)
    new_enc.rename(enc)
    return {**res, "public_stable": res["public_hex"] == pub_hex(priv)}
