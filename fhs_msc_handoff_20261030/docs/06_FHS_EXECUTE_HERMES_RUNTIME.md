<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 06 FHS EXECUTE HERMES RUNTIME｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。




## HANDOFF-v1｜原 WorkID、Lease、Journal、UNKNOWN 與復原

1. **原接線**：Goal→原 TPM/PIPD/PLAN→原 Fabric/HGK admission→原 Hermes Queue/Lease/Journal→bounded Worker→原世界狀態 Reader→不同 Principal Protected Checker→原 Delivery/Publisher。安裝目錄的 `hermes_cli/kanban_db.py` 中 `create_task/get_task/claim_task/complete_task` 及相鄰dispatch/connect來源已唯讀釘SHA；這不是新Queue或已載入證據。
2. **同 WorkID續工**：沿原Canonical WorkID及Hermes task_id關聯、Subject/SourceSHA/Scope/PolicyEpoch/operation_id/checkpoint重讀，不新建另一工作掩蓋失敗。不重執行已完成且同key的寫入。
3. **Lease fence**：原 SharedSpine `_assert_lease` 先驗 holder/token/expiry；fixture當期lease接受、舊lease回 `ERR_LEASE_EXPIRED`。原native admission另檢generation/CAS；worker在真正 effect前重讀原lease代數，不能用作者端fixture代替有效lease。
4. **At-most-once／UNKNOWN**：同 operation_id已確認有effect只續驗證；已確認無effect才由原Owner policy決定重送；UNKNOWN/PARTIAL只PARK該operation進原World Reconcile/補償，絕不盲retry。原 `core.effect_route` 靜態實測UNKNOWN→RECONCILE_BEFORE_RETRY。HGK一般`recovery.restore_database`沒有operation_id，不能當成此工作effect journal/reconcile替代；這個能力差額只影響後續真effect，不阻斷無效果首工作。
5. **ProviderOff與lane**：本首工作explicit ProviderOff=true，可用原deterministic reader/Compiler完全完成；沒有從legacy ON/OFF推出外呼布林。若需要provider而PolicyOff，拒收該capability，不私換provider。未來有三lane時`required/selected/actual_served`逐一回讀；作者端選型/fixture不充served。
6. **退出／回復**：source drift→停受影輸出並重新讀來源；本地草稿失敗→核本WorkID exact preimage/部分檔，不刪他人內容；UNKNOWN→保留Journal/residue，原Owner受權補償；Checker不足→只不發Independent/Release。首工作的read/draft/PI不等這些後續receipt。

## 本輪同域受影修復：r2 §4.3/4.4 SharedSpine與W18

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


---



## R2 單 WorkID 自主閉環／World Reconcile 演算法（原 Hermes Queue）

**Trigger**：普通 Goal + valid Source／KnownAnswer，或原 Hermes 存在 `WorkID+Cursor` 的恢復；不要求每次重貼 B1 長 Prompt。

**流程**：讀原 Fabric `Active→Loaded→Consumed` Policy epoch 與原 HGK lane route／SharedSpine；原 Plan Writer CAS 產 task dependency；在真 effect 之前才讀 original Issuer Permit、驗 `WorkID,subject,candidate_sha,scope,lease_generation,nonce,expiry`；在 journal 持久化 intent，委派原 Hermes Worker 實際執行，收 `worker_pid,actual_served_model,task_response_raw,world_raw`；由不同 principal Checker 對原 Oracle 判定並交原 Publisher。

**Crash/Resume**：如果 `operation intent` 已寫、但 world result UNKNOWN，原 Reader **先 reconcile**，不得盲重試或重播 nonce；lease_generation/old PID fencing；valid Cursor 重啟只做受影差額，成功收據同 SHA 復用，不重問 KnownAnswer。

**拒收**：`selected_model != actual_served`、原 HGK Resolver 只是 ISOLATED candidate、`staged_policy != consumed`、無真原 Permit、Maker=Checker、ProviderOff 仍外呼、當期原 Worker PID 不存在，均不得稱 E2E 成功。L0/L1 draft 與無關 READY 任務可繼續。

