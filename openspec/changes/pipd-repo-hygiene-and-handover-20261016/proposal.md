# Proposal — pipd-repo-hygiene-and-handover-20261016

## Why

前回合（S4 FINAL）已將 S4 Preview MVP 階段交還 Owner，但**對外第一層仍是 repo 首頁**：`README.md` 的
current-state 節停在 `2026-10-14`，本地則累積 29 個 worktree 與一個停在舊分支、帶 `+203/−6` 未提交產品碼的
主 clone。外部驗收官與外部工程團隊看到的是**過期的現況與臟的本地樹**，而既有歸宿（`ADR-0008` 衛生清冊、
`ADR-0009` session 移交）尚未涵蓋本 session 的結案狀態。

## What Changes

- **首頁真實性**：`README.md` current-state 節就地刷新至 `2026-10-16`（PR #18／#17 open、`.4` immutable、
  `TEMP_CLOSED_RECOMMENDED`、claim ceiling 不變），並更正一列過期車道模型（`opencode-go/glm-5.3-flash`
  → 現行 `opencode-go/deepseek-v4.1-flash`）。**否決第二輪重構**（已於先前回合完成）。
- **本地工程衛生**：回收 12 個可還原 worktree（守門：`dirty==0` 且分支尖端等於 `origin/<branch>`）；
  救援主 clone 的 6 個未提交檔到新分支（**不丟棄、不 push、不動原分支**）；刪除可重生暫存。
- **既有歸宿更新**：`docs/adr/ADR-0008`（衛生清冊補本地面）與 `docs/adr/ADR-0009`（session 移交補 S4 FINAL
  與本回合狀態、open TT、rollback、下一步）。**不新增目錄家族**。
- **交付**：1 條 docs-only 產品分支（`README.md`、`ADR-0008`、`ADR-0009`，不含 `src/`、`schemas/`、`skills/`）
  供 Owner 合併 ＋ 1 條 scoped 證據分支供外部驗收官驗收。

## Impact

- **產品程式 0 行變更**；`main`、`v0.1.1-preview.4` 之 Tag／資產、PR 狀態、registry 皆不受影響。
- 受影響規格：`repo-hygiene-and-handover`（本 change 新增）。
- 風險：本地刪除動作 → 以「可還原性」為唯一守門；不可還原者一律不刪而改救援或記錄。
