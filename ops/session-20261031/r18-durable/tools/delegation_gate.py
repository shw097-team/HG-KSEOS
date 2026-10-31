"""Issuer-side gate for the owner delegation: fail-closed enforcement of the signed scope.

A signature nobody checks is theatre. This gate verifies the Ed25519 signature over the canonical
DelegationRecord, re-derives the subject digest from the package bytes, and decides PERMIT_DERIVED or a
typed REFUSED. Every decision is appended to governance/delegation_effects.jsonl.

    exit 0  PERMIT_DERIVED     effect is inside the signed scope
    exit 7  REFUSED_<CODE>     effect is outside it

Claim ceiling: a derived permit is NOT a native bundle, NOT an Issuer PERMIT for HOST_OP/RELEASE, and
NOT an acceptance signature. It authorises only the read/draft/candidate-branch work the owner named.
"""
import argparse
import base64
import hashlib
import json
import os
import pathlib
import sys
from datetime import datetime, timezone
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROUND = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
GOV = ROUND / "governance"
EFFECTS = GOV / "delegation_effects.jsonl"
DENYLIST = GOV / "revoked_delegations.json"

CANON_PREFIX = "412b3519"

HARD_DENY = {"RELEASE", "HOST_INSTALL", "secrets", "force-push", "main", "merge", "tag",
             "LOCAL_DRAFT_WRITE"}


