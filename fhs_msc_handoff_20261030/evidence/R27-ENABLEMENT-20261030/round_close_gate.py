#!/usr/bin/env python3
"""round_close_gate — a round may not be reported complete while it still owes something.

Three failures this repository kept repeating, and one gate for all three:

  the round was green while rows stayed NOT_RUN     -> refuse while a blocking TT is OPEN
  a lane was claimed but not dispatched             -> every claimed lane needs a receipt that passes
                                                       lane_evidence_gate
  a claim rested on my own earlier summary          -> a MEASURED claim may not cite a derived artefact

It reads the plane rather than inventing a parallel one: open blocking TTs already live in tt_records.

Exit 0 = the round may close, and a closure receipt is written.
Exit 2 = it may not, with the reasons. Exit 3 = an input could not be read.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sqlite3
import sys
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import lane_evidence_gate  # noqa: E402

# A MEASURED claim must rest on something outside the reasoning that produced it.
PRIMARY_SOURCES = {
    "delivery", "registry", "git", "filesystem", "receipts", "config", "both", "run", "code",
    "R2-A", "R2-B", "R2-C", "delivery+Fabric", "predecessor run",
}
DERIVED_SOURCES = {"ledger", "synthesis", "previous run", "earlier round", "memory", "skill"}


def open_blocking_tts(db: pathlib.Path) -> list[dict]:
    if not db.exists():
        raise FileNotFoundError(db)
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    rows = [dict(r) for r in con.execute(
        "SELECT tt_id,subject,owner,close_criteria,created_at FROM tt_records "
        "WHERE status='OPEN' AND blocking=1 ORDER BY created_at")]
    con.close()
    return rows


def check_ledger(path: pathlib.Path) -> dict:
    """Refuse a MEASURED claim whose only support is something this agent wrote earlier."""
    if not path.exists():
        return {"checked": 0, "problems": [], "skipped": "ledger missing"}
    problems = []
    checked = 0
    text = path.read_text(encoding="utf-8", errors="replace").strip().splitlines()
    if not text:
        return {"checked": 0, "problems": [], "skipped": "ledger empty"}
    header = text[0].split("\t")
    try:
        i_claim = header.index("claim_id")
    except ValueError:
        i_claim = 0
    i_status = header.index("status") if "status" in header else None
    i_source = header.index("source") if "source" in header else None
    for line in text[1:]:
        cells = line.split("\t")
        if len(cells) < 2:
            continue
        checked += 1
        claim = cells[i_claim]
        status = cells[i_status].strip().upper() if i_status is not None and i_status < len(cells) else ""
        source = cells[i_source].strip() if i_source is not None and i_source < len(cells) else ""
        if status.startswith("MEASURED"):
            if not source:
                problems.append(f"{claim}: MEASURED with no source")
            elif source.lower() in DERIVED_SOURCES:
                problems.append(f"{claim}: MEASURED rests on a derived artefact ({source})")
            elif source not in PRIMARY_SOURCES and source.lower() not in {s.lower() for s in PRIMARY_SOURCES}:
                problems.append(f"{claim}: MEASURED cites an unrecognised source ({source})")
    return {"checked": checked, "problems": problems}


def main() -> int:
    ap = argparse.ArgumentParser(description="refuse to close a round that still owes something")
    ap.add_argument("--round", required=True)
    ap.add_argument("--db", default="var/shared-spine/hg-kseos.db")
    ap.add_argument("--lane-receipt", action="append", default=[],
                    help="LANE=path (repeatable), e.g. PLAN=C:/wg/plan1/plan_receipt.json")
    ap.add_argument("--nonce", default=None, help="round nonce expected in every lane receipt")
    ap.add_argument("--claim-ledger", default=None)
    ap.add_argument("--allow-open-tt", action="append", default=[],
                    help="TT id that is knowingly carried into this round (repeatable)")
    ap.add_argument("--json-out", default=None)
    args = ap.parse_args()

    problems: list[str] = []
    blocks: list[dict] = []

    db = pathlib.Path(args.db)
    if not db.is_absolute():
        db = (pathlib.Path.cwd() / db).resolve()
    try:
        tts = [t for t in open_blocking_tts(db) if t["tt_id"] not in set(args.allow_open_tt)]
    except FileNotFoundError:
        print(json.dumps({"verdict": "DB_MISSING", "db": str(db)}))
        return 3
    blocks.extend(tts)
    for t in tts:
        problems.append(f"blocking_tt_open: {t['tt_id']} — {t['subject'][:90]}")

    lanes_used = []
    for spec in args.lane_receipt:
        if "=" not in spec:
            problems.append(f"bad_lane_argument: {spec}")
            continue
        lane, path = spec.split("=", 1)
        rp = pathlib.Path(path)
        if not rp.exists():
            problems.append(f"lane_receipt_missing: {lane} {path}")
            continue
        receipt = json.loads(rp.read_text(encoding="utf-8"))
        verdict = lane_evidence_gate.judge(receipt, lane, args.nonce)
        lanes_used.append({"lane": lane, "receipt": path, "gate": verdict["verdict"],
                           "asked": verdict.get("asked"), "served": verdict.get("served"),
                           "rank": verdict.get("rank"), "seconds": verdict.get("seconds")})
        if verdict["verdict"] != "LANE_SERVED_AS_CLAIMED":
            for p in verdict["problems"]:
                problems.append(f"lane_not_evidenced: {lane} {p}")

    ledger = check_ledger(pathlib.Path(args.claim_ledger)) if args.claim_ledger else {"checked": 0, "problems": []}
    problems.extend(f"claim_source: {p}" for p in ledger["problems"])

    ok = not problems
    receipt = {
        "schema": "ROUND-CLOSURE/1",
        "round": args.round,
        "verdict": "ROUND_MAY_CLOSE" if ok else "ROUND_MAY_NOT_CLOSE",
        "closed_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "lanes_used": lanes_used,
        "blocking_tts_open": [t["tt_id"] for t in blocks],
        "claims_checked": ledger.get("checked", 0),
        "problems": problems,
        "rule": "a round may not close while it owes a blocking TT, a claimed lane has no receipt, "
                "or a MEASURED claim rests on a derived artefact",
    }
    if args.json_out:
        out = pathlib.Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
        receipt["written"] = str(out)
        receipt["digest"] = hashlib.sha256(out.read_bytes()).hexdigest()
    print(json.dumps({k: receipt[k] for k in ("verdict", "round", "blocking_tts_open", "problems")},
                     ensure_ascii=False))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
