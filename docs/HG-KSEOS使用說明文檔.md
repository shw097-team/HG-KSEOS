# HG-KSEOS 使用說明文檔

## 1. 文件目的

本文件說明 HG-KSEOS 本機 canonical local 系統的安裝、操作、驗證、備份、回滾與交付。

**Current claim**: `HG-KSEOS_LOCAL_DELIVERY_PASS — EXTERNAL FINAL ACCEPTED`。Current changeset = **Task-014**（Self-Bootstrap Named Method Runtime Readiness + Task-013 Final Closure，`HGK-SELF-BOOTSTRAP-NAMED-METHOD-RUNTIME-READINESS-TASK013-FINAL-CLOSURE-014`）。Task-011/012/013 為 historical accepted lineage，不再作為 current changeset。Historical baseline：E10（task-009/010）為 lineage，已 superseded。後續新增 tracked ChangeSet 會形成新 candidate，未重新 seal 前不得沿用舊 acceptance。production 一律 `NOT_CLAIMED`。

歷史沿革：系統早期先以「本機 companion」於 maker workspace 施工（見 Release/Changelog），該階段已結束；本文描述 current canonical runtime。

## 2. 權威來源

權威順序依 source-freeze 工件執行；P0-CIP r2、實作前開發文檔包 r2、三份藍圖、FINAL_r2 控制包與 Hermes DOC-01..20 均以 hash 綁定。低權威來源不得覆寫高權威規則。

## 3. 目錄角色

`C:\Projects\Agent_Workspace\HG-KSEOS` 是 current canonical local root（writable root，唯一 canonical）。Source/Authority、Shared Spine、RBWI/WP、WorkOrder、AGENTS/SKILLS、Harness/Loop、證據與 reducers 皆在此 root。Obsidian vault、LLM Wiki 產出、RAG/KG 皆為 derived/candidate，不得成為第二 canonical truth。

## 4. 前置條件

需要 Windows、PowerShell 5.1+、Python 3.12 專案環境、Git 及 SQLite FTS5。Hermes core 使用獨立 Python 3.11 venv。

## 5. 安全邊界

禁止寫入來源、越出 maker root、路徑穿越、reparse point、未授權網路、秘密讀取、遠端發佈、部署與 production mutation。所有高風險擴權維持 HITL。

## 6. 快速健康檢查

執行 `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\doctor.ps1`。只有 `blocking` 為空且 `verdict=PASS` 才是本機核心健康。

## 7. 初始建置

全新 HG-KSEOS canonical local installation / bootstrap environment 才可執行 `scripts\bootstrap.ps1`。若資料庫已存在，bootstrap 會 fail closed；既有環境改用 migrate/doctor。

## 8. Shared Spine

canonical database 為 `var/shared-spine/hg-kseos.db`。所有 requirements、provider lifecycle、TT 與 release decision 都由單一 writer 契約管理。

## 9. Requirements

PREDEV 240 與 P0 259 共 499 條 requirement；`ATOMIC_CHILD_REQUIREMENTS.csv` 另保存 1040 個拆分子項。不得用子項取代 499 個 canonical parent identity。

## 10. Acceptance

`eval/FROZEN_ACCEPTANCE_CASES.csv` 精確包含 TST-001..092。執行 `scripts\acceptance.ps1` 產生逐案 fixture、evidence、hash 與 maker verdict。

## 11. 控制工件

`control/` 物化 FINAL_r2 的 18 skills、10 agents、12 prompts、8 workflows、6 state machines，以及 6 個 wrapper/control 文件；manifest 共 60 列。

## 12. Hermes 版本

Hermes 經 Task-013 side-by-side qualification 後認證為 v0.20.0、tag `v2026.8.3`、commit `3c27eb6234bf91b8ceee9e9071591b31e9b148cb`（exact-tag/commit 三者對齊；不使用 floating latest；不使用 `hermes update` 作為升級方式）。

