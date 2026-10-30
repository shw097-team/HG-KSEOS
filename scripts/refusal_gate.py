#!/usr/bin/env python3
"""refusal_gate — a refusal is a claim and must be as falsifiable as a pass.

A pass has an oracle, an officer and a gate. A refusal historically had a one-line reason, a registry row
and an expiry, which made it the cheapest assertion in the system and the easiest one to be wrong about.

This gate refuses a refusal that does not carry:

  cited_text      the delivery sentence that creates the obligation, quoted
  absent_object   the object that does not exist, named — not the circumstance
  reproduction    at least one command that was actually run while looking for it
  falsifier       what would have to become true for the refusal to be withdrawn
  expiry          a date

Exit 0 = every refusal is falsifiable. Exit 2 = at least one is not, with per-item reasons.
Read-only: it never edits the record it judges.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

REQUIRED = ("cited_text", "absent_object", "reproduction", "falsifier", "expiry")

# A refusal may not rest on a circumstance. These are the words that give a guess the shape of a finding.
CIRCUMSTANCE = (
    "no host capability",
    "not available on this machine",
    "not deployed",
    "not present here",
    "only one host",
    "runs interactively",
    "absent",
    "unavailable",
)


def _refusals(doc: dict) -> list[dict]:
    for key in ("refusals", "withdrawn_refusals", "items"):
        value = doc.get(key)
        if isinstance(value, list):
            return [r for r in value if isinstance(r, dict)]
    return []


def judge(doc: dict) -> dict:
    items = _refusals(doc)
    if not items:
        return {"verdict": "NO_REFUSALS_FOUND", "checked": 0, "failures": []}
    failures = []
    for i, r in enumerate(items, 1):
        ident = r.get("wp") or r.get("id") or f"#{i}"
        missing = [k for k in REQUIRED if not r.get(k)]
        reasons = []
        if missing:
            reasons.append("missing:" + ",".join(missing))
        if r.get("reason"):
            low = str(r["reason"]).lower()
            hit = [c for c in CIRCUMSTANCE if c in low]
            if hit:
                reasons.append("circumstance_not_object:" + hit[0])
        if r.get("cited_text") and len(str(r["cited_text"]).strip()) < 20:
            reasons.append("cited_text_too_short_to_be_a_quote")
        if reasons:
            failures.append({"item": ident, "reasons": reasons})
    return {
        "verdict": "REFUSALS_FALSIFIABLE" if not failures else "REFUSAL_NOT_FALSIFIABLE",
        "checked": len(items),
        "failures": failures,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="judge whether refusals are falsifiable claims")
    ap.add_argument("record", help="JSON file containing a refusal record")
    ap.add_argument("--json", action="store_true", help="emit the verdict as one JSON object")
    ap.add_argument("--require", action="append", default=None,
                    help="extra required field (repeatable); overrides the default set when given")
    args = ap.parse_args()

    global REQUIRED
    if args.require:
        REQUIRED = tuple(args.require)

    path = pathlib.Path(args.record)
    if not path.exists():
        print(json.dumps({"verdict": "RECORD_MISSING", "path": str(path)}))
        return 3
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # a record that cannot be parsed cannot be judged
        print(json.dumps({"verdict": "RECORD_UNREADABLE", "detail": str(exc)[:200]}))
        return 3

    result = judge(doc)
    result["record"] = str(path)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"{result['verdict']}: {result['checked']} refusal(s) in {path}")
        for f in result["failures"]:
            print(f"  {f['item']}: {'; '.join(f['reasons'])}")
    return 0 if result["verdict"] == "REFUSALS_FALSIFIABLE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
