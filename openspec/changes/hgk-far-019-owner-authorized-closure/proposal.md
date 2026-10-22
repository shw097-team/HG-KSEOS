# FAR-20261016-018 — R7～R11 殘留結案與移交（FAR 研究輪）

## Why

`CNV-EVIDENCE-ARCHIVE-R7R11-20261016` 已把八支候選證據做過只讀預檢、並在真實 Repo Maintainer 授權後合併了
證據鏈 #4/#5/#7/#9/#11；外部驗收報告 `EIA-FABRIC-CNV-R7-R11-20261016` 仍留下十項 finding 的處置、兩項
本輪自發現的車道綁定缺陷、三支獨立 swarm 車道帶來的七條 errata、兩支已瘦身但尚未實地驗證的 skills、
未執行的 peer chain、以及本 SESSION 的結案／移交義務。這些項目散落在多份 artifact，沒有一份「殘留全集 +
唯一裁決 + 可執行/OWNER-gated 分界」。

## What changes

新增 FAR 研究輪 `FAR-20261016-018`：以 FAR 方法產出（1）W1 殘留全集、（2）W2 缺陷檔案（含 checker 隔離
可行性實測）、（3）唯一一份排名工程裁決 `FAR_RULING.md`，並直接執行裁決中 agent 可執行之低阻力項目、
把 OWNER-gated 項目備妥為單一動作；最後產出移交 checkpoint 與單一證據 MD，並把證據推送到
`shw097-team/Fabric` 的新 `EVIDENCE/` 前綴供外部驗收。

## Non-goals

full 221／G-A～H、production 晉升、R7-02 跨 REPO 程式碼晉升、peer chain 合併、PR #12 晉升、canonical
控制平面編輯、重新瘦身 skills、建立第二控制平面或新 verifier 系統。

## Claim ceiling

`LOCAL`：本輪只宣告本地可重導的完成；外部接受仍待真實驗收官，`full_convergence_verdict` 維持
`TEMP_CLOSED_CHALLENGE`、`production_verdict` 維持 `FAIL_CLOSED`、`canonical_AO_acceptance` 維持 `NOT_ISSUED`。
