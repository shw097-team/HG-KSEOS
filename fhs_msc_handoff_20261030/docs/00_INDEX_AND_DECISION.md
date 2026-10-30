<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 00 INDEX AND DECISION｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。




## HANDOFF-v1｜當期施工交接裁決與唯一首工作

本輪有效完成目標只有 `PIPD_CONSTRUCTION_HANDOFF_READY`。首工作為原 `WP-FHS-15`，業務成果為普通 Goal→來源/KnownAnswer 約束的三 SPEC→原 PIPD 功能 PI→TaskSpecSeed 與 PD 晚綁接收契約。此首工作的入口與本文第一受影契約在原書原位生效；不把未完成的全部產品要求當成本輪先決條件。

前版 `REPAIR_INCOMPLETE / SBL-D00-L00070-C01 / 7649` 保留為全產品語義修補差額。本輪不宣稱全產品已完成，也不把該差額改標外部 HOLD；其中對首工作有用的 FUO 十欄已在 `02_FIRST_WORK/RUN/FUO.json` 具體填列。其餘原 ID、承諾、負例與原 WP 的施工/驗收義務完整保留。

`SOURCE_READ/LOCAL_DRAFT` 可以現在合法開始；即時 Host Loaded、Native Permit、World Raw、不同 Principal Checker 只在對應原生效果/驗收階段要求，不反向作為本輪 Spec/PI 的輸入。包內 Worker/WorkOrderCandidate 是接收候選，不是已准入 WorkID。

## 本輪同域受影修復：r2 §0 正文適用／來源法位

## 0. 本版如何施工、如何讀取，以及不允許的誤讀

1. **實質正文字句是工作契約，不是證據收據。** 後段各 `原 ID` 的動作、輸入、輸出、POS/NEG、NoFit 和回復為原 BODY 規格的來源約束施工投影，未實際執行不得自稱 Native PASS。
2. **原規範不能被後發文件跨域覆寫。** 各 Domain 原 Writer/Owner 是 Normative；BODY、r1、r2 為設計候選；外部輪子是 Support。任何原始來源語義衝突維持 CR_OPEN 並停止受影能力，而不猜測修正 Native Enum。
3. **高保留 ≠ 全量安裝**。本版在正文逐名保留 Native20 20、Default30 30、Donor24 24、Method25 25、TECH386 386、R15 949、Cell 192、AC15、96 Oracle、WP22、PD Edge31、B1 Case/Node282；對不觸發者標示保留原處置／不啟動，不自行調整原 Disposition。
4. **One Canonical Plan Owner / Multi Scoped Methods**。同一 Goal 可分時用 OpenSpec Delta、Superpowers TDD、FAR、gstack Review；只有一個原 Canonical Plan Writer，且各方法無權自行頒發 Permit、Checker PASS、Release。修正 r1「每 Goal 只能使用一種方法」的過窄解讀。
5. **本地與遠端分開綁定**：以本冊 STATIC-v1 的實測表及 index/untracked 原始輸出為準；不得從舊遠端 SHA 推定本機狀態。
6. **每個帶原 ID 的微型工程項**均受本檔 §3 的 Lifecycle/Guard/NoFit/Parity/回復共同規則約束，該共同規則與每條下方原源功能要**聯合適用**，不能只挑共同樣板當單項完成。


---



## R2 AUDIT F01–F16：真修補讀取索引

本版 17 冊 current section 只存當期修補正文；原 Revision2 逐冊位元組封存於獨立 Evidence Archive，唯一 EffectiveReader 索引 `STATIC_REPAIR_v1/CURRENT_READER_LOCATORS_2221.json`。SBL 14 冊每個帶量詞原句在每冊獨立展開、149 Child 切出自己的 POS/NEG；`R2_SBL_COMPOUND_ATOMIZATION.json` 是源線索／機器分解紀錄，**不等於 Protected Case PASS**。Reader 不得以 Source/Manifest SHA 或章節是否存在取代語義驗收。

- F-01/F-08：14 SBL 分冊每原句多子項與 149 Child 各原 Consumer/正反例。
- F-02/F-03：192 Cell legacy host/Provider raw token 不轉正式 boolean，ChatGPT48 為另冊候選，不覆寫 DeepSeek 原ID。
- F-04/F-05/F-14：69 OriginalDisposition source-literal/OwnerACK 區別，Default30 保留 mandatory 而不假 installed。
- F-07：三 SPEC、Intent、PI、PD/DEV/OPS/TQAEP schema-shape 狀態與獨立 effect 檢查。
- F-06/F-11：四庫指定 symbol、Receiver/Tester/Launcher 未查清時受影 HOLD。
- F-09/F-10：949 Owner 批准差額及單當期 Reader locator/歷史 archive。
- F-12：282 個真正 Runner 缺 Entry 保持 NOT_RUN，逐 case Registry Request。
- F-13：R2 可重播 static runner 與捕獲 stdout/exit，Old20 非實機收據。
- F-15/F-16：單人 Owner KnownAnswer、W18 fresh PID/正常 Goal 與真 Host locator 不可預填。

