"""Settle TT-EXECUTE-TRANSPORT-MISSING-SESSION-001 through the typed spine API.

FAR-20261031-029 / decision FAR-029-DECISION-01: the ticket's close criterion is "the EXECUTE lane is
served end to end at the ordered arm", and the round that met it is measured, not asserted:

  C:/wg/probe/exec_delta1_receipt.json
    lane EXECUTE, rank 1, served opencode-go/deepseek-v4.1-flash, exit 0, nonce present,
    usage_receipt_ok true, asked == served, console_window_events_delta 0.

The evidence is registered first and the ticket is closed against that registration, so the transition
carries a locator + digest rather than a sentence.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(r"C:/Projects/Agent_Workspace/HG-KSEOS")
sys.path.insert(0, str(ROOT / "src"))

from hg_kseos.spine import SharedSpine  # noqa: E402

RECEIPT = pathlib.Path(r"C:/wg/probe/exec_delta1_receipt.json")
TT = "TT-EXECUTE-TRANSPORT-MISSING-SESSION-001"
EVIDENCE_ID = "EV-EXECUTE-LANE-SERVED-MIMO-ERA-20261031"

receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
att = (receipt.get("attempts") or [{}])[0]
measured = {
    "lane": "EXECUTE",
    "rank": att.get("rank"),
    "model": att.get("model"),
    "exit": att.get("exit"),
    "nonce_present": att.get("nonce_present"),
    "usage_receipt_ok": att.get("usage_receipt_ok"),
    "console_window_events_delta": att.get("console_window_events_delta"),
}
assert measured["rank"] == 1, f"not rank 1: {measured}"
assert measured["exit"] == 0, f"not served: {measured}"
assert measured["nonce_present"] and measured["usage_receipt_ok"], f"receipt incomplete: {measured}"
assert measured["console_window_events_delta"] == 0, f"a window was emitted: {measured}"

sha = hashlib.sha256(RECEIPT.read_bytes()).hexdigest()
spine = SharedSpine(ROOT / "var" / "shared-spine" / "hg-kseos.db")
spine.register_evidence(EVIDENCE_ID, "lane_receipt", str(RECEIPT), sha, producer="hgk-lane-dispatch")
try:
    spine.close_tt(TT, EVIDENCE_ID)
    outcome = "CLOSED"
except Exception as exc:  # noqa: BLE001 - a already-closed ticket is a fact, not a crash
    outcome = f"NOT_CLOSED: {type(exc).__name__}: {exc}"

print(json.dumps({"tt": TT, "outcome": outcome, "evidence_id": EVIDENCE_ID, "sha256": sha,
                  "measured": measured}, ensure_ascii=False, indent=1))
