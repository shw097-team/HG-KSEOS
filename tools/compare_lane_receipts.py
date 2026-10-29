#!/usr/bin/env python3
"""A2 / TT-R20-9: refuse to compare two lane receipts that were produced by different sources.

The defect this answers: three R20 receipts recorded `nonce_present_raw_stdout=false` while the byte-exact
stdout they themselves wrote contained the nonce. That is impossible for a plain byte search on the buffer
it was handed, and a control run of the current source records both nonce fields true -- so those receipts
came from another revision or composition path, and nothing in them said which. A receipt that cannot name
its producer must not be silently compared with one that can.

Usage:
    python tools/compare_lane_receipts.py A.json B.json
Exit: 0 = same producer AND comparable fields agree; 3 = comparable field differs; 4 = producer mismatch
      or a receipt carries no producer identity (uncomparable).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

COMPARABLE = ("served_arm", "required_arm", "ok", "code")


def producer(doc: dict) -> str | None:
    p = doc.get("producer") or {}
    return p.get("script_sha256")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    args = ap.parse_args(argv)
    docs = []
    for p in (args.a, args.b):
        try:
            docs.append(json.loads(Path(p).read_text(encoding="utf-8")))
        except Exception as exc:  # noqa: BLE001
            print(f"unreadable receipt {p}: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 4
    pa, pb = producer(docs[0]), producer(docs[1])
    if not pa or not pb:
        print(json.dumps({"schema": "R20.RECEIPT_COMPARE/1", "comparable": False,
                          "code": "ERR_PRODUCER_UNKNOWN",
                          "detail": {"a": pa, "b": pb},
                          "say": "a receipt without producer identity cannot be compared; re-issue it "
                                 "with the current dispatcher instead of interpreting the old fields"},
                         ensure_ascii=False))
        return 4
    if pa != pb:
        print(json.dumps({"schema": "R20.RECEIPT_COMPARE/1", "comparable": False,
                          "code": "ERR_CROSS_REVISION_COMPARISON",
                          "detail": {"a": pa, "b": pb},
                          "say": "these receipts were produced by different sources; a difference between "
                                 "them describes the producers, not the lanes"},
                         ensure_ascii=False))
        return 4
    diffs = {k: {"a": docs[0].get(k), "b": docs[1].get(k)}
             for k in COMPARABLE if docs[0].get(k) != docs[1].get(k)}
    print(json.dumps({"schema": "R20.RECEIPT_COMPARE/1", "comparable": True, "producer": pa,
                      "differences": diffs}, ensure_ascii=False, indent=1))
    return 0 if not diffs else 3


if __name__ == "__main__":
    raise SystemExit(main())
