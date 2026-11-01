<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 03 ARCHITECTURE ABI AND EFFECT｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。




## HANDOFF-v1｜首工作 Effect、Scope 與原生准入分流

| 階段 | Producer → 原 ABI/Reader → Consumer | 現在可做／效果前條件 |
|---|---|---|
| source | 原 Goal/KnownAnswer→TPM corpus Reader→三 SPEC draft | 只讀 admitted corpus；核 SHA；不索 Native Permit |
| draft | 原 TPM `plan_spec`→三 SPECDraft→原 PIPD Intake | 只寫 receiver-authorized isolated draft root 下五個精確檔名；無正式庫寫入 |
| PI/TaskSpecSeed | 原 PIPD Compiler→19 Schema/frozen Reader→receiver adapter | strict payload與非 record sidecar 分離；本輪 static ACK有效於接收；不是原 HGK Canonical TaskSpec |
| Canonical admission | 原 adapter→`native_admission.taskspec_request/workorder_request`→`SharedSpine.create_taskspec/create_workorder` | 原 HGK自行解析 frozen Requirement及真 target identity、principal、scope、HEAD；其 transaction內原 admission 保留，不在作者端呼叫 |
| effect | 原已准入 WorkOrder→Hermes bounded worker→原 Effect Receiver | RepoWrite用 DEV ECP；HostOp用獨立 OPS；UserOp用使用者 scope；RemoteWrite與Release分開原有權 Receiver/Issuer；缺哪一類只 PARK該效果 |

原 TaskSpec/WorkOrder 的建立本身屬 Canonical state mutation，仍走原 HGK受保護准入。這與「讀來源／做本地草稿不必先有 Native effect Permit」是兩條界線，不可互相冒用。原五檔 WriteSet=`ProductSPEC.json, ArchitectureSPEC.json, ProgramSPEC.json, SourceReadback.json, FUO.json`；基準目錄由接收端在施工時晚綁並核 canonical path/preimage，禁止`**`、junction/escape或 source root。尚未配置的 runtime目錄是合法晚綁輸入，並非重複向 Owner索本輪已授的文稿權限。

## 本輪同域受影修復：四庫 Reader／Effect 接線與原 ABI

## 四庫 2026-10-30 `main` 原始碼錨定（GitHub 唯讀）

| Repo/HEAD | 原始碼實測存在的路徑／符號 | 接線或禁止 | 本輪效力 |
|---|---|---|---|
| `Fabric` `316b691460638bdf38475c2c58aaad406aa6eb4f` | `FABRIC/fabric/consumers/hgk_policy_consumer.py` `route_event`、`load_router`；`rp002/RP002_CHANGE_CLASS_ROUTER.yaml` | `route_event` 依 change_class 選原 HERMES_NATIVE/ORACLE_TO_HGK 等 Consumer；文件不能把 `apply_preapproved` 的 raw hash 當真 HGK active grant | REMOTE_SOURCE_OBSERVED；Host Loaded 未證 |
| `HG-KSEOS` `f6dfb1e57162dc3868dc488482d249fc095eb429` | `src/hg_kseos/providers.py` `ProviderRegistry.advance` / lifecycle；`src/hg_kseos/lane_route_resolver.py` | Provider PIN/Installed/Certified/Enabled 順序，不跨級；lane resolver 檔案註記 `CANDIDATE, ISOLATED. Not wired into the launcher`，不得宣稱已 served/loaded | REMOTE_SOURCE_OBSERVED；Launcher bind HOLD |
| `SBL` `fd62537a7ba29c3f2905fe42ddde9534674405d7` | `sbl_harness/__init__.py` 的 `HARNESS_ABI`/`HGK_PIN`；`sbl_core/modes.py` `MODES`、`DISPOSITIONS` | PREW3_SHADOW=`SHADOW_NOEFFECT`，SWOF_CONNECTED=`BLOCKED_EXTERNAL`；SBL Adapter 不簽 HGK Permit | REMOTE_SOURCE_OBSERVED；Host consumer ACK HOLD |
| `PIPD-LS-SP` `f6335a94157c61da75d92121d14c43feb413e981` | `src/pipd_ls_sp/cli.py` `COMMANDS` 恰 13；`pipeline.py` deterministic；`registry.py` `SOURCE_ORDER` 恰19；`requirements.lock` | 19 Contract/13 CLI exact-set，`requirements.lock` version-pinned 但**未 hash-pinned**；不可因 lock 存在自稱供應鏈完全可再現 | REMOTE_SOURCE_OBSERVED；Windows SchemaHost HOLD |