- **Certified**: `ACTIVE_SELECTED_CERTIFIED`（Task-013 全部 gate PASS 後）。
- **Rollback baseline**: v0.18.2、tag `v2026.7.7.2`、commit `9de9c25f620ff7f1ce0fd5457d596052d5159596` 保留為 sealed rollback baseline，直到 final acceptance 完成不得刪除（rollback drill 已 PASS）。
- **Live runtime switch（HITL）**: 本機 desktop runtime 目前仍為 v0.18.2；切換到 certified v0.20 必須依 §40 的 exact-tag side-by-side 程序（disposable venv + 隔離 HERMES_HOME），不得直接覆寫 v0.18.2 安裝。`scripts\hermes-core.ps1` 在切換前會 fail-closed 回報版本 mismatch。

## 12a. Runtime / Governance 雙層所有權

```text
HG-KSEOS Governance / Normative Control Plane
   → thin runtime binding
      → Hermes v0.20 Runtime / Orchestration Plane
         → admitted WorkOrder → Codex CLI → OpenCodex → OpenCode Go → deepseek-v4-flash
```

- HG-KSEOS 擁有：authority、source admission、intent、requirements、RBWI/WP、TaskSpec、WorkOrder admission、normative lifecycle、risk/HITL policy、evidence contract、independent checker、reducers、evolution qualification/promotion authority、release/package/handoff、Canonical Shared Spine。
- Hermes v0.20 擁有：durable Kanban runtime task plane、worker dispatch/dependency/retry/heartbeat/reclaim、worktree 物化、`/goal` continuation 與 completion contract、SessionDB、runtime checkpoint、tool self-recovery、context compression、approvals 執行機制、Skills/Curator 機制、MCP startup。
- Shared Spine 只存 pointer / normative state / evidence refs / rollback pointer，不鏡像 Hermes runtime 狀態。

## 13. Hermes 核心驗證

執行 `scripts\hermes-core.ps1` 僅驗證固定版本，不會 setup、登入、安裝 gateway、更新或卸載。

## 14. Hermes Provider

Hermes 使用 provider `opencode-go`、model `deepseek-v4-flash`（base `https://opencode.ai/zen/go/v1`），v0.18.2 與 certified v0.20.0 相同，未變更。憑證以 `OPENCODE_GO_API_KEY` env-ref 存放於 Hermes auth store（`%LOCALAPPDATA%\hermes\.env`），不寫入任何 evidence。OpenAI OAuth credential 保留未動；OpenAI fallback = false；unadmitted provider = 0。Provider 正向 pilot（P1–P10）、Hermes→Codex closed loop 與 Task-013 real Codex route（Codex CLI → OpenCodex → OpenCode Go → deepseek-v4-flash）均 PASS。DeepSeek prompt caching 在 OpenCode Go gateway 上實測：重複 9092-token prefix 的第二次呼叫 `prompt_cache_hit_tokens=9088`（hit 由 provider metadata 量測，未編造節省百分比）。

## 15. Hermes 回滾

官方 `uninstall --full --yes --dry-run` 已驗證；真實卸載會刪除目前 checkout，必須另行取得 destructive approval，並先保存 backup/receipt。TST-054（uninstall residue）已以 disposable venv 完成 INDEPENDENT_CASE_PASS。

## 16. Provider Lifecycle

合法順序為 DISCOVERED→IDENTIFIED→PINNED→INSTALLED→CONFIGURED→DOCTOR_PASS→PILOT_PASS→CERTIFIED→ENABLED。任何跳級都會被拒絕。

## 17. FTS5 Retrieval

SQLite FTS5 是唯一目前啟用的 retrieval provider。無來源支援時必須 abstain；來源撤回後須重建並證明不可再檢索。

## 18. Knowledge Distillation

候選內容先進 quarantine，再由獨立 verifier 與 evidence 決定 promotion。來源文字、tool output 與 MCP description 一律視為 DATA。

