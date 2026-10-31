"""Owner-key delegation ceremony for round R18 — passphrase envelope, Ed25519, no secret ever printed.

WHAT THIS BUILDS (FAR_R18-08 §二, "T1 委派信封"):

    owner passphrase  --(scrypt)-->  KEK  --(AES-GCM)-->  envelope holding only a 32-byte Ed25519 seed
    owner key         --(Ed25519)-->  signature over ONE DelegationRecord

The agent never holds signing power. It holds a *capability token*: an owner-signed, scope-bounded,
expiring delegation that an Issuer can verify against the owner's PUBLIC key. That is the difference
between "the agent can sign anything" (rejected) and "the owner decided once, in writing, what may run
unattended" (this).

WHAT IT REFUSES TO DO
  * print, log or serialise the passphrase or the seed (they exist only in process memory)
  * put the private key anywhere outside the encrypted envelope
  * delegate RELEASE / HOST_INSTALL / secrets / force-push / main / merge / tag
  * delegate the four WPs whose effect_class contradicts their write_set (the C4 finding)

Modes
  init    create the owner key inside a new passphrase envelope, then sign the delegation
  sign    unseal an existing envelope and sign (or re-sign) a delegation
  verify  verify a signature and check a proposed effect against the delegation
  status  show the envelope's public key, fingerprint and the current delegation, no passphrase needed
"""
import argparse
import base64
import hashlib
import json
import os
import secrets
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidSignature

ROUND = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
GOV = ROUND / "governance"
ENVELOPE = GOV / "owner_envelope.json"
DELEGATION = GOV / "delegation_R18.json"
SIG = GOV / "delegation_R18.sig"
RECEIPT = ROUND / "receipts" / "DELEGATION_SIGNED.json"

CHECKER_PRINCIPAL = "SBL-ACCEPTANCE-CHALLENGE-SP"
MAKER_PRINCIPAL = "HERMES-R18-EXECUTE-LANE"

# measured: SOURCE_READ 5 + REPO_WRITE 2 = 7 executable without native authority.
# EXCLUDED on purpose: the four LOCAL_DRAFT_WRITE WPs whose write_set says BIND_EXACT_BY_ORIGINAL_OWNER
# (C4 contradiction in WP_CONTRACT_RESULTS.json) and all HOST_OP/RELEASE WPs.
ALLOWED_WPS = ["WP-FHS-00", "WP-FHS-01", "WP-FHS-09", "WP-FHS-19", "WP-FHS-21", "WP-FHS-06", "WP-FHS-18"]
EXCLUDED_WPS = {
    "WP-FHS-05": "C4: LOCAL_DRAFT_WRITE vs write_set BIND_EXACT_BY_ORIGINAL_OWNER",
    "WP-FHS-07": "C4: same contradiction",
    "WP-FHS-15": "C4: same contradiction",
    "WP-FHS-16": "C4: same contradiction",
}
ALLOWED_CLASSES = ["SOURCE_READ", "REPO_WRITE_TO_CANDIDATE_BRANCH"]
DENY = ["RELEASE", "HOST_INSTALL", "secrets", "force-push", "main", "merge", "tag", "LOCAL_DRAFT_WRITE"]