**來源證據界線**：GitHub commit/檔案 blob SHA 不是 Windows process PID、loaded hash、Owner grant、Issuer Permit 或 Native Runner 調用；本輪已保存 local HEAD/index/untracked 原始輸出；只對實測工作樹作判斷。所有 Repo patch 須有現役 Owner 的 exact WriteSet/DEV-ECP/受權 Scope。本版可提供 static patch 契約，不能執行真四庫修改。


---



## R2 Receiver-to-Producer、實效及授權型別（不取代原 ABI）

| 邊 | 原 Producer | 可接受的最低具名入參 | 原 Consumer / OUTPUT | 必須 NACK |
|---|---|---|---|---|
| Goal→SPEC | 單人 Owner/SourceReader | subject, source_sha, known_answer, kind, mode, host | SBL TPM / Product+Arch+Program SPEC | blank goal/foreign source |
| SPEC→PI | PIPD Intake/Authority/Profile | exact source clauses, atom polarity, owner, acceptance_cue | PIPD 原 PI Writer / traced PI | no source/no atom/unknown sidecar |
| PI→PD | PI原 Writer + Local RepoProbe | real worktree root, head, dirty, exact write scope | PIPD 原 PD Binder / late binding | assumed GitHub head/`**` glob |
| PD→DEV ECP | PIPD ECP Writer | exact preimage/write scope/idempotency/rollback | HGK 原 Issuer / governed Repo effect | no token/no rollback |
| PD→OPS ECP | Host Owner | separate Host effect, permit, TTL, epoch, nonce | HGK 原 Host Ops Receiver | DEV token as OPS |
| Policy→Exec | Fabric active/loaded/consumed + HGK SharedSpine | active epoch/loaded SHA/WorkID/lease/operation intent | Hermes 真 Worker / WorldRaw | staged as active, stale lease |
| Result→Checker | World Raw / Candidate hash | checker distinct identity, actual raw, oracle SHA | Original Protected Checker / signed result | mock,self-accept,foreign raw |
| W18 normal | fresh Hermes PID | ordinary Goal, effective profile, task served, resume cursor | original Planner/Worker/Issuer | asks B1 long prompt, repeats nonce |

以上是可給 Receiver 作者對齊的**設計 typed interface**；真 Registry `$id` 和 Owner Effective ABI 依原授權讀回。不新設第四個 Lane/Permit/Queue。Source Read 不索 Host Ops Permit；RepoWrite、HostOps、Remote、Release 必分別按原 effect authority。



## 本版未受影條文（完整沿用、當期生效）

## R2-03-EFFECT：效果與退出按類處理

| EffectClass | tier | permission_basis | Done | rollback/compensation/residue |
|---|---|---|---|---|
| SOURCE_READ | L1 | 原唯讀 ACL/read scope | 讀取 hash/時間/來源及讀取錯誤；world diff=0 | 丟棄快照重讀；不要求 Permit 或卸載收據 |
| LOCAL_DRAFT_WRITE | L0 | 明列隔離 output root 的使用者授權 | 新檔 UTF8/LF/hash/readback；原來源 hash 不變 | 回復本輪 preimage 或刪本輪新檔；不刪他人產物 |
| REPO_WRITE | L2 | DEV ECP + exact WriteSet + 原 HGK admission | pre/post HEAD/diff/test/raw/受影 residue | 原 preimage inverse patch；HEAD 漂移先停，不能 reset 他人變更 |
| HOST_OP | L3 | OPS ECP + Host Owner/Issuer + nonce/TTL/epoch | 真 Host LoadedSHA/consumer ACK/卸載或復原 readback | 原 Host restore/unload；UNKNOWN 先 reconcile，殘留列表交 Owner |
| USER_OP | L3 | USER ECP + 本使用者資料 scope | user store pre/post digest + 新 PID 讀回 | 受權逆操作或補償資料；保留 operation journal |
| REMOTE_WRITE | L3 | REMOTE ECP + 原遠端 principal scope | 遠端 object id/version/ACK/readback | 原服務 inverse 或補償；已被讀取的資料標 residue |
| RELEASE | L4 | 原 Publisher/GHP-02 + 受保護 Checker | release id/signature/實際 channel readback | 由原 Publisher 撤回或新版更正；歷史收據不可抹除 |

`NONE` 只做記憶體計算；無 Permission/Receipt 欄時標 NA(no effect)，不能強迫捏造 token。LOCAL_DRAFT_WRITE 可以是 L0 隔離產物；Repo/product build 若有源碼/工具變更必為 L2。SWOF_W2_SHADOW_NO_WRITE 只有 SOURCE_READ，build 必另開 PRODUCT_BUILD_LOCAL subject，不能共用 Shadow grant。

