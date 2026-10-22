# Spec delta — unmerged-candidate-merge

## ADDED Requirements

### Requirement: 併入 main 前必須以量測決定，不得以敘事決定
對每條未併分支 SHALL 量測「併入會實際加入什麼」、「是否與現行 main 衝突」、「是否觸及 `src/`／`schemas/`／
`skills/`」、「分支性質」；量測結果為空的 SHALL 判為取代；衝突者 SHALL 不併入。

#### Scenario: 只有乾淨且小的候選被併入
- **WHEN** 對 21 條未併分支執行裁決
- **THEN** 併入者 SHALL 全數為無衝突且不觸及產品程式路徑者，且其餘 SHALL 逐條具名留痕

### Requirement: main 的寫入必須先測後推
在任何對 `main` 的寫入之前，本地 SHALL 完成合併並通過全套產品測試與該 base 帶來的守門測試；紅燈時
SHALL NOT 推進。

#### Scenario: 組合守門在併後樹上通過
- **WHEN** PR #18（帶來 doc-identity guard）與 docs 候選同時併入
- **THEN** 併後樹上該守門 SHALL 為全通過（併前基準為 7 failed／4 passed）

### Requirement: 授權鏈必須逐字留痕且不得誇大
Owner 覆寫其顧問建議時，證據 SHALL 以 `OVERRIDDEN_BY_OWNER` 表述；SHALL NOT 以「外部已接受」描述；
授權範圍 SHALL 逐字限定於裁決列為可併入者。

#### Scenario: 讀者能分辨授權來源
- **WHEN** 外部驗收官讀取證據包
- **THEN** 應能取得 Owner 指令原文、原閘門、顧問建議，以及三者之間的覆寫關係
