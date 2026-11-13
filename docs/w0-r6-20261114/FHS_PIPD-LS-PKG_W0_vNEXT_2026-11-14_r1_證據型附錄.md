---
artifact_id: FHS-PIPD-LS-PKG-W0-vNEXT-20261114-r1-APPENDIX
artifact_layer: W0-EVIDENCE
language: zh-TW
version: 2026-11-14_r1
round: W0_R6_W1ENTRY_20261114
paired_body: FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r1_實質正文.md
evidence_root: C:/Projects/Agent_Workspace/FHS_NEXT_Workspace/W0_R6_W1ENTRY_20261114/
claim_ceiling: 審計用附錄，不是第二份規範；所有 PASS 只在其 Subject/Scope/Host/Epoch 內有效
sensitive: 無密鑰、無 Token、無 DB、無 raw lane stdout 全文（只留 digest 與 tail）
---

# 證據型附錄｜FHS_PIPD-LS-PKG_W0 vNEXT `2026-11-14_r1`

> 導航：正文在 `FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r1_實質正文.md`（同目錄）。本附錄只放**可重算的定位與回執**；正文不放的原始 stdout 全文留在 `W0_R6_W1ENTRY_20261114/out/`。
> 兩檔互記版本；互嵌 SHA 會造成循環，故以單向 manifest 為準（§1）。

---

## 1. 檔案 manifest（單向、可獨立核對）

manifest 檔：`W0_R6_W1ENTRY_20261114/out/MANIFEST_SOURCES.json`（本節數值即其內容）

| 檔案 | bytes | sha256（前 24） |
|---|---:|---|
| `spec/FHS_PIPD-LS-PKG_W0_20261112_r8.md` | 680998 | `42546311c3c62ae4c7214037` |
| `spec/FHS_PIPD-LS-PKG_W0_20261112_r7.md` | 677204 | `35daf4c1ab1dda913344f6c4` |
| `_local/FHS_vNEXT_W0_TRANSITION_BASELINE_AND_W1_ENTRY_20261112.md` | 114616 | `f1ee542923e3725b8d87040a` |
| `_local/W0_AS_BUILT.md` | 38379 | `b6f1dbb61484ffbc52350119` |
| `provenance/SOURCE_IMPORT_MAP.json` | 256666 | `1bae7892372ae63a085ff432` |
| `HG-KSEOS/config/lane-routing-registry.yaml` | 45026 | `3583f71bc35ab63470cff42e` |
| `HG-KSEOS/config/model-lane-assignment.json` | 61601 | `3a4e9b2ed4a20f304ef568ff` |
| `HG-KSEOS/config/lane-route-slots.candidate.json` | 43520 | `7a164911bf89d080106b5dda` |
| `HG-KSEOS/config.live/hermes-codex-lane.live.json`（新） | 1221 | `6002efa4f07c3e28a5dd04ce` |
| `HG-KSEOS/config.live/hermes-codex-lane.live.PREIMAGE_20261112.json`（舊） | 1221 | `be2cd0c85a2d6c10d55b57fe` |
| `control/FHS_NEXT_W0_THIN_EXECUTION_CONTROL_20261111.md` | 9617 | `51f66aec59a9678ed5c8954a` |
| `control/FHS_NEXT_W0_THIN_BOOTSTRAP_PROMPT_20261111.md` | 1947 | `66a414f4bbf95850cfe2ed4f` |
| `ops/tools/fhs_3lm.py`（還原後＝map 值） | 10651 | `0c5fc66370d9d6f594a99aa5` |
| `ops/tools/fhs_3lm_hgk_local.py`（本根 adapter） | 3441 | `389f3ab847cfa103be867c2f` |
| `ops/selfcheck.py` | 22153 | `760ac3b2c03288df7049c439` |
| `_local/rounds/W0_R2_REREG_20261112/COPY_REGISTER_CURRENT.json` | 248539 | `f94494e468fe1ce21b703010` |
| `_local/rounds/W0_R2_REREG_20261112/G19_REREG_CHECK.json` | 565 | `15f91fc693f710321da8a58c` |
| `Fabric/INTEGRATION/FHS/README.md` | 5463 | `3c1c2b0ae20f0028876720a6` |
| `Fabric/INTEGRATION/FHS/repository-map.json` | 1558 | `373120f50433677205e9127f` |
| `owner_envelope/design/OWNER_WINDOW_DECLARATION.json` | 1393 | `1dbd9d4c33cafd043b0a050a` |

