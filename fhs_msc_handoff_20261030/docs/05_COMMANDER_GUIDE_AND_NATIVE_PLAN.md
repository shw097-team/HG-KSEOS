<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 05 COMMANDER GUIDE AND NATIVE PLAN｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。




## HANDOFF-v1｜Hermes 普通 Goal 自主續工入口

接收端先讀交付根 `HANDOFF_README.md` 與 `02_FIRST_WORK/TaskSpecSeed.json`，驗 `CURRENT_READER_SCOPE.json` 與 SHA Manifest，沿原 TPM/PIPD/PLAN接收這句普通 Goal：「依 WP-FHS-15 讀既有來源和已知答案，於允許隔離草稿區產生三 SPEC；ProviderOff=true；只作 SOURCE_READ/LOCAL_DRAFT。」不要求使用者再貼 B1 長 Prompt、重問已知授權或等待全7649子項完成。

KnownAnswer key綁 subject/source_sha/scope/question，未過期即重用；本輪實測重問=0。來源改變只 invalidate依賴它的 SPEC/PI，其他 READY繼續。PLANNED TQAEP 不索尚不存在的 live checker receipt；傳給下游的每個功能 Atom都有自己的 Consumer、POS/NEG，不用上輪44條身份投影取代。

接到合法原 HGK Canonical WorkOrder後，Hermes將其真 WorkID與原 Hermes task_id作受權關聯記錄，沿既有 Queue/Lease/Journal繼續；原 TaskSpec/WO constructor不會替你創造可用 Permit，亦不宣稱 create_workorder 的 Python回傳值就是 WorkID。原 Canonical readback才證明該 WorkID存在。

## 本輪同域受影修復：r2 §1.3 角色與 Guide 入口

### 1.3 三 SP：Portable 與 Native 雙形態，不混 Writer／Checker

| SP／形態 | 觸發與操作→結果 | 原消費者、限制與失敗 |
|---|---|---|
| **TPM-SP Portable** | Goal/Source/K0–K3 Readset→Product/Architecture/Program 三 SPEC 候選、QuestionDelta、18 Stage 的 Proposal | PIPD Intake／原 TPM Writer；不可把 Skill 記錄當正式 PI/PD。缺 Reader 只停受影 SPEC。 |
| **Native FHS-TPM** | 已准入的 PLAN WorkOrder→原 PLAN Role/Revision CAS→同 WorkID 的真 PlanRevision | 原 HGK PLAN Consumer；沒有真 Registry/Permit 不自稱 Native Stage Done。 |
| **Commander-Skill Portable** | 使用者選擇 A/B/C Guide、合法 Work Plan Scope→Program Action Proposal/NeedInfo | 原 PLAN Producer 或原 PIPD；不建立新的 Executor Queue，不重問已有 Decision。 |
| **Native FHS-Commander** | 有權原 PLAN／Guide Request→原 Writer CAS Replan/Scope/Epoch→同 WorkID 可恢復 Cursor | 原 HGK/TPM；沒有原 Enum/Adapter 則 `COMMANDER_ABI_HOLD`，不得製作新 issuer。 |
| **Acceptance Challenge-SP Portable** | Frozen Readset/CaseSpec→有界異構 Review／Attack Finding→Advisory Inbox | 原 AO/Challenge Consumer；外部模型不同不等於獨立 principal。 |
| **Native FHS-Acceptance Challenge** | 原有保護的 Raw/Oracle/Checker Principal→15 異構 AC Edge、適用 96 Oracle 的 Verdict→原 Reducer | Maker 不能改 Oracle／簽 Verdict；不以 Portable Skill Finding 作獨立 PASS。 |


---




## 本版未受影條文（完整沿用、當期生效）

## R2-05-ABC：Guide 與 Native PLAN 的反循環輸入

A READONLY：Portable Guide 讀 frozen SPEC/PI/PD/ECP/TQAEP、原 CurrentRevisionReader，回 PlanRevisionProposal；不需要它尚未建立的 WorkOrder，不能寫 Target Repo。B ADVISORY_LOCAL_WRITE：只在本輪隔離建議目錄記 proposal/diff，effect=LOCAL_DRAFT_WRITE；交原非 legacy Native PLAN Producer，CAS(base_revision,proposal_hash) 必得真 Writer ACK。C 若 A/B 缺權限或 loader，PARK 受影寫入，保留 source/ref/first_fail；不能呼叫已停用 sbl-commander-sp。

Probe 次序：確認 Host skill manifest+trigger/nontrigger→讀 loaded SHA（檔案在磁碟不是 loaded）→讀 Native PLAN schema/revision/reducer→檢同 Subject→submit proposal 只在原 Producer 能力和權限已存在時。Guide 不自行落 native WorkOrder，原 PLAN Writer 選合法 ready card，原 Issuer 後續准入。

POS：Reader 得 revision r，proposal base=r，原 Writer ACK r+1；NEG：base=r-1 → PLAN_CAS_NACK，不覆寫別人的 revision。POS：無 effect 權限仍可產唯讀計畫；NEG：為取得首 WorkOrder 先要求同 WorkOrder permit → BOOTSTRAP_DEPENDENCY_INVERSION。退出只撤本輪 proposal，不改原 PLAN state。

## R2-05-ACTUAL-PLAN：原Source入口讀回

| path/SHA | symbol/signature | interpretation |
|---|---|---|
| C:\Projects\Agent_Workspace\HG-KSEOS\src\hg_kseos\lifecycle.py / 5d4d03356d00c7e19299b7b3d5ddb4cd6dc202d80f164988ef70c033c528c684 | __init__(self, spine: SharedSpine) @L101; admit_workorders(self, project_id: str, *, admission_bundles: dict &#124; None=None) @L332; admit_requirement(self, project_id: str, requirement_id: str, wording: str, *, owner: str='owner', priority: str='P1', admission_bundles: dict &#124; None=None) @L574; completion_sweep(self, project_id: str) @L638 | 只讀AST入口；未調用admit/authorize或改state |
| C:\Projects\Agent_Workspace\HG-KSEOS\src\hg_kseos\native_admission.py / 314eeacd207c6808dfa7ddcf5ef12092861eeb2ff96b24ec5a216970fc889440 | hold_snapshot(self) @L245; authorize(self, connection, operation, request, bundle) @L445 | 只讀AST入口；未調用admit/authorize或改state |
| C:\Projects\Agent_Workspace\HG-KSEOS\src\hg_kseos\role_binding.py / 94084205266e1a841ce0f9be1696813085ef26fbda48ade830cf5f66eff2b938 | load_canonical_binding(spine: Any, workorder_id: Any) @L118; find_session_binding(spine: Any, session_id: Any) @L181 | 只讀AST入口；未調用admit/authorize或改state |

已讀原HGK `profiles/construction-commander/README.runtime-contract.md`：Denied candidate write / AcceptanceReceipt / promotion / release。本候選Guide只產隔離proposal，該profile本身不因此獲Writer權。Native PLAN Producer/CurrentRevisionReader若未有真binding仍C PARK，不回叫legacy。這個來源契約不保證現役Host已Loaded。
