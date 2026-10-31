#!/usr/bin/env python3
"""CAP-BOOT minimal HostOccupant: loaded-ACK feature.

Reproduce (unit self-test, no install required):
    python candidate/package/occupant/capboot_attest.py --self-test

This file is the occupant payload for WP-FHS-17. It is NOT a printer stub:

  * it reads its OWN bytes from its own resolved origin at load time;
  * it reads the package manifest next to itself and verifies that the
    manifest's pinned occupant digest is its own digest, so a manifest that
    describes some other file cannot be used to qualify this binary;
  * it checks the caller's expectation (occupant + manifest digest, subject,
    need id) and refuses instead of emitting an ACK when they do not match;
  * it echoes the loader's per-run token, so an attestation from any other
    spawn (or a stale file) cannot be substituted for this run's child;
  * it computes a `functional_output` digest over the real input, then
    re-reads its origin after the feature work so bytes swapped underneath a
    running process are visible rather than hidden.

Contract (WP card output clause: "needed能力最小HostOccupant+loaded ACK"):

  input  : JSON {need_id, subject_sha256, nonce, payload,
                 expect:{occupant_sha256, manifest_sha256}}
  output : JSON {record, origin, pid, sha_at_start, sha_at_end, ack:{...}}
           where ack.loaded_sha256 is computed BY THIS PROCESS.

The parent loader is never trusted to supply the digest.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time

VERSION = "1.0.0"
OCCUPANT_ID = "OCC-CAPBOOT-LOADED-ACK"
FEATURE = "CAP-BOOT.loaded-ACK"
MANIFEST_NAME = "capboot_attest.manifest.json"


def canonical(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_origin() -> tuple[str, str]:
    origin = os.path.realpath(__file__)
    with open(origin, "rb") as fh:
        return origin, sha256_bytes(fh.read())


def manifest_path() -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), MANIFEST_NAME)


def ack_digest(ack: dict) -> str:
    body = {k: v for k, v in ack.items() if k != "ack_digest"}
    return sha256_bytes(canonical(body))


def functional_output(fields: dict) -> str:
    """Substantive result of the needed capability: a digest that binds the
    served occupant, the admitted subject/need/nonce and the real input."""
    body = {k: fields[k] for k in
            ("occupant_id", "version", "need_id", "subject_sha256", "nonce",
             "loaded_sha256", "manifest_sha256", "input_sha256", "payload_digest")}
    return sha256_bytes(canonical(body))


def emit(record: dict, out_path: str | None) -> int:
    text = json.dumps(record, ensure_ascii=False, sort_keys=True)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    sys.stdout.write(text + "\n")
    return 0


def refuse(code: str, detail: str, out_path: str | None, token: str = "") -> int:
    rec = {"record": "capboot.loaded_attestation", "verdict": "REFUSED",
           "code": code, "detail": detail, "pid": os.getpid(),
           "ppid": os.getppid(), "token": token,
           "origin": os.path.realpath(__file__), "at": time.time()}
    emit(rec, out_path)
    return 4


def run(inp: dict, delay_ms: int, out_path: str | None, token: str = "") -> int:
    started = time.time()
    origin, sha_start = read_origin()
    mp = manifest_path()
    if not os.path.isfile(mp):
        return refuse("MANIFEST_MISSING", mp, out_path, token)
    with open(mp, "rb") as fh:
        manifest_bytes = fh.read()
    manifest_sha = sha256_bytes(manifest_bytes)
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        return refuse("MANIFEST_UNPARSEABLE", f"{type(exc).__name__}: {exc}", out_path, token)
    pinned = manifest.get("occupant") or {}
    if pinned.get("sha256") != sha_start:
        return refuse("MANIFEST_OCCUPANT_DIGEST_MISMATCH",
                      f"manifest pins {pinned.get('sha256')} but loaded bytes are {sha_start}",
                      out_path, token)
    expect = inp.get("expect") or {}
    if expect.get("occupant_sha256") != sha_start:
        return refuse("EXPECT_OCCUPANT_MISMATCH", str(expect.get("occupant_sha256")),
                      out_path, token)
    if expect.get("manifest_sha256") != manifest_sha:
        return refuse("EXPECT_MANIFEST_MISMATCH", str(expect.get("manifest_sha256")),
                      out_path, token)
    need_id = inp.get("need_id")
    subject = inp.get("subject_sha256")
    nonce = inp.get("nonce")
    if not need_id or not nonce or not isinstance(subject, str) or len(subject) != 64:
        return refuse("INPUT_UNBOUND", "need_id/subject_sha256/nonce are required",
                      out_path, token)

    input_sha = sha256_bytes(canonical(inp))
    payload = inp.get("payload")
    payload_digest = sha256_bytes(canonical(payload))
    fo = functional_output({
        "occupant_id": OCCUPANT_ID, "version": VERSION, "need_id": need_id,
        "subject_sha256": subject, "nonce": nonce, "loaded_sha256": sha_start,
        "manifest_sha256": manifest_sha, "input_sha256": input_sha,
        "payload_digest": payload_digest})
    ack = {
        "occupant_id": OCCUPANT_ID,
        "version": VERSION,
        "feature": FEATURE,
        "need_id": need_id,
        "subject_sha256": subject,
        "nonce": nonce,
        "origin": origin,
        "pid": os.getpid(),
        "loaded_sha256": sha_start,
        "manifest_sha256": manifest_sha,
        "input_sha256": input_sha,
        "payload_digest": payload_digest,
        "payload_echo": payload,
        "functional_output": fo,
        "manifest_bound": True,
    }
    ack["ack_digest"] = ack_digest(ack)
    # Deliberate window: the loader may swap the file while we run. The second
    # read makes that visible instead of certifying a stale pre-hash.
    if delay_ms > 0:
        time.sleep(delay_ms / 1000.0)
    origin_end, sha_end = read_origin()
    record = {
        "record": "capboot.loaded_attestation",
        "verdict": "ATTESTED",
        "feature": FEATURE,
        "origin": origin,
        "origin_end": origin_end,
        "pid": os.getpid(),
        "ppid": os.getppid(),
        "token": token,
        "argv": sys.argv,
        "python": sys.version.split()[0],
        "started_at": started,
        "ended_at": time.time(),
        "sha_at_start": sha_start,
        "sha_at_end": sha_end,
        "changed_during_invoke": sha_start != sha_end,
        "manifest_path": mp,
        "manifest_sha256": manifest_sha,
        "input_sha256": input_sha,
        "functional_output": fo,
        "ack": ack,
        "ack_digest": ack["ack_digest"],
    }
    if sha_start != sha_end:
        record["verdict"] = "REFUSED"
        record["code"] = "ORIGIN_CHANGED_DURING_INVOKE"
    return emit(record, out_path)


def self_test() -> int:
    import tempfile

    here = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(here, MANIFEST_NAME), "rb") as fh:
        man_sha = sha256_bytes(fh.read())
    _, own = read_origin()
    inp = {"need_id": "SELF", "subject_sha256": "0" * 64, "nonce": "self",
           "payload": {"op": "self-test"},
           "expect": {"occupant_sha256": own, "manifest_sha256": man_sha}}
    with tempfile.TemporaryDirectory() as td:
        op = os.path.join(td, "out.json")
        rc = run(inp, 0, op)
        if rc != 0:
            return rc
        rec = json.load(open(op, encoding="utf-8"))
        assert rec["sha_at_start"] == rec["sha_at_end"] == own
        assert rec["ack_digest"] == ack_digest(rec["ack"])
        assert rec["ack"]["functional_output"] == functional_output({
            "occupant_id": OCCUPANT_ID, "version": VERSION, "need_id": "SELF",
            "subject_sha256": "0" * 64, "nonce": "self", "loaded_sha256": own,
            "manifest_sha256": man_sha, "input_sha256": rec["input_sha256"],
            "payload_digest": rec["ack"]["payload_digest"]})
        # A redirection attempt must be refused, not silently accepted.
        bad = dict(inp, expect={"occupant_sha256": "f" * 64, "manifest_sha256": man_sha})
        rc_bad = run(bad, 0, os.path.join(td, "bad.json"))
        assert rc_bad == 4
        print(json.dumps({"self_test": "PASS", "loaded_sha256": own,
                          "manifest_sha256": man_sha,
                          "redirect_refused": rc_bad == 4}, ensure_ascii=False))
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    out_path = None
    delay_ms = 0
    input_path = None
    token = ""
    i = 1
    while i < len(argv):
        if argv[i] == "--attest-out":
            out_path = argv[i + 1]
            i += 2
        elif argv[i] == "--token":
            token = argv[i + 1]
            i += 2
        elif argv[i] == "--delay-ms":
            delay_ms = int(argv[i + 1])
            i += 2
        elif argv[i] == "--input":
            input_path = argv[i + 1]
            i += 2
        else:
            i += 1
    if input_path:
        with open(input_path, encoding="utf-8") as fh:
            inp = json.load(fh)
    else:
        inp = json.loads(sys.argv[-1]) if len(sys.argv) > 1 else {}
    return run(inp, delay_ms, out_path, token)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
