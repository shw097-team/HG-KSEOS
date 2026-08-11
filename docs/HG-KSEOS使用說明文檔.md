# HG-KSEOS 使用說明文檔

> 本文是 **projection / operational manual**，不是 authority / policy source / requirement source。
> 權威來源依 §Authority（P0-CIP r2、實作前開發文檔包、三份藍圖、FINAL_r2 控制包、Hermes DOC-01..20，均 hash 綁定）。
> **Current claim**: `HG-KSEOS_LOCAL_DELIVERY_PASS — EXTERNAL FINAL ACCEPTED`。Current changeset = **Task-015**（Final External Evidence Coherence + Unique Denominator + Receipt Lineage，`HGK-TASK014-FINAL-EXTERNAL-EVIDENCE-COHERENCE-UNIQUE-DENOMINATOR-RECEIPT-LINEAGE-015`）。Task-011/012/013/014 為 historical accepted lineage。Production 一律 `NOT_CLAIMED`。歷史施工細節見 §Changelog / Historical Baselines。

---

# Part I — 5 分鐘開始

## 1. HG-KSEOS 是什麼

HG-KSEOS 是受治理的多閘門本機交付系統：把「使用者目標 → 來源 → 需求 → 設計 → 計畫 → WorkOrder → 實作 → 測試 → 修補 → 獨立驗收 → reducers → local delivery」整條鏈路自動化，並以 immutable evidence、independent checker 與 fail-closed 閘門維持可稽核性。

## 2. 目前狀態

- **Current claim**: `HG-KSEOS_LOCAL_DELIVERY_PASS — EXTERNAL FINAL ACCEPTED`（以 current External Acceptance 為準；hard-check denominator 按 **unique predicate ID** 計數，duplicate ID 本身是 fail-closed defect）。
- **Hermes**: v0.20.0（tag `v2026.8.3`、commit `3c27eb6234bf91b8ceee9e9071591b31e9b148cb`）`ACTIVE_SELECTED_CERTIFIED`；provider `opencode-go`、model `deepseek-v4-flash`。
- **Named methods**: OpenSpec `CERTIFIED_ACTIVE_BROWNFIELD`；gstack `CERTIFIED_ACTIVE_SELECTED_SLICES`。
- **Production**: `NOT_CLAIMED`（Local Delivery PASS ≠ Production Authorized）。

## 3. Canonical Root

`C:\Projects\Agent_Workspace\HG-KSEOS` 是唯一 canonical local root（writable root）。Source/Authority、Shared Spine、RBWI/WP、WorkOrder、AGENTS/SKILLS、Harness/Loop、證據與 reducers 皆在此 root。Obsidian vault、LLM Wiki 產出、RAG/KG 皆為 derived/candidate。

## 4. 啟動與健康檢查

```text
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\doctor.ps1     # blocking 為空且 verdict=PASS 才是健康
python -m hg_kseos.cli doctor
```

## 5. 建立新專案（最少輸入）

```text
python -m hg_kseos.cli project start --goal "<目標>" --source <路徑> --target-root <目標目錄>
```

最少輸入：`goal`、`source_paths`、`target_root`。其餘欄位自動推導。

## 6. 查看狀態 / Resume / Stop

```text
python -m hg_kseos.cli project status <project_id>
python -m hg_kseos.cli project resume <project_id>      # 中斷後恢復
python -m hg_kseos.cli project checkpoint <project_id>  # 寫入 normative checkpoint
python -m hg_kseos.cli evolution status                 # evolution 訊號/候選
```

Stop：完成後由 reducers 收尾；attempt budget 耗盡會 `FAILED + STOP_ESCALATE`（不無限遞迴）。

---

# Part II — 一條龍 Autonomous Project Lifecycle

## 7. 流程

```text
User goal / source
→ Source Discovery → Source Admission → Intent → Requirements → Design → Plan → WorkOrders
→ Hermes runtime → Codex implementation → tests → repair → independent acceptance → reducers
→ local delivery
```

- **external GPT 不是 normal lifecycle dependency**。
- User 不需要手動選 Agent / Skill / RAG / KG。
- normal unnecessary HITL = 0。
- 高風險 / authority / credential 才 HITL（見 §8）。

## 8. Automatic vs HITL

```text
Task routing / Memory / RAG / KG / Skill selection / WorkOrder planning
repair / tests / independent checker / candidate evolution     AUTO
credential / destructive action / constitutional / production  HITL
```

## 9. Governed Evolution

