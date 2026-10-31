"""R19 delegation amendment (FAR R19 option B) — signed through the LIVE owner window.

What changes and what does not:

  * adds WP-FHS-05, WP-FHS-07, WP-FHS-15, WP-FHS-16 to the allowlist (they were outside it)
  * adds the class LOCAL_DRAFT_WRITE, which the R18 record listed in `deny`, and bounds it to
    the R19 round directory; every other denial stays (RELEASE, HOST_INSTALL, secrets, force-push,
    main, merge, tag)
  * does NOT add HOST_OP or RELEASE — those still need a native registry revision (option A)

The private key never leaves the broker process; this process only receives a signature over the
canonical bytes it constructed. The R18 record is preserved byte-for-byte as a backup before the
canonical path is rewritten, and the new record names what it supersedes.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import shutil
import time
import urllib.request

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
GOV = ROUND / "governance"
HOME = pathlib.Path(os.path.expanduser("~/.hgk-owner"))
TASK = "R19-FHS-SKELETON-SPINE"
WRITE_SET = [r"C:\Projects\Agent_Workspace\var\R19-FHS-20261029\**", r"C:\Projects\Agent_Workspace\var\R19-NATIVE-EXEC\**"]


def canon(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def subject_digest() -> str:
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


def main() -> int:
    win = json.loads((HOME / "window.json").read_text(encoding="utf-8"))
    if not (win.get("state") == "OPEN" and win.get("expires_at", 0) > time.time()):
        print(json.dumps({"signed": False, "error": "ERR_WINDOW_NOT_LIVE", "window": win.get("window_id")}))
        return 2

    prev_path = GOV / "delegation_R18_canonical.json"
    prev = json.loads(prev_path.read_text(encoding="utf-8"))
    backup = GOV / ("delegation_%s_SUPERSEDED.json" % prev.get("delegation_id", "prev"))
    if not backup.exists():
        shutil.copy2(prev_path, backup)
    shutil.copy2(GOV / "delegation_R18_canonical.sig", backup.with_suffix(".sig"))

    envelope = json.loads((HOME / "owner.key.enc").read_text(encoding="utf-8"))
    pub_hex = envelope["public_hex"]
    token = (HOME / "window.token").read_text(encoding="utf-8").strip()
    now = time.time()

    rec = {
        "schema": "HGK.OWNER_DELEGATION/2",
        "delegation_id": "R19-CANON-" + hashlib.sha256((win["window_id"] + TASK + "amend").encode()).hexdigest()[:8],
        "round": TASK,
        "supersedes": prev.get("delegation_id"),
        "amendment_reason": ("FAR R19 option B: the R18 record allowlisted 7 of 22 work packages and listed "
                             "LOCAL_DRAFT_WRITE in deny, so two completed rows could not be closed; this record "
                             "adds that class, bounded to the R19 round directories."),
        "subject_package": prev["subject_package"],
        "subject_digest_sha256": subject_digest(),
        "owner_identity": prev["owner_identity"],
        "owner_fingerprint": envelope.get("key_fingerprint"),
        "owner_public_key_hex": pub_hex,
        "signing_window_id": win["window_id"],
        "signing_window_task": win.get("task_id"),
        "signing_window_scope": win.get("scope"),
        "signing_window_effect_ceiling": win.get("effect_class_ceiling"),
        "signing_window_max_ops": win.get("max_ops"),
        "maker_principal": prev["maker_principal"],
        "checker_principal": prev["checker_principal"],
        "wp_allowlist": sorted(set(prev["wp_allowlist"]) | {"WP-FHS-05", "WP-FHS-07", "WP-FHS-15", "WP-FHS-16"}),
        "effect_class_allowlist": sorted(set(prev["effect_class_allowlist"]) | {"LOCAL_DRAFT_WRITE"}),
        "deny": [d for d in prev["deny"] if d != "LOCAL_DRAFT_WRITE"],
        "local_draft_write_set": WRITE_SET,
        "local_draft_write_set_note": ("LOCAL_DRAFT_WRITE is permitted only inside these roots; a write outside "
                                       "them is outside the delegation and must be refused by the consumer"),
        "not_before": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now)),
        "not_after": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(now + 30 * 86400)),
        "max_effects_per_class": {**prev["max_effects_per_class"], "LOCAL_DRAFT_WRITE": 40},
        "nonce_seed": hashlib.sha256(os.urandom(16)).hexdigest()[:32],
        "claim_ceiling": ("authorises only the listed WPs/classes for this subject digest until not_after. "
                          "Not a native bundle, not a release authority, not an acceptance signature."),
    }
    body = canon(rec)
    req = {"token": token, "kind": "row", "effect_class": "REPOSITORY_WRITE",
           "body_json": body.decode("utf-8"), "payload_sha256": hashlib.sha256(body).hexdigest(),
           "enrollments_sha256": win.get("enrollments_sha256_at_open")}
    try:
        r = urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:%d/sign" % int(win["port"]),
                                                          data=json.dumps(req).encode(),
                                                          headers={"Content-Type": "application/json"}), timeout=60)
        resp = json.loads(r.read())
    except Exception as e:
        print(json.dumps({"signed": False, "error": "%s: %s" % (type(e).__name__, e)}, ensure_ascii=False))
        return 3
    if "signature_hex" not in resp:
        print(json.dumps({"signed": False, "broker": resp}, ensure_ascii=False))
        return 4

    sig = bytes.fromhex(resp["signature_hex"])
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex)).verify(sig, body)
        ok = True
    except InvalidSignature:
        ok = False
    if not ok:
        print(json.dumps({"signed": False, "error": "SIGNATURE_DOES_NOT_VERIFY"}, ensure_ascii=False))
        return 5

    prev_path.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    (GOV / "delegation_R18_canonical.sig").write_text(resp["signature_hex"] + "\n", encoding="ascii")

    receipt = {
        "schema": "R19.DELEGATION.SIGNED_AMENDMENT/1",
        "signed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "delegation_id": rec["delegation_id"],
        "supersedes": rec["supersedes"],
        "owner_fingerprint": rec["owner_fingerprint"],
        "signature_verifies": True,
        "signing_window_id": win["window_id"],
        "ops_used_after": resp.get("ops_used"),
        "payload_sha256": req["payload_sha256"],
        "wp_allowlist": rec["wp_allowlist"],
        "effect_class_allowlist": rec["effect_class_allowlist"],
        "deny": rec["deny"],
        "local_draft_write_set": WRITE_SET,
        "previous_record_preserved": str(backup),
        "private_key_exposure": "none: the key stayed in the broker process; this process received a signature only",
    }
    (ROUND / "receipts" / "DELEGATION_SIGNED_AMENDMENT_R19.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
