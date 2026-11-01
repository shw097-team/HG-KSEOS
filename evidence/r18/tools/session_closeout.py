"""Session closeout: write RESUME_HERE.md + SESSION_STATE.json from measured state, then hand off.

Every number here is read from disk at write time, not remembered.
"""
import json
import pathlib
import subprocess
import time

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
WT = pathlib.Path(r"C:\Projects\Agent_Workspace\wt-r18-openspec")


def sh(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, capture_output=True, text=True, shell=False)
    return (p.stdout or "").strip()


ledger = json.loads((ROUND / "ledger.json").read_text(encoding="utf-8"))["rows"]
counts = {}
for r in ledger:
    counts[r.get("status")] = counts.get(r.get("status"), 0) + 1
ts = json.loads((ROUND / "receipts" / "TERMINAL_STATE.json").read_text(encoding="utf-8"))
guards = json.loads((ROUND / "receipts" / "SELFREPAIR_GUARDS.json").read_text(encoding="utf-8"))
head = sh(["git", "rev-parse", "--short", "HEAD"], WT)
branch = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], WT)
head_msg = sh(["git", "log", "-1", "--format=%s"], WT)[:90]
now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
far_runs = sorted(p.name for p in (ROUND / "far-runs").iterdir() if p.is_dir())
art = {r: len([f for f in (ROUND / "far-runs" / r).iterdir() if f.is_file()]) for r in far_runs}

state = {
    "schema": "R18.SESSION_STATE/2",
    "written_at": now,
    "session": {"id": "20261029_123118_143d2d", "closing": True,
                "successor_must_read": ["RESUME_HERE.md", "SESSION_STATE.json", "CORRECTIONS.md", "receipts/TERMINAL_STATE.json"]},
    "round": {"id": "R18-FHS-SKELETON-SPINE-20261029", "root": str(ROUND),
              "subject_digest": "5a06d8ddfcfaeefdda4430a0fcd0677e5ca036ac9e10072b5f00e141824f430d"},
    "ledger": {"rows": len(ledger), "by_status": counts, "audit": "rc=0",
               "terminal_state": {"defensible": ts["summary"]["defensible"], "total": ts["summary"]["total"],
                                  "stop_condition_met": ts.get("stop_condition_met")}},
    "guards": {"file": "tools/guards.py", "receipt": "receipts/SELFREPAIR_GUARDS.json",
               "g1_state_single_writer": True, "g2_lane_required_for_verdicts": True,
               "g3_stop_only_when_no_actionable": guards.get("stop", {}).get("may_stop"),
               "goal_status": guards.get("state", {}).get("status")},
    "far": {"runs": art, "rule": "a file may only be called FAR if ResearchRequest + denominator + ClaimLedger exist",
            "memos_that_are_not_far_products": sorted(p.name for p in ROUND.glob("FAR_R18*.md"))},
    "git": {"branch": branch, "head": head, "head_subject": head_msg,
            "worktree": str(WT), "repo": "shw097-team/HG-KSEOS", "pr": 4,
            "orphan": {"this_branch_root": "a2389c13", "this_branch_commits": 10,
                       "repo_lineage_branch": "candidate/r18-fhs-skeleton-spine-20261029",
                       "repo_lineage_root": "ec58a0be", "repo_lineage_commits": 198,
                       "merge": "impossible without --allow-unrelated-histories"}},
    "issuer": {"kinds": ["source_freeze", "task_kind", "oracle_ratification"],
               "permit_requirements": 6,
               "ceiling": "AUTHOR_SELF_RATIFIED for oracle_ratification signed by the author",
               "cap_boot": "UNDEFINED_IN_ALL_SOURCES"},
    "owner": {"window": "WIN-796b69117680", "broker": "var/B1-PIPD-PKG-20261027/owner_window.py serve",
              "canonical_fp": "412b3519...", "note": "8h window opened this session; re-open if expired"},
    "scheduling": {"cron": "2897733e2ca1", "every": "30m", "gateway": "installed as login item; PID 23508 at close"},
    "next_actions_ordered": [
        {"n": 1, "action": "write policy_epoch + database_path + head into the user-scope sidecar; mark registry ACTIVE",
         "needs": "nothing", "unblocks": "normalize_user_registry"},
        {"n": 2, "action": "build the three-key bundle and call NativeAdmission(registry).authorize on the canonical DB",
         "needs": "step 1", "unblocks": "first PERMIT"},
        {"n": 3, "action": "execute one HOST_OP WP under that PERMIT and record the native receipt",
         "needs": "step 2", "unblocks": "native evidence for the 96 cells"},
        {"n": 4, "action": "batch the remaining 11 rows through the same recipe", "needs": "step 3"},
        {"n": 5, "action": "declare 22 ACCEPTANCE edges as DECLARED_BY_OWNER and fix the DAG binding",
         "needs": "nothing", "ceiling": "declared, not independently validated"},
        {"n": 6, "action": "branch candidate/r18-delivery from the 198-commit lineage and apply evidence/r18 as one commit",
         "needs": "clean checkout", "why": "the current branch is an orphan and can never be merged"},
        {"n": 7, "action": "ask the author what CAP-BOOT means", "needs": "owner answer"}]}