## 19. Memory

PII memory 需要明示 admission；過期或 revoked memory 不得出現在 active retrieval。錯誤 citation 會阻擋 promotion。

## 20. Agent 與租約

agent 不得自授權、共享 writer root 或寫入 checker partition。過期／錯誤 lease token、cycle 與 partial child failure 均 fail closed。

## 21. Harness

每個 action 必須具備 precondition、scope、network、rollback、evidence 與 attempt budget。`plans/HARNESS_ACTIONS.jsonl` 保存逐次結果，不覆寫失敗歷史。

## 22. Windows 路徑

使用 LiteralPath/resolve 驗證，拒絕 reserved names、case collision、symlink/junction/reparse point。Unicode 與含空白 temp path 已有 deterministic test。

## 23. Network

正式 command registry 預設 `network=OFF`。Hermes 安裝的 GitHub/locked package download 是獨立、已記錄的有限網路例外。

## 24. Secrets

證據不得保存 token/key 值。Hermes runtime validation 只移除已知 secret env name，不讀取或輸出內容；若 stdout 洩漏必須 redact 並啟動 revoke/rotate。

## 25. Observability

結構化事件不得預設記錄 prompt/content。no-progress watchdog、retry budget 與 terminal state 必須可觀測。

## 26. FinOps

budget policy 依 continue/degrade/stop-escalate 三段執行。超過 stop threshold 不得繼續遞迴或無限重試。

## 27. SBOM

執行 `scripts\sbom.ps1` 生成 CycloneDX 1.6 與 reconciliation receipt；目前只聲明本機 installed-package exact reconciliation，不聲明漏洞掃描通過。

## 28. 測試

執行 `scripts\test.ps1`。測試涵蓋 Spine、knowledge、agents/providers、controls、security、recovery、HLPE、Hermes qualification 與 assurance gates。

## 29. 備份

執行 `scripts\backup.ps1` 建立不可覆寫 SQLite backup 與 SHA-256 manifest。備份位於 ignored `var/backups/`。

## 30. 還原演練

執行 `scripts\restore-drill.ps1`，只會寫入 create-new `worktrees/restore-drill/`，並驗證 hash、integrity、schema、requirement/provider counts 與 observed RTO。

## 31. TT Reconciliation

更新 `source-freeze/TT_LEDGER.csv` 後執行 `scripts\reconcile-tt.ps1`。`TEMP_CLOSED` 在 Shared Spine 仍視為 open/blocking，直到符合 close criteria。

## 32. Release Reduction

blocking TT、過期／scope mismatch evidence 或 exact-set mismatch 都會把候選降為 FAIL/TEMP_CLOSED。LLM judge 不能覆寫 deterministic oracle。

## 33. Local Package

`scripts\package.ps1` 產生 deterministic local ZIP 與 readback receipt。ZIP 代表 current local-delivery payload（不包含 production deployment）；TST-092 已以獨立 checker 在 same-HEAD/same-package 上完成 INDEPENDENT_CASE_PASS（exact-set、0 hash mismatch）。

## 34. Independent NRTV

獨立 checker 必須從 frozen inputs 與版本化證據重跑，不可沿用 maker 的內部推理。maker pass 與 independent pass 是不同欄位。

## 35. 已知限制

- `TT-A3-HERMES-RUNTIME`：`TEMP_CLOSED_CORE`（non-blocking；Hermes runtime 核心驗證部分項目以 temp-closed 揭露）。
- Memory/Knowledge/RAG/KG 均為 local-first SQLite/FTS runtime（RUNTIME_PASS）；GraphRAG、graphiti、vector backend 依 source 為 `DEFERRED_SOURCE_BACKED`，未宣稱 runtime。
- production 一律 `NOT_CLAIMED`；本文件與所有 evidence 僅代表 local delivery candidate。

## 36. 問題處理與交接

