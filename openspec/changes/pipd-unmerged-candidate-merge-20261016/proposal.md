# Proposal — pipd-unmerged-candidate-merge-20261016

## Why
`main` (`d3bd5456`) 之外有 21 條分支與 4 條開放 PR。其中只有少數是「乾淨、小、具必要性」的真候選，其餘是
證據載體或已被後續 PR 取代。沒有裁決就動手，會把證據灌進 main、或併入需要人工解衝突的陳舊分支。

## What Changes
- 以唯讀量測（`diff --shortstat`／`merge-tree`／觸及目錄）對 21 條分支逐條裁決。
- **只併 3 條**：PR #18、PR #17、`docs/repo-state-and-handover-refresh-20261016`。
- 其餘 18 條分類留痕（9 證據／8 衝突即取代／1 意圖不明），並明文列為不做。
- `main` 自 `d3bd5456` 前進至 `dd0d5ce9`（三個 `--no-ff` 合併提交，先測後推、單一 push）。

## Impact
- 落地 8 檔（4 來自 #18、1 來自 #17、3 來自 docs 候選）；`src/`、`schemas/`、`skills/` 變動為 **0**。
- `v0.1.1-preview.4` tag 物件與資產未動；無 tag、無 release、無 force。
- 未竟：PR #18／#17 在托管側仍顯示 `open / not-merged`（直接推合併提交所致）——**Owner 才可關閉**。
