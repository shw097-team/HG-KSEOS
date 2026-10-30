"""R14-TS15 — make the engine route the three kinds the order names, under a real HGK WorkOrder.

The order rejects "fixtures exist" as evidence. Two of the three kinds (AGENT_SKILL, SIMPLE_AGENT) raise
SBL_E_UNKNOWN_KIND, and CLI_TOOL already routes. Changing a product repo is not something the round may do silently,
so this issues the native chain first (FROZEN requirement -> TaskSpec -> WorkOrder), then the edit is made under that
WorkOrder and the result is recorded through record_workorder_result with writer != checker.
"""
from __future__ import annotations
import json
from pathlib import Path

from hg_kseos.spine import SharedSpine

HGK = Path(r"C:/Projects/Agent_Workspace/HG-KSEOS")
SBL = Path(r"C:/Projects/Agent_Workspace/SBL")
DB = HGK / "var/shared-spine/hg-kseos.db"
OUT = Path(r"C:/Projects/Agent_Workspace/_r14_packet/raw/ts15_wo.json")
REQ, TS, WO = "REQ-R14-TS15-KINDS", "TS-R14-TS15-KINDS", "WO-R14-TS15-KINDS"


def main() -> int:
    import subprocess
    head = subprocess.run(["git", "-C", str(SBL), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    spine = SharedSpine(DB)
    with spine.connect() as con:
        have_req = con.execute("SELECT state FROM requirements WHERE requirement_id=?", (REQ,)).fetchone()
    if have_req is None:
        with spine.transaction() as conn:
            conn.execute(
                "INSERT INTO requirements (requirement_id,project_id,source_locator,wording,priority,state,version,"
                "acceptance_id,rollback_pointer,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (REQ, "HGK-P0", "SBL_R14_POST_R13 order R14-TS15", 
                 "The engine must route CLI_TOOL, AGENT_SKILL and SIMPLE_AGENT requirement kinds.", 1, "FROZEN", 1,
                 "ACC-R14-TS15", f"RB-{REQ}", "2026-10-22T00:00:00Z", "2026-10-22T00:00:00Z"))
    with spine.connect() as con:
        have_ts = con.execute("SELECT 1 FROM taskspecs WHERE taskspec_id=?", (TS,)).fetchone()
    if have_ts is None:
        spine.create_taskspec(
            taskspec_id=TS, requirement_id=REQ,
            objective="Route three new requirement kinds to a permitted build target; no second router.",
            owner="CODEX_MAKER_R14", writable_root=SBL,
            permissions={"scope": ["sbl_core/m03_routing.py", "tests/test_core_modules.py"],
                         "approval_ref": "SBL_R14_POST_R13 R14-TS15", "deployment": "FORBIDDEN"},
            tests=["tests/test_core_modules.py::test_route_known_kinds",
                   "tests/test_core_modules.py::test_unknown_kind_raises"],
            evidence_plan="raw/ts15_kinds_test.log plus the workorder row in the shared spine")
    with spine.connect() as con:
        have_wo = con.execute("SELECT 1 FROM workorders WHERE workorder_id=?", (WO,)).fetchone()
    if have_wo is None:
        spine.create_workorder(workorder_id=WO, taskspec_id=TS, writer="codex", worktree=SBL, base_head=head)
    with spine.connect() as con:
        row = con.execute("SELECT state,base_head FROM workorders WHERE workorder_id=?", (WO,)).fetchone()
    doc = {"schema": "SBL-TS15-WORKORDER/1", "requirement": REQ, "taskspec": TS, "workorder": WO,
           "workorder_state": row["state"], "base_head": row["base_head"], "sbl_head": head,
           "writable_scope": ["sbl_core/m03_routing.py", "tests/test_core_modules.py"],
           "claim_ceiling": "the chain exists; the change itself is not made by this script"}
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: doc[k] for k in ("workorder", "workorder_state", "base_head")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
