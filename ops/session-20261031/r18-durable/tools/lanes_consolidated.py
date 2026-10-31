"""Consolidate every lane attempt of this round into one attributable table.

Sources: each dispatch's own *.attempts.ndjson (per-attempt rank, arm, exit, nonce, usage). Nothing is
taken from the model's prose. Two controls are recorded explicitly because otherwise the table would be
unfalsifiable:
  * a rank-3 out-of-spec arm once SERVED with a valid nonce - so "nonce present" alone does not prove
    the required arm ran, only the arm column does;
  * a bounded writer's destructive cleanup command was refused by policy mid-run - so the sandbox is not
    decorative, and that refusal is evidence, not an error to hide.
"""
import glob
import json
import os
from pathlib import Path

ROUND = Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
REQ = {"PLAN": "GPT 6.1 Sol medium / OpenAI OAuth",
       "EXECUTE": "DeepSeek V4.1 Flash / OpenCode Go",
       "VERIFY_SECURITY": "GPT 6.1 Sol medium / OpenAI OAuth"}

rows = []
for path in sorted(glob.glob(str(ROUND / "**" / "*.ndjson"), recursive=True)):
    for line in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        if "lane" not in d:
            continue
        rows.append({
            "receipt": os.path.basename(path), "at_utc": d.get("at_utc"), "lane": d.get("lane"),
            "rank": d.get("rank"), "arm": d.get("transport_model") or d.get("model"),
            "exit": d.get("exit"), "seconds": d.get("seconds"), "nonce_present": d.get("nonce_present"),
            "usage_receipt_ok": d.get("usage_receipt_ok"),
            "stderr_tail": (d.get("stderr_tail") or "")[:180].replace("\n", " | "),
        })

served = [r for r in rows if r["nonce_present"] and r["exit"] in (0, "OK", "COMPLETED")]
by_lane = {}
for lane in REQ:
    lane_rows = [r for r in rows if r["lane"] == lane]
    good = [r for r in lane_rows if r in served]
    by_lane[lane] = {
        "required_arm": REQ[lane],
        "attempts": len(lane_rows),
        "served_attempt": ({"rank": good[-1]["rank"], "arm": good[-1]["arm"],
                            "seconds": good[-1]["seconds"]} if good else None),
        "required_arm_satisfied": bool(good) and good[-1]["arm"] == {"PLAN": "gpt-6.1-sol",
                                                                    "VERIFY_SECURITY": "gpt-6.1-sol",
                                                                    "EXECUTE": "opencode-go/deepseek-v4.1-flash"}[lane],
        "out_of_spec_serves": [{"rank": r["rank"], "arm": r["arm"]} for r in good
                               if r["arm"] != {"PLAN": "gpt-6.1-sol", "VERIFY_SECURITY": "gpt-6.1-sol",
                                               "EXECUTE": "opencode-go/deepseek-v4.1-flash"}[lane]],
    }

policy_blocks = [r for r in rows if "blocked by policy" in ((r.get("stdout_tail") or "") + (r["stderr_tail"] or ""))]
receipt = {
    "schema": "R18.LANES.CONSOLIDATED/1",
    "session_pin_is_not_a_lane_binding": True,
    "session_pin": "deepseek-v4.1-flash on opencode-go (this chat's model) - never used as lane evidence",
    "by_lane": by_lane,
    "controls": {
        "out_of_spec_arm_served_once": any(v["out_of_spec_serves"] for v in by_lane.values()),
        "reading": "an out-of-spec arm did serve with a valid nonce earlier in the round, which is why the "
                   "qualifying test is the served ARM column, not the presence of a nonce",
        "destructive_command_refused_by_policy": len(policy_blocks),
        "policy_block_example": (policy_blocks[0]["stderr_tail"] if policy_blocks else None),
    },
    "attempts": rows,
}
(ROUND / "receipts" / "LANES_CONSOLIDATED.json").write_text(
    json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "out_of_spec_serves"}
                  for k, v in by_lane.items()}, ensure_ascii=False, indent=1))
print("policy_blocks:", len(policy_blocks), "| attempts:", len(rows))
