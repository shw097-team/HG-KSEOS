# OR-8 — external_holds for 5 external owner classes (SOURCE/ABI/HOST/CHECKER/RELEASE)

- items: **11**
- verify after signing: `python tools/check_external_holds.py --receipts-dir _handover/R20-FHS-20261029/owner_receipts`
- if unsigned: 11 holds stay OPEN; affected consumers keep DOC_ROUTE_HOLD (DOC-00:1582)
- claim ceiling: release gate is owner-only (DOC-02:10643); this packet cannot substitute for it

## Items

| # | id | current | next legal action |
|---|---|---|---|
| 1 | `SRC-L-009 v1產出指令` | SOURCE | 提供該版本bytes或確認由已指定thin+AUDIT替代本輪repair控制 |
| 2 | `149 child inherited context fragment / B1九個UNRESOLVED Node` | SOURCE | 讀回原Parent/fragment/Node來源並ratify相容mapping |
| 3 | `13原verb vs 當期14 parser` | ABI | 判定compile-cc版本相容/alias及13原verb承諾 |
| 4 | `19 Schema內層{}與native EffectClass value set未ratify` | ABI | 將domain semantic Reader與原Registry兼容綁定；enum由原Owner裁定 |
| 5 | `DOC07 ↔ legacy DOC03、12risk→9context` | ABI | 提供loss ledger/alias migration與roundtrip |
| 6 | `192 legacy ON/OFF label與ProviderOff含義矛盾` | ABI | 確認原raw token到boolean映射；重測provider禁止外呼 |
| 7 | `Fabric Active/Loaded/Consumer、HGK Issuer/Wake/Lease/NormalMode` | HOST | 唯讀當期原Registry/module origin/loaded SHA，再依原OPS准入最小needed子圖 |
| 8 | `Default30/Donor24/Method25/TECH386 upstream pin/license/適用Host` | HOST | 依每ID BuildOrUseRecipe補pin/license/manifest/help，純方法不造installer |
| 9 | `B1 282 RunnerBindings` | HOST | 原Registry以case_id/source/Host解析signature與raw schema |
| 10 | `不同受保護principal` | CHECKER | 原protected Reader核identity及Raw/oracle，真實執行 |
| 11 | `正式Publisher/GHP-02` | RELEASE | 只在原發行授權成立後發布與readback |

## What to fill

`per_id_reply_or_supersession`, `signed_at_utc`, `signed_by`

Signature is the OWNER's act. The agent prepares the packet and verifies the result; it does not sign, and a packet left unsigned changes no state.
