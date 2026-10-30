#!/usr/bin/env python3
"""lane_evidence_gate — a round cannot claim a lane it did not dispatch.

The mandate "use three lanes" lived in the prompt and in no gate. EXECUTE and VERIFY left artefacts that
were checked; PLAN left nothing, so nothing noticed that it had never been dispatched — across every round
to date, `--lane PLAN` had been invoked zero times while the research was written by the session model,
which is the EXECUTE lane's model.

This gate makes a lane claim falsifiable. Given a dispatch receipt it verifies, fail-closed:

  lane            the receipt is for the lane the round claims
  served == asked the attempt reports the model that was actually asked for (no silent substitution)
  rank 1          the first attempt is the in-force primary arm, or --allow-rank names another
  ok + usage      the dispatch succeeded and the usage receipt parsed
  nonce           the round's nonce appears in the receipt
  exit 0          the attempt exited cleanly

Exit 0 = the lane was served as claimed. Exit 2 = it was not, with the reasons.
Read-only.
"""

from __future__ import annotations

import argparse
import json
import pathlib


def judge(receipt: dict, lane: str, nonce: str | None = None, allow_rank: int = 1) -> dict:
    problems: list[str] = []
    attempts = receipt.get("attempts") or []
    if not attempts:
        return {"verdict": "NO_ATTEMPT", "lane": lane, "problems": ["receipt carries no attempt"]}
    a = attempts[0]

    if receipt.get("lane") != lane:
        problems.append(f"lane_mismatch: receipt={receipt.get('lane')} claimed={lane}")
    if a.get("rank") != allow_rank:
        problems.append(f"rank_not_primary: rank={a.get('rank')} allowed={allow_rank}")
    if a.get("exit") != 0:
        problems.append(f"dispatch_exit_nonzero: exit={a.get('exit')}")
    if not receipt.get("ok"):
        problems.append("dispatch_not_ok")
    if not receipt.get("usage_receipt_ok"):
        problems.append("usage_receipt_not_ok")

    asked = receipt.get("used_transport_model")
    served = a.get("model")
    if asked and served and asked != served:
        problems.append(f"silent_substitution: asked={asked} served={served}")

    if nonce:
        blob = json.dumps(receipt, ensure_ascii=False)
        found = nonce in blob
        if not found and receipt.get("attempt_log_dir"):
            logdir = pathlib.Path(receipt["attempt_log_dir"])
            if logdir.is_dir():
                for f in logdir.glob("*.txt"):
                    try:
                        if nonce in f.read_text(encoding="utf-8", errors="replace"):
                            found = True
                            break
                    except OSError:
                        continue
        if not found:
            problems.append(f"nonce_not_echoed: {nonce}")

    return {
        "verdict": "LANE_SERVED_AS_CLAIMED" if not problems else "LANE_CLAIM_UNSUPPORTED",
        "lane": lane,
        "asked": asked,
        "served": served,
        "rank": a.get("rank"),
        "seconds": a.get("seconds"),
        "problems": problems,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="verify that a lane claim is backed by its dispatch receipt")
    ap.add_argument("receipt", help="JSON receipt written by hgk-lane-dispatch --json-out")
    ap.add_argument("--lane", required=True, help="PLAN | EXECUTE | VERIFY_SECURITY")
    ap.add_argument("--nonce", default=None, help="the round nonce that must appear in the receipt")
    ap.add_argument("--allow-rank", type=int, default=1, help="accept this rank as the serving arm")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    path = pathlib.Path(args.receipt)
    if not path.exists():
        print(json.dumps({"verdict": "RECEIPT_MISSING", "receipt": str(path)}))
        return 3
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"verdict": "RECEIPT_UNREADABLE", "detail": str(exc)[:200]}))
        return 3

    out = judge(receipt, args.lane, args.nonce, args.allow_rank)
    out["receipt"] = str(path)
    if args.json:
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(f"{out['verdict']}: {args.lane} asked={out.get('asked')} served={out.get('served')} rank={out.get('rank')}")
        for p in out["problems"]:
            print(f"  - {p}")
    return 0 if out["verdict"] == "LANE_SERVED_AS_CLAIMED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
