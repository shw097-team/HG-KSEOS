<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 10 B1 W18 SELF BOOTSTRAP｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。


## 本輪同域受影修復：r2 §4.4 W18常態模式

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



## R2 W18：E33–E42 真使用者普通 Goal 驗收矩陣（不是通用 PASS）

| Case | 刺激／輸入 | 原 Host 期望正例 | 負例／第一失敗 | 真狀態 |
|---|---|---|---|---|
| E33 | fresh Hermes PID + ordinary goal | 自動選原 effective profile，無 B1 Prompt | 需要重貼長 Prompt → NORMAL_BOOTSTRAP_FAIL | NOT_RUN |
| E34 | 不手選 Lane | PLAN actual served raw | selected-only → NOT_SERVED | NOT_RUN |
| E35 | 書面批准 WorkScope | EXECUTE actual served raw + original WorkID | missing permit → ADMISSION_DENIED | NOT_RUN |
| E36 | 原獨立安全需求 | VERIFY_SECURITY actual served raw + checker distinct | Maker自簽 → TQ_SOD | NOT_RUN |
| E37 | ProviderOff | 無禁用的 provider 外呼 | unexpected egress → POLICY_PROVIDER_BYPASS | NOT_RUN |
| E38 | restart after journal intent | same WorkID/cursor, lease fencing | double effect/old nonce → REPLAY_NACK | NOT_RUN |
| E39 | deliberate source drift | affected scope requalification | stale signed source used → SOURCE_DRIFT | NOT_RUN |
| E40 | World result unknown | reconcile before retry | treat timeout as NO_EFFECT → UNKNOWN_REPLAY | NOT_RUN |
| E41 | KnownAnswer Ledger populated | owner reask count=0 | duplicate question → QUESTION_LEDGER_REASK | NOT_RUN |
| E42 | unrelated READY + affected HOLD | other READY executes independently | global fail-closed → OVER_GOVERNANCE | NOT_RUN |

所有真正 PASS 要具有 `same subject/source_sha/candidate/host_pid/epoch/Raw SHA/checker`；本文只有可執行之準入/拒收設計與原驗收欄，不能宣稱 W18 已通。



## 本版未受影條文（完整沿用、當期生效）

## R2-10-NORMAL：新 PID、普通 Goal、零 B1 專用 Prompt

NormalModeLaunchContract 是原 Hermes startup/default-profile Reader 的設計契約，不新建 launcher。輸入 ordinary_goal、fresh_session_id、原 default_profile_sha、既有 admitted work refs（可空）；output 為 pid/start_time/process_origin/loaded_profile_sha、auto-selection trace、每 Lane required/selected/served Raw 及 WorkID/cursor。啟動前從正式 profile loader 讀 manifest 與 hash；讀不到只 NORMAL_MODE_NOT_QUALIFIED，不能用 test-only profile 補位。

NM01：新目標 → TPM/SPEC→原 PIPD→合法 plan；NM02：既有 admitted work → 原 cursor resume，Owner 重問=0；NM03：provider-off/能力不足 → 正確 NOFIT 或離線合法 read，不能私換 provider。每條都用新 PID，禁止注入 B1 長 Prompt、手選 lane 或預填成功 receipt。

E33 的正式 default profile、E37 的受治理 route、E38 的真 served、E42 的移除 test-only 後重跑，連同原 E34–36/E39–41 全部保存原 Oracle。POS：新 PID 只給 ordinary goal，自動命中正式入口且三 Lane 按 need 真 served；NEG：拔掉 B1 專用 fixture 後失效卻仍 PASS → NORMAL_MODE_NOT_QUALIFIED。此測試需原 Host Owner 綁定 launcher，不以文件例子冒執行。

## R2-10-OWNER：效率與不阻斷驗收

GOV-UX-01 同 Subject/SourceSHA/Scope/Epoch 的有效 QuestionLedger answer 連續讀兩次，第二輪 unnecessary_owner_prompts=0；變更 scope 不可重用，需明列一個 material question。GOV-UX-02 issuer 缺件的 A PARK，合法 B/C READY 有 output；記 ready_progress、elapsed、retries。GOV-UX-03 只產 L0 SPEC 的普通 Goal 不得排三十項 Host installer；Default 產品承諾保留但僅 need-qualified scope 啟動 CAP-BOOT。

退出/重入：只有原 startup profile/Host Owner 能撤回部署；未部署的作者文稿只撤候選。未知 effect 先原 world reconciliation。G-A/G-B、三 GWO、NormalMode、Release 是不同 claim，不互相借 PASS。
