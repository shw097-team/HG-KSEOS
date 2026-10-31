"""Set the session /goal for the FHS-MSC R19 round (same persistence the `/goal` command uses)."""
import os
import sys
from datetime import datetime, timezone

HOME = os.environ.get("HERMES_HOME") or r"C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes"
sys.path.insert(0, os.path.join(HOME, "hermes-agent"))

from hermes_cli import goals as G  # noqa: E402

SESSION_ID = sys.argv[1]

headline, contract = G.parse_contract(
    "R19：接續並完成 FHS-MSC Skeleton+Spine r2-revision2 的實作與檢驗（22 個 WP-FHS typed DAG）。\n"
    "outcome: 每個仍 actionable 的 WP 以真實收據前進（DONE 需證據可重跑；HOLD 需具名 owner + "
    "next_legal_action + resume_predicate），並把本回合實作、測試、證據索引、SHA 與重現指令推到指定 Repo 的候選分支 + PR。\n"
    "verification: 凍結主體逐檔 sha256 重驗；候選 validate.py 與 96 格 oracle 在隔離副本重跑並與宣稱比對；"
    "每個 DONE 的證據路徑存在且可重跑；native 效果若無 Issuer PERMIT 以 typed refusal 證明 gate 會拒收。\n"
    "constraints: 只候選、不動 main、不 force-push、不 merge/tag/release；不自我驗收、不共用 maker/checker principal；"
    "不自造 Issuer/Permit/Registry revision；來源 bytes 唯讀；Raw/DB/Key/Token 不上推。\n"
    "boundaries: 缺 native PERMIT 的 L2/L3/L4 效果只能 PARK 並記錄恢復指標；不以 advisory 或自測冒充獨立 PASS。\n"
    "stop_when: ledger 無 actionable AGENT 列，只剩具名 HARD blocker（缺憑證/指定車道不可用/不可復原破壞）。"
)

state = G.GoalState(goal=headline or "FHS-MSC R19", status="active")
state.contract = contract
state.created_at = datetime.now(timezone.utc).timestamp()
state.subgoals = [
    "R18 -> R19 狀態逐列對帳（ledger/FINAL_WP_STATE/DRIVER_STATE 不一致修正）",
    "凍結主體 83/83 sha256 + validate.py fresh 重跑",
    "WP-05 PIPD 編譯器真 writer ACK",
    "WP-19 SBOM/secret 可重算",
    "WP-18 SOURCE-BYTES-UNCHANGED 真 bounded repair（red-patch-green-unpatch-red）",
    "WP-06 真實可逆 repo diff + 回滾",
    "WP-15/16 原 sbl-tpm-sp invoke 收據",
    "WP-21/09 96 格 oracle 重算 + 獨立 checker verdict",
    "native 權限：owner 信封 + registry 修訂計畫（不自簽）",
    "FAR：殘餘阻斷裁決",
    "交付：真血統分支 + commit + push + PR",
    "STATUS/HANDOFF + RESUME_HERE + SESSION_STATE",
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