發生 mismatch 時停止受影響 flow，保存 evidence，開 TT 並標明最早 owner、close criteria 與 rollback。交接 packet 缺 rollback、capability 或 field-level verdict 時不得 ACK。

## 37. Knowledge Workbench（Obsidian + LLM Wiki）

Knowledge Workbench 為產品正式 extension（source P0 disposition 與 current execution state 見下）：

- **Obsidian**：官方 `obsidianmd/obsidian-releases` v1.13.4（user-level 安裝於 `%LOCALAPPDATA%\Programs\Obsidian`）。`source_p0_disposition=OPTIONAL`、`current_execution_scope=USER_AUTHORIZED_ACTIVE_EXTENSION_THIS_RUN`。功能 inventory 30/30 RUNTIME_PASS。
- **LLM Wiki**：`atomicstrata/llm-wiki-compiler` v1.1.0（npm，MIT，isolated prefix `var/workbench/llm-wiki`）。角色 `knowledge.K09.wiki_compiler`。CLI inventory 16/16；`ingest/status/schema/profile/lint/review/state/recover/rules` 等 local 功能 RUNTIME_PASS。
- **AI 編譯路徑**：`llmwiki compile/refresh/query` 需要 ANTHROPIC provider credential → `EXTERNAL_CREDENTIAL_GATED`（未偽裝為 PASS、未寫入任何 secret）。
- **Canonical truth 不變**：Git Markdown / Source Ledger / Shared Spine 仍是唯一 authority；Obsidian vault 與 LLM Wiki 產出皆為 derived/candidate/workbench，禁止第二 canonical truth。
- **Obsidian 編輯流向**：編輯 → filesystem/Git diff → candidate → 驗證/admission → KnowledgePack/Wiki/RAG/KG rebuild，不得直接成為 authority。
- **Withdrawal/Conflict**：withdraw source → LLM Wiki/RAG/KG/Obsidian 一致失效；同 rank 衝突不靜默合併，走 Conflict/TT。
- **Fallback**：Obsidian/LLM Wiki 不可用時，Git Markdown + RAG core 獨立運作（UEX-W09 PASS）。
- **Uninstall**：移除 workbench 擴充後 core HG-KSEOS 仍完整運作（UEX-W10 PASS）；llm-wiki 安裝於 var/workbench isolated prefix，不影響 canonical。
- **AI 功能若需 external credential**：terminal = `EXTERNAL_CREDENTIAL_GATED`，不購買、不綁卡、不寫 secret。

## 38. Autonomous Project Lifecycle（自動專案生命週期）

HG-KSEOS 提供產品級頂層專案入口，使新專案不再需要外部 GPT 逐輪生成施工指令。

### A. 5分鐘 Quick Start

1. `python -m hg_kseos.cli doctor` — 健康檢查。
2. `python -m hg_kseos.cli project start --goal "<目標>" --source <路徑> --target-root <目標目錄>` — 建立專案。
3. `python -m hg_kseos.cli project status <project_id>` — 查看狀態。
4. `python -m hg_kseos.cli project resume <project_id>` — 中斷後恢復。
5. `python -m hg_kseos.cli project checkpoint <project_id>` — 寫入 checkpoint。
6. `python -m hg_kseos.cli evolution status` — 查看 evolution 訊號/候選。

最少輸入：`goal`、`source_paths`、`target_root`。其餘欄位 best-effort 自動推導，只有法位衝突/目標不明/credential/destructive/security 才需要使用者。

### B. 新專案一條龍

```text
目標/文件 → HG-KSEOS → 規劃 → 實作 → 自修補 → 驗收 → 交付
```

- 系統自動：source intake/hash/admission、intent roundtrip、TaskSpec/WorkOrder 自動生成、執行/修補/checkpoint/resume、independent acceptance、release/delivery。
- 使用者介入時機：僅 authority boundary（credential、destructive、constitutional、production）。

