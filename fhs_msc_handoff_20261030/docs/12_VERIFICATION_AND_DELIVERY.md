<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 12 VERIFICATION AND DELIVERY｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。




## HANDOFF-v1｜最小交接靜態驗收與 ClaimCeiling

交付前只驗首工作必要閉包：原 Compiler/Reader真功能PI與TaskSpecSeed；原22WP圖無環/無futureReceipt前置；缺OPS僅PARK受影分支；source漂移、ProviderOff、舊Lease、UNKNOWN的原Reader/接收契約拒收或Reconcile。原5個受影測試重用，環境搜尋路徑與必需fixture修正後通過；本輪最小檢查35 PASS。所有命令、環境、exit、stdout/stderr/SHA保存於新證據，沒有重跑無關全庫測試。

一次輕量全局一致性回歸核完整17冊/14SBL升級冊、2221原ID唯一Locator、原負例與未受影內容保留、來源/Reader SHA、原DAG、Schema、relative links、原工作樹未改，最後兩ZIP各只正式封裝一次並逐檔讀回。成功只標`PIPD_CONSTRUCTION_HANDOFF_READY`，不得讀為NATIVE_ADMITTED、NATIVE_VERIFIED、INDEPENDENT_PASS或RELEASED。

## 本輪同域受影修復：r2 §11 身份回歸/四庫施工

## 11. 修補 BODY 17 份、四庫原位施工與真使用流程驗收

### 11.1 四庫真正該動的最小適用 Patch（只在原合法 Dev ECP 下寫入）

| 原庫／路徑 | Inputs→Original Entry／修補動作→Outputs | Dedicated Negative、阻斷與回退 |
|---|---|---|
| Fabric `FABRIC/fabric/consumers/hgk_policy_consumer.py` | 原 `FAB`/`load_router()` 以 Repo manifest approved Root 相對解析 `FABRIC/rp002/RP002_CHANGE_CLASS_ROUTER.yaml`，保留 `route_event` contract；回原 Policy Consumer | wrong root/traversal/junction NACK；`apply_preapproved` 只 Canary，不能當 Loaded/Consumed；回舊受信版本 |
| HGK `src/hg_kseos/providers.py` | 凍結 legacy `(57,50,7)` fixture，新 Hermes 原 `ProviderRegistry` 按 Version/Artifact Pin/CaseID/Security Invariants Qualification | 新版未知測試 fail 不能通過，舊版舊 Fixture 不被刪；回已合格 pin |
| HGK `src/hg_kseos/lane_route_resolver.py` ＋原 Launcher Locator | 原候選池只提供 Owner Pool／Runtime Failure Fallback 運算；由原 HGK 受保護 Registry/Launcher 執行（正式路徑未在本版證實） | Candidate ≠ Loaded；未有已核准 Host/Registry Binding→ABI_BIND_HOLD |
| HGK 原 Native Admission／Spine | 原 `SharedSpine.transaction()` 和受保護原 Issuer 綁 WorkID/Permit/Lease/Nonce/Operation；不拷 B1 snapshot 當生產 | stale generation/replay/cancel unknown effect NACK，Journal 保留 |
| SBL `sbl_harness/__init__.py` | `HGK_PIN` 已硬綁候選 registry/dispatcher path，修改為原 HGK 已批准 Launcher/Registry locator（不自行臆造新路徑） | 無真 Entry/ABI→HARNESS_BIND_HOLD；Adapter 不提供 permit_signing |
| SBL `sbl_core/modes.py` | 原 `ack_signature` 只三身份字段可保留作 ModeGate 初篩；`SWOF_CONNECTED` 真效果仍需 HGK Receiver 的完整 Scope/Epoch/TTL/Operation | HMAC-only／Wrong Scope／Expired/Replay→Effect DENY；Standalone合法本地成果不受影 |
| PIPD `src/pipd_ls_sp/{cli,pipeline,registry}.py` | 直接復用 13 CLI/19 Schema/Deterministic Compiler；`compile-cc` 另案，不改原 Exact-set | Source/Schema/Repo HEAD stale NACK；不存在原 API 時 ABI_BIND_HOLD |
| PIPD `requirements.lock`／原 Skill 目錄 | 對真受影 Wheels 鎖 Hash/Origin；OpenSpec 警告與 invalid Delta 回原 Validate，Project-local Skill 單一有效來源 | 不能用 generatedBy 1.8.0 宣稱正在跑 1.15.0；缺真 Loaded/Trigger 只有 HOST_PENDING |

