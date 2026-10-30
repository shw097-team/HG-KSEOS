<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 04 FABRIC HGK CONTROL｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。




## HANDOFF-v1｜對齊現役 Fabric／HGK 接收面

Fabric 現役 `FABRIC/fabric/consumers/hgk_policy_consumer.py::route_event` 與 `RP002_CHANGE_CLASS_ROUTER.yaml` 的 source SHA 已釘住。`RUNTIME_TRANSIENT→HERMES_NATIVE` 只用於原 runtime 之 session/heartbeat/scratch等事件，不能拿這個 change class 把任意 RepoWrite、Profile或Pipeline變更洗成無效果。

HGK現役 `src/hg_kseos/native_admission.py::taskspec_request/workorder_request` 的純 request constructor 已用靜態 fixture實際接收本首工作的欄位映射；foreign worktree以`ERR_NATIVE_TASKSPEC_ROOT`拒收。本輪沒有呼叫`authorize`、`create_taskspec`、`create_workorder`或任何 signing/issuer。真實 RequirementID、TaskSpecID、WorkOrderID由原 Canonical admission在原 Owner scope解析/配置；candidate subject ID不能代替真 WorkID。

若真正進入 OPS才缺 grant，原 DAG的受影後代 PARK；`WP00/01/05/15` 仍可 source/draft/compile。原插件 `affected_work` 實測結果在 `OPS_PARK_AFFECTED_CONE.json`。不增設第二 policy、issuer、queue或state DB，不以 elapsed time或既有文件封裝當 receipt。

## 本輪同域受影修復：r2 §4 真四庫 ABI 與 Native Effect

## 4. 四庫確定性接線修補：真正的原 ABI 與受界停點

### 4.1 本次實查 Source 摘要（不要把假想方法寫成 HGK API）