### C. Automatic vs HITL

```text
Task routing         AUTO
Memory/RAG/KG        AUTO
Skill selection      AUTO
WorkOrder planning   AUTO
repair               AUTO
tests                AUTO
independent checker  AUTO
candidate evolution  AUTO
credential           HITL
destructive action   HITL
constitutional       HITL
production           HITL
```

### D. Governed Evolution（受治理自進化）

```text
observe → gap → FIT-GAP → candidate → sandbox → eval → independent checker
→ promotion gate → canary / rollback
```

使用者不需要每次輸入「請自我進化」。只有 source 定義的 authority gate（例如 COV-11-06：promotion 需 independent verifier + Human Policy Owner）才需要 Human `APPROVE / REJECT`。

### E. Project status / diagnostics

```text
python -m hg_kseos.cli project status <project_id>   # lifecycle state / transitions
python -m hg_kseos.cli evolution status              # signals / candidates
```

### F. Knowledge Workbench

- Obsidian：official `obsidianmd/obsidian-releases` v1.13.4（source P0 OPTIONAL/PLANNED_NOT_EXECUTED；current execution = USER_AUTHORIZED_ACTIVE_EXTENSION_THIS_RUN，installed + runtime-qualified）。
- LLM Wiki：`atomicstrata/llm-wiki-compiler` v1.1.0（MIT，npm pin）；AI compile/refresh 路徑為 EXTERNAL_CREDENTIAL_GATED（不存 secret）。
- Canonical truth：Git Markdown / Source Ledger / Shared Spine；Obsidian 編輯 = candidate，不得直接成為 authority。
- Withdrawal/conflict：withdraw → LLM Wiki/RAG/KG/Obsidian 一致失效；conflict 不靜默合併。
- Fallback：Obsidian/LLM Wiki 不可用時 Git Markdown + RAG core 獨立運作。

### G. Recovery

- `resume`：讀 checkpoint、驗 hash、跳過已完成 immutable work、續跑第一個未完成合法 state。
- `rollback`：WorkOrder rollback pointer + rollback_records；canary regression → auto-disable + rollback + TT。
- `restore`：backup/restore drill（RTO <15ms）。
- `cancel`：CANCELLED side state；attempt budget 耗盡 → FAILED + STOP_ESCALATE（不無限遞迴）。

## 39. 產品入口命令（實作驗證）

```text
python -m hg_kseos.cli project start|status|resume|advance|checkpoint|intake
python -m hg_kseos.cli evolution status|signal|candidate
```

以上命令皆由 `src/hg_kseos/cli.py` 實作並有對應測試（`tests/test_autonomy_evolution.py`）。

## 40. Hermes v0.20 Native Runtime Reuse Convergence（Task-013）

### 40.1 認證身份

- 版本 `0.20.0`／tag `v2026.8.3`／commit `3c27eb6234bf91b8ceee9e9071591b31e9b148cb`（三者對齊，source + runtime readback 皆 PASS）。
- 安裝方式：exact-tag git checkout → 隔離 venv（系統 Python 3.11.9）→ editable install；`HERMES_HOME`、config、kanban.db 全部隔離在 disposable qualification root（`%TEMP%\hgk-hermes-v020-qual`），未污染 production v0.18.2 安裝。
- 禁止：`hermes update`、floating main、覆寫 v0.18.2、系統 PATH 變更。

### 40.2 Kanban 使用規則

- 用途：cross-role／durable／restart-surviving／parallel-dependent tasks → Hermes Kanban card（create→ready→claim→running→complete；dependency 以 parent/child gating；HITL 以 block + typed reason；retry 以 max-retries + run ledger；heartbeat/reclaim 單一 writer 由原子 claim 保證）。
- 不用：small atomic task 不強迫 Kanban（直接 Hermes turn / 既有 bounded lane）；簡單任務禁止每個步驟都開 card。
- HG-KSEOS WorkOrder → Hermes Kanban 為 thin adapter：Shared Spine 只存 workorder_id/pointer/normative state；Kanban board/task id/runtime state 由 Hermes 持有。

