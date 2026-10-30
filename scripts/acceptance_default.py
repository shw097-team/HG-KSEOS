#!/usr/bin/env python3
"""Every round must end GRANTED or REFUSED_NAMED. NOT_RUN is not a terminal state.

Five consecutive FAR rounds in this repository ended with `ACC = NOT_RUN`. Each looked finished --
they carried verdicts, AO briefs and receipts -- but a round whose acceptance is NOT_RUN still binds
nothing, so the next round starts from the same state. The repair is a default: the closing step is
mechanical and it has only two legal outcomes.

  GRANTED        an oracle was registered BEFORE the check, and the check passed against it
  REFUSED_NAMED  a named owner refused, with an expiry; the round is closed as not accepted

Anything else -- including 'we will decide later' -- exits non-zero.

Usage:
    python scripts/acceptance_default.py --round R --requirement REQ-1 \
        --oracle oracle.json --verdict verdict.json --out var/R/acceptance.json
    python scripts/acceptance_default.py ... --refusal-owner OWNER --expires 2026-11-30
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _refusal_verdict(record: Path) -> dict:
    """Judge a refusal record with the same gate a pass faces.

    A one-line reason plus an expiry used to be enough to close a round as REFUSED_NAMED, which made a
    refusal the cheapest claim in the system. It now has to name the absent object, quote the sentence that
    created the obligation, show the search, and carry a falsifier.
    """
    here = Path(__file__).resolve().parent
    if str(here) not in sys.path:
        sys.path.insert(0, str(here))
    import refusal_gate  # noqa: PLC0415

    if not record.exists():
        return {"verdict": "RECORD_MISSING", "record": str(record)}
    try:
        doc = json.loads(record.read_text(encoding="utf-8"))
    except Exception as exc:  # unreadable is not acceptable
        return {"verdict": "RECORD_UNREADABLE", "detail": str(exc)[:200]}
    return refusal_gate.judge(doc)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", required=True)
    ap.add_argument("--requirement", required=True)
    ap.add_argument("--oracle", default=None, help="oracle registered before the check")
    ap.add_argument("--verdict", default=None, help="checker verdict document")
    ap.add_argument("--refusal-owner", default=None)
    ap.add_argument("--expires", default=None, help="YYYY-MM-DD; required for a named refusal")
    ap.add_argument("--reason", default=None)
    ap.add_argument("--refusal-record", default=None,
                    help="JSON refusal record; must pass refusal_gate.py before a refusal may close a round")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    now = datetime.now(timezone.utc)
    oracle = Path(a.oracle) if a.oracle else None
    verdict = Path(a.verdict) if a.verdict else None

    state, detail = None, {}
    if a.refusal_owner:
        if not a.expires:
            print(json.dumps({"verdict": "INVALID", "detail": "a named refusal needs --expires"}))
            return 2
        if not a.refusal_record:
            print(json.dumps({"verdict": "NOT_ALLOWED",
                              "detail": "a named refusal must cite a record that survives refusal_gate",
                              "fix": "pass --refusal-record <json>; a one-line reason is not a finding"}))
            return 2
        gate = _refusal_verdict(Path(a.refusal_record))
        if gate.get("verdict") != "REFUSALS_FALSIFIABLE":
            print(json.dumps({"verdict": "NOT_ALLOWED",
                              "detail": "the refusal record is not falsifiable",
                              "gate": gate}, ensure_ascii=False))
            return 2
        state = "REFUSED_NAMED"
        detail = {"owner": a.refusal_owner, "expires": a.expires, "reason": a.reason,
                  "refusal_record": str(a.refusal_record), "refusal_gate": gate["verdict"]}
    else:
        if not oracle or not verdict:
            print(json.dumps({"verdict": "NOT_ALLOWED",
                              "detail": "no oracle+verdict and no named refusal: NOT_RUN is not a terminal state",
                              "fix": "either supply --oracle and --verdict, or --refusal-owner and --expires"}))
            return 2
        if not oracle.exists() or not verdict.exists():
            print(json.dumps({"verdict": "NOT_ALLOWED", "detail": "oracle or verdict missing"}))
            return 2
        if oracle.stat().st_mtime > verdict.stat().st_mtime:
            print(json.dumps({"verdict": "NOT_ALLOWED",
                              "detail": "the oracle was written AFTER the verdict: an oracle registered after the check proves nothing"}))
            return 2
        v = json.loads(verdict.read_text(encoding="utf-8"))
        passed = any(v.get(k) in ("PASS", "ACCEPTED", True) for k in ("verdict", "overall", "status")) or \
                 v.get("accepted") is True
        state = "GRANTED" if passed else "REFUSED_BY_CHECKER"
        detail = {"oracle_sha256": digest(oracle), "verdict_sha256": digest(verdict),
                  "verdict_document": v}

    rec = {
        "schema": "ACCEPTANCE-DEFAULT/1",
        "round": a.round,
        "requirement": a.requirement,
        "state": state,
        "decided_at_utc": now.isoformat(timespec="seconds"),
        "detail": detail,
        "rule": "a round closes GRANTED or REFUSED_NAMED; NOT_RUN is not a terminal state",
    }
    if a.out:
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"state": state, "round": a.round, "out": a.out}, ensure_ascii=False))
    return 0 if state in ("GRANTED", "REFUSED_NAMED") else 2


if __name__ == "__main__":
    sys.exit(main())