## R2-03-ABI：五個 typed handoff

1. Source/Intent/Profile → PI：原 Intake/Source/Profile Writer 供應 source digest、atoms、profile；PI Writer 消費 strict schema。副檔存十二軸風險與原 27/149 映射；禁止注入 `_profile_meta`。DOC07 ↔ legacy DOC03、12→9 未 Owner 綁定時只此 promotion HOLD。
2. PI → PD：原 Binder 以真 root/HEAD/index/untracked/ACL/reparse 產 RepoContext；PI 語義不能隨 Host 改寫。HEAD 變動 → `PD_BIND_STALE`；重新讀回，不擴 WriteSet。
3. PD → ConstructionContract + DEV ECP：exact repo files/preimage、expected_changes、tests、rollback 分開交原 Construction/ECP Writer。ECP payload 不等於 HGK Permit。
4. PD → OPS ECP：Host/User/Remote/Release 必拆不同 scope 與 receiver；nonce/TTL/epoch/principal 由真 Issuer 綁。DEV credential 送 Host install → `WRONG_EFFECT_GRANT`。
5. PlannedTQAEP → Checker request：receipt-free 計畫只列 case/oracle/fixtures；原受保護 Reader 解析 Raw、確認不同 principal 才可簽 verdict。Maker 的 expected/fixture 不得轉成 actual raw。

本輪已讀的 native Schema、required、strict unknown 欄拒收與 CLI 實測在 [BODY-02](02_PIPD_LIFECYCLE_AND_TPM.md)。這些是 Repo schema readback，不是 Windows LoadedRegistry ACK。外層 source trace sidecar 只與 payload hash 關聯，不塞進原 strict payload。

## R2-03-SUBJECT：跨域訊息關聯

設計 sidecar 必具 subject_id/source_manifest_sha/candidate_sha/producer/consumer/schema_ref/payload_sha/effect_class/observed_at。接收端先驗 hash/currentness/schema，再驗 authority，最後做 domain predicate；順序錯誤不得靠 generic ACK 補救。ACK 應含 consumer identity、原 schema version、接收 payload hash；NACK 應含 first_fail/affected_scope/next_legal_action/resume_predicate。這是 Reader 設計，非新 native `$id`。

POS：AC-E07 Lease object 只交 SharedSpine CAS；AC-E12 只收 checker run request / protected receipt。NEG：Lease object 交 verdict reader → `NACK_WRONG_DOMAIN_SCHEMA`。Owner 缺 Registry 時此邊 ABI_BIND_HOLD，其他已綁 Reader 可進行。失敗撤本輪 adapter candidate；對 UNKNOWN native effect 只 reconcile，不擦 Journal。

## STATIC-v1 真實版本與本地實作綁定

| Repo | 本地 HEAD | 本輪遠端 main | tracked dirty entries / untracked entries |
|---|---|---|---|
| HG-KSEOS | `190df334532ac5a9c4df7e20155a165098625069` | `f6dfb1e57162dc3868dc488482d249fc095eb429` | 8 / 490 |
| SBL | `826ca066a1c2df2976c0d402018b79e1c79a444f` | `fd62537a7ba29c3f2905fe42ddde9534674405d7` | 4 / 58833 |
| Fabric | `fffcb98bf8063e04f3fad2c726eb43fd70336d04` | `316b691460638bdf38475c2c58aaad406aa6eb4f` | 2 / 53 |
| PIPD-LS-SP | `e95942abcb6aa07e69304607ab8afc22a74fc67d` | `f6335a94157c61da75d92121d14c43feb413e981` | 0 / 0 |

本地 HEAD、index blob、staged、unstaged、untracked 均分別保存；遠端以本輪授權憑證唯讀取得 main 完整 blob 樹。兩者不相同，不得以遠端 SHA 當本機 RepoContext。原 R2 的「四庫等同本地」前提在本輪撤銷。工作樹現有變更不由本輪修補、重設或清理。設計 Reader 的 SourceSHA 不等於 Loaded、Actual Served、Permit 或 Checker 收據。

## STATIC-v1 Agent_Workspace 原 PIPD 工作樹

本地主要實作另有 `C:/Projects/Agent_Workspace/PIPD`，HEAD=`995c7ad0c69a05a0c5cf6528155a62020ce31f87`；其 staged/unstaged/untracked 與 `C:/Projects/pipd-ls-sp` 分別保存。原四庫來源與遠端主線不預設相等；Compiler 細節差異依本版 BODY02 的分版本契約。
