"""Record the WO-R14-TS15-KINDS result through the governed acceptance gate (writer != checker)."""
from __future__ import annotations
import json
from pathlib import Path
from hg_kseos.spine import SharedSpine

HGK = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS")
spine = SharedSpine(HGK / "var/shared-spine/hg-kseos.db")
WO = "WO-R14-TS15-KINDS"
with spine.connect() as con:
    row = con.execute("SELECT state FROM workorders WHERE workorder_id=?", (WO,)).fetchone()
if row["state"] != "CREATED":
    print(json.dumps({"skipped": True, "state": row["state"]}))
    raise SystemExit(0)
r = spine.record_workorder_result(
    WO, writer="codex", checker="openai-codex/gpt-6.1-sol", verdict="PASS",
    evidence_refs=["raw/ts15_sbl_full2.log", "raw/ts15_wo.json", "SBL candidate/r14-ts15-kinds 10d510f"])
out = Path(r"C:/Projects/Agent_Workspace/_r14_packet/raw/ts15_result.json")
out.write_text(json.dumps({"schema": "SBL-TS15-WO-RESULT/1", "workorder": WO, "result": r,
                           "writer": "codex", "checker": "openai-codex/gpt-6.1-sol",
                           "claim_ceiling": "routing for the three kinds is real and tested; generation/installation/"
                                            "use of three new programs is still absent"},
                          indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({"state": r.get("state", "?"), "verdict": r.get("verdict", "?")}, ensure_ascii=False))