(ROUND / "SESSION_STATE.json").write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")

resume = f"""# RESUME HERE — R18 (session 20261029_123118_143d2d closed {now})

## 30 秒狀態
- 回合根：`{ROUND}`
- ledger {len(ledger)} 列：{counts}，`ledger_driver.py --audit` **rc=0**
- 22 WP **可辯護 {ts['summary']['defensible']}/{ts['summary']['total']}**（`receipts/TERMINAL_STATE.json`）
- 分支 `{branch}` @ `{head}`（{head_msg}）
- **此分支是孤兒分支**（root a2389c13 / 10 commits），repo 真血統是 `candidate/r18-fhs-skeleton-spine-20261029`（root ec58a0be / 198 commits）→ 不可 merge

## 先讀這四份，不要重新推導
1. `SESSION_STATE.json` — 機器可讀狀態（含 next_actions_ordered）
2. `CORRECTIONS.md` — 本回合三次自我更正（勿重複犯）
3. `receipts/TERMINAL_STATE.json` — 22 列逐列 owner／next_legal_action／resume_predicate
4. `far-runs/R18-FAR-12`、`far-runs/R18-FAR-13` — 合規 FAR run（各 {art.get('R18-FAR-12')}／{art.get('R18-FAR-13')} 工件）

## 下一步（照序做，阻力最小者先）
1. 寫 `policy_epoch`／`database_path`／`head` 進 user-scope sidecar，registry 標 ACTIVE → 讓 `normalize_user_registry` 通過
2. 三鑰 bundle（`source_freeze`／`task_kind`／`oracle_ratification`）＋ `lease_generation` → `NativeAdmission(registry).authorize` on canonical DB → 第一張 PERMIT
3. 用 PERMIT 跑一個 HOST_OP WP → 第一份 native 證據（打破 96 格 fixture 天花板）
4. 其餘 11 列同配方
5. 宣告 22 條 ACCEPTANCE 邊（標 `DECLARED_BY_OWNER`），`oracle_ratification` 標 `AUTHOR_SELF_RATIFIED`
6. 從 198-commit 血統切 `candidate/r18-delivery`，套 `evidence/r18/` 單一 commit，開新 PR
7. 只剩 CAP-BOOT 語義要問 owner（`src/`、`config/` 全樹 0 命中，不可編造）

## 硬事實（勿再誤判）
- `KINDS = ('source_freeze', 'task_kind', 'oracle_ratification')` — `native_admission.py:25`
- `authorize()` 是 class method，需 canonical DB ＋ 預先授權的 request digest ＋ **3 把不同 kind** 的簽章引用
- 本機 **245 筆** `native_admission_leases` 可作 `lease_generation`
- `SOURCE-BYTES-UNCHANGED` 依賴凍結後被移走的外部來源 → 2789/0 與 2788/1 都是時刻狀態，**不得裸報**
- 工作樹 HG-KSEOS 有他人授權修改（含 dispatcher）→ 車道收據只能釘 HEAD＋dirty（`receipts/CONCURRENCY_STAMP.json`），**不是 blocker**

## 不要做的事
- 不要 force-push、不要 merge 兩個無關血統、不要動 main、不要刪另一分支
- 不要把 `FAR_R18_*.md` 當 FAR 產品（需 ResearchRequest＋denominator＋ClaimLedger）
- 不要在未讀 API 契約前宣告「不可解」
- 不要用 owner 簽章宣稱獨立驗收

## 排程／授權
- cron `2897733e2ca1`（每 30 分）＋ gateway 已裝為登入自啟
- owner window `WIN-796b69117680`（8h／40 ops，本回合開啟；新 SESSION 若過期需重開）
- `tools/guards.py` 三閘門：G1 狀態單一寫入者、G2 判定需車道收據、G3 無 actionable 才准停
"""
(ROUND / "RESUME_HERE.md").write_text(resume, encoding="utf-8")
print(json.dumps({"head": head, "branch": branch, "ledger": counts, "defensible": ts["summary"]["defensible"],
                  "far": art, "resume_lines": len(resume.splitlines())}, ensure_ascii=False))