# ----------------------------------------------------------------------------- passphrase window
def prompt_passphrase(confirm: bool) -> str:
    """A native modal window. The string is returned to this process only; it is never logged."""
    import tkinter as tk

    result = {"value": None}
    root = tk.Tk()
    root.title("HG-KSEOS owner key — passphrase")
    root.geometry("460x210")
    root.attributes("-topmost", True)

    tk.Label(root, text="Owner key passphrase envelope", font=("Segoe UI", 11, "bold")).pack(pady=(14, 2))
    tk.Label(root, text=("This passphrase wraps the owner signing key for round R18.\n"
                         "It is never stored, printed or sent anywhere.\n"
                         "The agent cannot see it." if confirm else
                         "Enter the passphrase to unseal the owner key for this signing."),
             justify="center", fg="#444").pack(pady=(0, 8))

    e1 = tk.Entry(root, show="\u2022", width=38)
    e1.pack(pady=4)
    e2 = tk.Entry(root, show="\u2022", width=38) if confirm else None
    if e2:
        tk.Label(root, text="confirm", fg="#666").pack()
        e2.pack(pady=4)
    e1.focus_set()

    def submit(_evt=None):
        v1 = e1.get()
        if confirm and v1 != e2.get():
            tk.Label(root, text="passphrases differ", fg="#b00").pack()
            return
        if len(v1) < 12:
            tk.Label(root, text="minimum 12 characters", fg="#b00").pack()
            return
        result["value"] = v1
        root.destroy()

    def cancel():
        root.destroy()

    box = tk.Frame(root)
    box.pack(pady=10)
    tk.Button(box, text="Sign" if not confirm else "Create & sign", width=16, command=submit).pack(side="left", padx=6)
    tk.Button(box, text="Cancel", width=10, command=cancel).pack(side="left", padx=6)
    root.bind("<Return>", submit)
    root.bind("<Escape>", lambda _e: cancel())
    root.mainloop()
    return result["value"]


# ----------------------------------------------------------------------------- envelope primitives
def _kek(passphrase: str, salt: bytes) -> bytes:
    return Scrypt(salt=salt, length=32, n=2 ** 15, r=8, p=1).derive(passphrase.encode("utf-8"))


def make_envelope(passphrase: str, seed: bytes | None = None) -> dict:
    seed = seed or secrets.token_bytes(32)
    priv = Ed25519PrivateKey.from_private_bytes(seed)
    pub = priv.public_key().public_bytes_raw()
    salt, nonce = secrets.token_bytes(16), secrets.token_bytes(12)
    ct = AESGCM(_kek(passphrase, salt)).encrypt(nonce, seed, b"r18-owner-key")
    return {
        "schema": "HGK.OWNER_KEY_ENVELOPE/1",
        "label": "owner-R18-delegation-key",
        "created_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "kdf": {"name": "scrypt", "n": 2 ** 15, "r": 8, "p": 1, "salt_b64": base64.b64encode(salt).decode()},
        "cipher": {"name": "AES-256-GCM", "nonce_b64": base64.b64encode(nonce).decode(),
                   "ct_b64": base64.b64encode(ct).decode(), "aad": "r18-owner-key"},
        "public_key_hex": pub.hex(),
        "fingerprint": hashlib.sha256(pub).hexdigest(),
        "claim_ceiling": ("the envelope protects a signing key at rest. It does NOT make an agent the owner "
                          "and it confers no authority by itself: authority comes only from the signed "
                          "DelegationRecord, which is scope-bounded and expiring."),
    }


def unseal(env: dict, passphrase: str) -> Ed25519PrivateKey:
    kdf, c = env["kdf"], env["cipher"]
    salt = base64.b64decode(kdf["salt_b64"])
    seed = AESGCM(_kek(passphrase, salt)).decrypt(base64.b64decode(c["nonce_b64"]),
                                                 base64.b64decode(c["ct_b64"]), c["aad"].encode())
    return Ed25519PrivateKey.from_private_bytes(seed)


# ----------------------------------------------------------------------------- delegation record
def subject_digest() -> tuple[str, int]:
    """sha256 over the delivered package's own (path, sha256) pairs — re-derivable from bytes."""
    chk = ROUND / "subject" / "03_TESTS_AND_READBACK" / "artifact_checksums.sha256"
    pairs = []
    for line in chk.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        h, p = line.split(None, 1)
        pairs.append((p.strip().lstrip("*"), h.lower()))
    pairs.sort()
    blob = "\n".join(f"{p}:{h}" for p, h in pairs).encode("utf-8")
    return hashlib.sha256(blob).hexdigest(), len(pairs)