| Repo 固定源 | 已證實的真定位／函式 | 可直接進行的最小工程轉換 | 缺失時封鎖與退回 |
|---|---|---|---|
| `Fabric/FABRIC/fabric/consumers/hgk_policy_consumer.py` | `FAB=Path(r"C:\Projects\Agent_Workspace\Fabric")`, `load_router()`, `route_event()`, `apply_preapproved()`；原 Router 檔在 `FABRIC/rp002/` | 原位相對 Trusted Fabric Root 定位、Reject `../`／Junction，保持 `route_event` 原回傳形狀；`apply_preapproved()` 僅 Canary，不替代 Active/Consumed | 找不到原 Active／Host Loaded/Consumed Reader→`POLICY_CONSUMED_HOLD`，保留 Stage |
| `HG-KSEOS/src/hg_kseos/spine.py` | `SharedSpine(database,schema)`, `.transaction()` 使用 SQLite BEGIN IMMEDIATE、WAL；原 taskspec 狀態 `DRAFT→ADMITTED→RUNNING→VERIFIED→PACKAGED` 等 | 原 WorkID/Lease/Reducer 只能用其所在模組正式 API；禁止 FHS 直接改 DB 表或創第二 Dispatcher | 缺原 Admission/Lease 入口→`NATIVE_BIND_HOLD`；只有設計 Proposal |
| `HG-KSEOS/src/hg_kseos/providers.py` | `ProviderRegistry(spine)`, `.import_protected_ledger(path)`, `.advance(...)`，`qualify_hermes_core()` 歷史測試固定 57/50/7 | 分離 legacy qualification fixture 與新版本具名不變量；原 lifecycle/Registry 保留 | 真版本 Pin/Raw/Served 缺→`QUALIFICATION_HOLD` |
| `HG-KSEOS/src/hg_kseos/lane_route_resolver.py` | 候選純計算 pool/fallback logic，明示非 Launcher | 將原現有可用 Launcher 對接原 Registry 的 Proposal，先核 Signature/Module SHA；不新增路由權威 | 入口不可定位→`ABI_BIND_HOLD`；不可當它正在生效 |
| `HG-KSEOS/src/hg_kseos/lane_admission.py` | `LaneAdmission`, `decide_status`, `write_receipt` 供候選 lane probe；`ADMITTED` 要實際 completed model call+tool roundtrip+served match | 只有原受保護 Receiver 可提升 Native Admission，候選 probe 不簽正式 Permit | 只有 HTTP 200→`UNPROVEN` |
| `SBL/sbl_harness/__init__.py` | `HGK_PIN` 指向原未見 `config/lane-route-slots.candidate.json`、`scripts/hgk-lane-dispatch.py`；`HARNESS_ABI` 提供 plan/execute/verify 但 `not_provided` 明示 native_effect/permit_signing/admission | 原位改由 HGK Owner 提供的正式 Registry Locator/Dispatcher Binding；SBL 僅 consume、安裝/卸載限其檔案 Allowlist | 正式入口未確認→`HARNESS_BIND_HOLD`，不能用 B1 候選直接執行 |
| `SBL/sbl_core/modes.py` | `ack_signature(issuer,permit_id,subject_id,key)` HMAC length-prefixed；`_ack_state()` 驗三欄＋Issuer Allowlist/secret | HMAC 作 ModeGate 初篩可以保留，真正 Effect 仍交原 HGK Receiver 檢 Scope/Epoch/TTL/Operation/Nonce/Subject | 不得以 HMAC mode ack-only 解鎖 `SWOF_CONNECTED` 任意效果 |
| `PIPD-LS-SP/src/pipd_ls_sp/cli.py` | `COMMANDS` 13 Exact-set；`src/pipd_ls_sp/pipeline.py::intake()`/`freeze_authority()`；`registry.py::SOURCE_ORDER` 19 Schema | 原 CLI/Pipeline 直接復用，驗 Source Digest、Repo Context、合法 Schema `$id`；保留 `compile-cc` 爭議為 Versioned Candidate | 不增第14命令；缺原 Writer Consent→`PIPD_ABI_HOLD` |
| `PIPD-LS-SP/requirements.lock` | 原 Lock 自述只版本 pin、未 hash-pin；原 `.hermes/skills/openspec-apply-change/SKILL.md` 標 `generatedBy:1.8.0` | 在原 Build Scope 補 Artifact Hash／Provenance，Skill 用既有 Project Skill Location 選單一有效來源，Validate 警告/Delta | 無 Hash/Host Loader Raw 只影響受影可重現供應鏈／Skill Claim，不阻無關 Reader |

### 4.2 五條正式 Typed Adapter Flow：Input/Producer→輸出→Consumer、正負例

1. **Policy Flow**：Original Fabric Source＋Owner Approved Epoch→原 `route_event()` 是決策 Reader，不是 Host Activation；由原 Host Consumer 產 `ActiveEpoch/LoadedSHA/ConsumedACK` 真 Receipt；HGK 只 consume 相同 PolicyEpoch。Stage/Canary 冒 Active→`POLICY_CONSUMED_HOLD`。回復原 epoch 只由 Fabric Owner 執行。
2. **Plan Flow**：SBL Goal/ThreeSPEC→Portable TPM/Commander 產 Candidate；有合法原 HGK PLAN Request 才由真 PLAN Writer 改 `PlanRevision`（CAS、原 WorkID、Scope/Owner）；文稿不自行更動 SharedSpine。錯 Revision/Foreign WorkID→`PLAN_REVISION_NACK`。
3. **Execution Flow**：PIPD PD/DEV/OPS ECP→原 HGK WorkOrder/Permit/Lease→Hermes pinned Profile+Worker；原 Worker/Tool 只執 exact `OperationSemanticID/WriteSet/HostTarget`；返回 Native Raw；若無實際 Issuer/launcher ABI 只能 `ADMISSION_HOLD`。真 Process PID、Loaded Module Origin、Requested/Served 都必讀。
4. **World Flow**：Hermes Tool 完成事件→原 Receiver 查受治理世界狀態和 Journal→分類 `APPLIED/PARTIAL/NO_EFFECT/UNKNOWN`；ToolDone 不等於 EffectKnown，未知必 `RECONCILE_REQUIRED`；Repo/Host/User/Remote 由各原 Owner 按原補償 ECP 清理 residue。
5. **Checker Flow**：Frozen World Raw+Original Oracle+Same Subject/Candidate/Scope→原 AC15 Handoff→有獨立 Credential/ACL 之 Protected Checker 判定→原 HGK Reducer ACK/HOLD；同模型不同不保證 SoD、同 Principal 更不能。正式 Release 需原 Publisher 與 SourceFreeze。