```text
observe → gap → FIT-GAP → candidate → sandbox → tests/negative/security/holdout/NRTV
→ independent checker → policy gate → canary / rollback
```

Human 角色 = **Authority / Policy Gate**，不是逐步操作員。COV-11-06：promotion 需要 independent verifier + Human Policy Owner（source-resolved）；不存在「LOW risk 一律自動 promote」。

## 10. Self-Repair（兩層，不重複）

- **Hermes tool self-recovery**：terminal retry/truncation readback、write_file on-disk verify、patch already-applied no-op、search near-miss、failure hints、iteration budget。
- **HG-KSEOS product-level self-repair**：failed acceptance、requirement mismatch、security regression、architecture defect → repair WorkOrder → 獨立 recheck。
- Hermes 負責 runtime 摩擦修復；HG-KSEOS 負責產品規範性修復。

---

# Part III — Hermes v0.20 Runtime

## 11. 身份與所有權

- **版本**: `0.20.0` / tag `v2026.8.3` / commit `3c27eb6234bf91b8ceee9e9071591b31e9b148cb`（exact-tag 三者對齊；禁止 floating latest / `hermes update`）。
- **Canonical executable**: `var\hermes-v020\venv\Scripts\hermes.exe`（config/hermes.json `HGK-HERMES-BINDING/2`，`ACTIVE_SELECTED_CERTIFIED`；`scripts\hermes-core.ps1` PASS）。
- **Canonical HERMES_HOME**: `var\hermes-v020\home`（隔離；kanban.db、SessionDB 獨立；不污染 desktop home）。
- **Provider/model**: `opencode-go` / `deepseek-v4-flash`（base `https://opencode.ai/zen/go/v1`；憑證 `OPENCODE_GO_API_KEY` env-ref，不寫入 evidence）。

責任劃分：

```text
HG-KSEOS = governance / normative plane（authority、WorkOrder admission、evidence、checker、reducers、release）
Hermes   = runtime orchestration plane（Kanban、/goal、SessionDB、checkpoint、tool recovery、compression、approvals）
Codex    = bounded coding executor
OpenCodex = transport（ocx start --port 10100 後 codex 路由才可用）
OpenCode Go / DeepSeek = provider / model
```

Rollback baseline：v0.18.2（tag `v2026.7.7.2`、commit `9de9c25f…`）保留為 sealed rollback baseline。Desktop 互動表面與 canonical 解析路徑為兩件事（見 §Changelog）。

## 12. Kanban 何時用

```text
small atomic task                    → direct/bounded execution（不強迫 card）
long persistent objective            → Hermes /goal
durable / cross-role / restart-surviving → Hermes Kanban
parallel dependent tasks             → Kanban dependency graph
```

**Hermes runtime state ≠ HGK normative project state**：

```text
HGK WORKORDERS_ADMITTED → Kanban ready
HGK EXECUTING           → Kanban running
HGK BLOCKED_HITL        → Kanban blocked + governance reason
HGK REPAIRING           → repair/retry task
HGK RELEASE_REDUCING    → HGK owns（Kanban 不擁有）
HGK DELIVERED           → HGK owns（Kanban 不擁有）
```

HG-KSEOS WorkOrder → Hermes Kanban 為 thin adapter：Shared Spine 只存 workorder_id / pointer / normative state。

## 13. `/goal` 何時用

- long-running WorkOrder → 把 WorkOrder contract 投影成 goal completion contract（outcome / verification / constraints / boundaries / stop_when）。
- **`/goal done` ≠ HG-KSEOS PASS**：goal judge 只是 runtime stop helper；final acceptance 仍須 raw evidence → independent checker → reducers → release。

## 14. Runtime checkpoint vs Normative checkpoint

- **Hermes 保存**: session、goal、worker、Kanban runtime、runtime checkpoint。
- **HG-KSEOS 保存**: project normative state、authority refs、WorkOrder IDs、session/Kanban refs、source/evidence hashes、release state、rollback pointer。
- 兩者不是鏡像；Shared Spine 只存 pointer/ref。

## 15. Tool recovery / Compression / Approvals

- Tool self-recovery 由 Hermes v0.20 提供（reuse binding matrix：duplicates=0，HG-KSEOS 無重複 wrapper）。
- Context compression 使用 Hermes v0.20（enabled；HG-KSEOS Memory/RAG/SourceUnit 不因 compression 刪除）。
- Approvals：`approvals.mode: manual`（fail-closed；不得以 `off` 作正常 profile）；`rm -rf` 等危險 pattern 觸發 `pending_approval`；Windows-native path guard 由 HGK security 層保留。