本附錄與正文自身的 digest 由 §9 的 `DELIVERY.json` 於寫入後計算並單向記錄（不內嵌）。

---

## 2. 版本 delta：r26 → r8 → 本 vNEXT r1

| 面向 | r26（668540 B `0ea05544…`，歷史母本） | r8（680998 B `42546311…`） | 本 vNEXT r1（本回合） |
|---|---|---|---|
| 角色 | 作者端 W0 施工母本 | 受界現行工作基準（r26 原文＋R6/R7/R8 追加） | **過渡基線＋W1 準入**的實測回寫 |
| 車道 | 未含 | 含 R4/R5 車道結果 | 三車道 bind/assert 全綠；EXECUTE transport only；PLAN/VERIFY 被 assignment 拒 |
| Codex pin | 舊 | overlay `4f91ae86…` | overlay 更新為 `83f5c2dd…`（alpha.4.1），pre-image 保留 |
| 複本台帳 | 73 群／394 | 73／394 | 41／343（業主重排後重宣告，lineage 保留） |
| Guard | 未含 epoch 缺陷記錄 | 未含 | 記錄 `_live_epoch()` 讀 `revision` 的欄位錯接 |
| 不變量 | 50 CH／22 WP／36 edge／485 slots／949／192／96／282 | 同 | **同（未改任何分母）** |

**取代關係**：本 vNEXT 只取代「過渡基線的當期狀態敘述」，**不取代** r8 的正文、不取代 r26，也不構成 PLP 正式取代舊 Reader。

---

## 3. 可重現命令與 exit code（本回合實測）

工作目錄固定 `C:/Projects/Agent_Workspace/FHS_NEXT`，`PY` 為唯一可信直譯器
`C:/Users/user/AppData/Local/hermes/cache/scratch/fhs_next/venv311/Scripts/python.exe`（Python 3.11.9；裸 `python` 在本機不可用）。

