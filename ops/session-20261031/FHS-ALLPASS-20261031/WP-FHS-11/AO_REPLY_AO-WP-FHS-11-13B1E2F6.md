我會先讀取這份 AO brief 與倉庫規範，確認查核範圍及必要證據。
三個 Hermes 正向回覆各自帶有不同 token；九格表則列出本輪 3 格、沿用前輪 6 格。我會繼續比對 PIPD manifest、原始 usage 與沿用收據，確認每個 PASS 都有對應量測。
原始 session 記錄確認三輪都呼叫了 `skill_view`，負向輪也確實收到「Skill not found」。九格表的六個沿用 PASS 則有證據缺口：引用的收據只記錄通用 token 測試，沒有各 profile 的 digest／badge 量測。我會用記憶體內測試檢查 rollup 的拒收條件，不寫入檔案。
整體 **FAIL**：第 4 條未通過。九格表算術正確，但六個沿用 PASS 缺少各 profile 的量測證據，其中四格的 archive prefix 已過期。全程唯讀，未修改檔案或執行 canonical acceptance。

NONCE-ECHO: AO-WP-FHS-11-13B1E2F6

```json
{
  "requirement": "WP-FHS-11",
  "clauses": [
    {
      "id": 1,
      "verdict": "PASS",
      "evidence": "HERMES_CELL_{LITE,STANDARD,ASSURED}.json.trigger_raw_result contains respectively WP11-HERMES-LITE-88211EA6, WP11-HERMES-STANDARD-013532D2, WP11-HERMES-ASSURED-49EF3B5A. Each matches its own skill_view response body in Hermes state.db messages 13361, 13382, 13395. Each full digest matches its corresponding PIPD export_manifest.json archive.sha256; independently hashing all three archives and manifests also matched the receipt bindings. Persisted final-answer tokens are masked, consistent with agent/redact.py; the receipts retain full stdout."
    },
    {
      "id": 2,
      "verdict": "PASS",
      "evidence": "wp11_hermes_cells.py cell() removes the probe in finally and records its absence before calling the negative run. All three checks.skill_removed_before_negative are true. Independently inspected negative sessions 20261101_115854_6a75e6, 20261101_115925_af770f, 20261101_115955_414834: skill_view tool messages 13373, 13389, 13399 return success=false and Skill not found. Full final answers 13378, 13392, 13400 contain neither their cell token nor digest; all negative usage files report completed=true and failed=false."
    },
    {
      "id": 3,
      "verdict": "PASS",
      "evidence": "Opened each served.usage_file directly. Positive sessions 20261101_115844_9ed225, 20261101_115913_70f3de, 20261101_115943_56cd5d each report model=deepseek-v4.1-flash, provider=opencode-go, completed=true, api_calls=2. These fields and session_id match each receipt.served. run_once() obtains them from the Hermes --usage-file output rather than assigning model/provider literals."
    },
    {
      "id": 4,
      "verdict": "FAIL",
      "evidence": "NINE_CELL_TABLE.json has denominator=9 and nine unique cells; counts correctly total 3 measured plus 6 carried. However, the six carried rows reuse generic CODEX_CELL_RECEIPT.json/CLAUDE_CELL_RECEIPT.json and token-only clean-run files, without per-profile digest/badge measurements. Codex and Claude LITE archive_prefix=e3e993b0e079 differs from current PIPD 6dadaf36a9ec; both STANDARD prefixes=52712b6316fb differ from current 9ef70b690d01. In-memory execution of wp11_nine_cell_rollup.py reproduced fail-open behavior: retaining only generic host receipts still yields carried_pass=6 and exit=0; replacing prior receipt data with verdict=VOID also yields carried_pass=6; replacing one Hermes receipt with only verdict=PASS yields measured_pass=3 despite null measured fields. Removing all prior receipts correctly yields six UNMEASURED and exit=1, but that boundary check does not establish cell-specific evidence."
    },
    {
      "id": 5,
      "verdict": "PASS",
      "evidence": "Independently inspected stored system prompts: all positive sessions contain the probe index entry but neither token nor archive digest; negative prompts omit that entry. Positive tool messages 13361, 13382, 13395 show successful native skill_view calls returning each probe body. This supports NINE_CELL_TABLE.json.note describing index-first, body-on-demand loading. Measurement scope is an explicitly requested synthetic probe containing copied profile facts; it does not establish installation or execution of the PIPD archive itself."
    }
  ],
  "overall": "FAIL"
}
```