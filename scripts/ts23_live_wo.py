"""Record the TS23 dogfood change in the LIVE spine, with the verdict the evidence supports.

The subagent ran the native chain against an isolated spine backup because the live DB was outside its write roots.
This creates the live record: same requirement/taskspec/workorder shape, verdict FAIL, because the acceptance step
needs an independent principal and no independent reviewer ever read the artefacts.
"""
from __future__ import annotations
import json
from pathlib import Path
from hg_kseos.spine import SharedSpine

HGK = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS")
REQ, TS, WO = "REQ-R14-TS23-M2-TRIAD", "TS-R14-TS23-M2-TRIAD", "WO-R14-TS23-M2-TRIAD"
spine = SharedSpine(HGK / "var/shared-spine/hg-kseos.db")
with spine.connect() as con:
    have = con.execute("SELECT 1 FROM workorders WHERE workorder_id=?", (WO,)).fetchone()
if have:
    with spine.connect() as con:
        print(json.dumps({"existing": con.execute("SELECT state FROM workorders WHERE workorder_id=?", (WO,)).fetchone()["state"]}))
    raise SystemExit(0)
with spine.connect() as con:
    req = con.execute("SELECT 1 FROM requirements WHERE requirement_id=?", (REQ,)).fetchone()
if req is None:
    with spine.transaction() as conn:
        conn.execute(
            "INSERT INTO requirements (requirement_id,project_id,source_locator,wording,priority,state,version,"
            "acceptance_id,rollback_pointer,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (REQ, "HGK-P0", "SBL_R14_POST_R13 order R14-TS23",
             "A maintainer must be able to see, before publishing, which files a bounded change touched and which "
             "checks it would break - computed from the change itself rather than from a plan.", 1, "FROZEN", 1,
             "ACC-R14-TS23", "RB-REQ-R14-TS23-M2-TRIAD", "2026-10-22T00:00:00Z", "2026-10-22T00:00:00Z"))
with spine.connect() as con:
    ts = con.execute("SELECT 1 FROM taskspecs WHERE taskspec_id=?", (TS,)).fetchone()
if ts is None:
    spine.create_taskspec(
        taskspec_id=TS, requirement_id=REQ,
        objective="Generate, install and use three small programs (CLI_TOOL, AGENT_SKILL, SIMPLE_AGENT) for the "
                  "requirement, each with a red->green test, then have an INDEPENDENT principal accept them.",
        owner="CODEX_MAKER_R14", writable_root=Path(r"C:/Projects/Agent_Workspace/_r14_packet/raw/ts23_sandbox"),
        permissions={"scope": ["ts23_sandbox/**"], "approval_ref": "SBL_R14_POST_R13 R14-TS23",
                     "deployment": "FORBIDDEN"}, tests=["ts23-newlines", "ts23-headings", "ts23-review"],
        evidence_plan="raw/ts23_m2_dogfood.json plus the red->green per program")
with spine.connect() as con:
    wo = con.execute("SELECT 1 FROM workorders WHERE workorder_id=?", (WO,)).fetchone()
if wo is None:
    spine.create_workorder(workorder_id=WO, taskspec_id=TS, writer="codex",
                           worktree=Path(r"C:/Projects/Agent_Workspace/_r14_packet/raw/ts23_sandbox"),
                           base_head="2dde2d84a2a6d95ccc6acb9356570bed68ab2f05")
r = spine.record_workorder_result(
    WO, writer="codex", checker="openai-codex/gpt-6.1-sol", verdict="FAIL",
    evidence_refs=["raw/ts23_m2_dogfood.json", "raw/ts23_live_wo_note.md"])
out = Path(r"C:/Projects/Agent_Workspace/_r14_packet/raw/ts23_live_wo.json")
out.write_text(json.dumps({"schema": "SBL-TS23-LIVE-WO/1", "workorder": WO, "result": r,
                           "verdict_reason": "artifacts verified working by the orchestrator; acceptance requires an "
                                             "independent principal and none reviewed the artefacts",
                           "claim_ceiling": "M2 not passed; no semantic completeness; no M3 work"},
                          indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({"workorder": WO, "verdict": r.get("verdict"), "state": r.get("state")}, ensure_ascii=False))