### 40.3 `/goal` 使用規則

- 用途：long-running WorkOrder → 把 WorkOrder contract 投影成 goal completion contract（outcome/verification/constraints/boundaries/stop_when）。
- `/goal done` 不等於 HG-KSEOS PASS：goal judge 只是 runtime stop helper；final acceptance 仍須 raw evidence → HG-KSEOS independent checker → reducers → release。
- Resume：goal state 存於 SessionDB `state_meta`（key `goal:<session_id>`），process restart 後可恢復。

### 40.4 Runtime checkpoint vs Normative checkpoint

- Hermes v0.20 負責：session state、goal state、worker runtime state、Kanban state、Hermes checkpoint runtime。
- HG-KSEOS 負責：project normative checkpoint、source hashes、WorkOrder IDs、Hermes session/Kanban refs、evidence refs、release state、rollback pointer。
- 不鏡像 Hermes runtime；Shared Spine 只存 pointer/ref。

### 40.5 Tool recovery / Compression / Approvals

- Tool self-recovery（terminal retry/truncation readback、write_file on-disk verify、patch already-applied、search near-miss）由 Hermes v0.20 提供；HG-KSEOS 未發現重複 wrapper（reuse binding matrix 20 項、duplicates=0）。
- Context compression 使用 Hermes v0.20（enabled、threshold 0.5、target_ratio 0.2 顯式設定）；HG-KSEOS Memory/RAG/SourceUnit 不因 compression 刪除。
- Approvals 顯式 policy：`approvals.mode: manual`（fail-closed；timeout 60s；不得以 `off` 作正常 profile）。實測：`rm -rf` 觸發 `pending_approval`，agent 拒絕繞過；POSIX 危險 pattern 由 Hermes 攔截，Windows-native path guard 由 HGK security 層保留。

### 40.6 Skill governance

- Hermes 負責 skill file 機制／loading／invocation／curator（archive-only，永不 promote，只作用於 `created_by=agent`）。
- HG-KSEOS 負責 candidate admission、FIT-GAP、sandbox、negative/security、holdout、NRTV、independent checker、promotion policy、COV-11-06 Human Policy Owner gate、rollback acceptance。

### 40.7 v0.20 未啟用／deferred

- MCP：本輪無 active requirement → `DEFERRED_NOT_REQUIRED`（不新增 MCP server）。
- A2A、signed webhooks、voice、wake words、desktop plugin SDK、新 GUI：`STANDBY`／`NOT_REQUIRED`（不裝服務、不開 port）。
- Codex App-Server runtime：`NOT_PRIMARY`（current certified route 不變）。

### 40.8 v0.20 Switch / Rollback 程序（HITL）

1. 依 §12 的 exact-tag 程序建 disposable venv + 隔離 HERMES_HOME（不覆寫 v0.18.2）。
2. 驗證 `hermes --version` = v0.20.0、`hermes doctor` blocking=[]、一次 real inference、一次 real Codex route。
3. 將 config/hermes.json `executable` 指向 v0.20 venv，`scripts\hermes-core.ps1` 通過。
4. Rollback：刪除 disposable root，還原 config/hermes.json rollback baseline（v0.18.2），`hermes-core.ps1` 恢復 PASS。
5. 全程 production `NOT_CLAIMED`。

## 41. Named Method Runtime Readiness（Task-014）

Task-014 將 OpenSpec 與 gstack 兩個 named-method 工具以真實 runtime 身份接進 HG-KSEOS（self-bootstrap：HG-KSEOS 自己完成 detect→FIT-GAP→install→route→pilot→negative→rollback→independent certify）。

**OpenSpec（brownfield spec projection）**

