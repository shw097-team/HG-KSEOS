# W0 R6 — vNEXT W0 交付與 W1 準入（2026-11-14）

**Round**：`W0_R6_W1ENTRY_20261114` ｜ **Branch**：`w0-r6-20261114`（候選，未合併 `main`）
**Domain**：`hgk_admission`／`fabric_policy` 的**狀態與驗收**面（本目錄只放狀態與證據，不發 WorkID、不發 Permit）
**Claim ceiling**：`SOURCE_READ + HOST_RAW + AUTHOR_DESIGN + LOCAL_CHECK`；**不是** Native、**不是** Independent、**不是** Release。

## 內容

| 檔案 | 角色 | bytes | sha256 |
|---|---|---:|---|
| `FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r1_實質正文.md` | W0 vNEXT 實質正文（可續工） | 21791 | `c4617197f47bb2c2437b9340b4cffda740369bf7c4796f1aba3a6166a8656d7f` |
| `FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r1_證據型附錄.md` | 證據型附錄（manifest／POS-NEG／HOLD／推送／更正） | 17289 | `5de9a02a2f6f500fcb40a1fc9d107b70d72511dcd868eef70adaf64373f7843a` |
| `CORRECTION_20261114.json`（在 round `out/`） | 兩筆更正的原始紀錄 | 1268 | 見 round `out/` |
| `DELIVERY.json` | 兩檔 bytes／sha256 的單向 manifest | — | — |
| `W0_R6_W1_HANDOFF_SBL.md`（在 SBL 分支） | SBL 側交接，不複製全文 | 3094 | — |

## 本輪的三個控制平面事實

1. `hgk-lane-policy.py validate` → `fatal=false`、`findings=[]`、`debt=[]`、`checked_sites=87`、`status=CANDIDATE`。
2. 車道：registry epoch `41`（`3583f71b…`）／assignment revision `44` epoch `41`（`3a4e9b2e…`）／pool revision `37` epoch `41`（`7a164911…`）；三車道 `--bind` ＋ `--assert --assert-arm opencode-go/deepseek-v4.1-flash` 皆 `ok=true`。
3. 實派：EXECUTE 傳輸層 served（rank1 deepseek、nonce 回聲、`turn.completed` usage）但 **usage row 缺** → origin 判 `ok=false`（`ERR_LANE_ALL_ROUTES_EXHAUSTED`）；PLAN／VERIFY 為 `ERR_ARM_NOT_IN_ASSIGNMENT`（exit 4）。

## 兩個原域缺口（需 HGK 原域處理）

- `H-GUARD-EPOCH`：`hgk-lane-guard.py::_live_epoch()` 讀 assignment `revision`（44）與 registry `epoch`（41）比較 → 所有呼叫 `ERR_LANE_STALE_EPOCH`。同檔已含 `epoch=41`／`registry_epoch=41`。
- `H-MANDATE-PLAN-VERIFY`：PLAN／VERIFY chain 中 deepseek 分別為 rank 2／rank 3，`--require-arm` 只認 assigned arm。

## 不可從本目錄做的事

發 WorkID／Grant／Permit、簽 Independent verdict、宣告 Release、以本目錄任何文字取代原 Domain Reader。