### 11.2 BODY-00～12 逐冊實質修改與輸出

| BODY | 原來源不降級／本次必接功能 | 本次可交給原 Consumer 的真輸出／失敗與回退 |
|---|---|---|
| 00 | Normal Goal、Source、Authority、Tier/Effect、Resume | GoalCard／Readset／NeedDelta；無合法 Source 不簽 PI |
| 01 | 三 SPEC、三 SP 雙形態、唯一 Plan Owner | Product/Architecture/Program SPEC→原 PIPD Intake；缺 Source 關受影 SPEC |
| 02 | K0–K3、18 Stage、19 Schema/13 CLI/8 Skill、五出口 | 原 PI/PD/DEV/OPS/TQAEP 分流；Oracle/State Map 缺件則受影 HOLD |
| 03 | EffectClass 正交、五 Typed ABI、Tier 顯示投影 | 正式 ECP/Scope/Original Receiver；L1/L2 語義矛盾不可放行 |
| 04 | Fabric Source→Active→Loaded→Consumed，HGK Protected Registry／Provider | 同 PolicyEpoch 的 Host ACK、真 Permit；只有 Canary 不算 Active |
| 05 | Commander A/B/C Guide／Native PlanRevision CAS | Program Plan Proposal/同 WorkID Resume，無第二 Scheduler |
| 06 | 原 SharedSpine、Hermes bounded Worker、Crash/Unknown/Compensation | WorkOrder/Intent/World/Checker，無雙重 Commit |
| 07 | AC15 異構／96 Oracle／Challenge Portable/Native | Advisory Finding→Protected AO Inbox→原 Checker；無假 PASS |
| 08 | 五集合485實質選型，HotSwap/Retire、原 Disposition | CapabilityPlan→Host Occupant→有效載入，缺件精準 NOFIT |
| 09 | 七痛點、三 SP、14 SBL 原 DOC、149 Child | FUO/Need/Host Artifact；不把 B1 66/254/629 當 Full Product |
| 09A | 949 Atom 原名/功能／各正反例 | 每 R15 依 Need 原 Source/Consumer；未觸發不刪產品義務 |
| 09B | 192 Cell，Provider ON/OFF 原 token | 每 Host/Mode/Kind 真 Trigger/Nontrigger、`OWNER_BIND_HOLD` 直到標籤確定 |
| 10 | W18 普通 Goal Fresh PID、自啟動、無長 B1 Prompt | 真 default profile/Skill/Served/Resume |
| 10A | 120 Parent/124 Child/38 Node 原 Case ID | 對應真 Runner 只讀 Locator；缺原 Binding 不宣稱執行 |
| 10B | 27 PI/31 PD Edge OBS/DEV/OPS/USER | 原 Effect/ECP/TQAEP Consumer、Exact Oracle |
| 11 | 22 WP typed DAG、Done/Resume/Skip/FirstFail | 依 Goal 只取必要依賴閉包、可繼續不受影 WP |
| 12 | MVI Design/Native/Checker/Release 分立 | FUO 可交付但不等於正式 Publisher Release |

### 11.3 可落地的執行順序：不用新增 Gate、也不轉交使用者選輪子

**原既有 WP**：`WP-FHS-00/01` Source/Authority→`02/03/04/17` Fabric/HGK/Hermes/必要 CAP→`05/15` 原 PIPD/TPM→`06/08/09` 最小合法可逆 Native/Worker/Checker（依原有 typed DAG 的具體前置拓撲排序）；其餘 07/10/11/12/13/14/16/18/19/20/21 依當期 Goal/Host/Need 形成 Closure。原 WP17 即 CAP-BOOT 在第一次 Effect 前按需要具備，不能因所有 Default30 未安裝就造成整體 HOLD。[BODY11 原 WP 各獨立 Trigger/Done]

**最小有界成果三個層級**：`DESIGN_OUTPUT` 可合法產三 SPEC/候選；`MVI_NATIVE` 必有同 Subject Fabric Consumed+HGK Permit+Hermes World＋原 Checker；`FULL_PRODUCT_RELEASE` 必原 SBL949/192、HGK20卷原義、各原 Checker/SourceFreeze/Publisher 適用義務全數處置。歷史 B1 的 30 Installed 只有 12 Effect Runner、240 Admitted、244 Case Total 等各自分母；四庫共用的 B1 GATES 不能當四次獨立驗收。[BODY10/12；歷史 B1 GATES]

