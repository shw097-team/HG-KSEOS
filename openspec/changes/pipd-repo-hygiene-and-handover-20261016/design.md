# Design — pipd-repo-hygiene-and-handover-20261016

## Context

- 前回合已把 S4 Preview MVP 交還 Owner；本回合不碰產品程式（`src/`／`schemas/`／`skills/`），因此**不重跑產品測試**
  （產品 0 行變更時，重跑不構成新證據）。
- 上位報告 §8 明列不批准：新增框架／新控制平面／第九 Skill／`.hgk` 全量遷移／公開 Directory 施工。

## Decisions

| # | 決策 | 理由 | 被否決的替代方案 |
|---|---|---|---|
| D1 | **以既有歸宿就地更新**（`ADR-0008`／`ADR-0009`／README） | 三處已在先前回合建立且被外部驗收官引用；新增文件會製造第二真相源 | 新增 `HYGIENE_REPORT.md`／`HANDOVER.md`（否決：重複真相＋過度工程） |
| D2 | **docs 分支自 `origin/main` 起算**（`d3bd545`），非自證據分支 | 自證據分支起算會把 80+ 證據提交帶進 PR，Owner 無法只審 3 檔 | 自證據分支或本地 stale `main`（`2245914`）起算（否決） |
| D3 | **衛生動作以「可還原性」為守門**：`dirty==0` ∧ 尖端在 origin | 刪除是唯一不可逆動作；遠端存在即保證可還原 | 以「看起來舊」為判準（否決：不可還原） |
| D4 | **未提交碼救援而非丟棄**（新分支 `rescue/r5p-uncommitted-20261016`） | 203 行未提交產品碼的意圖未知，只有原作者能判定；保存成本近零 | `git checkout -- .`／`clean -fd`（否決：消滅不可回復的工作） |
| D5 | **README 不重構** | 已於先前回合完成結構化重構（492 行、導覽＋claim ceiling）；缺口僅在「現況節過期」 | 第二輪重構（否決：無缺陷證據，違反 §8 界線） |
| D6 | **`.gitignore` 止漏為條件式**（僅當能證明單一安全前綴） | 硬加過寬規則會遮蔽真實治理狀態（`.hgk` 是治理 runtime） | 無條件新增 ignore（否決） |
| D7 | **`.hgk` 追蹤狀態不動** | §8 不批准全量遷移；211 個未追蹤檔多為治理 runtime 與回合存檔 | 提交或遷移（否決） |
| D8 | **證據封包由 shipped bytes 重算 manifest** | 上一回合的 CRLF 正規化曾造成 2/12 假不符 | 由工作區副本計算（否決：會被 `.gitattributes` 正規化） |

## Risks & mitigations

- **R1 誤刪未推分支的 worktree** → 守門 `pushed_to_origin`；任一不成立即跳過並記錄。
- **R2 docs 分支意外含產品檔** → 交付後以 `git diff --name-only origin/main...<branch>` 驗 `D-04`／`D-05`。
- **R3 首頁宣告升高 claim** → `D-08` 檢查 `NOT_GRANTED` 仍在，且不新增任何 Full PASS 語句。
- **R4 本地 stale `main`（`2245914`，落後 origin 153）** → 本回合不動，列為 Owner 閘門（是否切回並 fast-forward）。