**新版本：** `2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND`；`NO_NATIVE_EFFECT / NOT_INDEPENDENTLY_RATIFIED`。



## 本版未受影條文（完整沿用、當期生效）

## R2-00-ENTRY：依消費工作進入正文

先讀 [產品與權威](01_PRODUCT_AUTHORITY_SPINE.md)，再讀 [生命週期](02_PIPD_LIFECYCLE_AND_TPM.md) 與 [ABI/效果](03_ARCHITECTURE_ABI_AND_EFFECT.md)。來源／Profile 衝突只 PARK 依賴該綁定的 PI promotion；L0 設計與合法 L1 Reader 繼續。實際施工的排程只用 [22 WP](11_WORKPACKAGES_AND_DAG.md) 的 typed edges，不能把此入口頁當第二 Scheduler。

## R2-00-TIER：唯一風險層級

`L0=設計/本輪隔離文稿；L1=唯讀/靜態；L2=有界受權 Repo 寫入；L3=受准入 Native/User/Remote 效果；L4=原 Publisher 發行`。tier 是此設計投影，不替代真 Host enum。EffectClass 是正交維度；對 legacy `L1 patch` 或 `HOST_LOAD_SCOPE` 必先拒收，再由原 Owner 重新綁定，不能重新解釋成許可。

POS：L1 Source reader 讀 54 份已定位來源，沒有 Repo diff；授權 L2 只更動 exact WriteSet。NEG：L1+REPO_WRITE 或 L1+HOST_OP → `DENY_EFFECT_MISMATCH`，尚未啟動 effect worker；傳入「以前批准」仍須比對 Scope/Epoch。

## R2-00-RESUME：單人 Owner 與局部工作

`QuestionKey=(subject,source_sha,scope,policy_epoch,question_id)`；已知有效答覆只讀回，不重新提問。A 需 Issuer 缺件則 PARK(A,owner,next_action,resume_predicate)；B source read、C 已授隔離文稿保持 READY。原 Queue 負責 fairness；此文件不造第二 Queue。POS：同一 key 連續兩次輸入 owner_prompts 第二次=0，B/C 有 output；NEG：只因 A PARK 將 B/C 改 WAIT → `GLOBAL_OVERBLOCKING`。elapsed、ready_progress、retry 記實數，不虛設未經來源核准的毫秒 SLA。

詳見 [修補閉環](../REPAIR_CLOSURE_REPORT.md)、[覆蓋實數](../COVERAGE_REPORT.md) 與 [來源解析](../02_EVIDENCE_AUDIT_APPENDICES/10_STATIC_v1_SOURCE_MANIFEST.md)。

## STATIC-v1 真實版本與本地實作綁定

| Repo | 本地 HEAD | 本輪遠端 main | tracked dirty entries / untracked entries |
|---|---|---|---|
| HG-KSEOS | `190df334532ac5a9c4df7e20155a165098625069` | `f6dfb1e57162dc3868dc488482d249fc095eb429` | 8 / 490 |
| SBL | `826ca066a1c2df2976c0d402018b79e1c79a444f` | `fd62537a7ba29c3f2905fe42ddde9534674405d7` | 4 / 58833 |
| Fabric | `fffcb98bf8063e04f3fad2c726eb43fd70336d04` | `316b691460638bdf38475c2c58aaad406aa6eb4f` | 2 / 53 |
| PIPD-LS-SP | `e95942abcb6aa07e69304607ab8afc22a74fc67d` | `f6335a94157c61da75d92121d14c43feb413e981` | 0 / 0 |

本地 HEAD、index blob、staged、unstaged、untracked 均分別保存；遠端以本輪授權憑證唯讀取得 main 完整 blob 樹。兩者不相同，不得以遠端 SHA 當本機 RepoContext。原 R2 的「四庫等同本地」前提在本輪撤銷。工作樹現有變更不由本輪修補、重設或清理。設計 Reader 的 SourceSHA 不等於 Loaded、Actual Served、Permit 或 Checker 收據。
