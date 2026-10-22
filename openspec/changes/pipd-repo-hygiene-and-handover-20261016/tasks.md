# Tasks — pipd-repo-hygiene-and-handover-20261016

## 1. Admission & lanes（E0）

- [ ] 1.1 HGK typed admission：`ADMISSION_OK`、`WO-TS-20261016-01..05`、checkpoint 記錄
- [ ] 1.2 GSTACK named-method route check（含負向對照 NATIVE）
- [ ] 1.3 OpenSpec change 建立並 `validate --strict`
- [ ] 1.4 KANBAN gate DAG（E0–E7 依賴鏈）

## 2. Local hygiene（E1–E3）

- [ ] 2.1 回收 12 個可還原 worktree（守門 `dirty==0` ∧ 尖端在 origin；排除使用中者）
- [ ] 2.2 救援主 clone 6 個未提交檔至 `rescue/r5p-uncommitted-20261016`
- [ ] 2.3 刪除可重生 `_scratch`；`.gitignore` 止漏（條件式）

## 3. Docs-only branch（E4）

- [ ] 3.1 `README.md` current-state 節刷新至 2026-10-16
- [ ] 3.2 更正過期車道模型列
- [ ] 3.3 `docs/adr/ADR-0008` 更新（本地衛生清冊）
- [ ] 3.4 `docs/adr/ADR-0009` 更新（結案移交）
- [ ] 3.5 驗證 `git diff --name-only origin/main...<branch>` 恰為 3 檔、無 `src/`／`schemas/`／`skills/`

## 4. Evidence & verify（E5–E6）

- [ ] 4.1 證據包（六件具名 ＋ 單一對外 MD）
- [ ] 4.2 shipped-bytes manifest ＋ fresh-extract 自驗
- [ ] 4.3 push 證據分支 ＋ 遠端尖端回讀
- [ ] 4.4 VERIFY 車道獨立複驗；裁決逐字入包
- [ ] 4.5 檢測清單回填（`D-01..D-16`）

## 5. Evolution（E7）

- [ ] 5.1 FAR-021 五件（含 `LEARNING.md`、`DEVIATIONS_ADDENDUM.md`）
- [ ] 5.2 skill 更新（可重用規則）
- [ ] 5.3 memory 更新（僅跨 session 事實）
- [ ] 5.4 Owner 交還包（`OWNER_ACTION_REQUIRED`）