| # | 命令 | 實測 exit | 關鍵輸出 | Raw |
|---|---|---:|---|---|
| 1 | `"$PY" ops/selfcheck.py` | **1**（16 案中 15 PASS） | `pos 9 / neg 7 / pass 15 / fail 1`；`neg_all_refused_correctly=true`；唯一 FAIL＝`POS-02` | `_local/W0_TEST_READBACK.json`；`out/selfcheck.stdout.txt` |
| 2 | `"$PY" ops/tools/spec_identity_check.py --spec-dir _local/W0_SPEC --manifest provenance/SOURCE_IMPORT_MAP.json` | 0 | `ok=true`；`distinct` 四項皆 true（Artifact／OriginalConsumer／ACC±／BodySHA256） | `out/spec_identity.json` |
| 3 | `"$PY" ops/tools/gate_corpus.py` | 0 | `declared 31 / matched 31 / missing 0 / scanned 76` | `out/gate_corpus.json` |
| 4 | `"$PY" ops/tools/reregister_copies.py` → `"$PY" ops/tools/reregister_check.py` | 0 → 0 | 重宣告 41 群／343 copies；檢查 `verdict=PASS`、`members_read=343` | `out/COPY_REGISTER_CURRENT.json`、`out/G19_REREG_CHECK.json`、`out/REREG_ROUND_DECLARATION.json` |
| 5 | `"$PY" ops/tools/lane_pin.py --check` | 0（修 pin 前為 **3**） | `digest_match=true`、`sidecars_complete=true`、`reported_version=codex-cli 0.167.0-alpha.4.1` | `out/lane_pin.json` |
| 6 | `"$PY" HG-KSEOS/scripts/hgk-lane-policy.py validate` | 0 | `fatal=false`、`findings=[]`、`debt=[]`、`checked_sites=87`、`status=CANDIDATE` | `out/validator.json` |
| 7 | `"$PY" ops/tools/fhs_3lm_hgk_local.py --menu` | 0 | `registry_sha256=3583f71b…`、pool `7a164911…` | `out/lane_plane/menu.json`（＋adapter 註記 `.adapter.txt`） |
| 8 | `--bind PLAN opt1` / `--bind EXECUTE primary` / `--bind VERIFY opt1` | 0 / 0 / 0 | 三份 binding 寫入 `ops/lanes/bindings/` | `out/lane_plane/bind_*.json` |
| 9 | `--assert <binding> --assert-arm opencode-go/deepseek-v4.1-flash` ×3 | 0 / 0 / 0 | 三次皆 `ok=true`、`arm=opencode-go/deepseek-v4.1-flash` | `out/lane_plane/assert_*.json` |
| 10 | `hgk-lane-dispatch.py --lane EXECUTE … --require-arm opencode-go/deepseek-v4.1-flash --nonce FHS-W0R6-EXEC-D1` | 0（工具自身判 `ok=false`） | rank1 深seek、nonce 回聲、`turn.completed` usage input 8348；`usage_rows_after_offset=0` → `ERR_LANE_ALL_ROUTES_EXHAUSTED` | `out/EXECUTE_RECEIPT.json` |
| 11 | 同上 `--lane PLAN` | **4** | `ERR_ARM_NOT_IN_ASSIGNMENT`（deepseek 為 PLAN chain rank 2） | `out/PLAN_RECEIPT.json` |
| 12 | 同上 `--lane VERIFY_SECURITY` | **4** | `ERR_ARM_NOT_IN_ASSIGNMENT`（rank 3） | `out/VERIFY_SECURITY_RECEIPT.json` |
| 13 | `hgk-lane-guard.py --lane EXECUTE --maker-model deepseek… --target-model deepseek…` | **2** | `REFUSE`；`sod_distinct_model` 失敗 → 正確拒收 | `out/guard/neg_same_model.json` |
| 14 | `hgk-lane-guard.py … --admission ADMITTED --expected-epoch 33` | **3** | `ERR_LANE_STALE_EPOCH`（`--expected-epoch=33` vs `live_epoch=44`）＋`epoch_current` 亦失敗 | `out/guard/neg_stale_epoch2.json` |
| 15 | `hgk-lane-guard.py … --admission ADMITTED`（不同模型） | **3** | `epoch_current: registry_epoch=41 live_epoch=44` → 缺陷證據 | `out/guard/pos_distinct_admitted.json` |

**第 1 條的兩個 FAIL 歷史**：本回合第一次跑是 15/16（只有 POS-02）；在修即時 locator 時改到 map 內的 `ops/tools/fhs_3lm.py`，POS-01 立刻變 FAIL，形成 14/16。還原為 map 值後回到 15/16。**這個順序本身就是 gate 有咬合的證據**（它抓到作者自己的越界）。

---

## 4. POS／NEG 逐項（本回合）

| Case | 類型 | 斷言 | 結果 | 證據位置 |
|---|---|---|---|---|
| POS-01 | POS | 每個匯入檔重雜湊等於 map `target_sha256` | PASS（433 files；4 筆由宣告的 supersession 承接） | `W0_TEST_READBACK.json` |
| POS-02 | POS | `control/` seed 與規格庫原件位元同一 | **FAIL → 具名 HOLD** | 同上，`copies_found=0` |
| POS-03 | POS | PIPD CLI 恰好 13 verbs | PASS | 同上 |
| POS-04 | POS | `compile-pi` 重現 origin fixture digest `9cc0c1b1…c1c99` | PASS | 同上 |
| POS-05…09 | POS | 見 `W0_TEST_READBACK.json` 逐案 | PASS | 同上 |
| NEG-01…07 | NEG | 每條負例都被正確拒收 | PASS（`neg_all_refused_correctly=true`） | 同上 |

