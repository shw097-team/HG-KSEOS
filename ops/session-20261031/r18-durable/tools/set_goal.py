"""Set the session /goal for the FHS-MSC R18 round (the /goal surface, programmatically).

Same persistence the `/goal` slash command uses: state_meta key `goal:<session_id>`.
"""
import os
import sys
from datetime import datetime, timezone

HOME = os.environ["HERMES_HOME"]
sys.path.insert(0, os.path.join(HOME, "hermes-agent"))

from hermes_cli import goals as G  # noqa: E402

SESSION_ID = sys.argv[1]

headline, contract = G.parse_contract(
    "執行 HERMES_FHS-MSC_SKELETON_SPINE_revision2_Native_Direct_Thin_Prompt_2026-10-29_r1："
    "以既有 WP-FHS-00..21 typed DAG 直接原生施工 FHS-MSC Skeleton+Spine，"
    "完成受影接線、必要實作、FAR 研究、測試、bounded repair、回歸、獨立驗收與交付。\n"
    "outcome: 22 個 WP 全部到達可辯護狀態（DONE/REUSE 需收據可解析；HOLD 需具名 owner、"
    "next_legal_action、resume_predicate），並產出一份 STATUS/HANDOFF 與四庫候選分支/commits/PR。\n"
    "verification: 每個 DONE 列的證據路徑必須存在且可重跑；候選自身 validate.py 與 96 格 oracle "
    "在隔離副本上重跑並與宣稱數字比對；獨立 checker 車道（不同 principal）對凍結候選出 verdict；"
    "native 效果若無 Issuer PERMIT 必須以 typed refusal 證明 gate 會拒收。\n"
    "constraints: 只候選、不動 main、不 force-push、不 merge/tag/release；不自我驗收、不共用 "
    "maker/checker principal；不把 gstack/Challenge/advisory 當 Independent PASS；"
    "來源 bytes 唯讀，全部工作在 var/R18-FHS-SKELETON-SPINE-20261029；"
    "Raw/DB/Key/Token/個資不上推。\n"
    "boundaries: 缺 native Issuer PERMIT 的 L2/L3/L4 效果只能 PARK 並記錄恢復指標，"
    "不得以候選 ECP/字串或舊 receipt 冒充；不得自造第二 Planner/Checker/Issuer/Queue。\n"
    "stop_when: KANBAN 全部卡片 reconciled 且 ledger 無 actionable AGENT 列，"
    "或只剩具名 HARD blocker（缺憑證/指定車道不可用/不可復原破壞）。"
)

state = G.GoalState(goal=headline or "FHS-MSC R18", status="active")
state.contract = contract
state.created_at = datetime.now(timezone.utc).timestamp()
state.subgoals = [
    "WP-00 來源/Manifest/ZIP/22-WP DAG 完整驗證（PASS 收據）",
    "SharedSpine：專案 + 22 條 requirement 凍結 + native gate 拒收證明",
    "KANBAN 22 張 WP 卡 + SWARM 平行驗證 + GSTACK route + OPENSPEC delta",
    "L0/L1 WP 真施工：WP-01/19/21/15/16/05/07/04 逐一收據",
    "候選自身 suites 重跑（validate.py 2789 / oracle96 679）與數字比對",
    "WP-18 bounded repair：紅→補→綠，殘留具名",
    "WP-09 獨立驗收（不同 principal，claim ceiling 明示）",
    "MVS01-10 本次真收據映射",
    "交付：四庫候選分支 + commit + push + PR（不 main/不 force）",
    "STATUS/HANDOFF + RESUME_HERE + 機器可讀狀態，Kanban 對帳",
]
state.gates = [
    G.GoalGate(command="python -B C:/Projects/Agent_Workspace/var/R18-FHS-SKELETON-SPINE-20261029/tools/ledger_driver.py --audit",
               timeout_seconds=300, max_retries=5),
]
G.save_goal(SESSION_ID, state)

back = G.load_goal(SESSION_ID)
print("saved goal for", SESSION_ID)
print("status:", back.status, "| subgoals:", len(back.subgoals), "| gates:", len(back.gates))
print("headline:", back.goal[:120])
print("contract fields set:", [k for k, v in back.contract.to_dict().items() if v])
