"""Sign the R18 delegation with the CANONICAL owner key, through the existing owner window.

FAR_R18-10 D1/D2: my earlier envelope (`be760975…`) was a second owner key. The canonical owner identity
is `~/.hgk-owner/owner.key.enc` (fingerprint `412b3519…`), and the canonical signing path is
`var/B1-PIPD-PKG-20261027/owner_window.py`: open a bounded window (task/scope/TTL/max_ops), then POST a
payload to the local broker, which keeps the private key in its own process and never exposes it.

Semantics of reusing it: the broker signs arbitrary canonical JSON under an allowed `kind`; `row` is the
allowed kind that corresponds to registering a signed record. No modification to their tool.

Outputs (all under the R18 round dir, nothing of theirs is touched):
  governance/delegation_R18_canonical.json  the record that was signed
  governance/delegation_R18_canonical.sig   hex signature
  receipts/DELEGATION_SIGNED_CANONICAL.json receipt: window id, ops used, fingerprints, scope
"""
import hashlib
import json
import os
import pathlib
import sys
import time
import urllib.request

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
GOV = ROUND / "governance"
HOME = pathlib.Path(os.path.expanduser("~/.hgk-owner"))
TASK = "R18-FHS-SKELETON-SPINE-20261029"
ALLOWED_WPS = ["WP-FHS-00", "WP-FHS-01", "WP-FHS-09", "WP-FHS-19", "WP-FHS-21", "WP-FHS-06", "WP-FHS-18"]
CLASSES = ["SOURCE_READ", "REPO_WRITE_TO_CANDIDATE_BRANCH"]
DENY = ["RELEASE", "HOST_INSTALL", "secrets", "force-push", "main", "merge", "tag", "LOCAL_DRAFT_WRITE"]


def canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


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
    return hashlib.sha256(("\n".join(p + ":" + h for p, h in pairs)).encode()).hexdigest()


def main():
    win = json.loads((HOME / "window.json").read_text(encoding="utf-8"))
    now = time.time()
    if win.get("state") == "CLOSED" or win.get("expires_at", 0) <= now:
        print(json.dumps({"signed": False, "error": "ERR_WINDOW_NOT_LIVE", "window": win.get("window_id"),
                          "state": win.get("state"), "expires_in_s": win.get("expires_at", 0) - now},
                         ensure_ascii=False))
        return 2
    if win.get("task_id") != TASK:
        print(json.dumps({"signed": False, "error": "ERR_WINDOW_FOR_OTHER_TASK", "task_id": win.get("task_id")},
                         ensure_ascii=False))
        return 2

    envelope = json.loads((HOME / "owner.key.enc").read_text(encoding="utf-8"))
    pub_hex = envelope["public_hex"]
    token = (HOME / "window.token").read_text(encoding="utf-8").strip()
    port = win.get("port")

    rec = {
        "schema": "HGK.OWNER_DELEGATION/2",
        "delegation_id": "R18-CANON-" + hashlib.sha256((win["window_id"] + TASK).encode()).hexdigest()[:8],
        "round": TASK,
        "subject_package": "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2",
        "subject_digest_sha256": subject_digest(),
        "owner_identity": "CANONICAL_HGK_OWNER (~/.hgk-owner/owner.key.enc)",
        "owner_fingerprint": envelope.get("key_fingerprint"),
        "owner_public_key_hex": pub_hex,
        "signing_window_id": win["window_id"],
        "signing_window_task": win.get("task_id"),
        "signing_window_scope": win.get("scope"),
        "signing_window_effect_ceiling": win.get("effect_class_ceiling"),
        "signing_window_max_ops": win.get("max_ops"),
        "maker_principal": "HERMES-R18-EXECUTE-LANE",
        "checker_principal": "SBL-ACCEPTANCE-CHALLENGE-SP",
        "wp_allowlist": ALLOWED_WPS,
        "effect_class_allowlist": CLASSES,
        "deny": DENY,
        "not_before": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now)),
        "not_after": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now + 30 * 86400)),
        "max_effects_per_class": {"SOURCE_READ": 200, "REPO_WRITE_TO_CANDIDATE_BRANCH": 20},
        "nonce_seed": hashlib.sha256(os.urandom(16)).hexdigest()[:32],
        "claim_ceiling": ("authorises only the listed WPs/classes for this subject digest until not_after. "
                          "Not a native bundle, not a release authority, not an acceptance signature."),
    }
    body = canon(rec)
    req = {
        "token": token,
        "kind": "row",
        "effect_class": "REPOSITORY_WRITE",
        "body_json": body.decode("utf-8"),
        "payload_sha256": hashlib.sha256(body).hexdigest(),
        "enrollments_sha256": win.get("enrollments_sha256_at_open"),
    }
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:%d/sign" % int(port), data=json.dumps(req).encode(),
            headers={"Content-Type": "application/json"}), timeout=60)
        resp = json.loads(r.read())
    except Exception as e:
        print(json.dumps({"signed": False, "error": "ERR_BROKER:%s: %s" % (type(e).__name__, e)},
                         ensure_ascii=False))
        return 3

    if "signature_hex" not in resp:
        print(json.dumps({"signed": False, "broker": resp}, ensure_ascii=False))
        return 4

    sig = bytes.fromhex(resp["signature_hex"])
    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex))
    try:
        pub.verify(sig, body)
        ok = True
    except InvalidSignature:
        ok = False

    GOV.mkdir(parents=True, exist_ok=True)
    (GOV / "delegation_R18_canonical.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1),
                                                       encoding="utf-8")
    (GOV / "delegation_R18_canonical.sig").write_text(resp["signature_hex"] + "\n", encoding="ascii")
    receipt = {
        "schema": "R18.DELEGATION.SIGNED_CANONICAL/1",
        "signed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "delegation_id": rec["delegation_id"],
        "owner_identity": rec["owner_identity"],
        "owner_fingerprint": rec["owner_fingerprint"],
        "signature_verifies": ok,
        "signing_window_id": win["window_id"],
        "signing_window_max_ops": win.get("max_ops"),
        "ops_used_after": resp.get("ops_used"),
        "payload_sha256": req["payload_sha256"],
        "subject_digest_sha256": rec["subject_digest_sha256"],
        "wp_allowlist": rec["wp_allowlist"],
        "not_after": rec["not_after"],
        "private_key_exposure": "none: the key stayed in the broker process; the agent only received a signature",
    }
    (ROUND / "receipts" / "DELEGATION_SIGNED_CANONICAL.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=1))
    return 0 if ok else 5


if __name__ == "__main__":
    sys.exit(main())