def canonical(rec):
    return json.dumps(rec, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def subject_digest():
    chk = ROUND / "subject" / "03_TESTS_AND_READBACK" / "artifact_checksums.sha256"
    pairs = []
    for line in chk.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        h, p = line.split(None, 1)
        pairs.append((p.strip().lstrip("*"), h.lower()))
    pairs.sort()
    return hashlib.sha256("\n".join(p + ":" + h for p, h in pairs).encode()).hexdigest()


def load_signed():
    """Canonical delegation first (owner 412b3519…); the second-key envelope is a drill artefact only."""
    can_rec, can_sig = GOV / "delegation_R18_canonical.json", GOV / "delegation_R18_canonical.sig"
    if can_rec.is_file() and can_sig.is_file():
        rec = json.loads(can_rec.read_text(encoding="utf-8"))
        sig = bytes.fromhex(can_sig.read_text(encoding="ascii").strip())
        env = {"fingerprint": rec.get("owner_fingerprint"),
               "public_key_hex": rec.get("owner_public_key_hex"),
               "source": "delegation_R18_canonical.json"}
        return env, rec, sig
    if not ((GOV / "owner_envelope.json").is_file() and (GOV / "delegation_R18.json").is_file()
            and (GOV / "delegation_R18.sig").is_file()):
        return None, None, None
    env = json.loads((GOV / "owner_envelope.json").read_text(encoding="utf-8"))
    rec = json.loads((GOV / "delegation_R18.json").read_text(encoding="utf-8"))
    sig = base64.b64decode((GOV / "delegation_R18.sig").read_text(encoding="ascii").strip())
    return env, rec, sig


def revoked_ids():
    if not DENYLIST.is_file():
        return set()
    try:
        return set(json.loads(DENYLIST.read_text(encoding="utf-8")).get("revoked", []))
    except Exception:
        return set()


def consumed():
    n = 0
    per = {}
    if EFFECTS.is_file():
        for line in EFFECTS.read_text(encoding="utf-8").splitlines():
            try:
                ev = json.loads(line)
            except Exception:
                continue
            if ev.get("decision") == "PERMIT_DERIVED":
                n += 1
                per[ev.get("effect_class")] = per.get(ev.get("effect_class"), 0) + 1
    return n, per


def decide(wp, effect_class, target, now, sig_ok, digest_ok, rec, used_per_class):
    if not sig_ok:
        return "REFUSED_BAD_SIGNATURE"
    if not digest_ok:
        return "REFUSED_SUBJECT_DIGEST_DRIFT"
    if effect_class in HARD_DENY or effect_class in (rec.get("deny") or []):
        return "REFUSED_CLASS_DENIED"
    if effect_class not in (rec.get("effect_class_allowlist") or []):
        return "REFUSED_CLASS_NOT_ALLOWLISTED"
    if wp not in (rec.get("wp_allowlist") or []):
        if wp in (rec.get("wp_excluded_with_reason") or {}):
            return "REFUSED_WP_EXCLUDED"
        return "REFUSED_WP_NOT_ALLOWLISTED"
    if not (datetime.fromisoformat(rec["not_before"]) <= now <= datetime.fromisoformat(rec["not_after"])):
        return "REFUSED_EXPIRED_OR_NOT_YET_VALID"
    quota = (rec.get("max_effects_per_class") or {}).get(effect_class)
    if quota is not None and used_per_class.get(effect_class, 0) >= quota:
        return "REFUSED_QUOTA_EXHAUSTED"
    if effect_class == "REPO_WRITE_TO_CANDIDATE_BRANCH":
        t = (target or "").lower()
        if not t or t in ("main", "master") or not (t.startswith("candidate/") or t.startswith("refs/heads/candidate/")):
            return "REFUSED_TARGET_NOT_CANDIDATE"
    return "PERMIT_DERIVED"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wp", required=True)
    ap.add_argument("--class", dest="cls", required=True)
    ap.add_argument("--target", default="")
    ap.add_argument("--now", default="", help="ISO timestamp override, for expiry negative controls")
    ap.add_argument("--consume", action="store_true", help="record the effect (otherwise dry-run)")
    ap.add_argument("--reason", default="")
    ap.add_argument("--allow-noncanonical-owner", action="store_true",
                    help="drill only: run the gate with a non-canonical owner key so its own positive "
                         "controls stay exercisable. Never use this to claim authority.")
    a = ap.parse_args()

    env, rec, sig = load_signed()
    if env is None:
        out = {"schema": "R18.DELEGATION_GATE/1",
               "at_utc": datetime.now(timezone.utc).isoformat(),
               "wp": a.wp, "effect_class": a.cls, "target": a.target,
               "decision": "REFUSED_REVOKED",
               "detail": "no delegation on disk: withdrawal is effective immediately",
               "recorded": False}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 8
    if rec.get("delegation_id") in revoked_ids():
        out = {"schema": "R18.DELEGATION_GATE/1",
               "at_utc": datetime.now(timezone.utc).isoformat(),
               "wp": a.wp, "effect_class": a.cls, "target": a.target,
               "delegation_id": rec.get("delegation_id"),
               "decision": "REFUSED_REVOKED",
               "detail": "delegation_id is in governance/revoked_delegations.json",
               "recorded": False}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 8
    owner_is_canonical = str(env.get("fingerprint", "")).startswith(CANON_PREFIX)
    if not owner_is_canonical and not a.allow_noncanonical_owner:
        out = {"schema": "R18.DELEGATION_GATE/1",
               "at_utc": datetime.now(timezone.utc).isoformat(),
               "wp": a.wp, "effect_class": a.cls, "target": a.target,
               "owner_fingerprint": env.get("fingerprint"),
               "canonical_owner_prefix": CANON_PREFIX,
               "decision": "REFUSED_NONCANONICAL_OWNER",
               "detail": ("this delegation is signed by a second owner key. The canonical owner identity is "
                          "~/.hgk-owner/owner.key.enc (fingerprint prefix %s). Re-sign under that key via the "
                          "existing owner window, or pass --allow-noncanonical-owner for a drill only." % CANON_PREFIX),
               "recorded": False}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 9
    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(env["public_key_hex"]))
    try:
        pub.verify(sig, canonical(rec))
        sig_ok = True
    except InvalidSignature:
        sig_ok = False
    digest_ok = subject_digest() == rec.get("subject_digest_sha256")
    now = datetime.fromisoformat(a.now) if a.now else datetime.now(timezone.utc)
    total, per = consumed()

    decision = decide(a.wp, a.cls, a.target, now, sig_ok, digest_ok, rec, per)
    out = {
        "schema": "R18.DELEGATION_GATE/1",
        "at_utc": datetime.now(timezone.utc).isoformat(),
        "wp": a.wp, "effect_class": a.cls, "target": a.target,
        "signature_valid": sig_ok, "subject_digest_matches": digest_ok,
        "delegation_id": rec.get("delegation_id"),
        "owner_fingerprint": env["fingerprint"],
        "decision": decision,
        "consumed_before": total,
        "claim_ceiling": rec.get("claim_ceiling"),
        "reason": a.reason,
    }
    out["recorded"] = bool(a.consume and decision == "PERMIT_DERIVED")
    if out["recorded"]:
        EFFECTS.parent.mkdir(parents=True, exist_ok=True)
        with EFFECTS.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(out, ensure_ascii=False) + chr(10))
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if decision == "PERMIT_DERIVED" else 7


if __name__ == "__main__":
    sys.exit(main())
