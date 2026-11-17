---
artifact_id: FHS-vNEXT-PLP-W0-BLUEPRINT/2026-11-14-r1
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


# FHS_vNEXT_PLP_W0_藍圖&skeleton

**W0 波次藍圖（Identity／Source／Need／WP／Effect／POS-NEG／Output）｜2026-11-14**
本檔是 L2 §12 指定的 W0 三件之一（`藍圖&skeleton`），不是新 Canonical，也不改 r8 任何條款。

## 1｜Identity 與法位

| 項 | 值 |
|---|---|
| Wave | **W0**（L2 §03：n=4，W0–W4；W18 非施工波） |
| 主波 WP 集合 | `WP-FHS-00`／`01`／`15`／`16`／`19`／`21`（L2 §04 W0） |
| 現行 W0 規格 | `spec/FHS_PIPD-LS-PKG_W0_20261112_r8.md`（680,998 B，`42546311c3c62ae4c7214037…`） |
| 交付視圖 | `…_r2_實質正文.md`（31526 B）＋`…_r2_證據型附錄.md`（50289 B） |
| 本波狀態 | `W0_SCOPE_COMPLETE`（作者端／local check 層） |

上游 pin：L0 `33e49ca22872b135…`、L1 `bd2ab0b74f21da6b…`、L2 `a6077aa208aa9cbc…`。

## 2｜Source（本波讀什麼）

| 來源 | 角色 | 本波用途 |
|---|---|---|
| 31 冊語料（`SOURCE_LOCK_V3.json`，31 sources） | 產品／工程母卷 | D1 身分對帳、gate_corpus 31/31 |
| `FHS-08` BODY-08（`1df046803197…`） | 485 槽原處置 | D2 exact-key 與 digest |
| `FHS-07` ACCEPTANCE_CHALLENGE | 96 Oracle 12×8 | D4 CasePlan |
| 三庫 import（433 entries／423 distinct） | 工程基座 | P0-03 分母對帳、D3 供應鏈 |
| `hgk-main` @ `970d1ab1…` | HGK 完整 checkout | P1-01／D5 full scan |

## 3｜Need 與必須輸出

| Need（L2 §04 W0） | 本波輸出 | 驗收面 |
|---|---|---|
| Owner 可立即讀到來源綁定的三 SPEC | 三份異質 SPEC＋`spec_identity` exit 0 | P0-09 |
| 原分母與 NEG 承接 | D1（31）／D2（485）／D4（96）／D3（供應鏈） | P0-09 |
| W0 r8＋r26 交付來源完整合併 | r2 正文＋附錄（AsBuilt 全文） | P0-01／P0-11 |
| 來源樹與主機狀態可讀回 | HOST_READBACK／G16B full scan | P0-02／P1-01 |

## 4｜Effect 與權限邊界

- 本波只做 `SOURCE_READ` ＋ `LOCAL_DRAFT_WRITE` ＋ `LOCAL_CHECK`；不派 `DEV/OPS/USER/RELEASE`。
- 原域寫入零：`Fabric/ SBL/ HG-KSEOS/` 未被修改；所有原域修補只以 PR 候選形式存在。
- 三車道回執（PLAN rank 2／EXECUTE rank 1／VERIFY rank 3）為 `LANE_SERVED`，不等於原域 ACK。

## 5｜POS／NEG（本波）

**POS**：普通短 Goal 在合法 read/draft 可取得具 Source／Consumer／FUO 的三 SPEC；本波另交付五份可重算台帳（D1–D5）。

**NEG（必拒）**：
- 把 `PASS_WRAPPER_SCOPED` 當 Protected PASS；
- 用缺 OPS 阻擋 Draft；
- 用 485 個數字冒充 485 筆 exact-key；
- 用 aggregate 未載明演算法的 digest 冒充可重算；
- 用 `CASE_PLANNED` 冒充 `RUNNER_PASS`。

## 6｜Output（交給 W1 的三件）

1. `FHS_vNEXT_PLP_W0_草案.md`（可施工範圍）
2. `FHS_vNEXT_PLP_W0_定案.md`（As-Built 與判決）
3. 本檔的 skeleton 結構（CH/WP/Effect 對照）

## 7｜Skeleton（W0 章節骨架，供 W1 續接）

| 章節 | 內容 | 狀態 |
|---|---|---|
| W0-A 來源融合 | 31 冊＋三庫 import | DONE |
| W0-B 三 SPEC | Product／Architecture／Program | DONE（Draft FUO） |
| W0-C 分母台帳 | D1／D2／D4 | DONE（VERIFY PASS） |
| W0-D 供應鏈 | D3 | DONE（3 gaps 具名） |
| W0-E 主機與掃描 | HOST_READBACK／G16B | DONE |
| W0-F 判準與簽核 | POS-02 pin 判準、owner 雙簽 | DONE |
