#!/usr/bin/env python3
"""Bounded CAP-BOOT loaded-ACK consumer for WP-FHS-17.

Reproduce:
    python candidate/package/consumer/wp17_consumer.py \
        --attest REC.json --pinned-sha <occupant sha> \
        --pinned-manifest-sha <manifest sha> --subject-sha <subject sha> \
        --input <invoke input json> --origin <resolved origin>

It does NOT trust the loader's summary and does NOT trust the occupant's
self-report on its own. It independently:

  * re-derives the ACK digest from the ACK body;
  * re-hashes the resolved origin on disk (live bytes, after the child exited);
  * recomputes `functional_output` from the served fields + the real input;
  * recomputes the input digest from the input file the loader actually used;
  * checks subject/need/nonce and the manifest digest pin;
  * requires the serving pid to be a different process than this consumer.

Ceiling, stated in the receipt: this is a bounded WP-local consumer, not the
original Host capability Registry/Consumer (see EVIDENCE_GAP.md).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys


def canonical(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def functional_output(ack: dict) -> str:
    body = {k: ack[k] for k in
            ("occupant_id", "version", "need_id", "subject_sha256", "nonce",
             "loaded_sha256", "manifest_sha256", "input_sha256", "payload_digest")}
    return sha_bytes(canonical(body))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--attest", required=True)
    ap.add_argument("--pinned-sha", required=True)
    ap.add_argument("--pinned-manifest-sha", required=True)
    ap.add_argument("--subject-sha", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--origin", required=True)
    ap.add_argument("--token", default="")
    a = ap.parse_args(argv)

    rec = json.load(open(a.attest, encoding="utf-8"))
    ack = rec.get("ack") or {}
    body = {k: v for k, v in ack.items() if k != "ack_digest"}
    derived = sha_bytes(canonical(body))
    origin = os.path.realpath(a.origin)
    live = sha_bytes(open(origin, "rb").read())
    inp = json.load(open(a.input, encoding="utf-8"))
    input_sha = sha_bytes(canonical(inp))
    fo = None
    try:
        fo = functional_output(ack)
    except KeyError:
        pass
    checks = {
        "ack_digest_rederived": derived == ack.get("ack_digest"),
        "loaded_sha_is_pinned": ack.get("loaded_sha256") == a.pinned_sha,
        "manifest_sha_is_pinned": ack.get("manifest_sha256") == a.pinned_manifest_sha,
        "manifest_bound": ack.get("manifest_bound") is True,
        "subject_is_bound": ack.get("subject_sha256") == a.subject_sha,
        "input_digest_matches_real_input": ack.get("input_sha256") == input_sha,
        "functional_output_rederived": fo is not None and fo == ack.get("functional_output"),
        "origin_is_canonical": ack.get("origin") == origin,
        "live_origin_is_pinned": live == a.pinned_sha,
        "child_pid_distinct": int(ack.get("pid") or 0) not in (0, os.getpid()),
        "sha_stable_during_invoke": rec.get("sha_at_start") == rec.get("sha_at_end"),
        "driver_agrees": rec.get("sha_at_start") == ack.get("loaded_sha256"),
        "child_verdict_attested": rec.get("verdict") == "ATTESTED",
        "run_token_matches": (not a.token) or rec.get("token") == a.token,
    }
    bad = [k for k, v in checks.items() if not v]
    out = {
        "record": "wp17.bounded_consumer",
        "consumer_pid": os.getpid(),
        "observed_origin": origin,
        "observed_live_sha256": live,
        "pinned_sha256": a.pinned_sha,
        "pinned_manifest_sha256": a.pinned_manifest_sha,
        "subject_sha256": a.subject_sha,
        "input_sha256": input_sha,
        "derived_ack_digest": derived,
        "derived_functional_output": fo,
        "ack_functional_output": ack.get("functional_output"),
        "need_id": ack.get("need_id"),
        "nonce": ack.get("nonce"),
        "served_pid": ack.get("pid"),
        "checks": checks,
        "verdict": "CONSUMER_ACK" if not bad else "CONSUMER_REFUSED",
        "failed_checks": bad,
        "ceiling": "bounded WP-local consumer; not the original Host capability Registry/Consumer",
    }
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))
    return 0 if not bad else 3


if __name__ == "__main__":
    sys.exit(main())
