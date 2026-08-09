# HG-KSEOS 使用說明文檔

## 1. 文件目的

本文件說明 HG-KSEOS 本機 canonical local 系統的安裝、操作、驗證、備份、回滾與交付。

**Current claim**: `HG-KSEOS_LOCAL_DELIVERY_PASS — EXTERNAL FINAL ACCEPTED`。Current changeset = **Task-011**（Autonomous Project Lifecycle + Governed Evolution，`HGK-AUTONOMOUS-PROJECT-LIFECYCLE-GOVERNED-EVOLUTION-CLOSURE-011`）；external acceptance semantic closure = **Task-012**（`HGK-TASK011-AUTONOMY-EVOLUTION-EXTERNAL-ACCEPTANCE-SEMANTIC-CLOSURE-012`）。Historical baseline：E10（task-009/010）為 lineage，已 superseded。後續新增 tracked ChangeSet 會形成新 candidate，未重新 seal 前不得沿用舊 acceptance。production 一律 `NOT_CLAIMED`。

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

Hermes 固定為 v0.18.2、tag `v2026.7.7.2`、commit `9de9c25f620ff7f1ce0fd5457d596052d5159596`。不得使用 floating latest。

## 13. Hermes 核心驗證

執行 `scripts\hermes-core.ps1` 僅驗證固定版本，不會 setup、登入、安裝 gateway、更新或卸載。

## 14. Hermes Provider

Hermes v0.18.2 使用 provider `opencode-go`、model `deepseek-v4-flash`（base `https://opencode.ai/zen/go/v1`）。憑證以 `OPENCODE_GO_API_KEY` env-ref 存放於 Hermes auth store（`%LOCALAPPDATA%\hermes\.env`），不寫入任何 evidence。OpenAI OAuth credential 保留未動。Provider 正向 pilot（P1–P10）與 Hermes→Codex closed loop 已 PASS。

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
