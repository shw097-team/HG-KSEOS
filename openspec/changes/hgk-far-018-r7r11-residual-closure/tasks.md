# Tasks — FAR-20261016-018

Status discipline: a box is ticked ONLY when the artifact proving it exists on disk. The round's own
premature ticks were caught and corrected here; an unchecked box is an honest statement, not a gap in work.

- [x] R0 Gate-1 route 經 live named-method registry，含不相關 flow 負控制（`ROUTE_CHECK.json`）
- [x] R1 CAPC contract C0–C9 編譯 → `PROMPT_COMPILE_PASS`（`compiler/*.stdout.txt`、`compiler-receipt.json`）
- [x] R2 HGK typed admission（project `FAR-018-R7R11-RESIDUAL`、WO-TS-RESIDUAL-01..05）
- [ ] R3 Kanban 板＋卡生命週期（create→claim→heartbeat→complete/block，全 CLI 收據）
- [ ] R4 W1 殘留全集（獨立子代理，primary sources）
- [ ] R5 W2 缺陷檔案（含 OS 強制唯讀隔離可行性實測、指標逐條驗證）
- [ ] R6 EXECUTE 車道：`opencode-go/deepseek-v4.1-flash`（CODEX CLI）產出可執行項目的 artifact
- [ ] R7 VERIFY/SECURITY 車道：pin `openai-codex/gpt-6.1-sol`（rank 2，`--require-arm`）獨立覆核
- [ ] R8 OWNER-gated 項目備妥為單一動作形式（不合併、不晉升、不編輯控制平面）
- [ ] R9 證據推送 `shw097-team/Fabric` 新前綴＋遠端 readback
- [ ] R10 移交 checkpoint＋單一證據 MD（鏡像三 review root，SHA-256 相等）
- [ ] R11 自檢測／自修補／自驗收＋受治理自我進化紀錄

## Disclosed deviations carried from R1 (recorded, not hidden)

- **duplication gate flagged**: the round's contract is 0.596 shingle-similar to the previous round's
  contract (`compiler/duplication.stdout.txt`). Cause: the mandate ordered search-and-reuse, and the C0–C9
  scaffolding was deliberately reused rather than re-derived; the round-specific blocks are new. Disposition:
  disclosed as the measurable cost of reuse-first, and the artifact actually fed to the execution lane (the
  writer brief) is newly authored rather than a restatement.
- **contract schema has no home for a missing governing file**: `source_scan.missing` is a set of source
  *families*, and extra top-level keys are refused, so the absent `Fabric/AGENTS.md` cannot be declared inside
  the contract. Recorded in the round's residual register and named in the ruling instead.