**退場與回歸**：本次新增的每個版本/Skill/Plugin 要驗 exact Artifact Origin、License、HostCaps、Fresh Session Load/Trigger/Nontrigger、Provider Off、Cancelled Unknown World、Compensation、Uninstall Residue；未通過時停對應 Need，原已合格 Occupant 保留；不存在重建全套系統或盲目安裝485工具。


## 本輪同域受影修復：r2 §12操作例/§13退出

## 12. 實際操作範例（Source-grounded、不可假冒 Native API）

本章給出能由現有四庫真正存在的 CLI/函式消費之**單一步驟**，而非憑空發明 HGK `read_admitted_work()` 等方法。真 WorkOrder/Permit 仍由原 HGK Issuer 和 Protected Runner 產生，不在此文件做「無憑證自造 Permit」操作。

```python
# True read-only SQLite observation. SharedSpine._open() sets journal_mode=WAL;
# therefore do NOT use its .connect() for a strict non-mutating source probe.
# This source-bound code does not issue WorkOrder, Permit, or admission.
from pathlib import Path
import sqlite3

p = Path('C:/Projects/Agent_Workspace/HG-KSEOS/var/shared-spine/hg-kseos.db').resolve()
if not p.is_file():
    raise FileNotFoundError('HGK_SPINE_READ_ONLY_SOURCE_MISSING')
db = sqlite3.connect(p.as_uri() + '?mode=ro', uri=True, timeout=10)
try:
    db.execute('PRAGMA query_only=ON')
    tables = db.execute('SELECT name FROM sqlite_master WHERE type=?', ('table',)).fetchall()
    assert tables  # parseability only; not runtime/admission acceptance
finally:
    db.close()
# Actual modifications must use the ORIGINAL HGK protected API and owner ECP.
```

```python
# Existing PIPD parser/source contract probe: no new 14th verb.
from pipd_ls_sp.cli import COMMANDS
from pipd_ls_sp.registry import SOURCE_ORDER
assert len(COMMANDS) == 13 and 'compile-cc' not in COMMANDS
assert len(SOURCE_ORDER) == 19
# This static probe does NOT attest live Host effective load or native execution.
```

```text
Hermes bounded invocation (original launcher ABI to be read from HGK Owner):
  Input: Existing HGK WorkOrder/Permit+Lease/Exact WriteSet/PolicyEpoch
  Guard: Registry/Issuer/Receiver genuine signature and Host/Scope
  Action: Existing Hermes process+approved worker, not Kanban effect dispatcher
  Output: worker PID+profile SHA+actual served+world readback+raw
  Unknown/Timeout: old operation ID reconcile, never blind retry
  Forbidden: construct fake Permit, overwrite Oracle, make release based on ToolDone
```

**部署修補優先順序**：Fabric 相對根路徑→HGK Launcher/Admission 真 ABI→SBL Adapter/HMAC-only scope→Hermes actual loaded/served→PIPD original 5 exit/source lock→最低 Native E2E。前 r1 長篇 `fhs_contract_audit.py` 和只讀 CI 可在**另一份稽核附錄**作可選輔助，不能取代此施工順序。[四庫 source；BODY03/04/06]

## 13. 正文適用與退出裁決

- **本設計候選已恢復的實質內容**：原 485 具名技術承諾、949 原子、192 Host/Mode/Provider Cell、三 SP/18 Stage/五 PIPD 出口、15 AC Edge/96 Oracle、22 WP、31 B1 Edge/282 Case/Node、七痛點、15 TDR 與 W18 Native 常態路線；各自允許按 Need/Host/Scope 逐步進行，不新增第二控制權威。
- **仍不得自稱已跑過的原事實**：任一真 HGK Issuer／Permission/Legacy Tier Owner Signoff，Hermes Loaded Runtime/Toolset PID、Fabric Active/Consumed、原 Checker SoD、W18 Fresh PID、完整 949/192 Host 資格化、Original SourceFreeze/Release。欠缺證據保留 `ABI_BIND_HOLD/ADMISSION_HOLD/VERIFICATION_HOLD/RELEASE_HOLD`，不妨礙無關合法 Draft。
- **本檔與另一稽核檔的分工**：施工者主要只需讀本檔的每個原 ID 段及適用 WP；要證明來源、Missing、Version、Audit 所提出 F-01～F-28/RB-01～09、CR_OPEN、Exact ID 分母和全量 Manifest，才查 `r2_證據稽核附錄.md`。不把審計表誤作該功能的實體 Runner。


---



## R2 真 Host Path Locator 與 FirstFail 收件規則