## 16. Skills 治理邊界

- Hermes 負責 skill file 機制 / loading / invocation / curator（archive-only，永不 promote）。
- HG-KSEOS 負責 candidate admission、FIT-GAP、sandbox、negative/security、holdout、NRTV、independent checker、promotion policy、COV-11-06 Human Policy Owner gate、rollback acceptance。

---

# Part IV — Named Methods（OpenSpec / gstack）

## 17. OpenSpec（brownfield spec projection）

- **身份**: `@fission-ai/openspec@1.8.0`（tag `v1.8.0`、release commit `d57889664…`、MIT、Node >=20.19）— `CERTIFIED_ACTIVE_BROWNFIELD`。
- **角色**: `BROWNFIELD_ENGINEERING_DEFINITION_ADAPTER`。不是 Root SSOT、不是 release authority、不是 primary writer（Codex CLI 仍為 bounded writer）。
- 使用上游官方 Hermes skills-only 整合（`.hermes/skills/openspec-*/SKILL.md`，`skills.external_dirs` 載入）。
- **流程**: brownfield 需求 → deterministic route → OpenSpec explore/propose → spec delta → HGK Requirement/ADR/WorkOrder mapping → Hermes/Codex 實作 → tests → OpenSpec validate/archive → HGK final acceptance。

## 18. Spec Kit XOR

- `brownfield → OpenSpec active`；`greenfield → Spec Kit/native profile`。禁止雙 spec owner。
- tool unavailable → 顯式 `DEGRADED` / native fallback；禁止 silent imitation。

## 19. gstack（selected advisory slices）

- **身份**: `garrytan/gstack@1.61.0.0`（commit `94993f74012782fd94416dd44b8314f6363a13a4`、MIT、bun）— `CERTIFIED_ACTIVE_SELECTED_SLICES`。
- **Selected slices（advisory only）**: `office-hours`（ambiguity 諮詢）、`plan-eng-review`、`review`、`qa`、`cso`（security 諮詢）、`ship`（release-readiness advisory，`final_authority=false`）、`retro`。
- 生成：`bun run gen:skill-docs --host hermes`（54 skills，flat `gstack-*`）；`setup --host hermes` exit 0 ≠ certified（需 effective-load + real invocation）。
- 已知 pinned host-generation gap（已記錄 + thin adapter）：`gstack-review` 需要 `.hermes/skills/review/*`，generator 未生成 → adapter 把 repo `review/` 拷入 project `.hermes/skills/review/`。
- **邊界**: gstack ship ≠ ReleaseReducer；gstack review ≠ independent checker；gstack cso ≠ HGK security authority；gstack office-hours ≠ product authority。輸出 = EvidenceCandidate / advisory。

## 20. Named-Method Router（deterministic）

```text
brownfield/migration → openspec
greenfield           → XOR_GREENFIELD / native
plan                 → gstack.plan-eng-review（selected）
implementation done  → gstack.review
QA required          → gstack.qa
security-sensitive   → gstack.cso
release readiness    → gstack.ship（advisory only）
high-impact ambiguity→ gstack.office-hours
retro                → gstack.retro
其餘                 → native
```

- 決定來自 registry lookup，**不是 LLM 猜測**。
- **fake invocation = prohibited**；**silent fallback = prohibited**（unavailable → 顯式 DEGRADED + certified native fallback，EvidenceEnvelope 記錄）。

## 21. Fallback / Rollback（真實存在的程序）

- Hermes v0.20 rollback baseline：v0.18.2（還原 config executable + hermes-core.ps1 驗證）。
- OpenSpec disable → native PRW fallback（移除 external_dirs 綁定 + fixture skill projection；canonical Requirement/ADR/WorkOrder 不刪）。
- gstack disable → native review/QA/security/release advisory。
- Provider failure → route DEGRADED + native fallback。
- Checkpoint/resume、package rollback：見 §Part VI 與 scripts（backup/restore-drill）。

---

# Part V — Governance & Knowledge

## 22. 權威與治理

- 權威順序依 source-freeze 工件；低權威來源不得覆寫高權威規則。
- Canonical database: `var/shared-spine/hg-kseos.db`（單一 writer 契約）。
- 同 rank 衝突 → Conflict/TT，不靜默合併。

## 23. Knowledge Workbench（Obsidian + LLM Wiki）

