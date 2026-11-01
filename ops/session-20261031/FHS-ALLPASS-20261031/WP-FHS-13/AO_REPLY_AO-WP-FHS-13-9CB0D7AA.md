我會先讀取這份 AO brief 與儲存庫規則，確認查核範圍及執行條件。

這份 brief 要求唯讀查核 C1–C5，並另行判斷 maker／checker 的獨立性。我已找到量測工件；接下來會核對原始欄位、Consumer 與 swap 實作，不沿用既有 PASS 判定。此環境缺少 brief 規則引用的 Fabric 路徑，治理驗收範圍會受此限制。

原始 receipt 顯示 CONTROL 回傳 `cap-attest-v1`，交換後經 ABI Consumer 回傳 `cap-attest-v2`。NEG 的 `served:true` 表示目標仍有服務，需搭配 identity 已改變解讀。目前兩份 swap receipt 都未附 grant 綁定或簽章驗證結果，我會繼續核對 C5 的原始證據。

C5 有明確反證：引用的 grant 簽章可用公開金鑰驗證，但簽發時間比 ABI swap 晚 100 秒，writeset 也只涵蓋兩個 PIPD 原始碼檔案，未涵蓋 swap 目標。C1–C4 的欄位、實作及唯讀探測相符；既有工件未記錄 writer／checker 身分，無法證明角色分離。

**查核結果：FAIL。C1–C4 通過，C5 未通過。** 全程唯讀，未修改工件或 acceptance 狀態。

[引用的 grant](/C:/Projects/Agent_Workspace/HG-KSEOS/var/issuer-probe/grant.json:5) 的 Ed25519 簽章驗證成功，但簽發時間為 **00:21:20 +08:00**，晚於 ABI swap 的 **00:19:40**；writeset 亦未涵蓋 swap 目標。因此不能證明交換是在有效授權下執行。

獨立性未獲證明：工件沒有 writer／executor／checker 身分欄位，無法確定候選撰寫者與 swap 執行者是否同一 actor。現有 AO log 僅顯示 dispatch 啟動，未提供完成且可核驗的 distinct-checker receipt。此項限制另列，不作為 C1–C4 的失敗理由。

```json
{
  "requirement": "WP-FHS-13",
  "clauses": [
    {
      "id": "C1",
      "verdict": "PASS",
      "evidence": "PIPD/src/pipd_ls_sp/abi.py: ABI_VERSION=1; Need.version participates in resolution; Consumer.__call__ resolves through Registry on every call. Read-only in-memory checks passed: same Consumer observes v1 -> v2; missing need/method, duplicate binding and version mismatch refuse."
    },
    {
      "id": "C2",
      "verdict": "PASS",
      "evidence": "HOTSWAP_ABI_RECEIPT.json: before.identity and control.identity are cap-attest-v1; served=true; before.via=abi-consumer."
    },
    {
      "id": "C3",
      "verdict": "PASS",
      "evidence": "HOTSWAP_ABI_RECEIPT.json: steps=[swapped]; pos.identity=cap-attest-v2, served=true, via=abi-consumer, origin=abi-run/occupant.py. Current read-only ABI probe reproduced these values; occupant digest matches candidate_v2.py and receipt.candidate_sha256. Historical probes construct separate Consumer instances."
    },
    {
      "id": "C4",
      "verdict": "PASS",
      "evidence": "HOTSWAP_ABI_RECEIPT.json: control.identity=cap-attest-v1; neg.identity=cap-attest-v2. hotswap.py evaluates neg_ok as post-swap identity != expect_old. This establishes replacement of the tested identity endpoint; NEG copies POS rather than performing a separate invocation."
    },
    {
      "id": "C5",
      "verdict": "FAIL",
      "evidence": "Referenced var/issuer-probe/grant.json nonce PROBE-WP13-A1 has a valid Ed25519 signature against issuer.pub, but issued_at=1793463680 (2026-11-01 00:21:20 +08:00), 100 seconds after the ABI swap and 4361 seconds after the initial swap. Its REPOSITORY_WRITE writeset covers only PIPD abi.py and tools/hotswap.py, excludes both swap targets, and candidate_sha256 is empty. Neither swap receipt binds this grant."
    }
  ],
  "independence": {
    "distinct_checker_evidenced": false,
    "note": "Writer and swap-executor identities are unrecorded, so same-actor authorship/execution cannot be determined and separation cannot be claimed. Existing verdict/acceptance records identify no distinct checker; the AO log shows dispatch start without a completed checker receipt. This finding limits assurance independently of C1-C5."
  },
  "overall": "FAIL"
}
```