**W18 新鮮 PID UAT**：執行者應從當期 Host 取得新 PID/StartTime、Default Profile SHA、三 lane `required/selected/served` 的三份實際 `task_response_raw`、FirstFail/Resume cursor/Owner prompt count，為 E33～E42 逐案回填。缺原 Host 一律 `NATIVE_NOT_RUN`，不是成功 UAT。



## 本版未受影條文（完整沿用、當期生效）

## R2-06-REDUCER：proposal 到原 HGK 狀態的讀取契約

先以原 HGK module origin/schema SHA/serializer/reducer enum 做讀回，建立 proposal→native map。map 結果只有 EXACT_NATIVE、COMPAT_ADAPTER、UNSUPPORTED、ABI_BIND_HOLD；不以自行定義字串直接送 reducer。READY、LEASED 等下文是設計狀態，真事件 enum 以該 probe 綁定。

事件輸入 `work_id,event_id,expected_revision,lease_generation,worker_pid,operation_id,source_sha,policy_epoch`。PLAN 候選由原 Writer admitted 後才能進原 Queue；CAS(expected_revision) 只允許一 Worker claim。Claim→執行前記 operation intent；取得 Raw world readback 才提交 EFFECT_KNOWN。timeout 落 UNKNOWN，禁止同 nonce 重發；先以 operation_id 對 world reader 查 commit/partial/no-effect/unknown，NO_EFFECT 證明成立後才由 Issuer 決定新 nonce。部分效果以獨立 compensation ECP 修復，原 residue 不得刪。

READY>0 時 wake 只送原 Hermes wake endpoint。ACK 需 cursor/revision，Worker startup Raw 需新 PID、process origin、loaded profile、lease generation。wake timeout 可重送同 idempotent wake event，不可把效果一起重播。restart 由原 Journal cursor 恢復；generation 過期 Worker 的 Raw 只作觀測，不能 commit。READY=0 時等待原 wake，不部署新的 MissionController。

POS：Worker A intent 後 crash，新 PID B 先 reconcile 原 operation，再消費不同未完成工作；NEG：A lease generation=7，B 已升=8，A commit → LEASE_FENCING_DENY。POS：work X issuer 缺件 PARK，Y read-only READY 被服務；NEG：全 Queue WAIT → GLOBAL_OVERBLOCKING。

綁定步驟：原 HGK/Hermes Owner 讀目前 reducer/Wake API schema 與 help → 保存 module path+SHA+enum → 以 no-effect fixture 驗 serializer/CAS → 將同 Subject OPS ECP 交原 Issuer。未有本輪 Runtime Raw 一律 NATIVE_NOT_RUN。退出只關閉本輪 proposed mapping；已 admitted 舊 work 繼續依原 receipt，不重編 PI/PD。

## R2-06-ACTUAL-SOURCE：當期HGK Spine源碼接口

已實讀 `C:\Projects\Agent_Workspace\HG-KSEOS\src\hg_kseos\spine.py`，SHA `f99a402123f39b8ceaad9372aeec0555628ba643950a5c99a4c917fd9e6d6dcd`。以下是當期工作樹AST讀回，未匯入模組、未開世界資料庫、未調用任何mutation。

