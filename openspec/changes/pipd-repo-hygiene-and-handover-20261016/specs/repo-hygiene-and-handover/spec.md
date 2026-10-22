# Spec delta — repo-hygiene-and-handover

## ADDED Requirements

### Requirement: 首頁現況必須等於可驗事實

repo 首頁（`README.md`）的 current-state 節 SHALL 以**當下**可驗證的事實描述專案狀態，包含：`main` 尖端、
開放 PR 與其狀態、已發布 Release 的不可變性、claim ceiling，以及證據分支尖端。過期的模型／車道宣告 SHALL
被更正或標為歷史，不得以現行語氣呈現。

#### Scenario: 外部驗收官只讀首頁即可對齊

- **WHEN** 外部驗收官讀取 `README.md` current-state 節
- **THEN** 該節所述之 PR 狀態、claim ceiling 與證據指標 SHALL 與遠端讀回一致，且不得將候選變更描述為已合併

#### Scenario: 車道模型宣告與 registry 一致

- **WHEN** 首頁列出車道所綁 provider/model
- **THEN** 該值 SHALL 等於當下 registry 的實際指派，或 SHALL 被明確標示為歷史值

### Requirement: 本地工程衛生動作必須可還原

任何本地刪除 SHALL 具備可還原性證明：worktree 之回收 SHALL 僅限於工作區乾淨（`dirty==0`）且其分支尖端等於
`refs/remotes/origin/<branch>`；未提交工作 SHALL 以新分支承載（救援）而非丟棄；不可還原且不可重生者 SHALL
不刪除，改以記錄處置。

#### Scenario: 乾淨且已推的 worktree 才可回收

- **WHEN** 執行 worktree 回收
- **THEN** 每個被回收者 SHALL 滿足 `dirty==0` 且 `pushed_to_origin`，且使用中的 worktree SHALL 被排除

#### Scenario: 未提交產品碼不被丟棄

- **WHEN** 主 clone 存在未提交的產品碼
- **THEN** 該工作 SHALL 被提交到新分支以保存，原分支 SHALL 不被修改、不被推送

### Requirement: 結案與移交必須落既有歸宿

SESSION 結案／移交資訊 SHALL 寫入 repo 既有歸宿（`docs/adr/ADR-0009`），衛生清冊 SHALL 寫入
`docs/adr/ADR-0008`；本回合 SHALL NOT 新增目錄家族或第二控制平面。

#### Scenario: 下一個 session 可零猜測啟動

- **WHEN** 下一個 session 讀取移交文件
- **THEN** SHALL 能取得證據分支尖端、open TT、rollback 指令與未完成的 Owner 閘門清單