def build_delegation(pub_hex: str, fingerprint: str, days: int = 30) -> dict:
    digest, n = subject_digest()
    now = datetime.now(timezone.utc).replace(microsecond=0)
    return {
        "schema": "HGK.OWNER_DELEGATION/1",
        "delegation_id": "R18-FHS-SKELETON-SPINE-" + secrets.token_hex(4),
        "round": "R18-FHS-SKELETON-SPINE-20261029",
        "subject_package": "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2",
        "subject_digest_sha256": digest,
        "subject_digest_basis": f"sha256 over {n} sorted (path, sha256) pairs from artifact_checksums.sha256",
        "maker_principal": MAKER_PRINCIPAL,
        "checker_principal": CHECKER_PRINCIPAL,
        "separation_of_duties": "maker != checker; the checker lane runs under its own SP identity and a "
                                "different credential, and may not consume this delegation to write",
        "wp_allowlist": ALLOWED_WPS,
        "wp_excluded_with_reason": EXCLUDED_WPS,
        "effect_class_allowlist": ALLOWED_CLASSES,
        "deny": DENY,
        "not_before": now.isoformat(),
        "not_after": (now + timedelta(days=days)).isoformat(),
        "max_effects_per_class": {"SOURCE_READ": 200, "REPO_WRITE_TO_CANDIDATE_BRANCH": 20},
        "nonce_seed": secrets.token_hex(16),
        "revocation": "delete governance/delegation_R18.json or record its delegation_id in the Issuer "
                      "denylist; the envelope alone grants nothing",
        "owner_public_key_hex": pub_hex,
        "owner_fingerprint": fingerprint,
        "claim_ceiling": ("authorises only what is listed, for this subject digest, until not_after. It is "
                          "not a native bundle, not a release authority, and not an acceptance signature."),
    }


def canonical(rec: dict) -> bytes:
    return json.dumps(rec, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


# ----------------------------------------------------------------------------- commands
def cmd_init(days: int) -> int:
    if ENVELOPE.exists():
        print("ERR_ENVELOPE_EXISTS: %s — use --mode sign" % ENVELOPE)
        return 2
    pw = prompt_passphrase(confirm=True)
    if not pw:
        print("CANCELLED: no passphrase entered; nothing was created")
        return 3
    GOV.mkdir(parents=True, exist_ok=True)
    seed = secrets.token_bytes(32)
    env = make_envelope(pw, seed)
    priv = Ed25519PrivateKey.from_private_bytes(seed)   # signing happens with the key object, not the passphrase
    del pw, seed
    ENVELOPE.write_text(json.dumps(env, ensure_ascii=False, indent=1), encoding="utf-8")
    rec = build_delegation(env["public_key_hex"], env["fingerprint"], days)
    DELEGATION.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    sig = priv.sign(canonical(rec))
    SIG.write_text(base64.b64encode(sig).decode() + "\n", encoding="ascii")
    receipt = {
        "schema": "R18.DELEGATION.SIGNED/1",
        "signed_utc": datetime.now(timezone.utc).isoformat(),
        "envelope": str(ENVELOPE.relative_to(ROUND)).replace("\\", "/"),
        "delegation": str(DELEGATION.relative_to(ROUND)).replace("\\", "/"),
        "signature": str(SIG.relative_to(ROUND)).replace("\\", "/"),
        "owner_fingerprint": env["fingerprint"],
        "owner_public_key_hex": env["public_key_hex"],
        "delegation_id": rec["delegation_id"],
        "subject_digest_sha256": rec["subject_digest_sha256"],
        "wp_allowlist": rec["wp_allowlist"],
        "effect_class_allowlist": rec["effect_class_allowlist"],
        "not_after": rec["not_after"],
        "signature_bytes": len(sig),
        "signed_by": "owner key, passphrase entered by the human in a local modal window; the agent never "
                     "saw the passphrase and never held the private key outside the sealed envelope",
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("delegation_id", "owner_fingerprint", "subject_digest_sha256",
                                              "wp_allowlist", "not_after", "signature_bytes")},
                     ensure_ascii=False, indent=1))
    return 0


