"""Sign the R21 amendment through the owner broker.

Same broker contract as canonical_sign_delegation.py (kind "row", canonical JSON, signature verified
locally against the owner public key, private key never leaving the broker process). The difference is
that the payload comes from the amendment draft instead of a constant baked into the tool, because the
seven PARKED packages are in neither existing allowlist and both existing instruments deny HOST_INSTALL.

Owner authorisation: the owner signed R21 explicitly (message 2026-10-31, "授權簽 R21"). The scope this
file signs is the draft that was shown to them; it is not recomputed here.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import time
import urllib.request

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
GOV = ROUND / "governance"
HOME = pathlib.Path(os.path.expanduser("~/.hgk-owner"))
TASK = "R18-FHS-SKELETON-SPINE-20261029"
DRAFT = GOV / "delegation_R21_amendment_DRAFT_for_owner.json"


def canon(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def main() -> int:
    win = json.loads((HOME / "window.json").read_text(encoding="utf-8"))
    now = time.time()
    if win.get("state") == "CLOSED" or win.get("expires_at", 0) <= now:
        print(json.dumps({"signed": False, "error": "ERR_WINDOW_NOT_LIVE"}, ensure_ascii=False))
        return 2
    if win.get("task_id") != TASK:
        print(json.dumps({"signed": False, "error": "ERR_WINDOW_FOR_OTHER_TASK",
                          "task_id": win.get("task_id")}, ensure_ascii=False))
        return 2

    envelope = json.loads((HOME / "owner.key.enc").read_text(encoding="utf-8"))
    pub_hex = envelope["public_hex"]
    token = (HOME / "window.token").read_text(encoding="utf-8").strip()
    port = win.get("port")

    draft = json.loads(DRAFT.read_text(encoding="utf-8"))
    rec = dict(draft)
    for k in ("signed", "signature", "signing_instructions"):
        rec.pop(k, None)
    rec.update({
        "delegation_id": "R21-CANON-" + hashlib.sha256((win["window_id"] + draft["round"]).encode()).hexdigest()[:8],
        "owner_identity": draft["owner_identity"],
        "owner_fingerprint": envelope.get("key_fingerprint"),
        "owner_public_key_hex": pub_hex,
        "signing_window_id": win["window_id"],
        "signing_window_task": win.get("task_id"),
        "signing_window_scope": win.get("scope"),
        "signing_window_effect_ceiling": win.get("effect_class_ceiling"),
        "signing_window_max_ops": win.get("max_ops"),
        "not_before": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now)),
        "max_effects_per_class": {"SOURCE_READ": 200, "REPO_WRITE_TO_CANDIDATE_BRANCH": 20,
                                  "LOCAL_DRAFT_WRITE": 80, "HOST_INSTALL": 25},
        "nonce_seed": hashlib.sha256(os.urandom(16)).hexdigest()[:32],
        "claim_ceiling": ("authorises HOST_INSTALL for the seven listed PARKED packages, bounded to the "
                          "declared install targets, one PERMIT per package, until not_after. RELEASE stays "
                          "denied. Not a native bundle, not a release authority, not an acceptance signature."),
    })

    body = canon(rec)
    req = {"token": token, "kind": "row", "effect_class": "REPOSITORY_WRITE",
           "body_json": body.decode("utf-8"), "payload_sha256": hashlib.sha256(body).hexdigest(),
           "enrollments_sha256": win.get("enrollments_sha256_at_open")}
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

    out = GOV / "delegation_R21_signed.json"
    out.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    (GOV / "delegation_R21_signed.sig").write_text(resp["signature_hex"] + "\n", encoding="ascii")
    receipt = {"schema": "R21.DELEGATION.SIGNED/1", "signed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "delegation_id": rec["delegation_id"], "owner_fingerprint": rec["owner_fingerprint"],
               "signature_verifies": ok, "signing_window_id": win["window_id"],
               "ops_used_after": resp.get("ops_used"), "payload_sha256": req["payload_sha256"],
               "wp_allowlist": rec["wp_allowlist"], "effect_class_allowlist": rec["effect_class_allowlist"],
               "deny": rec["deny"], "not_after": rec["not_after"],
               "private_key_exposure": "none: the key stayed in the broker process; the agent only received a signature"}
    (ROUND / "receipts" / "DELEGATION_R21_SIGNED.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=1))
    return 0 if ok else 5


if __name__ == "__main__":
    raise SystemExit(main())