- **Canonical source** = Git Markdown / Source Ledger / Shared Spine。
- **Obsidian** = human workbench（v1.13.4，user-level）；**LLM Wiki** = derived compiler（`atomicstrata/llm-wiki-compiler` v1.1.0，npm pin，isolated prefix `var/workbench/llm-wiki`）；**RAG/KG** = retrieval/reasoning surfaces（SQLite/FTS5 local-first）。
- AI 編譯路徑（`llmwiki compile/refresh/query`）需要 ANTHROPIC credential → `EXTERNAL_CREDENTIAL_GATED`。
- GraphRAG / vector backend = `DEFERRED_SOURCE_BACKED`（本輪不啟用）。
- 編輯流向：filesystem/Git diff → candidate → 驗證/admission → rebuild；不得直接成為 authority。

## 24. 安全邊界

禁止：寫入來源、越出 WorkOrder admitted write-set / target-root / isolated worktree boundary、路徑穿越、reparse point、未授權網路、秘密讀取、遠端發佈、部署、production mutation。所有高風險擴權維持 HITL。證據不得保存 token/key 值。

---

# Part VI — Evidence / Acceptance / Release

## 25. 如何判斷 current candidate 是否可交付

依序檢查：

```text
fresh test denominator（current task/head 綁定；schema HGK-CURRENT-TEST-DENOMINATOR/2）
CoverageReducer v2 decision
UserExperienceReducer v1 decision
TST-092 independent receipt（current Task 命名 + same HEAD/package）
External Acceptance（unique hard-check IDs 全 PASS、duplicates=0）
Final Evidence（single current identity；status/counts 與 acceptance machine 一致）
blocking TT = 0
```

**ad-hoc verification ≠ canonical suite green**：前者是針對變更行為的聚焦檢查，後者是 fresh discovery 的完整套件結果。

## 26. Hard-Check denominator 語意

External Acceptance 的 hard-check denominator 按 **unique predicate ID** 計數；duplicate ID 本身是 fail-closed defect（`hard_check_row_total == hard_check_unique_id_total` 且 `duplicate_hard_check_id_count == 0`）。數量本身不是品質；不保證任何固定數字。

## 27. Evidence lineage

- Task-011/012/013/014 = historical accepted lineage（不可覆寫；TST-092 historical receipts immutable）。
- current closure = current candidate only。
- 舊 HEAD/package 保留在 Changelog / Historical Baselines，不得在普通使用章節稱 current。

## 28. Package / Release

- `scripts\package.ps1`（或 `tools/package_local.py`）產生 deterministic local ZIP + exact-set readback + manifest。
- TST-092 以獨立 checker 在 same-HEAD/same-package 上 INDEPENDENT_CASE_PASS。
- blocking TT、過期/scope-mismatch evidence、exact-set mismatch → FAIL/TEMP_CLOSED。LLM judge 不能覆寫 deterministic oracle。

## 29. 備份 / 還原

`scripts\backup.ps1`（不可覆寫 SQLite backup + SHA-256 manifest，`var/backups/`）；`scripts\restore-drill.ps1`（寫入 `worktrees/restore-drill/`，驗證 hash/integrity/schema/counts/RTO）。TT ledger：更新 `source-freeze/TT_LEDGER.csv` 後 `scripts\reconcile-tt.ps1`。

---

# Part VII — Diagnostics & Troubleshooting

## 30. Diagnostics（實際存在命令）

```text
python -m hg_kseos.cli doctor
python -m hg_kseos.cli project status <id> | resume <id> | checkpoint <id>
python -m hg_kseos.cli evolution status | signal | candidate
powershell -File .\scripts\doctor.ps1 | hermes-core.ps1 | sbom.ps1 | test.ps1
hermes doctor / hermes --version            # canonical v0.20 executable
openspec doctor                             # 於 OpenSpec fixture root
bun run gen:skill-docs --host hermes        # gstack 重新生成 Hermes skills
ocx status / ocx start --port 10100         # Codex transport
```

## 31. Troubleshooting