### 4.3 Native E2E 自主執行狀態機：Actor、事件、Fence、Unknown Effect、補償

| 事件／原狀態 | Actor、前置及受限 Payload | 成功後狀態與 World Readback | NEG／恢復／補償 |
|---|---|---|---|
| `GOAL_ACCEPTED` | SBL GoalCard/QuestionLedger，SourceSHA、Mode/Kind/Host | `SPEC_CANDIDATE`／合法 FUO | 缺來源→NEED_SOURCE，不能造 PI |
| `PLAN_READY` | TPM 三 SPEC＋PIPD PI/PD/ECP/TQAEP；Owner-bound Source/Scope | 原 WorkOrder 候選，尚不能 Effect | 缺 PIPD Writer/Oracle→PIPD_HOLD |
| `POLICY_CONSUMED` | Fabric 原 Owner ActiveEpoch＋真 Host Loaded/Consumed | 同 Epoch 所需資格成立 | 只有 Canary→POLICY_HOLD |
| `ADMISSION` | HGK 原 Issuer/Receiver 證 Permit/TTL/Nonce/Subject/Operation/WriteSet | `ADMITTED`（原 State Enum 讀值，不自造） | Foreign/Stale/Replay/OutScope→DENIED，不 Spawn |
| `LEASE_CAS` | HGK SharedSpine transaction、WorkerIdentity、LeaseGeneration/FencingToken | 唯一當期 holder 可進 `RUNNING` | 舊 Generation 的 Worker ACK 無效，不因 timeout 假定無效果 |
| `INTENT_DURABLE` | HGK 原 Journal 原 OperationSemanticID+PreImage+ExpectedWorldDiff | Durable operation intent，准 Worker bounded invoke | 不應先 Tool Invoke 後記 Intent；若存取失敗停止 |
| `EXECUTE` | Hermes 真 Loaded Profile＋Worker PID/ModuleSHA/ActualServed；Coder Tool ACL 由原 Receiver | 僅 exact Scope 操作，Raw 附 OperationRef | 子代理繼承 Toolset 不等於新 Permit；超 scope DENY |
| `WORLD_RECONCILE` | 原 Receiver 比對 PreImage/Journal/PostWorld | `APPLIED`、`PARTIAL`、`NO_EFFECT`、`UNKNOWN`（**判定分類**，非假定 Native enum） | `APPLIED` 只續收證據；`PARTIAL` 原 Compensation ECP；`NO_EFFECT` 仍須 fresh original admission；`UNKNOWN` HOLD、不可重試 |
| `CHECKER` | Original Protected AO 讀 Raw/Oracle，獨立 Principal/ACL | 原 verdict→Reducer 合法下一 State | Maker 自評、Oracle 被改或來源錯→VERIFICATION_HOLD |
| `CHECKPOINT/RESUME` | 新 PID 讀原 WorkID/LatestState/Lease/OpIntent/World，驗新 Scope/Epoch | 未受影依賴可繼續，已 Effect 不重執 | 已撤/過期 Permit 必重新原 Issuer 准入；舊 Holder CAS NACK |
| `RELEASE` | Original Publisher/SourceFreeze/Proof | 本 Scope 受准交付/發布 | 缺一 Receipt→RELEASE_HOLD，不假宣全域完成 |

**四個極端例子**：A 完成世界寫入但 ACK 遺失→B 新 PID 必以同 `OperationSemanticID` 從 Journal/World 認定 APPLIED，不得再呼叫一次；A Lease 已到期但後送 ACK→Fence 令其拒收，世界效果仍須 Reconcile；部分改檔→不以 Failed=NoEffect 直接重跑，進原 Compensation ECP；Provider quota→只有 Owner 池內相容下順位可自動切，Governance/ProviderOff 的否決不容替代。[BODY06 `R2-06-REDUCER`；BODY10]