| source symbol:line | actual signature | actual source guard/readback |
|---|---|---|
| _open:60 | self | return connection |
| acquire_lease:128 | self, resource_id: str, holder: str, token: str, ttl_seconds: int=300 | raise LeaseConflict(f"ERR_DUAL_WRITER:{resource_id}:{existing['holder']}") |
| release_lease:148 | self, resource_id: str, holder: str, token: str | """Release a lease and return a typed receipt.; raise LeaseConflict(f"ERR_LEASE_RELEASE_AUTH:{resource_id}"); return {"schema": "HGK-LEASE-RELEASE/1", "released": True, "resource_id": resource_id, |
| _assert_lease:165 | self, connection: sqlite3.Connection, resource_id: str, holder: str, token: str | raise LeaseConflict(f"ERR_LEASE_REQUIRED:{resource_id}"); raise LeaseConflict(f"ERR_LEASE_EXPIRED:{resource_id}") |
| transition_requirement:215 | self, requirement_id: str, to_state: str, actor: str, token: str, expected_version: int, evidence_ref: str, idempotency_key: str, payload: dict[str, Any] &#124; None=None | raise InvariantViolation(f"ERR_REQUIREMENT_UNKNOWN:{requirement_id}"); return dict(duplicate) &#124; {"idempotent_replay": True}; raise StaleState(; if to_state not in allowed:; raise InvariantViolation(f"ERR_ILLEGAL_TRANSITION:{prior['state']}->{to_state}"); raise StaleState(f"ERR_CONCURRENT_UPDATE:{requirement_id}"); return {"event_id": event_id, "resulting_version": resulting_version, "to_state": to_state} |
| resolve_acceptance:460 | self, acceptance_id: str, *, verdict: str, evidence_ref: str, actor: str, token: str, expected_version: int, idempotency_key: str, requirement_id: str &#124; None=None, payload: dict[str, Any] &#124; None=None | raise InvariantViolation(f"ERR_ACCEPTANCE_VERDICT:{verdict}"); raise InvariantViolation("ERR_ACCEPTANCE_CRITICAL_FIELD_MISSING"); raise InvariantViolation("ERR_ACCEPTANCE_SUBJECT_BINDING_REQUIRED"); raise InvariantViolation(f"ERR_ACCEPTANCE_UNKNOWN:{acceptance_id}"); raise InvariantViolation(; raise InvariantViolation(f"ERR_ACCEPTANCE_EVIDENCE_UNKNOWN:{evidence_ref}"); raise InvariantViolation(; return {"event_id": spent["event_id"], "resulting_version": spent["resulting_version"],; if from_state not in TRANSITIONS["acceptance"] or verdict not in \; raise InvariantViolation(f"ERR_ACCEPTANCE_ILLEGAL_TRANSITION:{from_state}->{verdict}"); live_version = 0 if from_state == "NOT_RUN" else 1; raise StaleState(; raise StaleState(f"ERR_ACCEPTANCE_CONCURRENT_UPDATE:{acceptance_id}"); return {"event_id": event_id, "resulting_version": live_version + 1, |

`TRANSITIONS`實際task states含DRAFT/ADMITTED/RUNNING/REPAIR/VERIFIED/PACKAGED/REJECTED/FAILED/CANCELLED；requirement另有CANDIDATE/FROZEN/IMPLEMENTED/VERIFIED/REPAIR/ACCEPTED/REJECTED/ROLLED_BACK；acceptance為NOT_RUN→PASS或FAIL。這三套不得互換。概念READY是dependency+admission可執行predicate，不能寫成這份Native enum。

Proposal→native設計綁定：PLAN_CANDIDATE只對應DRAFT候選，真Admission後才是ADMITTED；worker start要原task transition合法至RUNNING；無法直接對應的UNKNOWN effect、lease_generation、WakeEndpoint維持Adapter ABI_HOLD，不以自造欄位塞原serializer。source acquire_lease實際signature是resource_id/holder/token/ttl_seconds，不宣稱它已具本候選generation欄。expected_version/idempotency_key是transition_requirement原參數；重試必照原API及world reconciliation。

POS設計：同resource有效holder/token與expected_version才能transit，duplicate idempotency_key回原event。NEG：dual writer→ERR_DUAL_WRITER；wrong holder/token→ERR_LEASE_REQUIRED；expired→ERR_LEASE_EXPIRED；錯to_state→ERR_ILLEGAL_TRANSITION；version drift→StaleState。這些是源碼guard讀回，沒有當期World Raw就不是執行結果。Wake/Runtime原Owner需提供現役endpoint和loadedSHA後才解除受影ABI_HOLD。