- 不得把 `C:/Projects/Agent_Workspace/HG-KSEOS/var/shared-spine/hg-kseos.db` 的**示範字串**當現役唯一 SharedSpine 路徑。先從原 HGK `config/registry/HostReader` 取得 `spine_path` 與 Owner SHA；`resolve(strict=True)`、禁止越 root 的 junction/reparse，再 readonly open SQLite `?mode=ro`。找不到原 Registry 就 `HOST_LOCATOR_UNBOUND`，只停受影 DB 查詢。
- GitHub branch SHA 是 Remote Snapshot，不是 Windows local HEAD/index/untracked/loaded profile。先取得四庫 `git rev-parse HEAD / status --porcelain / staged-index / untracked / path alias`，Dirty 只能隔離有界 Worktree 施工。
- 對 20 項舊 `AUTHOR_SIDE_PASS` 一律只作歷史聲明；R2 新增 `R2_STATIC_REPLAY.py`、Negative fixtures 與捕獲 stdout/exit，執行時不得將 static result 當 Protected Checker。
- 把整個 Subject/SourceSHA/Scope/ABI/Original owner/Exact readback 等差額送回原 Receiver。當缺 **Issuer** 或 **Checker**，僅 effect 依賴錐 HOLD；合法 Design／ReadOnly 已交付不必重新索全部批准。



## 本版未受影條文（完整沿用、當期生效）

## R2-12-JOURNEY：同一 Subject 的可逆作者端切片

Goal「為普通目標產來源綁定變更規格」→ PM/SE/TPgM 三 SPEC（Portable TPM producer）→ IntentCard/Authority/Profile 候選（原 PIPD Reader）→ PI 候選（原 Writer ACK 前不 promotion）→ 真 RepoContext 的 PD 候選→DEV/OPS ECP 候選分開→Native PLAN proposal→Fabric Loaded/HGK Admission required→Hermes 原 Queue/worker expected→world Raw expected→獨立 Checker expected→bounded repair→交付。Source hash/candidate hash/Subject 逐邊不變；新 Candidate 必明示 supersedes，而非覆寫先前 Raw。

作者端 POS：缺 native permit 時正確停在 ADMISSION_HOLD，隔離 SPEC 檔仍交付可讀；NEG：把 ECP 字串當 Permit、把 PlannedTQAEP 當 Independent PASS、把舊 Host receipt 換入當期 source 均拒收。此例驗「合法停點」，沒有執行 Host 效果。

## R2-12-CLAIMS：不同驗收軸

FILE_READBACK_PASS、LOCAL_SCHEMA_FIXTURE_PASS、DESIGN_GUARD_PASS 僅是各自作者端證據。FULL_DOCUMENT_STATIC_PASS 需全部原語義及 26 項修復證據；SCHEMA_CONFORMANCE_VERIFIED 不等於 HOST_BOUND；HOST_BOUND 不等於 INSTALLED/ACTUALLY_INVOKED；WORLD_EFFECT_READBACK 不等於 INDEPENDENT_CASE_PASS；OWNER_RATIFIED/RELEASED 各需原主體本輪收據。

## R2-12-HANDOFF：下游接收與失敗

交付 typed refs：source manifest hash、candidate per-file hash、17 Body refs、26 closure refs、DAG、case plan、actual test logs、holds。Consumer 先驗 SHA/UTF8/LF/link，再讀原語義與當期 RepoContext；missing file、empty denominator、unknown schema、stale source → NACK，附 first_fail、affected_scope、具名 Owner、next_legal_action、resume_predicate。不得因靜態拒收器通過，推論所有 Native Case 已執行。

[根索引](../INDEX.md) · [來源證據](../02_EVIDENCE_AUDIT_APPENDICES/10_STATIC_v1_SOURCE_MANIFEST.md) · [需求覆蓋](../COVERAGE_REPORT.md) · [ABI/Fixtures](../02_EVIDENCE_AUDIT_APPENDICES/12_STATIC_v1_TESTS_AND_SCHEMA.md) · [衝突/HOLD](../REPAIR_CLOSURE_REPORT.md) · [QA/readback](../02_EVIDENCE_AUDIT_APPENDICES/13_STATIC_v1_CLAIM_CEILING.md)。

READ_ONLY 工作完成後不需要效果回滾；REPO/HOST/USER/REMOTE/RELEASE 按 BODY-03 的不同 Done/補償/殘留規則。原 Gate/Case/ID 的未受影義務持續有效，文件缺件不能重設已准入工作。