| 症狀 | 診斷 | 安全動作 | 升級/HITL 邊界 |
|---|---|---|---|
| Hermes version mismatch | `hermes --version` vs config pin | 依 §11 還原/指向 canonical executable | 切換 desktop surface = HITL |
| provider/model route mismatch | doctor / chat 測試 | 檢查 `OPENCODE_GO_API_KEY` env-ref | credential 遺失 = HITL |
| Kanban blocked | `hermes kanban` 看 reason | 依 governance reason 修正後 unblock | authority 衝突 = HITL |
| goal not progressing | `/goal status` | 檢查 turn budget / stop_when | — |
| OpenSpec unavailable | `openspec doctor` | 顯式 DEGRADED + native PRW fallback | 重裝需網路 = 記錄 |
| OpenSpec effective-load fail | `hermes skills list` 看 openspec-* | 檢查 skills.external_dirs（YAML list） | — |
| gstack skill/reference missing | 檢查 `.hermes/skills/gstack-*` + `review/` sidecar | 重新 gen:skill-docs + adapter 拷貝 review/ | — |
| named-method DEGRADED | router trace | native fallback（EvidenceEnvelope 記錄） | — |
| silent fallback blocked | cross-artifact checker | fail-closed，禁止 fake PASS | — |
| promotion waiting HITL | evolution status | 等待 Human Policy Owner APPROVE/REJECT | COV-11-06 = HITL |
| test denominator mismatch | denominator task/head 綁定檢查 | fresh discovery | — |
| TST-092 mismatch | receipt head/package vs git | 重新 seal | — |
| External Acceptance fail | unique-ID predicate 明細 | 修 smallest owner | — |
| Final Evidence currentness mismatch | raw-byte readback + cross checker | 重新 normalize（machine projection） | — |

---

# Part VIII — Production Boundary & Changelog

## 31b. Reference Project-001 Milestone（RP-001 operational delta）

RP-001（`HGK-REFERENCE-PROJECT-001`，SQS-THC / TW-ICT FSDT-Stack dogfooding）已
**MILESTONE_CLOSED**——從施工/驗收專案轉為完成的 dogfooding milestone。對日常操作的影響：

1. **普通使用者入口**：只需 `goal` + `source` + `target_root` 最少輸入（§5）；
   不用手選 WP / RBWI / Agent / Skill / provider / test runner。
2. **責任邊界**：HG-KSEOS = governance/normative；Hermes = runtime orchestration；
   Codex = bounded coding executor（§11）。
3. **normal repair loop**：`failure → smallest owner repair → affected regression → continue`；
   不做整輪 reseal（除非 platform-level invariant 變更）。
4. **Governed Evolution 升級條件**：只有真實平台級缺陷才形成 candidate；
   低價值 evidence cosmetics / readback-ordering debt 記 non-blocking debt，自然 reseal 時處理。
5. **Canonical Evidence Graph / Frozen Oracle / Subject**：是 milestone/qualification controls，
   不是每次日常修改都要 final seal。
6. **Release applicability**：`WORKSPACE_LOCAL`（日常）不需大型 package；
   `AUDIT_HANDOFF` 只需必要 review/attestation bundle；
   `DISTRIBUTABLE_RELEASE` 才啟完整 package/readback/rollback。
7. **self-closure trap guard**：product gates 已綠且只剩 non-blocking evidence debt →
   轉入真實任務，不再「驗收驗收」。
8. RP-001 retained regressions（EVO-003/004/005 gates）繼續在 canonical suite 保護；
   RP-001 closure record：`C:\Projects\Agent_Workspace\SQS-THC\evidence
eview\SQS_RP001_MILESTONE_CLOSURE_RECORD.md`。
9. User Guide 與 current authority 衝突時，authority / actual readback 優先，Guide 進修補。

## 32. Production Boundary

**Local Delivery PASS ≠ Production Authorized**。目前 `PRODUCTION = NOT_CLAIMED`：本文件與所有 evidence 只代表 local delivery candidate；未宣稱 remote CI / deploy / production 完成。

## 33. Changelog / Historical Baselines

早期施工歷史（companion / maker root / task-007..010 / Task-011 current / Task-012 / Task-013 old seal / Task-014 old seal）一律屬歷史，已由後續 sealed changeset 取代；TST-092 historical receipts（E08..E12、TASK013、HANDOFF、FINAL 等）immutable。各歷史 seal 的 HEAD/package 見對應 evidence/wave-* 工件。Task-015 是 HG-KSEOS 內部 evidence closure 終局線；下一工程階段 = Reference Project-001（真實新系統 dogfooding）。

**2026-08-11 RP-001 milestone**：`HGK-REFERENCE-PROJECT-001` 已 **MILESTONE_CLOSED**（見 §31b）。
RP-001 完成 WAVE1-WAVE5 + EVO-003/004/005：15/15 WO、211/211 SQS tests、274/274 HGK suite、
161/161 acceptance、EVO-005F frozen graph（root `6535d9cd…`）單一 truth。
此後 SQS 任務走 normal operational loop（`execute → test → repair → continue`）；
平台級 invariant defect 才升 HGK evolution candidate。