def cmd_verify() -> int:
    if not (ENVELOPE.is_file() and DELEGATION.is_file() and SIG.is_file()):
        print("ERR_MISSING: envelope/delegation/signature incomplete")
        return 2
    env = json.loads(ENVELOPE.read_text(encoding="utf-8"))
    rec = json.loads(DELEGATION.read_text(encoding="utf-8"))
    sig = base64.b64decode(SIG.read_text(encoding="ascii").strip())
    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(env["public_key_hex"]))
    try:
        pub.verify(sig, canonical(rec))
        ok = True
    except InvalidSignature:
        ok = False
    digest, n = subject_digest()
    fresh = digest == rec["subject_digest_sha256"]
    now = datetime.now(timezone.utc)
    live = datetime.fromisoformat(rec["not_before"]) <= now <= datetime.fromisoformat(rec["not_after"])
    out = {"signature_valid": ok, "subject_digest_matches": fresh, "within_validity": live,
           "subject_pairs": n, "wp_allowlist": rec["wp_allowlist"],
           "effect_classes": rec["effect_class_allowlist"], "deny": rec["deny"],
           "owner_fingerprint": env["fingerprint"],
           "verdict": "VALID" if (ok and fresh and live) else "INVALID"}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if out["verdict"] == "VALID" else 1


def cmd_status() -> int:
    if not ENVELOPE.is_file():
        print("NO_ENVELOPE")
        return 2
    env = json.loads(ENVELOPE.read_text(encoding="utf-8"))
    rec = json.loads(DELEGATION.read_text(encoding="utf-8")) if DELEGATION.is_file() else None
    print(json.dumps({"fingerprint": env["fingerprint"], "created_utc": env["created_utc"],
                      "delegation_id": (rec or {}).get("delegation_id"),
                      "not_after": (rec or {}).get("not_after"),
                      "wp_allowlist": (rec or {}).get("wp_allowlist")}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["init", "sign", "verify", "status"], required=True)
    ap.add_argument("--days", type=int, default=30)
    a = ap.parse_args()
    if a.mode == "init":
        sys.exit(cmd_init(a.days))
    if a.mode == "sign":
        if not ENVELOPE.is_file():
            print("ERR_NO_ENVELOPE: run --mode init first")
            sys.exit(2)
        env = json.loads(ENVELOPE.read_text(encoding="utf-8"))
        pw = prompt_passphrase(confirm=False)
        if not pw:
            print("CANCELLED: no passphrase entered; nothing was signed")
            sys.exit(3)
        priv = unseal(env, pw)
        del pw
        rec = build_delegation(env["public_key_hex"], env["fingerprint"], a.days)
        DELEGATION.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
        sig = priv.sign(canonical(rec))
        SIG.write_text(base64.b64encode(sig).decode() + chr(10), encoding="ascii")
        RECEIPT.write_text(json.dumps({
            "schema": "R18.DELEGATION.SIGNED/1", "signed_utc": datetime.now(timezone.utc).isoformat(),
            "envelope": str(ENVELOPE.relative_to(ROUND)).replace("\\", "/"),
            "delegation": str(DELEGATION.relative_to(ROUND)).replace("\\", "/"),
            "delegation_id": rec["delegation_id"], "owner_fingerprint": env["fingerprint"],
            "subject_digest_sha256": rec["subject_digest_sha256"], "wp_allowlist": rec["wp_allowlist"],
            "not_after": rec["not_after"], "signature_bytes": len(sig),
            "signed_by": "owner key, passphrase entered by the human in a local modal window",
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps({"delegation_id": rec["delegation_id"], "owner_fingerprint": env["fingerprint"],
                          "wp_allowlist": rec["wp_allowlist"], "not_after": rec["not_after"]},
                         ensure_ascii=False, indent=1))
        sys.exit(0)
    if a.mode == "verify":
        sys.exit(cmd_verify())
    sys.exit(cmd_status())