### 4.4 W18 Ordinary Goal：真正 Fresh PID 日常入口，不依賴 B1 長 Prompt

```text
Host start (new PID)
 → 原批准 Default Profile / AGENTS.md / Project Skills Manifest read and SHA
 → Host effective load + invoke/noninvoke + true requested/served
 → User ordinary Goal + Source Locator + Kind + Mode
 → SBL KnownAnswer/MethodDecision and current Source/Policy/Scope
 → [existing admitted WorkID ? read cursor+world+lease : create source-bound SPEC]
 → [no effect ? First Useful Outcome : original HGK approved WorkOrder]
 → Hermes bounded Worker / true raw / original Checker
 → Checkpoint by existing HGK SharedSpine, not private chat state
```

三個正常情境：**首次有效來源**→首個合法 FUO，不要求貼 B1 長 Prompt；**同 WorkID 重開進程**→校 Scope/Policy/World，Resume 未完成且未重播 Effect；**來源或 Policy 變更**→只 invalidate 受影計畫並重核 Admission，無關成果保留。任何 `Default Profile/Skills/Served` 未真讀回→`W18_NORMAL_HOLD`，非假稱 AUTO_READY。[BODY10 `R2-10-NORMAL`]

### 4.5 知識與記憶、Windows／桌面、CI 安全三條既有 Consumer 路線

**Knowledge**：原 KnowledgeFactory/G-KNOW/HLPE/SRU_OROCHI 接 Source/DocETL（受權提取 bytes＋SHA）→原 Clause Index/FTS5、可審 Retrieval→同 SourceSHA Citation、Known Answer/Question Ledger→若失效重索引受影條目。`LLM Wiki` 只作已選 Source-backed 顯示或候選，不改原 Clauses；Mem0/Letta/Qdrant/Chroma/Milvus/Neo4j/pgvector 等是否採用依 TECH386 原處置，沒有效益差額不擴第二 Knowledge DB。記憶資料 `timestamp`／`citation` 不同於 Canonical Source Freeze。[RBWI Group03；BODY08 TECH386]

**Windows／Host/UI**：Hermes CLI/Windows Host 原 Process/Skill Loader 先用真 Loaded Module；Codex、Claude Code、ChatGPT 各依原 Host Capability 做不同 Install/Invoke/Permission 的 POS+NEG；`Windows App SDK/WinUI 3/Named Pipe/AG-UI/A2UI` 保留 TECH386 原 ID，只有明確 UI/Interop 的 Product Need 才依原選型施工。Notebook/Web Chat 不冒充 OS FileSystem/Process Tool，Web DOC_MOUNT 不等於 Private Plugin Qualification。[SBL DOC10；BODY08 TECH386:TECH]

**Supply Chain**：原 CI 一個責任明確的 Build Pipeline 按 Scope 選：`Gitleaks` 受影 Secret Scan，`CodeQL/Semgrep/Ruff/pytest` 靜態／單測，`Syft→CycloneDX/SPDX` SBOM，`Trivy/Grype/OSV` 按實際 Consumer 做漏洞匹配，`Cosign/SLSA/Artifact Attestation` 記建置來源（不能取代 Native/Checker/Release），`OPA/TUF/OpenSSF Scorecard` 只依原 TECH disposition 及安全 Need。10 月 eMudhra 信任鏈事件只使真受影 CA Bundle/HTTPS Consumer 需要重新驗證；不強制全量工具重裝。PIPD 原 `requirements.lock` 無 Artifact Hash，應在原 Builder/Publisher 受控補鎖並做可重現安裝，不能單用版本字串代表來源安全。


## 本輪同域受影修復：原始碼錨點

## 四庫 2026-10-30 `main` 原始碼錨定（GitHub 唯讀）

