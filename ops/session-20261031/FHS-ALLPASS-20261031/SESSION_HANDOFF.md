# SESSION HANDOFF — FHS-MSC ALL-PASS + FAR 治理閉環
**Session**: 20261031_201542_761b82 ｜ **Closed**: 2026-11-01 ｜ **Owner**: shw097

---

## 1. 一句話現況

FHS 交付 **19 PASS / 3 FAIL / 0 NOT_RUN**（每個 FAIL 都帶具名 blocker），FAR 治理從「零收據」走到「**第一篇三車道 PUBLISHED**」，並在結案時發現並修掉兩處**工作留在可棄層**的問題。

---

## 2. 本次實際產出（全部已 commit + push）

### 2.1 FAR 治理（HG-KSEOS `candidate/r18-fhs-skeleton-spine-20261029`）

| 檔案 | 作用 | 驗證 |
|---|---|---|
| `scripts/far_round.py` | 一條指令跑 PLAN→EXECUTE→VERIFY，收據自動落盤 | FAR-052 實跑 63.43 s |
| `scripts/far_lane_gate.py` | FAR 需三車道收據 + synthesis 必須引用收據檔 | 21 篇 → 只有 052 PUBLISHABLE |
| `scripts/far_publish.py` | `CANDIDATE → LANES_SERVED → PUBLISHED` | 052 已 PUBLISHED（by owner:shw097） |
| `scripts/round_close_gate.py` | **從 mandate 推導**必要車道，不再信任呼叫者清單 | `NO_LANE_RECEIPT:PLAN/EXECUTE/VERIFY_SECURITY` |
| `config/acceptance/CELL_STATE_VOCABULARY.md` | 六種 cell 狀態，PASS 必須算術封閉 | — |

### 2.2 產品（PIPD `hgk/fhs-wp11-packager-repair-20261031`）

| 項目 | 數字 |
|---|---|
| `export_bundle.py` | profile 軸改變 bytes、非一般檔成員拒絕、assurance 下限 |
| `ASSURANCE.json` | 4 項能力，含 `independent_checker`（**本次補 commit**，原本只在工作區） |
| LITE / STANDARD / ASSURED | 16 檔 `6dadaf36a9ec` / 56 檔 `9ef70b690d01` / **83 檔 `5624006aa2f7`** |
| 測試 | adversarial 9/9、ABI 7/7、hotswap 5/5、export 13/13 |

### 2.3 研究（Fabric `far/far-031-fhs-msc-all-pass-20261031`）

FAR-036 … FAR-053，共 18 篇。**052 是唯一 PUBLISHED**，其餘標 `PROVENANCE_MISSING`（內容保留、地位撤回）。

---

## 3. 結案時發現的「放錯層」問題（本任務第 2 項要求）

| 問題 | 事實 | 處置 |
|---|---|---|
| **PIPD `ASSURANCE.json` 未 commit** | `independent_checker` 宣告只在工作區；沒有它 ASSURED 根本 export 不出來 | ✅ `28b5115` |
| **HG-KSEOS gate/publisher 未 commit** | `far_lane_gate.py`、`far_publish.py` 在最後一次 commit 後又被改過，FAR-052 的 promotion 走的是**只存在本機**的狀態機 | ✅ `5c4a3a3` |
| PIPD 238 個 dirty 檔 | 213 在 `.hgk/`、4 在 `dist/` — **產物與執行期狀態，屬可棄層，正確** | 不需 commit |
| PIPD 分支名 `rescue/r5p-uncommitted-20261016` | 名稱誤導，但 HEAD 的 commits 確實在 `origin/hgk/fhs-wp11-...` 上 | 已驗證，無需搬移 |

**結論：兩處真問題都已修；其餘 dirty 檔確實是可棄層。**

---

## 4. 三個 FAIL 的精確狀態

| WP | blocker | 精確描述 | 下一步 |
|---|---|---|---|
| **WP-11** | `HERMES_MODEL_HALF_UNMEASURED` | 9 格 = 6 PASS + 3 loader-capped；Hermes 三格只到 loader | 走 gateway HTTP 取一次回應 |
| **WP-12** | `RUNTIME_PATH_UNRESOLVED` | `hermes -z` 在 h22 內拋 `RuntimeError: ...screenshot_param`；venv 有 openai 2.24.0 且 symbol 可 import | 同上，**同一個實驗可同時關掉 WP-11 與 WP-12** |
| **WP-20** | `CELLS_NOT_MEASURED` | 192 = 18 PASS + 168 `NO_HOST_SURFACE` + 6 `NOT_RUN` | 需 host 定義裁示（A/B 兩讀法都能關閉） |

---

## 5. 待 OWNER 的三件事（性質已更正）

| # | 項目 | 真實性質 |
|---|---|---|
| **O-2** | `git push origin merge/epoch-40-ff-20261101:main` | 純 ff（4 ahead / 0 behind）。**授權邊界**，不是能力 |
| **O-1** | main 上 516 個 r18 沒有的檔案 | **不是 graft 問題**。230 共同路徑 / 516 main-only / 1,849 r18-only = 兩個樹。需**內容級 adoption**，先分類 516 檔 |
| **D-H** | 憑證輪替 | **降級**：該檔從未 commit（`git log --all` 零筆）、已在 `.gitignore`。衛生事項，非事故 |

---

## 6. 下一個 session 的開場指令

```
接續 SESSION HANDOFF（HG-KSEOS/ops/session-20261031/FHS-ALLPASS-20261031/SESSION_HANDOFF.md）。

第一件事：走 gateway HTTP 介面取一次模型回應 —— 同一個實驗同時關閉 WP-11 的三格與 WP-12。
第二件事：分類 main-only 的 516 個檔案（先 fhs_msc_handoff_20261030/ 223 檔與 src/ 27 檔），決定 O-1 是併入或保留分岔。
第三件事：FAR 一律用 `python scripts/far_round.py --run <id> --question "…"` 產生，不要手寫 synthesis。

已知限制：EXECUTE 的 brief 必須自足（明令不讀 repo），否則 600 秒停滯；PLAN/VERIFY 走 chatgpt.com OAuth，
EXECUTE 走 loopback 10101，`--identity-source codex-rollout` 必帶。
```

---

## 7. 本次最貴的一課

十次自我推翻，形狀只有兩種：**「觀測不足就下結論」** 與 **「補上對照組之後結論翻轉」**。

而 FAR 治理之所以失效九次，不是規則不嚴，是**遵守規則比違反規則貴**——手寫 1 步零失敗，合規 3 步 4 種具名失敗。閘門是事後罰款，改不了事前的成本。

`far_round.py` 把合規壓成 1 步 63 秒。**這是本次唯一一個真正改變行為的修補。**
