"""R14-TS30 — issue the M4 verdict from the ledger rather than from prose.

M4 is the terminal gate. It can only pass if the levels below it passed, so the verdict is computed: every obligation
is read from OBLIGATIONS.json, grouped by state, and each residual gap is named with the principal who owns it. A
ledger that still holds PARTIAL or BLOCKED rows cannot yield PASS, and this script says so instead of being argued with.
"""
from __future__ import annotations
import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

OUT = Path(r"C:/Projects/Agent_Workspace/_r14_packet/raw")
LEDGER = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS/var/R14-OBLIGATIONS/OBLIGATIONS.json")

OWNER = {
    "R14-TS10": "SBL tooling owner (four vendor verbs do not exist)",
    "R14-TS11": "host owner (install a third-party scanner set)",
    "R14-TS12": "host owner (three plugin surfaces HOST_PENDING)",
    "R14-TS13": "PIPD bundle owner (two schema-only negatives)",
    "R14-TS17": "PIPD bundle owner + suite owner (66 declared-only rows)",
    "R14-TS19": "document archive owner (upstream 全DOC藍圖(8).md absent on this host)",
    "R14-TS20": "document archive owner (upstream SpecBuild v2.0r1(1).md absent) + inventory author (single digest column)",
    "R14-TS23": "independent reviewer / Owner (M2 acceptance never happened)",
    "R14-TS25": "SWOF Native Owner (no W3 permit)",
    "R14-TS26": "SWOF Native Owner (depends on TS25)",
    "R14-TS27": "PIPD Source Owner (semantic denominator unsigned)",
    "R14-TS28": "release owner (candidate branch has no remote)",
    "R14-TS29": "SBL owner (D-19 needs an owner-defined canonical list) + host owner (CR authority)",
}


def main() -> int:
    led = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = led["items"]
    by_state: dict[str, list[dict]] = defaultdict(list)
    for it in items:
        by_state[it["state"]].append(it)
    not_done = [it for it in items if it["state"] != "DONE"]
    verdict = "PASS" if not not_done else "BLOCKED"
    rows = []
    for it in sorted(not_done, key=lambda x: x["id"]):
        rows.append({"id": it["id"], "state": it["state"], "title": it.get("title", ""),
                     "residual": it.get("next_action") or "(none recorded)", "owner": OWNER.get(it["id"], "unassigned")})
    m_levels = {
        "M1": {"status": "SIGNED", "evidence": "raw/ts22_m1_gate_packet.json",
               "note": "4/4 levels measured; signed under the Owner's explicit authorization"},
        "M2": {"status": "NOT_PASSED", "evidence": "raw/ts23_live_wo.json",
               "note": "the dogfood change works and was re-run here, but no independent principal accepted it; the live "
                       "spine records WO-R14-TS23-M2-TRIAD verdict FAIL"},
        "M3": {"status": "BLOCKED", "evidence": "raw/ts24_w3_route_out.json",
               "note": "no W3 permit exists by field signature (0 hits); route-out written, nothing claimed"},
        "M4": {"status": "BLOCKED", "evidence": "this verdict",
               "note": "cannot pass while M2 is not passed and M3 is blocked"},
    }
    doc = {"schema": "SBL-R14-TS30-M4-VERDICT/1",
           "issued_at_utc": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
           "verdict": verdict,
           "counts": {s: len(v) for s, v in sorted(by_state.items())},
           "total": len(items),
           "milestones": m_levels,
           "residual": rows,
           "claim_ceiling": ("M4 is NOT passed. SBL_FULL_PRODUCT is NOT complete, no semantic completion percentage may "
                             "be quoted (TS27 denominator unsigned), and no DOC-00..13 semantic acceptance is claimed. "
                             "What is claimed: 17 obligations closed with their own receipts, M1 signed, one real "
                             "WorkOrder chain executed end to end, and every remaining gap named with its owner."),
           "next_owner_action": [r for r in rows if r["state"] in ("BLOCKED", "BLOCKED_SOFT")]}
    (OUT / "ts30_m4_verdict.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = ["# R14 — TS30: the M4 verdict", "",
             f"**Verdict: {verdict}.** M4 does not pass, so `SBL_FULL_PRODUCT` is not complete.", "",
             f"Issued {doc['issued_at_utc']} from the obligation ledger ({doc['total']} rows): "
             + ", ".join(f"{k} {v}" for k, v in doc["counts"].items()) + ".", "",
             "## The four gates, as measured", "",
             "| Gate | Status | Why |", "|---|---|---|"]
    for k, v in m_levels.items():
        lines.append(f"| {k} | **{v['status']}** | {v['note']} |")
    lines += ["", "## What still stands between here and M4", "",
              "| Obligation | State | Residual gap | Who can close it |", "|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['id']} | {r['state']} | {r['residual']} | {r['owner']} |")
    lines += ["", "## Claim ceiling", "", doc["claim_ceiling"], "",
              "## Why this is not rounded up", "",
              "A terminal verdict computed from a ledger cannot be better than the ledger. Every row above was closed only "
              "by a receipt the audit could resolve; the rows that remain are the work, not a reporting gap. Three of them "
              "(TS25/26/27) need a signature that belongs to another principal, two need an artifact this host does not "
              "have, and one (TS23) needs an independent reviewer to read what was built.", ""]
    (OUT / "ts30_m4_verdict.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"verdict": verdict, "counts": doc["counts"], "residual_rows": len(rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