**POS-02 的完整量測**（不縮小分母）：宣告路徑 `C:\Projects\Agent_Workspace\知識庫\實作相關DOC\FHS／FHS-MSC／SBL\FHS\FHS_PIPD-LS-PKG\實作\FHS_NEXT\EXECUTION_CONTROL\` 下兩檔；以**檔名**在 ① 知識庫 FHS 子樹（深度 ≤6）② `G:\Projects\封存\FHS_封存_20261110`（307,627 檔）③ `G:\Projects\封存\FHS_二次精簡封存_20261110`（28,975 檔）比對 → **0 命中**。結論：不是重新命名，是原件不在本機。`control/` 兩檔 bytes 未變（`51f66aec…`／`66a414f4…`）。

---

## 5. 原域 Consumer／Checker 回執（本回合）

**全部 `NOT_OBSERVED`**，逐項不冒充：

| 原域 | 需要的回執 | 本回合 |
|---|---|---|
| Fabric Policy Consumer | ActiveEpoch＋LoadedDigest＋ACK | NOT_OBSERVED（只讀 mirror） |
| HGK Issuer／SharedSpine | WorkID／OperationID／Lease／World Raw | NOT_OBSERVED（未發 WorkID） |
| SBL PIPD Reader | 對 r8／本 vNEXT 的 scoped ACK | NOT_OBSERVED（既有 ACK `subject=None/scope=None`＝scoped，不延伸） |
| Protected Checker | 不同 Principal 的 verdict | NOT_RUN |
| Original Publisher | Release admission | NOT_GRANTED |

歷史 PR 狀態（**INHERITED_LOCATOR_NOT_REVALIDATED**，來自過渡基線 Current Status，本回合未重查 GitHub）：HG-KSEOS #19–#22、#24 已合併；#23 與 Fabric #57 `closed, unmerged`；入口仍為 README ＋ `repository-map.json`。

---

## 6. Owner key passphrase envelope（本回合）

| 欄 | 值 |
|---|---|
| 機制 | `owner_envelope/code/owner_window.py`（真遮罩口令 → ed25519 → `POST /sign`；關窗即丟棄金鑰） |
| 口令輸入 | **由業主本人於 tkinter 遮罩視窗輸入**（2026-11-14T00:13:39）；本文件與任何 log 皆無口令、無金鑰 |
| window_id | `WIN-9a9fd4263977` |
| task | `FHS-W0-W1ENTRY-20261114` |
| scope | `owner_semantic_accept`（僅此一項） |
| effect ceiling | `REPOSITORY_WRITE` |
| max_ops／ops_used | 2／**0** |
| 狀態 | 開啟期間 `usable=true`（`owner_window_probe.py` 讀回）；**2026-11-14T00:30:35 以 `close --force` 關閉**（`state=CLOSED`、ops 0/2、225 B 收據 `~/.hgk-owner/artifacts/WINDOW_CLOSE_FORCE_20261114T003035.json`） |
| 為什麼關閉 | broker 在口令解鎖後不再常駐（`close` 回 `NO_WINDOW`，即無可簽服務），留著 `state=OPEN` 只會讓下一個讀者以為有活的能力。以 `--force` 關閉**只改狀態並寫收據，不簽任何東西** |
| 簽了什麼 | **沒有簽任何東西**。簽 `owner_semantic_accept` 需業主指示確切 body；maker 不自行組 body 代業主接受，否則即為自我驗收 |

**未開啟的兩類**（照合約拒絕）：`release`／`sourcefreeze` 需 dedicated path（TTL ≤1h、ops ≤4）且本回合無此需求；`policy_authority`／`trust_anchor`／`owner_enrollment` 為永久禁止 kind。

---

## 7. HOLD 與 ResumeLedger

| HOLD_ID | AffectedScope | OriginalReader/Owner | FirstFail | ResumePredicate |
|---|---|---|---|---|
| `H-H16` | Protected SoD | HGK Trust/Issuer | wrapper-scoped 非 Protected PASS | 原域 Fail-Closed 回執 |
| `H-READER` | Canonical ACK | SBL/PIPD Reader | `subject=None/scope=None` | 同 Subject/Scope/Source 的 scoped ACK |
| `H-ENTRY` | 入口提升 | Fabric mirror Owner | NAV `effect_permission=NONE` | 只用導航；原 Reader 另核 |
| `H-POS02-ORIGIN` | control/ 原件比對 | 原 Owner | `copies_found=0`（約 336k 檔 0 命中） | 提供原件或宣告此 POS 作廢（不得改分母） |
| `H-GUARD-EPOCH` | 受影 lane dispatch | HGK 原域 | `registry_epoch=41` vs `live_epoch=44`（讀到 assignment `revision`） | 修 `_live_epoch()` 欄位後重跑 §3#14/#15 |
| `H-MANDATE-PLAN-VERIFY` | PLAN／VERIFY served | HGK 原域 assignment | `ERR_ARM_NOT_IN_ASSIGNMENT` exit 4 | 改派後不需 `--force-rank` 即 served |
| `H-USAGE-EXECUTE` | EXECUTE served | relay/ledger Owner | `usage_rows_after_offset=0` | 落帳後重派一次，`ok=true` |

**Resume 起點**：§3 的 15 條命令；不需重建 W0，不需重跑 r8 全流程。

---

## 8. 回退點與殘留

| 對象 | 回退方式 | 前像 |
|---|---|---|
| Codex pin overlay | 刪新檔／還原 pre-image | `hermes-codex-lane.live.PREIMAGE_20261112.json`（`be2cd0c8…`） |
| 複本台帳 | 使用 `COPY_REGISTER_PRE_OD3.json` | 舊台帳 73/394 數字不改 |
| `ops/tools/fhs_3lm.py` | 已還原（map `0c5fc663…`）；adapter 可整檔刪除 | 來源 `FHS/FHS_W0_R13_ACCEPTANCE_20261108/tools/fhs_3lm.py` |
| 本回合輸出 | 整目錄丟棄 | `FHS_NEXT_Workspace/W0_R6_W1ENTRY_20261114/` |
| owner 視窗 | `owner_window.py close`（只改狀態，不簽章） | window.json 記錄 |

**殘留**：`ops/lanes/bindings/*.json` 為本回合重寫的 binding（原檔被覆寫，屬同回合產物，非歷史來源）；`__pycache__` 於收尾時清；`out/EXECUTE_RECEIPT.json.attempts.ndjson` 只含 nonce 與 usage 摘要，不含憑證。

---

## 9. 交付清單與下載位置

| 檔案 | 本地絕對路徑 |
|---|---|
| 實質正文 | `C:\Projects\Agent_Workspace\FHS_NEXT_Workspace\deliverables\FHS_vNEXT_W0\FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r1_實質正文.md` |
| 證據型附錄（本檔） | `C:\Projects\Agent_Workspace\FHS_NEXT_Workspace\deliverables\FHS_vNEXT_W0\FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r1_證據型附錄.md` |
| 交付 manifest | `C:\Projects\Agent_Workspace\FHS_NEXT_Workspace\W0_R6_W1ENTRY_20261114\out\DELIVERY.json`（含兩檔 bytes／sha256，寫入後計算） |
| 全部 Raw | `C:\Projects\Agent_Workspace\FHS_NEXT_Workspace\W0_R6_W1ENTRY_20261114\out\` |

**不能主張**（重述）：原生准入、WorkID/Grant、Independent PASS、原域語義核簽、PLP 正式取代、W1 Repo 已建、任何 Release。

---

## 10. 對外推送（依 Fabric 分域規則，branch＋PR，未合併）

| Repo | Branch | 內容 | Readback | PR |
|---|---|---|---|---|
| `shw097-team/HG-KSEOS` | `w0-r6-20261114` | `docs/w0-r6-20261114/`：README、實質正文、證據型附錄、DELIVERY.json | 四檔 remote size 與 local 一致；正文／附錄 remote `sha256` == local `sha256`（以 base64 原樣位元組上傳） | **#25 open, merged=false**, head `04a1a54fb248` → base `main` — <https://github.com/shw097-team/HG-KSEOS/pull/25> |
| `shw097-team/SBL` | `w0-r6-20261114` | `docs/w0-r6-handoff-20261114/W0_R6_W1_HANDOFF.md` | remote `sha256` == local | **#68 open, merged=false**, head `35d5ee9cffee` → base `main` — <https://github.com/shw097-team/SBL/pull/68> |

**未推 Fabric**：Fabric `INTEGRATION/FHS` 是 `NAVIGATION_ONLY`／`effect_permission=NONE`，本回合的成果屬狀態與工程交接，不屬導航鏡像；且 Fabric #57 已 `closed, unmerged`（歷史事實，不改寫）。

**Token 處理**：僅從業主 `API KEY/GITHUB-REPO_SHW097-4.txt` 讀入記憶體並置於 Authorization header；未寫入 argv、URL、log、MD 或 commit，未落任何副本。