| Repo/HEAD | 原始碼實測存在的路徑／符號 | 接線或禁止 | 本輪效力 |
|---|---|---|---|
| `Fabric` `316b691460638bdf38475c2c58aaad406aa6eb4f` | `FABRIC/fabric/consumers/hgk_policy_consumer.py` `route_event`、`load_router`；`rp002/RP002_CHANGE_CLASS_ROUTER.yaml` | `route_event` 依 change_class 選原 HERMES_NATIVE/ORACLE_TO_HGK 等 Consumer；文件不能把 `apply_preapproved` 的 raw hash 當真 HGK active grant | REMOTE_SOURCE_OBSERVED；Host Loaded 未證 |
| `HG-KSEOS` `f6dfb1e57162dc3868dc488482d249fc095eb429` | `src/hg_kseos/providers.py` `ProviderRegistry.advance` / lifecycle；`src/hg_kseos/lane_route_resolver.py` | Provider PIN/Installed/Certified/Enabled 順序，不跨級；lane resolver 檔案註記 `CANDIDATE, ISOLATED. Not wired into the launcher`，不得宣稱已 served/loaded | REMOTE_SOURCE_OBSERVED；Launcher bind HOLD |
| `SBL` `fd62537a7ba29c3f2905fe42ddde9534674405d7` | `sbl_harness/__init__.py` 的 `HARNESS_ABI`/`HGK_PIN`；`sbl_core/modes.py` `MODES`、`DISPOSITIONS` | PREW3_SHADOW=`SHADOW_NOEFFECT`，SWOF_CONNECTED=`BLOCKED_EXTERNAL`；SBL Adapter 不簽 HGK Permit | REMOTE_SOURCE_OBSERVED；Host consumer ACK HOLD |
| `PIPD-LS-SP` `f6335a94157c61da75d92121d14c43feb413e981` | `src/pipd_ls_sp/cli.py` `COMMANDS` 恰 13；`pipeline.py` deterministic；`registry.py` `SOURCE_ORDER` 恰19；`requirements.lock` | 19 Contract/13 CLI exact-set，`requirements.lock` version-pinned 但**未 hash-pinned**；不可因 lock 存在自稱供應鏈完全可再現 | REMOTE_SOURCE_OBSERVED；Windows SchemaHost HOLD |

**來源證據界線**：GitHub commit/檔案 blob SHA 不是 Windows process PID、loaded hash、Owner grant、Issuer Permit 或 Native Runner 調用；本輪沒有看到 local HEAD/index/untracked，禁止推定本機 dirty=0。所有 Repo patch 須有現役 Owner 的 exact WriteSet/DEV-ECP/受權 Scope。本版可提供 static patch 契約，不能執行真四庫修改。


---




## 本版未受影條文（完整沿用、當期生效）

## R2-04-CURRENT：五層證據與現役唯讀起跑

Source→Stage→OwnerApprove→ActiveEpoch→LoadedSHA→ConsumerACK 各自是不同觀測。Stage/檔案存在只能證明候選可讀。原 Fabric Owner Reader 需回 active epoch、policy digest 和 host/process identity；HGK Reader 需回相同 epoch、loaded digest 與 consumer route ACK。Loaded 與 Active 不符只 PARK 依賴該 Policy 的 effect，合法 SOURCE_READ 繼續。

每 Lane 分開記 required、selected、served；PLAN/EXECUTE/VERIFY_SECURITY 必有該 task 的 request/response Raw、Provider identity、time 和 source/candidate。Model 已選而沒有 response 是 SERVED_NOT_OBSERVED。ProviderOff 不容許私換供應商，只有有來源證明的離線 Reader 或 NOFIT。

POS：同一 Subject 的 Policy digest 在 Active/Loaded/Consumer 三 Reader 一致，原 Issuer 才檢 scope/nonce/TTL。NEG：Stage-only、別 Host Loaded、過期 epoch 或別 task served → POLICY_NOT_LOADED / FOREIGN_HOST_RECEIPT。本輪 Repo HEAD 與 GitHub main 不一致，不能挑較新字串自動替換 Active。

退出：唯讀 probe 丟棄過時快照；Policy/Host 更新須另有 OPS ECP+原 Owner activation transaction，保留 preimage/epoch/consumer rollback ACK；UNKNOWN activation 先 reconcile，不藉文稿建立第二 Activator。