- Exact pin：`@fission-ai/openspec@1.8.0`（tag `v1.8.0`、release commit `d57889664…`、MIT、Node >=20.19）。
- 角色：`BROWNFIELD_ENGINEERING_DEFINITION_ADAPTER`；`engineering_definition.brownfield → openspec`，fallback `hgk_native_prw`。
- 使用上游官方 Hermes skills-only 整合（`.hermes/skills/openspec-*/SKILL.md`），透過 `skills.external_dirs` 載入；HG-KSEOS 不重寫 translator。
- XOR：brownfield（OpenSpec active）與 greenfield（Spec Kit STANDBY / native）互斥；OpenSpec 不是 Root SSOT、不是 release owner、不是 primary writer（Codex CLI 仍為 bounded writer）。
- 流程：brownfield 需求 → 自動 route OpenSpec → explore/propose → spec delta → Codex 實作 → tests → OpenSpec validate/archive → HGK independent checker + reducer 收尾。

**gstack（selected advisory slices）**

- Exact pin：`garrytan/gstack@1.61.0.0`（commit `94993f74012782fd94416dd44b8314f6363a13a4`、MIT、bun runtime）。
- 選定 slices（advisory only）：`office-hours`（ambiguity 諮詢）、`plan-eng-review`、`review`、`qa`、`cso`（security 諮詢）、`ship`（release-readiness advisory，`final_authority=false`）、`retro`。
- 生成：`bun run gen:skill-docs --host hermes`（54 skills，flat `gstack-*` 命名）；`setup --host hermes` 只印指示並 exit 0，不等於 certified（必須 effective-load + real invocation）。
- 已知 pinned host-generation gap（已記錄 + thin adapter 解決）：`gstack-review` 要求 `.hermes/skills/review/*`（checklist.md 等 sibling assets），generator 未生成——adapter 把 repo `review/` 拷入 project `.hermes/skills/review/`。
- 邊界：gstack ship ≠ release authority；gstack review ≠ independent checker；gstack cso ≠ HGK security authority；gstack office-hours ≠ product authority。輸出皆為 EvidenceCandidate / advisory，最終由 HGK checker/reducer 決定。

**Router（deterministic，不靠 LLM 猜）**

- `brownfield/migration → openspec`；`greenfield → XOR_GREENFIELD`；`high-impact ambiguity → gstack.office-hours`；`plan → gstack.plan-eng-review`；`implementation complete → gstack.review`；`QA → gstack.qa`；`security-sensitive → gstack.cso`；`release readiness → gstack.ship（advisory）`；`retro → gstack.retro`；其餘 → native。
- Provider 不可用：route state 顯式 `DEGRADED` + certified native fallback（EvidenceEnvelope 記錄 fallback）；禁止「tool 沒跑卻宣稱 tool PASS」。

**Activation invariant（fail-closed）**

- 任何 active canonical flow 引用的 named method 必須 runtime-ready（identity/pin/install/binding/doctor/pilot/independent-cert）或存在 certified native substitution，否則 `FAIL_CLOSED`（CoverageReducer 檢查 `*_missing_*`、`dual_spec_owner`、`second_orchestrator`、`release_authority_escape` 等一律為 0）。

**診斷 / 停用 / 回滾**

- 診斷：`openspec doctor`（於 fixture root）、`bun run gen:skill-docs --host hermes` 後檢查 `.hermes/skills/`、Hermes `skills list` 看 `gstack-*`/`openspec-*` 是否 discover。
- 停用：移除 `skills.external_dirs` 中的 fixture/gstack 路徑即停用 named-method skills；router 仍 fallback 到 native。
- 回滾：刪除 fixture `.hermes/skills`（candidate projection），native PRW/review/QA/security 全數保留；canonical Requirement/ADR/WorkOrder 不刪。
- Promotion 依 COV-11-06：independent verifier + Human Policy Owner 批准（本輪 A0 Prompt 提供 conditional authorization，source locator 記錄於 evidence）。
