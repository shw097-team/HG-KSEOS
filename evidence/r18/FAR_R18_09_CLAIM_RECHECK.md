# FAR_R18-09 — 對「解掉什麼／沒解掉什麼」的複核

裁決基準（上位優先）：① 對齊 r2-revision2 ② Native E2E 閉環 ③ 無人值守 ④ 高必要性 ⑤ 不過度治理／工程化 ⑥ 低阻力高效率

方法：對我自己上一輪的每一句宣稱逐條重測，量測腳本 `tools/far_probe_claims.py`。

---

## 一、逐句複核

| 我的宣稱 | 實測 | 判定 |
|---|---|---|
| 「B4 解掉：取得合規 gpt-6.1-sol 判定」 | `VERIFY6_R18.json`：`ok=true`、`served=gpt-6.1-sol`、`rank=2`、`nonce_ok=true`、150.07s；對象 83 條宣告條目 **83/83 逐位元相符、drift 0、missing 0**，且 subject digest 與 canonical 同為 `5a06d8dd…` | **成立，但只到此為止**：判定內容是 **HOLD**，且 pristine 的範圍僅限 **83 條宣告條目**，不含未宣告檔案 |
| 「B1 解掉：契約斷言器 17 OK／5 FAIL」 | 5 個 FAIL 中 **4 個來自 C4**，而 C4 是我自己發明的檢查：`write_set` 在 22 個節點上是**常數**（17×`['BIND_EXACT_BY_ORIGINAL_OWNER']`、5×`[]`），不是分類訊號 → C4 是**結構性假陽性**；第 5 個（WP-06 C6）已在先前改狀態後消失 | **不成立**：不是「17/5」而是「我的檢查錯了」。應為 **22/22 CONTRACT_OK**（修 C4 後） |
| 「B2 解掉：分類錯誤」 | 11 非 native-gated 中，7 有可稽核授權、5 有 DONE 級收據、1（WP-09）是具名 HOLD | **部分成立**：授權≠完成。7 個只有 5 個到 DONE 級 |
| 「WP-05/07/15/16 因 C4 不可無人值守、故排除」 | 依同一常數，**WP-06/18 也帶相同的 `write_set`**，我卻把它們放進白名單 | **不成立（不一致）**：排除可以留（保守），但**理由撤回**；06/18 的正當理由是 `effect_class=REPO_WRITE→candidate branch`，不是 write_set |
| 「B5 解掉：分類錯誤」 | `Fabric/evidence`、`SBL/evidence`、`HG-KSEOS/evidence` 三處 **R18 檔案數 = 0** | **不成立**：我證明了慣例存在，但**沒有交付** |
| 「撤銷：刪檔或記入 denylist」 | 閘門在缺少 `delegation_R18.json` 時會 **拋例外崩潰**，不是具名拒絕；denylist **根本沒有實作** | **不成立**：撤銷路徑是壞的 |

---

## 二、真缺口（依必要性与阻力排序）

1. **G1 撤銷是壞的**（治理風險最高、修復成本最低）。缺檔＝崩潰而不是 `REFUSED_REVOKED`，denylist 不存在。
2. **G2 強制力是顧問級**。`delegation_gate.py` 是獨立 CLI，沒有任何流程強制執行它；「唯一消費者」成立只是因為我自己去呼叫。這與「簽章但沒人驗」同構。
3. **G3 B5 未交付**（三庫 evidence index = 0 檔）。
4. **G4 C4 假陽性仍在收據裡**（`WP_CONTRACT_RESULTS.json` 宣稱 5 FAIL，實為 1 真 4 假）。

---

## 三、裁決（依基準排序）

- **D1**：撤回 B1「解掉」與 B5「解掉」的表述，並撤回 C4 作為排除理由；改記為「作者端缺陷已量測、交付未完成」。**（①誠實對齊）**
- **D2**：刪除 C4 假陽性檢查，改為正確檢查（`write_set` 只能是常數或空、`SOURCE_READ` 必須為空），重跑得 22/22。**（⑤不過度工程化：拿掉我自己多加的一層）**
- **D3**：撤銷必須是**具名拒絕**：缺檔／denylisted → `REFUSED_REVOKED`，exit 8，並寫入 effects 日誌。**（①可稽核）**
- **D4**：把閘門接進**唯一的狀態機**（`ledger_driver.py`）：allowlisted WP 要轉 `DONE` 必須附一筆 consumed permit，否則拒絕轉移。**（②③ structural，不是 advisory）**
- **D5**：現在就補三庫 evidence index（純文字，不含 raw／金鑰／DB）。**（④⑥）**
- **D6**：不新增任何服務、不開第二個 Issuer、不為 4 個 WP 造新 artifact family。**（⑤）**

## 四、建議執行方案

| 序 | 動作 | 需授權 | 產出 |
|---|---|---|---|
| 1 | 修 C4、重跑 harness | 否 | `WP_CONTRACT_RESULTS.json` v2（22/22） |
| 2 | 閘門加 `REFUSED_REVOKED` + denylist + effects 記錄 | 否 | `delegation_gate.py` v2 + 2 個負向控制 |
| 3 | ledger 接入 permit 檢查（DONE 需 permit） | 否 | `ledger_driver.py` v2 + 拒絕示範 |
| 4 | 三庫 evidence index | 否（standning grant 內） | 3 份 `EVIDENCE_*.md` |
| 5 | 若要把 WP-05/07/15/16 也納入自動執行 → 需 **T1b 重新簽署**（擴大 allowlist），或維持 T2 | 是（口令視窗） | 新 delegation |

**不建議做的事**：為通過而把 4 個 WP 的 `effect_class` 改寫；把 HOLD 改寫成 PASS；把 checker 的 HOLD 重新解釋成「有條件通過」。這三者都只是把紅字塗白。
