---
artifact_id: FHS-vNEXT-PLP-W0-DRAFT/2026-11-14-r1
artifact_layer: L3
wave: W0
subject: FHS_vNEXT_PLP_W0
version: 2026-11-14_r1
language: zh-TW
state: W0_SCOPE_COMPLETE
upstream_L0_sha256: 33e49ca22872b135
upstream_L1_sha256: bd2ab0b74f21da6b
upstream_L2_sha256: a6077aa208aa9cbc
w0_spec_current: spec/FHS_PIPD-LS-PKG_W0_20261112_r8.md @ 42546311c3c62ae4
claim_ceiling: SOURCE_READ + HOST_RAW + AUTHOR_DESIGN + LOCAL_CHECK + LANE_SERVED + WRAPPER_SCOPED_SOD + OWNER_SCOPED_ORIGINAL_ACK + W0_SCOPE_COMPLETE
not_claimed: PIPD_COMPILER_REPARSE, NATIVE_PASS, INDEPENDENT_PASS, RELEASE
canonical_compiler: NOT_INVOKED
source_mutation: NONE
---


# FHS_vNEXT_PLP_W0_草案

**W0 草案（真 Scope／Task／ABI／待施工面）｜2026-11-14**
本檔記錄 W0 實際施工範圍與接口，不是施工准許；任何 Repo 寫入仍需 owner 的 exact WriteSet。

## 1｜真 Scope

| 面 | 內容 | 邊界 |
|---|---|---|
| 讀 | 31 冊、三庫 import、r8／r26、L0/L1/L2 | 只讀 |
| 寫 | `FHS_NEXT/_local`、`ops`、`FHS_NEXT_Workspace/**` | 不碰原域 |
| 簽 | `control/` 判準、owner 雙簽 | 金鑰不落檔 |

## 2｜Task 與產出對照

| Task | 產出 | 位元組 | sha256 前 24 |
|---|---|---|---|
| D1_authority_conflict_ledger | `WP01_AUTHORITY_CONFLICT_LEDGER.json` | 24559 | `8c2e4837d4ede7d76f164b46…` |
| D2_485_disposition | `WP16_485_DISPOSITION.csv` | 50131 | `5e5de5bdcf20b899463dd7a6…` |
| D3_ci_supplychain_raw | `WP19_CI_SUPPLYCHAIN_RAW.json` | 4973 | `a8286bd4efab545ea0712ea7…` |
| D4_oracle96_caseplan | `WP21_ORACLE96_CASEPLAN.json` | 59993 | `edc605e6f62c0f8dad696eeb…` |
| G16B_fullscan | `G16B_FULLSCAN.json` | 137734 | `76174cbfbe5c0532087da9c4…` |
| FUO_manifest | `MANIFEST.json` | 4966 | `51455626e40226b58f4e2cbd…` |
| FUO_intent_card | `intent.card.json` | 4755245 | `e0bc7ce8fb50bb8aece54d6a…` |
| SELFCHECK | `SELFCHECK.txt` | 1708 | `3d4e6b637cab889d049410f7…` |

## 3｜ABI／接口（交給 W1）

| 接口 | Producer | Consumer | 版本／依據 |
|---|---|---|---|
| 三 SPEC（Product/Architecture/Program） | TPM 作者端 | 原 SBL PIPD Intake | `spec_identity` exit 0；共同 `SourceManifestSHA 1bae7892…` |
| 485 exact-key 台帳 | EXECUTE 車道 | 原 TechnologyAdmission Reader | digest `ff71ffa33a0f5a8ea85a47b3…`（＝L0 宣佈值） |
| 96 CasePlan | 作者端 | 原 Case Registry | 12×8，`runner_binding=null` |
| 供應鏈 raw | 作者端 | 原 CI／Publisher Reader | 9 artifacts＋3 gaps |
| G16B inventory | 作者端 | 原 HGK Program Reader | manifest 可重算 aggregate |

## 4｜待施工（明確不在本波）

- `WP-FHS-06` 首個可逆 DEV：需 exact WriteSet＋DEV ECP＋原 HGK 准入（W2）。
- 原 PIPD canonical 編譯（PI/PD/ECP/TQAEP）：需原 Compiler 載入（W1）。
- 96／282 逐案執行：需原 Runner 綁定（W3）。

## 5｜停損與恢復

- 任一原域缺件 → 只停該受影項，其他切片續行（L2 §04 W0「停損／恢復／回退」）。
- `last_good`：r8／r26／TRANS pin 全保留；本波新增檔案刪除即回退。
