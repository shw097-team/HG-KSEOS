<!-- artifact_version: 2026-10-30_CODEX-STATIC-REPAIR-v1.0_SOURCE_BOUND_HIGH_RETENTION; scope: FHS_DESIGN_READER; native: NATIVE_NOT_RUN; release: NOT_RUN -->

> **CURRENT FHS READER 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND**；原 Domain Writer 不變；歷史 fenced block 不得作有效條位。

# 09B KIND MODE HOST 192｜FHS-MSC_PIPD-LS-PKG 2026-10-30 整合實質正文

> **FHS-MSC_PIPD-LS-PKG / 2026-10-30_r2_HIGH_RETENTION_AUDIT_PATCHED_SOURCE_BOUND / EFFECTIVE_DESIGN_READER**。本冊按同域來源整合 2026-10-29 BODY revision2 和 2026-10-30 r2 最新受影修補。R2 受影條款在本冊設計閱讀範圍優先於被修補之歷史片段；但不覆寫 SBL/PIPD/Fabric/HGK 原 Writer、已生效 Policy/ABI。全部 Native／Owner Ratification／IndependentChecker／Release 未在本沙盒執行。
>
> **ClaimCeiling** `SOURCE_BOUND_INTEGRATED_DESIGN_WITH_LOCAL_READBACK`；`REPO_SOURCE_REMOTE_OBSERVED` 不代表 `LOCAL_REPOCONTEXT_BOUND`，不得藉本檔取得原授權。本冊有效設計正文包含未受影條文；原 Domain Canonical Writer 不移轉。


## 本輪同域受影修復：r2 §7 全量192 個Kind×Mode×Host×Provider

## 7. SBL 192 個 Kind×Mode×Host×Provider Legacy Cell：逐 Cell 生效行為

`CELL-<id>` 都保留原 `Kind/Mode/Host/legacy=ON|OFF`，並由本節每筆 Source Clause 的 ModeGate、HostCaps、POS/NEG、NoFit/卸載綁定。**原來源 ON/OFF 欄位有標籤語義衝突**：BODY09B 候選提出 ON→provider_off=UNBOUND_OWNER_ACK_REQUIRED、OFF→true，但仍需原 Product/Host Owner 签；未決為 `OWNER_BIND_HOLD`，不得以名稱猜測正式 Provider Enum，更不得 Provider-off 外呼。SWOF_W2 Shadow 無可寫世界；合法本地產品 Build 是另一 Subject。[BODY09B `R2-09B-CELL`]

<a id="current-6d0937e8fcff7541bf52"></a>
### CELL-d0cf30ffd7c1｜CLI_TOOL/STANDALONE｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:26`；真 Cell Id `CELL-d0cf30ffd7c1`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L29，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/CLI_TOOL/STANDALONE/ON：原Hermes tool/skill loader與worker fresh PID驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無OS process runner，不要求Host skill loader，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `d0cf30ffd7c1` 的唯讀 Cell 產品設計候選。

<a id="current-431987d350429a418602"></a>
### CELL-e8a4077d37ad｜CLI_TOOL/STANDALONE｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:37`；真 Cell Id `CELL-e8a4077d37ad`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L30，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/CLI_TOOL/STANDALONE/OFF：原Hermes tool/skill loader與worker fresh PID驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無OS process runner，不要求Host skill loader，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `e8a4077d37ad` 的唯讀 Cell 產品設計候選。

<a id="current-d6fd31c23abcda090c82"></a>
### CELL-6582a70fd427｜CLI_TOOL/STANDALONE｜Codex｜legacy=ON
- **原定位**：`BODY-09B:48`；真 Cell Id `CELL-6582a70fd427`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L31，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/CLI_TOOL/STANDALONE/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無OS process runner，不要求Host skill loader，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `6582a70fd427` 的唯讀 Cell 產品設計候選。

<a id="current-542b5ae2c4718ae27bbe"></a>
### CELL-434c21c50bc3｜CLI_TOOL/STANDALONE｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:59`；真 Cell Id `CELL-434c21c50bc3`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L32，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/CLI_TOOL/STANDALONE/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無OS process runner，不要求Host skill loader，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `434c21c50bc3` 的唯讀 Cell 產品設計候選。

<a id="current-3652512ac7e515c2c77d"></a>
### CELL-41348f62f97c｜CLI_TOOL/STANDALONE｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:70`；真 Cell Id `CELL-41348f62f97c`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L33，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/CLI_TOOL/STANDALONE/ON：Claude Code當期原loader＋乾淨session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無OS process runner，不要求Host skill loader，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `41348f62f97c` 的唯讀 Cell 產品設計候選。

<a id="current-4227ea2b6ae93d89f5ef"></a>
### CELL-4bf76833ac66｜CLI_TOOL/STANDALONE｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:81`；真 Cell Id `CELL-4bf76833ac66`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L34，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/CLI_TOOL/STANDALONE/OFF：Claude Code當期原loader＋乾淨session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無OS process runner，不要求Host skill loader，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `4bf76833ac66` 的唯讀 Cell 產品設計候選。

<a id="current-1cf1f909a8a7b56200be"></a>
### CELL-2738990e2c09｜CLI_TOOL/STANDALONE｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:92`；真 Cell Id `CELL-2738990e2c09`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L35，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/CLI_TOOL/STANDALONE/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無entrypoint或退出碼未記錄；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無OS process runner，不要求Host skill loader，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `2738990e2c09` 的唯讀 Cell 產品設計候選。

<a id="current-3bb2493e35069af20f7e"></a>
### CELL-3869542dc2f7｜CLI_TOOL/STANDALONE｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:103`；真 Cell Id `CELL-3869542dc2f7`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L36，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/CLI_TOOL/STANDALONE/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無entrypoint或退出碼未記錄；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無OS process runner，不要求Host skill loader，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `3869542dc2f7` 的唯讀 Cell 產品設計候選。

<a id="current-c519ab51b83ee5d5975c"></a>
### CELL-1407c7aa1d27｜CLI_TOOL/PREW3_SHADOW｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:114`；真 Cell Id `CELL-1407c7aa1d27`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L37，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/CLI_TOOL/PREW3_SHADOW/ON：原Hermes tool/skill loader與worker fresh PID驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無OS process runner，不要求Host skill loader，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `1407c7aa1d27` 的唯讀 Cell 產品設計候選。

<a id="current-67e965b5bc6e975dd798"></a>
### CELL-6b424688af61｜CLI_TOOL/PREW3_SHADOW｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:125`；真 Cell Id `CELL-6b424688af61`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L38，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/CLI_TOOL/PREW3_SHADOW/OFF：原Hermes tool/skill loader與worker fresh PID驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無OS process runner，不要求Host skill loader，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `6b424688af61` 的唯讀 Cell 產品設計候選。

<a id="current-f9a554a3fc36bc8c1fc0"></a>
### CELL-56eaea595d3d｜CLI_TOOL/PREW3_SHADOW｜Codex｜legacy=ON
- **原定位**：`BODY-09B:136`；真 Cell Id `CELL-56eaea595d3d`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L39，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/CLI_TOOL/PREW3_SHADOW/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無OS process runner，不要求Host skill loader，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `56eaea595d3d` 的唯讀 Cell 產品設計候選。

<a id="current-bb43dd40db6fac0ef07a"></a>
### CELL-0dff6839fdf7｜CLI_TOOL/PREW3_SHADOW｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:147`；真 Cell Id `CELL-0dff6839fdf7`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L40，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/CLI_TOOL/PREW3_SHADOW/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無OS process runner，不要求Host skill loader，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `0dff6839fdf7` 的唯讀 Cell 產品設計候選。

<a id="current-b8412443a70f0ec13b84"></a>
### CELL-1cf2ae4386cb｜CLI_TOOL/PREW3_SHADOW｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:158`；真 Cell Id `CELL-1cf2ae4386cb`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L41，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/CLI_TOOL/PREW3_SHADOW/ON：Claude Code當期原loader＋乾淨session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無OS process runner，不要求Host skill loader，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `1cf2ae4386cb` 的唯讀 Cell 產品設計候選。

<a id="current-dd8a715b2a2e220c9521"></a>
### CELL-b6b3031965fa｜CLI_TOOL/PREW3_SHADOW｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:169`；真 Cell Id `CELL-b6b3031965fa`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L42，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/CLI_TOOL/PREW3_SHADOW/OFF：Claude Code當期原loader＋乾淨session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無OS process runner，不要求Host skill loader，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `b6b3031965fa` 的唯讀 Cell 產品設計候選。

<a id="current-a8c1801e1a164fdb7a06"></a>
### CELL-e78d746c7bf7｜CLI_TOOL/PREW3_SHADOW｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:180`；真 Cell Id `CELL-e78d746c7bf7`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L43，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/CLI_TOOL/PREW3_SHADOW/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無entrypoint或退出碼未記錄；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無OS process runner，不要求Host skill loader，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `e78d746c7bf7` 的唯讀 Cell 產品設計候選。

<a id="current-7490da34e31e2cfce0c3"></a>
### CELL-fabd535f6b8d｜CLI_TOOL/PREW3_SHADOW｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:191`；真 Cell Id `CELL-fabd535f6b8d`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L44，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/CLI_TOOL/PREW3_SHADOW/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無entrypoint或退出碼未記錄；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無OS process runner，不要求Host skill loader，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `fabd535f6b8d` 的唯讀 Cell 產品設計候選。

<a id="current-c80b99158636d0c2c7d6"></a>
### CELL-68f927602c56｜CLI_TOOL/SWOF_CONNECTED｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:202`；真 Cell Id `CELL-68f927602c56`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L45，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/CLI_TOOL/SWOF_CONNECTED/ON：原Hermes tool/skill loader與worker fresh PID驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無OS process runner，不要求Host skill loader，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `68f927602c56` 的唯讀 Cell 產品設計候選。

<a id="current-80c97464cc61871da683"></a>
### CELL-09a9c6d13bb7｜CLI_TOOL/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:213`；真 Cell Id `CELL-09a9c6d13bb7`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L46，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/CLI_TOOL/SWOF_CONNECTED/OFF：原Hermes tool/skill loader與worker fresh PID驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無OS process runner，不要求Host skill loader，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `09a9c6d13bb7` 的唯讀 Cell 產品設計候選。

<a id="current-17f9b5c53ccff4d96173"></a>
### CELL-62767ea0b8e8｜CLI_TOOL/SWOF_CONNECTED｜Codex｜legacy=ON
- **原定位**：`BODY-09B:224`；真 Cell Id `CELL-62767ea0b8e8`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L47，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/CLI_TOOL/SWOF_CONNECTED/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無OS process runner，不要求Host skill loader，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `62767ea0b8e8` 的唯讀 Cell 產品設計候選。

<a id="current-8fa5dd0562eedd6b343a"></a>
### CELL-739b3b5375fc｜CLI_TOOL/SWOF_CONNECTED｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:235`；真 Cell Id `CELL-739b3b5375fc`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L48，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/CLI_TOOL/SWOF_CONNECTED/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無OS process runner，不要求Host skill loader，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `739b3b5375fc` 的唯讀 Cell 產品設計候選。

<a id="current-7b3b2c62543a1ed1a30c"></a>
### CELL-944d6c462137｜CLI_TOOL/SWOF_CONNECTED｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:246`；真 Cell Id `CELL-944d6c462137`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L49，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/CLI_TOOL/SWOF_CONNECTED/ON：Claude Code當期原loader＋乾淨session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無OS process runner，不要求Host skill loader，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `944d6c462137` 的唯讀 Cell 產品設計候選。

<a id="current-00124cc6d1ea8da03d23"></a>
### CELL-1444ab821832｜CLI_TOOL/SWOF_CONNECTED｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:257`；真 Cell Id `CELL-1444ab821832`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L50，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/CLI_TOOL/SWOF_CONNECTED/OFF：Claude Code當期原loader＋乾淨session驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無entrypoint或退出碼未記錄；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無OS process runner，不要求Host skill loader，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `1444ab821832` 的唯讀 Cell 產品設計候選。

<a id="current-85deaa598a7586d4b0bd"></a>
### CELL-f5c5147c11c1｜CLI_TOOL/SWOF_CONNECTED｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:268`；真 Cell Id `CELL-f5c5147c11c1`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L51，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/CLI_TOOL/SWOF_CONNECTED/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無entrypoint或退出碼未記錄；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無OS process runner，不要求Host skill loader，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f5c5147c11c1` 的唯讀 Cell 產品設計候選。

<a id="current-d2822b4df23a11c7bb32"></a>
### CELL-5bd80e6cf274｜CLI_TOOL/SWOF_CONNECTED｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:279`；真 Cell Id `CELL-5bd80e6cf274`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L52，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；OS process runner，不要求Host skill loader。
- input→behavior→typed output：source-bound input→乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/CLI_TOOL/SWOF_CONNECTED/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗乾淨binary/script/wheel的entrypoint/help/JSON/nonzero/uninstall；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無entrypoint或退出碼未記錄；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無OS process runner，不要求Host skill loader，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `5bd80e6cf274` 的唯讀 Cell 產品設計候選。

<a id="current-c5a9d4e686e474436ec7"></a>
### CELL-b368d7497e83｜AGENT_SKILL/STANDALONE｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:290`；真 Cell Id `CELL-b368d7497e83`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L53，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/AGENT_SKILL/STANDALONE/ON：原Hermes tool/skill loader與worker fresh PID驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒copy-only或錯誤trigger；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際skill loader；API_ONLY無loader為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `b368d7497e83` 的唯讀 Cell 產品設計候選。

<a id="current-6f45ffbc7748ae77b089"></a>
### CELL-a488c020ca0b｜AGENT_SKILL/STANDALONE｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:301`；真 Cell Id `CELL-a488c020ca0b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L54，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/AGENT_SKILL/STANDALONE/OFF：原Hermes tool/skill loader與worker fresh PID驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒copy-only或錯誤trigger；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際skill loader；API_ONLY無loader為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `a488c020ca0b` 的唯讀 Cell 產品設計候選。

<a id="current-43cb503a3c1c405f865f"></a>
### CELL-cab792bba33a｜AGENT_SKILL/STANDALONE｜Codex｜legacy=ON
- **原定位**：`BODY-09B:312`；真 Cell Id `CELL-cab792bba33a`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L55，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/AGENT_SKILL/STANDALONE/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒copy-only或錯誤trigger；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際skill loader；API_ONLY無loader為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `cab792bba33a` 的唯讀 Cell 產品設計候選。

<a id="current-70be5533cfc5d68822e4"></a>
### CELL-220de7b8b1e7｜AGENT_SKILL/STANDALONE｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:323`；真 Cell Id `CELL-220de7b8b1e7`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L56，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/AGENT_SKILL/STANDALONE/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒copy-only或錯誤trigger；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際skill loader；API_ONLY無loader為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `220de7b8b1e7` 的唯讀 Cell 產品設計候選。

<a id="current-e3ee1f7408b669e49163"></a>
### CELL-e05964530c47｜AGENT_SKILL/STANDALONE｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:334`；真 Cell Id `CELL-e05964530c47`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L57，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/AGENT_SKILL/STANDALONE/ON：Claude Code當期原loader＋乾淨session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒copy-only或錯誤trigger；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際skill loader；API_ONLY無loader為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `e05964530c47` 的唯讀 Cell 產品設計候選。

<a id="current-b753e4bec7df4353cb07"></a>
### CELL-ea5d66500738｜AGENT_SKILL/STANDALONE｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:345`；真 Cell Id `CELL-ea5d66500738`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L58，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/AGENT_SKILL/STANDALONE/OFF：Claude Code當期原loader＋乾淨session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒copy-only或錯誤trigger；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際skill loader；API_ONLY無loader為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `ea5d66500738` 的唯讀 Cell 產品設計候選。

<a id="current-d01009266243a67ca077"></a>
### CELL-cb678bd208a8｜AGENT_SKILL/STANDALONE｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:356`；真 Cell Id `CELL-cb678bd208a8`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L59，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/AGENT_SKILL/STANDALONE/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒copy-only或錯誤trigger；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際skill loader；API_ONLY無loader為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `cb678bd208a8` 的唯讀 Cell 產品設計候選。

<a id="current-200f92f88dfcb7ce4f37"></a>
### CELL-6e1c0fb8d36b｜AGENT_SKILL/STANDALONE｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:367`；真 Cell Id `CELL-6e1c0fb8d36b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L60，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/AGENT_SKILL/STANDALONE/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒copy-only或錯誤trigger；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際skill loader；API_ONLY無loader為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `6e1c0fb8d36b` 的唯讀 Cell 產品設計候選。

<a id="current-6d8e93dea7a4fa7acb6f"></a>
### CELL-dd676737681e｜AGENT_SKILL/PREW3_SHADOW｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:378`；真 Cell Id `CELL-dd676737681e`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L61，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/AGENT_SKILL/PREW3_SHADOW/ON：原Hermes tool/skill loader與worker fresh PID驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒copy-only或錯誤trigger；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際skill loader；API_ONLY無loader為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `dd676737681e` 的唯讀 Cell 產品設計候選。

<a id="current-c34abf307b550d5365e4"></a>
### CELL-6c0ad0177a48｜AGENT_SKILL/PREW3_SHADOW｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:389`；真 Cell Id `CELL-6c0ad0177a48`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L62，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/AGENT_SKILL/PREW3_SHADOW/OFF：原Hermes tool/skill loader與worker fresh PID驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒copy-only或錯誤trigger；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際skill loader；API_ONLY無loader為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `6c0ad0177a48` 的唯讀 Cell 產品設計候選。

<a id="current-6f8da7b9c6c0956dd232"></a>
### CELL-702455102b0e｜AGENT_SKILL/PREW3_SHADOW｜Codex｜legacy=ON
- **原定位**：`BODY-09B:400`；真 Cell Id `CELL-702455102b0e`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L63，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/AGENT_SKILL/PREW3_SHADOW/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒copy-only或錯誤trigger；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際skill loader；API_ONLY無loader為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `702455102b0e` 的唯讀 Cell 產品設計候選。

<a id="current-868c1ef8848b65953f11"></a>
### CELL-d7b2369a3d11｜AGENT_SKILL/PREW3_SHADOW｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:411`；真 Cell Id `CELL-d7b2369a3d11`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L64，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/AGENT_SKILL/PREW3_SHADOW/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒copy-only或錯誤trigger；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際skill loader；API_ONLY無loader為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `d7b2369a3d11` 的唯讀 Cell 產品設計候選。

<a id="current-2e70fd103a5b77f7353a"></a>
### CELL-3b2af66f8936｜AGENT_SKILL/PREW3_SHADOW｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:422`；真 Cell Id `CELL-3b2af66f8936`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L65，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/AGENT_SKILL/PREW3_SHADOW/ON：Claude Code當期原loader＋乾淨session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒copy-only或錯誤trigger；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際skill loader；API_ONLY無loader為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `3b2af66f8936` 的唯讀 Cell 產品設計候選。

<a id="current-dcdebd0f75bfdac1b3cf"></a>
### CELL-46f0028dabe2｜AGENT_SKILL/PREW3_SHADOW｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:433`；真 Cell Id `CELL-46f0028dabe2`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L66，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/AGENT_SKILL/PREW3_SHADOW/OFF：Claude Code當期原loader＋乾淨session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒copy-only或錯誤trigger；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際skill loader；API_ONLY無loader為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `46f0028dabe2` 的唯讀 Cell 產品設計候選。

<a id="current-dfaeb4be996325b21e7f"></a>
### CELL-ae3081300a06｜AGENT_SKILL/PREW3_SHADOW｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:444`；真 Cell Id `CELL-ae3081300a06`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L67，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/AGENT_SKILL/PREW3_SHADOW/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒copy-only或錯誤trigger；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際skill loader；API_ONLY無loader為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `ae3081300a06` 的唯讀 Cell 產品設計候選。

<a id="current-ecb7117c6de5d8bc271c"></a>
### CELL-79aa1ca6c95f｜AGENT_SKILL/PREW3_SHADOW｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:455`；真 Cell Id `CELL-79aa1ca6c95f`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L68，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/AGENT_SKILL/PREW3_SHADOW/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒copy-only或錯誤trigger；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際skill loader；API_ONLY無loader為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `79aa1ca6c95f` 的唯讀 Cell 產品設計候選。

<a id="current-ae8b9550499896d1d319"></a>
### CELL-706d7dabb0a0｜AGENT_SKILL/SWOF_CONNECTED｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:466`；真 Cell Id `CELL-706d7dabb0a0`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L69，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/AGENT_SKILL/SWOF_CONNECTED/ON：原Hermes tool/skill loader與worker fresh PID驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒copy-only或錯誤trigger；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際skill loader；API_ONLY無loader為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `706d7dabb0a0` 的唯讀 Cell 產品設計候選。

<a id="current-2f2edae5d61f22844b50"></a>
### CELL-aab24b0f82f9｜AGENT_SKILL/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:477`；真 Cell Id `CELL-aab24b0f82f9`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L70，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/AGENT_SKILL/SWOF_CONNECTED/OFF：原Hermes tool/skill loader與worker fresh PID驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒copy-only或錯誤trigger；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際skill loader；API_ONLY無loader為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `aab24b0f82f9` 的唯讀 Cell 產品設計候選。

<a id="current-7823ee36c5a42bd2c213"></a>
### CELL-75634c7787b2｜AGENT_SKILL/SWOF_CONNECTED｜Codex｜legacy=ON
- **原定位**：`BODY-09B:488`；真 Cell Id `CELL-75634c7787b2`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L71，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/AGENT_SKILL/SWOF_CONNECTED/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒copy-only或錯誤trigger；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際skill loader；API_ONLY無loader為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `75634c7787b2` 的唯讀 Cell 產品設計候選。

<a id="current-5608d4ad4dd8c40ea211"></a>
### CELL-e341b6d0f605｜AGENT_SKILL/SWOF_CONNECTED｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:499`；真 Cell Id `CELL-e341b6d0f605`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L72，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/AGENT_SKILL/SWOF_CONNECTED/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒copy-only或錯誤trigger；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際skill loader；API_ONLY無loader為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `e341b6d0f605` 的唯讀 Cell 產品設計候選。

<a id="current-ac681a6aa05c808025df"></a>
### CELL-e9941d45073f｜AGENT_SKILL/SWOF_CONNECTED｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:510`；真 Cell Id `CELL-e9941d45073f`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L73，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/AGENT_SKILL/SWOF_CONNECTED/ON：Claude Code當期原loader＋乾淨session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒copy-only或錯誤trigger；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際skill loader；API_ONLY無loader為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `e9941d45073f` 的唯讀 Cell 產品設計候選。

<a id="current-9c6294a226572a7d3f80"></a>
### CELL-e51ce0738940｜AGENT_SKILL/SWOF_CONNECTED｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:521`；真 Cell Id `CELL-e51ce0738940`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L74，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/AGENT_SKILL/SWOF_CONNECTED/OFF：Claude Code當期原loader＋乾淨session驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒copy-only或錯誤trigger；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際skill loader；API_ONLY無loader為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `e51ce0738940` 的唯讀 Cell 產品設計候選。

<a id="current-552d04f88d61aaee7f00"></a>
### CELL-48757186c510｜AGENT_SKILL/SWOF_CONNECTED｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:532`；真 Cell Id `CELL-48757186c510`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L75，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/AGENT_SKILL/SWOF_CONNECTED/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒copy-only或錯誤trigger；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際skill loader；API_ONLY無loader為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `48757186c510` 的唯讀 Cell 產品設計候選。

<a id="current-7af6518de15a74a6dea8"></a>
### CELL-9df05458d74f｜AGENT_SKILL/SWOF_CONNECTED｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:543`；真 Cell Id `CELL-9df05458d74f`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L76，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際skill loader；API_ONLY無loader為NOFIT。
- input→behavior→typed output：source-bound input→SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/AGENT_SKILL/SWOF_CONNECTED/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗SKILL.md/reference/manifest在允許Host discover/load/trigger/nontrigger/unload；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒copy-only或錯誤trigger；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際skill loader；API_ONLY無loader為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `9df05458d74f` 的唯讀 Cell 產品設計候選。

<a id="current-fc04b2fa4884709fca88"></a>
### CELL-52b5e63d094d｜SIMPLE_AGENT/STANDALONE｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:554`；真 Cell Id `CELL-52b5e63d094d`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L77，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/SIMPLE_AGENT/STANDALONE/ON：原Hermes tool/skill loader與worker fresh PID驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無限loop或工具擴權；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host tool-call runner；無tool capability為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `52b5e63d094d` 的唯讀 Cell 產品設計候選。

<a id="current-2be97aab52965b3ccecf"></a>
### CELL-1c821c1ea7d8｜SIMPLE_AGENT/STANDALONE｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:565`；真 Cell Id `CELL-1c821c1ea7d8`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L78，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/SIMPLE_AGENT/STANDALONE/OFF：原Hermes tool/skill loader與worker fresh PID驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無限loop或工具擴權；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host tool-call runner；無tool capability為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `1c821c1ea7d8` 的唯讀 Cell 產品設計候選。

<a id="current-979e1704f3c2a31856bf"></a>
### CELL-3a2a9dad37ae｜SIMPLE_AGENT/STANDALONE｜Codex｜legacy=ON
- **原定位**：`BODY-09B:576`；真 Cell Id `CELL-3a2a9dad37ae`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L79，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/SIMPLE_AGENT/STANDALONE/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無限loop或工具擴權；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host tool-call runner；無tool capability為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `3a2a9dad37ae` 的唯讀 Cell 產品設計候選。

<a id="current-9698b9e037ba36a2583b"></a>
### CELL-87b5a1fe58cf｜SIMPLE_AGENT/STANDALONE｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:587`；真 Cell Id `CELL-87b5a1fe58cf`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L80，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/SIMPLE_AGENT/STANDALONE/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無限loop或工具擴權；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host tool-call runner；無tool capability為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `87b5a1fe58cf` 的唯讀 Cell 產品設計候選。

<a id="current-80fb10460900c7be24af"></a>
### CELL-9e24d28c894c｜SIMPLE_AGENT/STANDALONE｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:598`；真 Cell Id `CELL-9e24d28c894c`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L81，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/SIMPLE_AGENT/STANDALONE/ON：Claude Code當期原loader＋乾淨session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無限loop或工具擴權；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host tool-call runner；無tool capability為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `9e24d28c894c` 的唯讀 Cell 產品設計候選。

<a id="current-b3966d9746f1c73d169f"></a>
### CELL-94a990f58257｜SIMPLE_AGENT/STANDALONE｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:609`；真 Cell Id `CELL-94a990f58257`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L82，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/SIMPLE_AGENT/STANDALONE/OFF：Claude Code當期原loader＋乾淨session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無限loop或工具擴權；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host tool-call runner；無tool capability為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `94a990f58257` 的唯讀 Cell 產品設計候選。

<a id="current-edf1dfb2b29b5de6d585"></a>
### CELL-f0a4964020d6｜SIMPLE_AGENT/STANDALONE｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:620`；真 Cell Id `CELL-f0a4964020d6`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L83，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/SIMPLE_AGENT/STANDALONE/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無限loop或工具擴權；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host tool-call runner；無tool capability為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f0a4964020d6` 的唯讀 Cell 產品設計候選。

<a id="current-6de16d224281e9d2563a"></a>
### CELL-8ba7cd2138c5｜SIMPLE_AGENT/STANDALONE｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:631`；真 Cell Id `CELL-8ba7cd2138c5`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L84，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/SIMPLE_AGENT/STANDALONE/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無限loop或工具擴權；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host tool-call runner；無tool capability為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `8ba7cd2138c5` 的唯讀 Cell 產品設計候選。

<a id="current-255ea0114b8016646bf7"></a>
### CELL-e704b0923b71｜SIMPLE_AGENT/PREW3_SHADOW｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:642`；真 Cell Id `CELL-e704b0923b71`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L85，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/SIMPLE_AGENT/PREW3_SHADOW/ON：原Hermes tool/skill loader與worker fresh PID驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無限loop或工具擴權；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host tool-call runner；無tool capability為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `e704b0923b71` 的唯讀 Cell 產品設計候選。

<a id="current-7af5ebbdfce61715d739"></a>
### CELL-834018317c72｜SIMPLE_AGENT/PREW3_SHADOW｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:653`；真 Cell Id `CELL-834018317c72`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L86，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/SIMPLE_AGENT/PREW3_SHADOW/OFF：原Hermes tool/skill loader與worker fresh PID驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無限loop或工具擴權；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host tool-call runner；無tool capability為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `834018317c72` 的唯讀 Cell 產品設計候選。

<a id="current-a114b77e203f0570ba74"></a>
### CELL-a433df5357ac｜SIMPLE_AGENT/PREW3_SHADOW｜Codex｜legacy=ON
- **原定位**：`BODY-09B:664`；真 Cell Id `CELL-a433df5357ac`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L87，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/SIMPLE_AGENT/PREW3_SHADOW/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無限loop或工具擴權；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host tool-call runner；無tool capability為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `a433df5357ac` 的唯讀 Cell 產品設計候選。

<a id="current-8faa9577aace6cd4ce63"></a>
### CELL-d92746482fe6｜SIMPLE_AGENT/PREW3_SHADOW｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:675`；真 Cell Id `CELL-d92746482fe6`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L88，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/SIMPLE_AGENT/PREW3_SHADOW/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無限loop或工具擴權；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host tool-call runner；無tool capability為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `d92746482fe6` 的唯讀 Cell 產品設計候選。

<a id="current-2314dfbf16535f281aee"></a>
### CELL-3083c98d4210｜SIMPLE_AGENT/PREW3_SHADOW｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:686`；真 Cell Id `CELL-3083c98d4210`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L89，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/SIMPLE_AGENT/PREW3_SHADOW/ON：Claude Code當期原loader＋乾淨session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無限loop或工具擴權；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host tool-call runner；無tool capability為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `3083c98d4210` 的唯讀 Cell 產品設計候選。

<a id="current-ead12cf9181350ae3e5f"></a>
### CELL-97174a3d45e8｜SIMPLE_AGENT/PREW3_SHADOW｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:697`；真 Cell Id `CELL-97174a3d45e8`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L90，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/SIMPLE_AGENT/PREW3_SHADOW/OFF：Claude Code當期原loader＋乾淨session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無限loop或工具擴權；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host tool-call runner；無tool capability為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `97174a3d45e8` 的唯讀 Cell 產品設計候選。

<a id="current-f20f2d812f2c39e5b6b0"></a>
### CELL-84fa01909649｜SIMPLE_AGENT/PREW3_SHADOW｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:708`；真 Cell Id `CELL-84fa01909649`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L91，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/SIMPLE_AGENT/PREW3_SHADOW/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無限loop或工具擴權；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host tool-call runner；無tool capability為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `84fa01909649` 的唯讀 Cell 產品設計候選。

<a id="current-a5cccd3ae43ce3969d86"></a>
### CELL-f77b24e32aaa｜SIMPLE_AGENT/PREW3_SHADOW｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:719`；真 Cell Id `CELL-f77b24e32aaa`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L92，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/SIMPLE_AGENT/PREW3_SHADOW/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無限loop或工具擴權；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host tool-call runner；無tool capability為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f77b24e32aaa` 的唯讀 Cell 產品設計候選。

<a id="current-fd985fa33e78f00e1d7d"></a>
### CELL-c1788f1272d7｜SIMPLE_AGENT/SWOF_CONNECTED｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:730`；真 Cell Id `CELL-c1788f1272d7`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L93，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/SIMPLE_AGENT/SWOF_CONNECTED/ON：原Hermes tool/skill loader與worker fresh PID驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無限loop或工具擴權；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host tool-call runner；無tool capability為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `c1788f1272d7` 的唯讀 Cell 產品設計候選。

<a id="current-6a4b81a18f7696357e26"></a>
### CELL-2a6bfd344f3f｜SIMPLE_AGENT/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:741`；真 Cell Id `CELL-2a6bfd344f3f`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L94，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/SIMPLE_AGENT/SWOF_CONNECTED/OFF：原Hermes tool/skill loader與worker fresh PID驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒無限loop或工具擴權；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host tool-call runner；無tool capability為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `2a6bfd344f3f` 的唯讀 Cell 產品設計候選。

<a id="current-de34330f6f9a21a7bf90"></a>
### CELL-e2daf2609c40｜SIMPLE_AGENT/SWOF_CONNECTED｜Codex｜legacy=ON
- **原定位**：`BODY-09B:752`；真 Cell Id `CELL-e2daf2609c40`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L95，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/SIMPLE_AGENT/SWOF_CONNECTED/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無限loop或工具擴權；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host tool-call runner；無tool capability為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `e2daf2609c40` 的唯讀 Cell 產品設計候選。

<a id="current-4960dc715ac4e8b7784b"></a>
### CELL-d880b5ac23a4｜SIMPLE_AGENT/SWOF_CONNECTED｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:763`；真 Cell Id `CELL-d880b5ac23a4`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L96，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/SIMPLE_AGENT/SWOF_CONNECTED/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒無限loop或工具擴權；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host tool-call runner；無tool capability為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `d880b5ac23a4` 的唯讀 Cell 產品設計候選。

<a id="current-e24f9086f3404be0f42c"></a>
### CELL-ef6dac107879｜SIMPLE_AGENT/SWOF_CONNECTED｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:774`；真 Cell Id `CELL-ef6dac107879`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L97，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/SIMPLE_AGENT/SWOF_CONNECTED/ON：Claude Code當期原loader＋乾淨session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無限loop或工具擴權；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host tool-call runner；無tool capability為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `ef6dac107879` 的唯讀 Cell 產品設計候選。

<a id="current-401a37bc85e305671cec"></a>
### CELL-c1ae4375bd05｜SIMPLE_AGENT/SWOF_CONNECTED｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:785`；真 Cell Id `CELL-c1ae4375bd05`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L98，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/SIMPLE_AGENT/SWOF_CONNECTED/OFF：Claude Code當期原loader＋乾淨session驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒無限loop或工具擴權；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host tool-call runner；無tool capability為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `c1ae4375bd05` 的唯讀 Cell 產品設計候選。

<a id="current-be401df55c35386daa79"></a>
### CELL-09c21bb6612b｜SIMPLE_AGENT/SWOF_CONNECTED｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:796`；真 Cell Id `CELL-09c21bb6612b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L99，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/SIMPLE_AGENT/SWOF_CONNECTED/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無限loop或工具擴權；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host tool-call runner；無tool capability為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `09c21bb6612b` 的唯讀 Cell 產品設計候選。

<a id="current-b9f11d7cf0f3cb902868"></a>
### CELL-9be3a648f57b｜SIMPLE_AGENT/SWOF_CONNECTED｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:807`；真 Cell Id `CELL-9be3a648f57b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L100，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host tool-call runner；無tool capability為NOFIT。
- input→behavior→typed output：source-bound input→agent config+tool allowlist+timeout/attempt budget+stop checkpoint→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/SIMPLE_AGENT/SWOF_CONNECTED/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗agent config+tool allowlist+timeout/attempt budget+stop checkpoint；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒無限loop或工具擴權；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host tool-call runner；無tool capability為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `9be3a648f57b` 的唯讀 Cell 產品設計候選。

<a id="current-abfaaa01b8e0cd7628be"></a>
### CELL-90776ef8d07b｜PLUGIN/STANDALONE｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:818`；真 Cell Id `CELL-90776ef8d07b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L101，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/PLUGIN/STANDALONE/ON：原Hermes tool/skill loader與worker fresh PID驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒不支援Host或未讀manifest權限；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host plugin loader；API_ONLY為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `90776ef8d07b` 的唯讀 Cell 產品設計候選。

<a id="current-9dae0909efe2dfe22114"></a>
### CELL-f6718f8c8a9f｜PLUGIN/STANDALONE｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:829`；真 Cell Id `CELL-f6718f8c8a9f`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L102，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/PLUGIN/STANDALONE/OFF：原Hermes tool/skill loader與worker fresh PID驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒不支援Host或未讀manifest權限；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host plugin loader；API_ONLY為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f6718f8c8a9f` 的唯讀 Cell 產品設計候選。

<a id="current-07b92e6f3b6b43b2c287"></a>
### CELL-b4c34ec88f14｜PLUGIN/STANDALONE｜Codex｜legacy=ON
- **原定位**：`BODY-09B:840`；真 Cell Id `CELL-b4c34ec88f14`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L103，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/PLUGIN/STANDALONE/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒不支援Host或未讀manifest權限；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host plugin loader；API_ONLY為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `b4c34ec88f14` 的唯讀 Cell 產品設計候選。

<a id="current-6fb0d18aeedfdb7b2a03"></a>
### CELL-530a88ba777d｜PLUGIN/STANDALONE｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:851`；真 Cell Id `CELL-530a88ba777d`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L104，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/PLUGIN/STANDALONE/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒不支援Host或未讀manifest權限；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host plugin loader；API_ONLY為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `530a88ba777d` 的唯讀 Cell 產品設計候選。

<a id="current-834d6ded7056bb8bae80"></a>
### CELL-1a9181fe48c5｜PLUGIN/STANDALONE｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:862`；真 Cell Id `CELL-1a9181fe48c5`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L105，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/PLUGIN/STANDALONE/ON：Claude Code當期原loader＋乾淨session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒不支援Host或未讀manifest權限；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host plugin loader；API_ONLY為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `1a9181fe48c5` 的唯讀 Cell 產品設計候選。

<a id="current-43af3108e98bb82e9693"></a>
### CELL-5334bc0dc4e0｜PLUGIN/STANDALONE｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:873`；真 Cell Id `CELL-5334bc0dc4e0`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L106，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/PLUGIN/STANDALONE/OFF：Claude Code當期原loader＋乾淨session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒不支援Host或未讀manifest權限；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host plugin loader；API_ONLY為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `5334bc0dc4e0` 的唯讀 Cell 產品設計候選。

<a id="current-76183414a2c52a0a3673"></a>
### CELL-ecca30d3d545｜PLUGIN/STANDALONE｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:884`；真 Cell Id `CELL-ecca30d3d545`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L107，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/PLUGIN/STANDALONE/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒不支援Host或未讀manifest權限；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host plugin loader；API_ONLY為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `ecca30d3d545` 的唯讀 Cell 產品設計候選。

<a id="current-d11d746587c02c9eddc1"></a>
### CELL-6acbaf567779｜PLUGIN/STANDALONE｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:895`；真 Cell Id `CELL-6acbaf567779`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L108，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/PLUGIN/STANDALONE/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒不支援Host或未讀manifest權限；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host plugin loader；API_ONLY為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `6acbaf567779` 的唯讀 Cell 產品設計候選。

<a id="current-8a3667dda5cd077b3131"></a>
### CELL-f686d9f67c17｜PLUGIN/PREW3_SHADOW｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:906`；真 Cell Id `CELL-f686d9f67c17`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L109，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/PLUGIN/PREW3_SHADOW/ON：原Hermes tool/skill loader與worker fresh PID驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒不支援Host或未讀manifest權限；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host plugin loader；API_ONLY為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f686d9f67c17` 的唯讀 Cell 產品設計候選。

<a id="current-a79d06d834717d3024d1"></a>
### CELL-675386c0f943｜PLUGIN/PREW3_SHADOW｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:917`；真 Cell Id `CELL-675386c0f943`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L110，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/PLUGIN/PREW3_SHADOW/OFF：原Hermes tool/skill loader與worker fresh PID驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒不支援Host或未讀manifest權限；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host plugin loader；API_ONLY為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `675386c0f943` 的唯讀 Cell 產品設計候選。

<a id="current-aebcba8be15d1d85b7bb"></a>
### CELL-412732ed745d｜PLUGIN/PREW3_SHADOW｜Codex｜legacy=ON
- **原定位**：`BODY-09B:928`；真 Cell Id `CELL-412732ed745d`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L111，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/PLUGIN/PREW3_SHADOW/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒不支援Host或未讀manifest權限；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host plugin loader；API_ONLY為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `412732ed745d` 的唯讀 Cell 產品設計候選。

<a id="current-a3b63cfe71cf159ff468"></a>
### CELL-9cc9f40bc2ac｜PLUGIN/PREW3_SHADOW｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:939`；真 Cell Id `CELL-9cc9f40bc2ac`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L112，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/PLUGIN/PREW3_SHADOW/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒不支援Host或未讀manifest權限；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host plugin loader；API_ONLY為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `9cc9f40bc2ac` 的唯讀 Cell 產品設計候選。

<a id="current-250dd045ae7fbbcab205"></a>
### CELL-2259ef3f0dc2｜PLUGIN/PREW3_SHADOW｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:950`；真 Cell Id `CELL-2259ef3f0dc2`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L113，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/PLUGIN/PREW3_SHADOW/ON：Claude Code當期原loader＋乾淨session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒不支援Host或未讀manifest權限；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host plugin loader；API_ONLY為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `2259ef3f0dc2` 的唯讀 Cell 產品設計候選。

<a id="current-1ab1728ecd4b75f50fff"></a>
### CELL-4f536bbc5402｜PLUGIN/PREW3_SHADOW｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:961`；真 Cell Id `CELL-4f536bbc5402`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L114，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/PLUGIN/PREW3_SHADOW/OFF：Claude Code當期原loader＋乾淨session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒不支援Host或未讀manifest權限；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host plugin loader；API_ONLY為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `4f536bbc5402` 的唯讀 Cell 產品設計候選。

<a id="current-3d551de9d23b0547e753"></a>
### CELL-bc4919027c0c｜PLUGIN/PREW3_SHADOW｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:972`；真 Cell Id `CELL-bc4919027c0c`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L115，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/PLUGIN/PREW3_SHADOW/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒不支援Host或未讀manifest權限；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host plugin loader；API_ONLY為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `bc4919027c0c` 的唯讀 Cell 產品設計候選。

<a id="current-976007c4abf0912c5b7f"></a>
### CELL-06bbd5e5ecb2｜PLUGIN/PREW3_SHADOW｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:983`；真 Cell Id `CELL-06bbd5e5ecb2`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L116，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/PLUGIN/PREW3_SHADOW/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒不支援Host或未讀manifest權限；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host plugin loader；API_ONLY為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `06bbd5e5ecb2` 的唯讀 Cell 產品設計候選。

<a id="current-70e785a1657d14e86a67"></a>
### CELL-d19d2e42002a｜PLUGIN/SWOF_CONNECTED｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:994`；真 Cell Id `CELL-d19d2e42002a`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L117，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/PLUGIN/SWOF_CONNECTED/ON：原Hermes tool/skill loader與worker fresh PID驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒不支援Host或未讀manifest權限；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host plugin loader；API_ONLY為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `d19d2e42002a` 的唯讀 Cell 產品設計候選。

<a id="current-449aab845ebfd1156218"></a>
### CELL-49cdd601f213｜PLUGIN/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1005`；真 Cell Id `CELL-49cdd601f213`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L118，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/PLUGIN/SWOF_CONNECTED/OFF：原Hermes tool/skill loader與worker fresh PID驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒不支援Host或未讀manifest權限；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host plugin loader；API_ONLY為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `49cdd601f213` 的唯讀 Cell 產品設計候選。

<a id="current-366a205dfbf7011f6cf5"></a>
### CELL-54d1a08c379f｜PLUGIN/SWOF_CONNECTED｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1016`；真 Cell Id `CELL-54d1a08c379f`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L119，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/PLUGIN/SWOF_CONNECTED/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒不支援Host或未讀manifest權限；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host plugin loader；API_ONLY為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `54d1a08c379f` 的唯讀 Cell 產品設計候選。

<a id="current-635e009518985062d1a6"></a>
### CELL-2ce069d50986｜PLUGIN/SWOF_CONNECTED｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1027`；真 Cell Id `CELL-2ce069d50986`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L120，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/PLUGIN/SWOF_CONNECTED/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒不支援Host或未讀manifest權限；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host plugin loader；API_ONLY為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `2ce069d50986` 的唯讀 Cell 產品設計候選。

<a id="current-ff15840b12764700fe95"></a>
### CELL-afca4537e0b5｜PLUGIN/SWOF_CONNECTED｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:1038`；真 Cell Id `CELL-afca4537e0b5`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L121，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/PLUGIN/SWOF_CONNECTED/ON：Claude Code當期原loader＋乾淨session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒不支援Host或未讀manifest權限；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host plugin loader；API_ONLY為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `afca4537e0b5` 的唯讀 Cell 產品設計候選。

<a id="current-1baf6783bf145966b7fd"></a>
### CELL-ae862affcd7c｜PLUGIN/SWOF_CONNECTED｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:1049`；真 Cell Id `CELL-ae862affcd7c`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L122，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/PLUGIN/SWOF_CONNECTED/OFF：Claude Code當期原loader＋乾淨session驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒不支援Host或未讀manifest權限；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host plugin loader；API_ONLY為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `ae862affcd7c` 的唯讀 Cell 產品設計候選。

<a id="current-4203ed5b303cb1a4755e"></a>
### CELL-8bf8d2ec3581｜PLUGIN/SWOF_CONNECTED｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:1060`；真 Cell Id `CELL-8bf8d2ec3581`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L123，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/PLUGIN/SWOF_CONNECTED/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒不支援Host或未讀manifest權限；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host plugin loader；API_ONLY為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `8bf8d2ec3581` 的唯讀 Cell 產品設計候選。

<a id="current-f00cce4a2b30e5162fc0"></a>
### CELL-085bc8fd7622｜PLUGIN/SWOF_CONNECTED｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:1071`；真 Cell Id `CELL-085bc8fd7622`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L124，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host plugin loader；API_ONLY為NOFIT。
- input→behavior→typed output：source-bound input→manifest publisher/version/license/permissions；Host載入、調用及移除→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/PLUGIN/SWOF_CONNECTED/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗manifest publisher/version/license/permissions；Host載入、調用及移除；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒不支援Host或未讀manifest權限；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host plugin loader；API_ONLY為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `085bc8fd7622` 的唯讀 Cell 產品設計候選。

<a id="current-38fea59648568d966fed"></a>
### CELL-f6053f9a9dbf｜PROFILE/STANDALONE｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:1082`；真 Cell Id `CELL-f6053f9a9dbf`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L125，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/PROFILE/STANDALONE/ON：原Hermes tool/skill loader與worker fresh PID驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host Profile Reader；無profile interface為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f6053f9a9dbf` 的唯讀 Cell 產品設計候選。

<a id="current-6af4b22d087b41c97a16"></a>
### CELL-48759a93f265｜PROFILE/STANDALONE｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1093`；真 Cell Id `CELL-48759a93f265`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L126，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/PROFILE/STANDALONE/OFF：原Hermes tool/skill loader與worker fresh PID驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host Profile Reader；無profile interface為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `48759a93f265` 的唯讀 Cell 產品設計候選。

<a id="current-f2e56f49d658b5b64c47"></a>
### CELL-ce7ed7519316｜PROFILE/STANDALONE｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1104`；真 Cell Id `CELL-ce7ed7519316`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L127，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/PROFILE/STANDALONE/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host Profile Reader；無profile interface為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `ce7ed7519316` 的唯讀 Cell 產品設計候選。

<a id="current-0c0fcdeecd428adbe0ec"></a>
### CELL-e9109bda38f1｜PROFILE/STANDALONE｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1115`；真 Cell Id `CELL-e9109bda38f1`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L128，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/PROFILE/STANDALONE/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host Profile Reader；無profile interface為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `e9109bda38f1` 的唯讀 Cell 產品設計候選。

<a id="current-42b197e30f31cc0e77e4"></a>
### CELL-67282ac08b7e｜PROFILE/STANDALONE｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:1126`；真 Cell Id `CELL-67282ac08b7e`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L129，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/PROFILE/STANDALONE/ON：Claude Code當期原loader＋乾淨session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host Profile Reader；無profile interface為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `67282ac08b7e` 的唯讀 Cell 產品設計候選。

<a id="current-f82aa2a991d1f04d639b"></a>
### CELL-77fe98764ab5｜PROFILE/STANDALONE｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:1137`；真 Cell Id `CELL-77fe98764ab5`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L130，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/PROFILE/STANDALONE/OFF：Claude Code當期原loader＋乾淨session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host Profile Reader；無profile interface為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `77fe98764ab5` 的唯讀 Cell 產品設計候選。

<a id="current-e59e40fa72b4bf149b1b"></a>
### CELL-24e9aedd8086｜PROFILE/STANDALONE｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:1148`；真 Cell Id `CELL-24e9aedd8086`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L131，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/PROFILE/STANDALONE/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host Profile Reader；無profile interface為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `24e9aedd8086` 的唯讀 Cell 產品設計候選。

<a id="current-9cc6a8cc39ef0f0937b5"></a>
### CELL-75540fe3412c｜PROFILE/STANDALONE｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:1159`；真 Cell Id `CELL-75540fe3412c`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L132，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/PROFILE/STANDALONE/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host Profile Reader；無profile interface為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `75540fe3412c` 的唯讀 Cell 產品設計候選。

<a id="current-9b121e130b810f91fddb"></a>
### CELL-e3f461767442｜PROFILE/PREW3_SHADOW｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:1170`；真 Cell Id `CELL-e3f461767442`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L133，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/PROFILE/PREW3_SHADOW/ON：原Hermes tool/skill loader與worker fresh PID驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host Profile Reader；無profile interface為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `e3f461767442` 的唯讀 Cell 產品設計候選。

<a id="current-933a10e5131893509754"></a>
### CELL-491bbc480824｜PROFILE/PREW3_SHADOW｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1181`；真 Cell Id `CELL-491bbc480824`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L134，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/PROFILE/PREW3_SHADOW/OFF：原Hermes tool/skill loader與worker fresh PID驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host Profile Reader；無profile interface為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `491bbc480824` 的唯讀 Cell 產品設計候選。

<a id="current-c79bdd2d33cb92c2c462"></a>
### CELL-24862363699e｜PROFILE/PREW3_SHADOW｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1192`；真 Cell Id `CELL-24862363699e`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L135，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/PROFILE/PREW3_SHADOW/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host Profile Reader；無profile interface為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `24862363699e` 的唯讀 Cell 產品設計候選。

<a id="current-c2e04321e4d58ca76222"></a>
### CELL-b41a32121615｜PROFILE/PREW3_SHADOW｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1203`；真 Cell Id `CELL-b41a32121615`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L136，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/PROFILE/PREW3_SHADOW/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host Profile Reader；無profile interface為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `b41a32121615` 的唯讀 Cell 產品設計候選。

<a id="current-bdfa8f8245b22801fffd"></a>
### CELL-8605451d5dd2｜PROFILE/PREW3_SHADOW｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:1214`；真 Cell Id `CELL-8605451d5dd2`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L137，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/PROFILE/PREW3_SHADOW/ON：Claude Code當期原loader＋乾淨session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host Profile Reader；無profile interface為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `8605451d5dd2` 的唯讀 Cell 產品設計候選。

<a id="current-0f3ec07236e7aa03c65c"></a>
### CELL-9ca3d0377ed8｜PROFILE/PREW3_SHADOW｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:1225`；真 Cell Id `CELL-9ca3d0377ed8`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L138，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/PROFILE/PREW3_SHADOW/OFF：Claude Code當期原loader＋乾淨session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host Profile Reader；無profile interface為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `9ca3d0377ed8` 的唯讀 Cell 產品設計候選。

<a id="current-3e96b2cf5ca8cb8a95b5"></a>
### CELL-dd12df59427a｜PROFILE/PREW3_SHADOW｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:1236`；真 Cell Id `CELL-dd12df59427a`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L139，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/PROFILE/PREW3_SHADOW/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host Profile Reader；無profile interface為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `dd12df59427a` 的唯讀 Cell 產品設計候選。

<a id="current-f46f8d9194454810ff1a"></a>
### CELL-5ce6176dde4b｜PROFILE/PREW3_SHADOW｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:1247`；真 Cell Id `CELL-5ce6176dde4b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L140，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/PROFILE/PREW3_SHADOW/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host Profile Reader；無profile interface為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `5ce6176dde4b` 的唯讀 Cell 產品設計候選。

<a id="current-dc80a1970e8fbf426149"></a>
### CELL-40ec4e4388b4｜PROFILE/SWOF_CONNECTED｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:1258`；真 Cell Id `CELL-40ec4e4388b4`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L141，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/PROFILE/SWOF_CONNECTED/ON：原Hermes tool/skill loader與worker fresh PID驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host Profile Reader；無profile interface為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `40ec4e4388b4` 的唯讀 Cell 產品設計候選。

<a id="current-9e83146cb486b532bc5b"></a>
### CELL-0836e4dc5096｜PROFILE/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1269`；真 Cell Id `CELL-0836e4dc5096`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L142，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/PROFILE/SWOF_CONNECTED/OFF：原Hermes tool/skill loader與worker fresh PID驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原Host Profile Reader；無profile interface為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `0836e4dc5096` 的唯讀 Cell 產品設計候選。

<a id="current-0cc11e0bfc7cd6cc2437"></a>
### CELL-57abd1af6eca｜PROFILE/SWOF_CONNECTED｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1280`；真 Cell Id `CELL-57abd1af6eca`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L143，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/PROFILE/SWOF_CONNECTED/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host Profile Reader；無profile interface為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `57abd1af6eca` 的唯讀 Cell 產品設計候選。

<a id="current-89b0deb44a33dea52569"></a>
### CELL-9bf92fc1f576｜PROFILE/SWOF_CONNECTED｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1291`；真 Cell Id `CELL-9bf92fc1f576`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L144，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/PROFILE/SWOF_CONNECTED/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原Host Profile Reader；無profile interface為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `9bf92fc1f576` 的唯讀 Cell 產品設計候選。

<a id="current-cfa1c0a66466f2a251db"></a>
### CELL-ac9b0f671ba6｜PROFILE/SWOF_CONNECTED｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:1302`；真 Cell Id `CELL-ac9b0f671ba6`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L145，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/PROFILE/SWOF_CONNECTED/ON：Claude Code當期原loader＋乾淨session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host Profile Reader；無profile interface為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `ac9b0f671ba6` 的唯讀 Cell 產品設計候選。

<a id="current-ea642bb82f10089238b4"></a>
### CELL-c798b8d56448｜PROFILE/SWOF_CONNECTED｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:1313`；真 Cell Id `CELL-c798b8d56448`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L146，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/PROFILE/SWOF_CONNECTED/OFF：Claude Code當期原loader＋乾淨session驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原Host Profile Reader；無profile interface為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `c798b8d56448` 的唯讀 Cell 產品設計候選。

<a id="current-9db483cc14e764761e59"></a>
### CELL-44b29464a95a｜PROFILE/SWOF_CONNECTED｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:1324`；真 Cell Id `CELL-44b29464a95a`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L147，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/PROFILE/SWOF_CONNECTED/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host Profile Reader；無profile interface為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `44b29464a95a` 的唯讀 Cell 產品設計候選。

<a id="current-5ec4d8f7611534212413"></a>
### CELL-db54604c0f5b｜PROFILE/SWOF_CONNECTED｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:1335`；真 Cell Id `CELL-db54604c0f5b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L148，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原Host Profile Reader；無profile interface為NOFIT。
- input→behavior→typed output：source-bound input→ProfileBinding/applicability+scope/loaded SHA與卸載還原→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/PROFILE/SWOF_CONNECTED/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗ProfileBinding/applicability+scope/loaded SHA與卸載還原；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒selected當loaded或跨Scope套Profile；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原Host Profile Reader；無profile interface為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `db54604c0f5b` 的唯讀 Cell 產品設計候選。

<a id="current-674dd15937fdf6285ed1"></a>
### CELL-afca55403585｜AGENT_OS/STANDALONE｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:1346`；真 Cell Id `CELL-afca55403585`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L149，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/AGENT_OS/STANDALONE/ON：原Hermes tool/skill loader與worker fresh PID驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒規劃文本冒可執行OS；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `afca55403585` 的唯讀 Cell 產品設計候選。

<a id="current-1925614ae564750edb36"></a>
### CELL-df93f59a1365｜AGENT_OS/STANDALONE｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1357`；真 Cell Id `CELL-df93f59a1365`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L150，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/AGENT_OS/STANDALONE/OFF：原Hermes tool/skill loader與worker fresh PID驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒規劃文本冒可執行OS；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `df93f59a1365` 的唯讀 Cell 產品設計候選。

<a id="current-be959f4cf0f070ecb29a"></a>
### CELL-6c851f664a31｜AGENT_OS/STANDALONE｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1368`；真 Cell Id `CELL-6c851f664a31`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L151，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/AGENT_OS/STANDALONE/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒規劃文本冒可執行OS；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `6c851f664a31` 的唯讀 Cell 產品設計候選。

<a id="current-9332b63ea8d85834fd78"></a>
### CELL-0af202afbd93｜AGENT_OS/STANDALONE｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1379`；真 Cell Id `CELL-0af202afbd93`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L152，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/AGENT_OS/STANDALONE/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒規劃文本冒可執行OS；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `0af202afbd93` 的唯讀 Cell 產品設計候選。

<a id="current-69e5c64dce5932fb016e"></a>
### CELL-97fb84872359｜AGENT_OS/STANDALONE｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:1390`；真 Cell Id `CELL-97fb84872359`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L153，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/AGENT_OS/STANDALONE/ON：Claude Code當期原loader＋乾淨session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒規劃文本冒可執行OS；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `97fb84872359` 的唯讀 Cell 產品設計候選。

<a id="current-bca8fa0f90dbb9122d3c"></a>
### CELL-c226c99e3199｜AGENT_OS/STANDALONE｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:1401`；真 Cell Id `CELL-c226c99e3199`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L154，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/AGENT_OS/STANDALONE/OFF：Claude Code當期原loader＋乾淨session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒規劃文本冒可執行OS；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `c226c99e3199` 的唯讀 Cell 產品設計候選。

<a id="current-dd8542e2ad0c7e9c2e85"></a>
### CELL-9e3a12ad436c｜AGENT_OS/STANDALONE｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:1412`；真 Cell Id `CELL-9e3a12ad436c`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L155，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/AGENT_OS/STANDALONE/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒規劃文本冒可執行OS；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `9e3a12ad436c` 的唯讀 Cell 產品設計候選。

<a id="current-f14fe6a5a4a2e140f974"></a>
### CELL-f18950ce731b｜AGENT_OS/STANDALONE｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:1423`；真 Cell Id `CELL-f18950ce731b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L156，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/AGENT_OS/STANDALONE/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒規劃文本冒可執行OS；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f18950ce731b` 的唯讀 Cell 產品設計候選。

<a id="current-5ab88ad0f656e0e73a80"></a>
### CELL-4199689808cf｜AGENT_OS/PREW3_SHADOW｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:1434`；真 Cell Id `CELL-4199689808cf`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L157，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/AGENT_OS/PREW3_SHADOW/ON：原Hermes tool/skill loader與worker fresh PID驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒規劃文本冒可執行OS；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `4199689808cf` 的唯讀 Cell 產品設計候選。

<a id="current-d2fe2a981e8e90b0ddb8"></a>
### CELL-b6ed07348d18｜AGENT_OS/PREW3_SHADOW｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1445`；真 Cell Id `CELL-b6ed07348d18`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L158，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/AGENT_OS/PREW3_SHADOW/OFF：原Hermes tool/skill loader與worker fresh PID驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒規劃文本冒可執行OS；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `b6ed07348d18` 的唯讀 Cell 產品設計候選。

<a id="current-95f1b14f1d7942da6a17"></a>
### CELL-ae25f61ef832｜AGENT_OS/PREW3_SHADOW｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1456`；真 Cell Id `CELL-ae25f61ef832`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L159，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/AGENT_OS/PREW3_SHADOW/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒規劃文本冒可執行OS；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `ae25f61ef832` 的唯讀 Cell 產品設計候選。

<a id="current-504de056c8db313cf777"></a>
### CELL-ec0547fd0acf｜AGENT_OS/PREW3_SHADOW｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1467`；真 Cell Id `CELL-ec0547fd0acf`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L160，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/AGENT_OS/PREW3_SHADOW/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒規劃文本冒可執行OS；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `ec0547fd0acf` 的唯讀 Cell 產品設計候選。

<a id="current-66b0276c7c1df3ac98b1"></a>
### CELL-2331ca9034c4｜AGENT_OS/PREW3_SHADOW｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:1478`；真 Cell Id `CELL-2331ca9034c4`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L161，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/AGENT_OS/PREW3_SHADOW/ON：Claude Code當期原loader＋乾淨session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒規劃文本冒可執行OS；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `2331ca9034c4` 的唯讀 Cell 產品設計候選。

<a id="current-0a9e2e36574e86aac37e"></a>
### CELL-c7f9eff2fddd｜AGENT_OS/PREW3_SHADOW｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:1489`；真 Cell Id `CELL-c7f9eff2fddd`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L162，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/AGENT_OS/PREW3_SHADOW/OFF：Claude Code當期原loader＋乾淨session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒規劃文本冒可執行OS；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `c7f9eff2fddd` 的唯讀 Cell 產品設計候選。

<a id="current-e24f9c3b1acea6942202"></a>
### CELL-f93b6704ee69｜AGENT_OS/PREW3_SHADOW｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:1500`；真 Cell Id `CELL-f93b6704ee69`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L163，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/AGENT_OS/PREW3_SHADOW/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒規劃文本冒可執行OS；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f93b6704ee69` 的唯讀 Cell 產品設計候選。

<a id="current-b320bdc2012fb9746bb6"></a>
### CELL-91838cb6a697｜AGENT_OS/PREW3_SHADOW｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:1511`；真 Cell Id `CELL-91838cb6a697`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L164，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/AGENT_OS/PREW3_SHADOW/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒規劃文本冒可執行OS；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `91838cb6a697` 的唯讀 Cell 產品設計候選。

<a id="current-0514430b396ce08bb9d8"></a>
### CELL-78e42a13bbff｜AGENT_OS/SWOF_CONNECTED｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:1522`；真 Cell Id `CELL-78e42a13bbff`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L165，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/AGENT_OS/SWOF_CONNECTED/ON：原Hermes tool/skill loader與worker fresh PID驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒規劃文本冒可執行OS；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `78e42a13bbff` 的唯讀 Cell 產品設計候選。

<a id="current-d9a2d8203a71a6621587"></a>
### CELL-8c30f1274481｜AGENT_OS/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1533`；真 Cell Id `CELL-8c30f1274481`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L166，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/AGENT_OS/SWOF_CONNECTED/OFF：原Hermes tool/skill loader與worker fresh PID驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒規劃文本冒可執行OS；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `8c30f1274481` 的唯讀 Cell 產品設計候選。

<a id="current-006dc0fed5673e2654c0"></a>
### CELL-9fdb959e54cd｜AGENT_OS/SWOF_CONNECTED｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1544`；真 Cell Id `CELL-9fdb959e54cd`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L167，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/AGENT_OS/SWOF_CONNECTED/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒規劃文本冒可執行OS；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `9fdb959e54cd` 的唯讀 Cell 產品設計候選。

<a id="current-bd69817d2d22295d74a5"></a>
### CELL-16b0d6f0aa4b｜AGENT_OS/SWOF_CONNECTED｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1555`；真 Cell Id `CELL-16b0d6f0aa4b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L168，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/AGENT_OS/SWOF_CONNECTED/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒規劃文本冒可執行OS；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `16b0d6f0aa4b` 的唯讀 Cell 產品設計候選。

<a id="current-6809ee90bd67bd516905"></a>
### CELL-9f3a107b084e｜AGENT_OS/SWOF_CONNECTED｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:1566`；真 Cell Id `CELL-9f3a107b084e`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L169，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/AGENT_OS/SWOF_CONNECTED/ON：Claude Code當期原loader＋乾淨session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒規劃文本冒可執行OS；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `9f3a107b084e` 的唯讀 Cell 產品設計候選。

<a id="current-e3a497d5657d1f9e11c7"></a>
### CELL-378b78d029ac｜AGENT_OS/SWOF_CONNECTED｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:1577`；真 Cell Id `CELL-378b78d029ac`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L170，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/AGENT_OS/SWOF_CONNECTED/OFF：Claude Code當期原loader＋乾淨session驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒規劃文本冒可執行OS；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `378b78d029ac` 的唯讀 Cell 產品設計候選。

<a id="current-39b03ba8c0ca1abf4421"></a>
### CELL-10cbe7b8ba17｜AGENT_OS/SWOF_CONNECTED｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:1588`；真 Cell Id `CELL-10cbe7b8ba17`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L171，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/AGENT_OS/SWOF_CONNECTED/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒規劃文本冒可執行OS；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `10cbe7b8ba17` 的唯讀 Cell 產品設計候選。

<a id="current-56e383108f73ceceb1b2"></a>
### CELL-95ae8bfac0e7｜AGENT_OS/SWOF_CONNECTED｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:1599`；真 Cell Id `CELL-95ae8bfac0e7`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L172，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT。
- input→behavior→typed output：source-bound input→正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/AGENT_OS/SWOF_CONNECTED/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗正式OS lifecycle/Registry/Team/Phase的原Reader與受權部署；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒規劃文本冒可執行OS；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無Native OS lifecycle；便攜Host只能規格預覽，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `95ae8bfac0e7` 的唯讀 Cell 產品設計候選。

<a id="current-da6bdd8ffe5ece122679"></a>
### CELL-d0ea4e9314ef｜AI_SYSTEM/STANDALONE｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:1610`；真 Cell Id `CELL-d0ea4e9314ef`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L173，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/AI_SYSTEM/STANDALONE/ON：原Hermes tool/skill loader與worker fresh PID驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒單Agent demo冒完整系統；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際system deployment orchestrator；無部署接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `d0ea4e9314ef` 的唯讀 Cell 產品設計候選。

<a id="current-5ecf98a2ed62cd299954"></a>
### CELL-e90fb5ce4fd3｜AI_SYSTEM/STANDALONE｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1621`；真 Cell Id `CELL-e90fb5ce4fd3`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L174，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/AI_SYSTEM/STANDALONE/OFF：原Hermes tool/skill loader與worker fresh PID驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒單Agent demo冒完整系統；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際system deployment orchestrator；無部署接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `e90fb5ce4fd3` 的唯讀 Cell 產品設計候選。

<a id="current-9f73168fc565d8ec290a"></a>
### CELL-980e1f8cdbf6｜AI_SYSTEM/STANDALONE｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1632`；真 Cell Id `CELL-980e1f8cdbf6`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L175，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/AI_SYSTEM/STANDALONE/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒單Agent demo冒完整系統；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際system deployment orchestrator；無部署接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `980e1f8cdbf6` 的唯讀 Cell 產品設計候選。

<a id="current-bf001de977990746bc33"></a>
### CELL-80e6856b5e3c｜AI_SYSTEM/STANDALONE｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1643`；真 Cell Id `CELL-80e6856b5e3c`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L176，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/AI_SYSTEM/STANDALONE/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒單Agent demo冒完整系統；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際system deployment orchestrator；無部署接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `80e6856b5e3c` 的唯讀 Cell 產品設計候選。

<a id="current-df6c571f97c90d960968"></a>
### CELL-ec2d6ac66d18｜AI_SYSTEM/STANDALONE｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:1654`；真 Cell Id `CELL-ec2d6ac66d18`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L177，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/AI_SYSTEM/STANDALONE/ON：Claude Code當期原loader＋乾淨session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒單Agent demo冒完整系統；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際system deployment orchestrator；無部署接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `ec2d6ac66d18` 的唯讀 Cell 產品設計候選。

<a id="current-85b3ef1216c50efb89c4"></a>
### CELL-4ed5ad806797｜AI_SYSTEM/STANDALONE｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:1665`；真 Cell Id `CELL-4ed5ad806797`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L178，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/AI_SYSTEM/STANDALONE/OFF：Claude Code當期原loader＋乾淨session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒單Agent demo冒完整系統；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際system deployment orchestrator；無部署接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `4ed5ad806797` 的唯讀 Cell 產品設計候選。

<a id="current-9ce408c167a6215d4243"></a>
### CELL-f478ba7d0b9a｜AI_SYSTEM/STANDALONE｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:1676`；真 Cell Id `CELL-f478ba7d0b9a`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L179，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/AI_SYSTEM/STANDALONE/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒單Agent demo冒完整系統；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際system deployment orchestrator；無部署接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f478ba7d0b9a` 的唯讀 Cell 產品設計候選。

<a id="current-ce23cdfaafd99db78d17"></a>
### CELL-057db0593627｜AI_SYSTEM/STANDALONE｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:1687`；真 Cell Id `CELL-057db0593627`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L180，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/AI_SYSTEM/STANDALONE/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒單Agent demo冒完整系統；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際system deployment orchestrator；無部署接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `057db0593627` 的唯讀 Cell 產品設計候選。

<a id="current-9be2c5332585ad790c1a"></a>
### CELL-cb6fcd8de73c｜AI_SYSTEM/PREW3_SHADOW｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:1698`；真 Cell Id `CELL-cb6fcd8de73c`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L181，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/AI_SYSTEM/PREW3_SHADOW/ON：原Hermes tool/skill loader與worker fresh PID驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒單Agent demo冒完整系統；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際system deployment orchestrator；無部署接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `cb6fcd8de73c` 的唯讀 Cell 產品設計候選。

<a id="current-2b0ac4d915d26463ff22"></a>
### CELL-41ed105d02da｜AI_SYSTEM/PREW3_SHADOW｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1709`；真 Cell Id `CELL-41ed105d02da`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L182，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/AI_SYSTEM/PREW3_SHADOW/OFF：原Hermes tool/skill loader與worker fresh PID驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒單Agent demo冒完整系統；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際system deployment orchestrator；無部署接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `41ed105d02da` 的唯讀 Cell 產品設計候選。

<a id="current-9f8801bd602f08a5819c"></a>
### CELL-836112ec4da9｜AI_SYSTEM/PREW3_SHADOW｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1720`；真 Cell Id `CELL-836112ec4da9`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L183，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/AI_SYSTEM/PREW3_SHADOW/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒單Agent demo冒完整系統；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際system deployment orchestrator；無部署接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `836112ec4da9` 的唯讀 Cell 產品設計候選。

<a id="current-c06001332c660ceb5d15"></a>
### CELL-83cb46793f3b｜AI_SYSTEM/PREW3_SHADOW｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1731`；真 Cell Id `CELL-83cb46793f3b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L184，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/AI_SYSTEM/PREW3_SHADOW/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒單Agent demo冒完整系統；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際system deployment orchestrator；無部署接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `83cb46793f3b` 的唯讀 Cell 產品設計候選。

<a id="current-27646f24b2f001341cad"></a>
### CELL-39e031d42387｜AI_SYSTEM/PREW3_SHADOW｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:1742`；真 Cell Id `CELL-39e031d42387`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L185，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/AI_SYSTEM/PREW3_SHADOW/ON：Claude Code當期原loader＋乾淨session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒單Agent demo冒完整系統；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際system deployment orchestrator；無部署接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `39e031d42387` 的唯讀 Cell 產品設計候選。

<a id="current-2404dae5e475310589d3"></a>
### CELL-f250e0e5814a｜AI_SYSTEM/PREW3_SHADOW｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:1753`；真 Cell Id `CELL-f250e0e5814a`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L186，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/AI_SYSTEM/PREW3_SHADOW/OFF：Claude Code當期原loader＋乾淨session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒單Agent demo冒完整系統；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際system deployment orchestrator；無部署接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f250e0e5814a` 的唯讀 Cell 產品設計候選。

<a id="current-32dc2ea13f9de117aa5b"></a>
### CELL-9742bec81e5a｜AI_SYSTEM/PREW3_SHADOW｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:1764`；真 Cell Id `CELL-9742bec81e5a`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L187，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/AI_SYSTEM/PREW3_SHADOW/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒單Agent demo冒完整系統；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際system deployment orchestrator；無部署接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `9742bec81e5a` 的唯讀 Cell 產品設計候選。

<a id="current-74c2a0cedc9022d7401c"></a>
### CELL-237ac6308b3f｜AI_SYSTEM/PREW3_SHADOW｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:1775`；真 Cell Id `CELL-237ac6308b3f`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L188，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/AI_SYSTEM/PREW3_SHADOW/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒單Agent demo冒完整系統；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際system deployment orchestrator；無部署接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `237ac6308b3f` 的唯讀 Cell 產品設計候選。

<a id="current-fb98f742d86bb0033fe8"></a>
### CELL-762256559527｜AI_SYSTEM/SWOF_CONNECTED｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:1786`；真 Cell Id `CELL-762256559527`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L189，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/AI_SYSTEM/SWOF_CONNECTED/ON：原Hermes tool/skill loader與worker fresh PID驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒單Agent demo冒完整系統；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際system deployment orchestrator；無部署接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `762256559527` 的唯讀 Cell 產品設計候選。

<a id="current-0d91c7c6c884102eb3bf"></a>
### CELL-42f5aee6701f｜AI_SYSTEM/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1797`；真 Cell Id `CELL-42f5aee6701f`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L190，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/AI_SYSTEM/SWOF_CONNECTED/OFF：原Hermes tool/skill loader與worker fresh PID驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒單Agent demo冒完整系統；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無實際system deployment orchestrator；無部署接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `42f5aee6701f` 的唯讀 Cell 產品設計候選。

<a id="current-55f3ac73c176d8f71ef9"></a>
### CELL-7b1a7a42e067｜AI_SYSTEM/SWOF_CONNECTED｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1808`；真 Cell Id `CELL-7b1a7a42e067`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L191，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/AI_SYSTEM/SWOF_CONNECTED/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒單Agent demo冒完整系統；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際system deployment orchestrator；無部署接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `7b1a7a42e067` 的唯讀 Cell 產品設計候選。

<a id="current-c1f37ac39b4f1f60fdf1"></a>
### CELL-f171ddc0382c｜AI_SYSTEM/SWOF_CONNECTED｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1819`；真 Cell Id `CELL-f171ddc0382c`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L192，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/AI_SYSTEM/SWOF_CONNECTED/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒單Agent demo冒完整系統；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無實際system deployment orchestrator；無部署接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f171ddc0382c` 的唯讀 Cell 產品設計候選。

<a id="current-897431eebf710f60ee19"></a>
### CELL-a50d9bf4ec2f｜AI_SYSTEM/SWOF_CONNECTED｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:1830`；真 Cell Id `CELL-a50d9bf4ec2f`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L193，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/AI_SYSTEM/SWOF_CONNECTED/ON：Claude Code當期原loader＋乾淨session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒單Agent demo冒完整系統；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際system deployment orchestrator；無部署接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `a50d9bf4ec2f` 的唯讀 Cell 產品設計候選。

<a id="current-b8e5fe356a7c8c84eb41"></a>
### CELL-90274105bfbf｜AI_SYSTEM/SWOF_CONNECTED｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:1841`；真 Cell Id `CELL-90274105bfbf`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L194，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/AI_SYSTEM/SWOF_CONNECTED/OFF：Claude Code當期原loader＋乾淨session驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒單Agent demo冒完整系統；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無實際system deployment orchestrator；無部署接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `90274105bfbf` 的唯讀 Cell 產品設計候選。

<a id="current-c1b0c1121075ba6e78d6"></a>
### CELL-b85f95d3b255｜AI_SYSTEM/SWOF_CONNECTED｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:1852`；真 Cell Id `CELL-b85f95d3b255`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L195，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/AI_SYSTEM/SWOF_CONNECTED/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒單Agent demo冒完整系統；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際system deployment orchestrator；無部署接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `b85f95d3b255` 的唯讀 Cell 產品設計候選。

<a id="current-e335d77c27e4dc2f1462"></a>
### CELL-1746d4d5a88d｜AI_SYSTEM/SWOF_CONNECTED｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:1863`；真 Cell Id `CELL-1746d4d5a88d`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L196，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；實際system deployment orchestrator；無部署接口為NOFIT。
- input→behavior→typed output：source-bound input→多組件DAG/ABI/部署健康/退場的整體consumer readback→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/AI_SYSTEM/SWOF_CONNECTED/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗多組件DAG/ABI/部署健康/退場的整體consumer readback；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒單Agent demo冒完整系統；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無實際system deployment orchestrator；無部署接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `1746d4d5a88d` 的唯讀 Cell 產品設計候選。

<a id="current-41e797d23e6bc90442f9"></a>
### CELL-336e267c9f1b｜GENIE/GENIE.md/STANDALONE｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:1874`；真 Cell Id `CELL-336e267c9f1b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L197，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/GENIE/GENIE.md/STANDALONE/ON：原Hermes tool/skill loader與worker fresh PID驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `336e267c9f1b` 的唯讀 Cell 產品設計候選。

<a id="current-3ef9ee3ea90a4c651ad5"></a>
### CELL-8f240272c803｜GENIE/GENIE.md/STANDALONE｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1885`；真 Cell Id `CELL-8f240272c803`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L198，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/GENIE/GENIE.md/STANDALONE/OFF：原Hermes tool/skill loader與worker fresh PID驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `8f240272c803` 的唯讀 Cell 產品設計候選。

<a id="current-887d43c73c7c465f8d9a"></a>
### CELL-5c0c72c957ed｜GENIE/GENIE.md/STANDALONE｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1896`；真 Cell Id `CELL-5c0c72c957ed`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L199，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/GENIE/GENIE.md/STANDALONE/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `5c0c72c957ed` 的唯讀 Cell 產品設計候選。

<a id="current-82c6c6de3a866d4db073"></a>
### CELL-d9f0da8c1631｜GENIE/GENIE.md/STANDALONE｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1907`；真 Cell Id `CELL-d9f0da8c1631`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L200，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/GENIE/GENIE.md/STANDALONE/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `d9f0da8c1631` 的唯讀 Cell 產品設計候選。

<a id="current-a6c1763e62fd0d8c4d69"></a>
### CELL-070f95d5c154｜GENIE/GENIE.md/STANDALONE｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:1918`；真 Cell Id `CELL-070f95d5c154`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L201，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/GENIE/GENIE.md/STANDALONE/ON：Claude Code當期原loader＋乾淨session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `070f95d5c154` 的唯讀 Cell 產品設計候選。

<a id="current-7771ca705bdc19dc3359"></a>
### CELL-479fa09ec346｜GENIE/GENIE.md/STANDALONE｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:1929`；真 Cell Id `CELL-479fa09ec346`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L202，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/GENIE/GENIE.md/STANDALONE/OFF：Claude Code當期原loader＋乾淨session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `479fa09ec346` 的唯讀 Cell 產品設計候選。

<a id="current-801b4a6944fb75998bd2"></a>
### CELL-9af02fa9e8ed｜GENIE/GENIE.md/STANDALONE｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:1940`；真 Cell Id `CELL-9af02fa9e8ed`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L203，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/GENIE/GENIE.md/STANDALONE/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `9af02fa9e8ed` 的唯讀 Cell 產品設計候選。

<a id="current-27f4dac759cbe7e01709"></a>
### CELL-c38a7e723977｜GENIE/GENIE.md/STANDALONE｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:1951`；真 Cell Id `CELL-c38a7e723977`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L204，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：STANDALONE_USER_CONSENT; no HGK dependency for local non-native outcome；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/GENIE/GENIE.md/STANDALONE/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `c38a7e723977` 的唯讀 Cell 產品設計候選。

<a id="current-b9c6bcd2e5cb14b7f289"></a>
### CELL-510726a815d2｜GENIE/GENIE.md/PREW3_SHADOW｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:1962`；真 Cell Id `CELL-510726a815d2`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L205，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/GENIE/GENIE.md/PREW3_SHADOW/ON：原Hermes tool/skill loader與worker fresh PID驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `510726a815d2` 的唯讀 Cell 產品設計候選。

<a id="current-4d1bfba576269f76fe18"></a>
### CELL-f842f5e447d1｜GENIE/GENIE.md/PREW3_SHADOW｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:1973`；真 Cell Id `CELL-f842f5e447d1`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L206，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/GENIE/GENIE.md/PREW3_SHADOW/OFF：原Hermes tool/skill loader與worker fresh PID驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f842f5e447d1` 的唯讀 Cell 產品設計候選。

<a id="current-3f99e2044494dc1fa70e"></a>
### CELL-82305af511e2｜GENIE/GENIE.md/PREW3_SHADOW｜Codex｜legacy=ON
- **原定位**：`BODY-09B:1984`；真 Cell Id `CELL-82305af511e2`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L207，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/GENIE/GENIE.md/PREW3_SHADOW/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `82305af511e2` 的唯讀 Cell 產品設計候選。

<a id="current-8346fd3c03f551a1a5c5"></a>
### CELL-bf764d5ba2c2｜GENIE/GENIE.md/PREW3_SHADOW｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:1995`；真 Cell Id `CELL-bf764d5ba2c2`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L208，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/GENIE/GENIE.md/PREW3_SHADOW/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `bf764d5ba2c2` 的唯讀 Cell 產品設計候選。

<a id="current-53115c3c7c4496a72b43"></a>
### CELL-d69adf2f1965｜GENIE/GENIE.md/PREW3_SHADOW｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:2006`；真 Cell Id `CELL-d69adf2f1965`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L209，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/GENIE/GENIE.md/PREW3_SHADOW/ON：Claude Code當期原loader＋乾淨session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `d69adf2f1965` 的唯讀 Cell 產品設計候選。

<a id="current-72059a9b4bd88d03d93c"></a>
### CELL-1ef60244801f｜GENIE/GENIE.md/PREW3_SHADOW｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:2017`；真 Cell Id `CELL-1ef60244801f`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L210，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/GENIE/GENIE.md/PREW3_SHADOW/OFF：Claude Code當期原loader＋乾淨session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `1ef60244801f` 的唯讀 Cell 產品設計候選。

<a id="current-97a28c66188fbb2453e5"></a>
### CELL-98d011df32e5｜GENIE/GENIE.md/PREW3_SHADOW｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:2028`；真 Cell Id `CELL-98d011df32e5`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L211，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/GENIE/GENIE.md/PREW3_SHADOW/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `98d011df32e5` 的唯讀 Cell 產品設計候選。

<a id="current-fd60866be50f6ce42ef7"></a>
### CELL-880fcebbf48e｜GENIE/GENIE.md/PREW3_SHADOW｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:2039`；真 Cell Id `CELL-880fcebbf48e`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L212，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：SOURCE_READ/NO_SWOF_WRITE；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/GENIE/GENIE.md/PREW3_SHADOW/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `880fcebbf48e` 的唯讀 Cell 產品設計候選。

<a id="current-1c19d946689b061c9f1b"></a>
### CELL-a8a335dada5e｜GENIE/GENIE.md/SWOF_CONNECTED｜Hermes Agent｜legacy=ON
- **原定位**：`BODY-09B:2050`；真 Cell Id `CELL-a8a335dada5e`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L213，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Hermes Agent/GENIE/GENIE.md/SWOF_CONNECTED/ON：原Hermes tool/skill loader與worker fresh PID驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Hermes Agent或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `a8a335dada5e` 的唯讀 Cell 產品設計候選。

<a id="current-fe825bbebc21a769ea14"></a>
### CELL-f9d246f739b8｜GENIE/GENIE.md/SWOF_CONNECTED｜Hermes Agent｜legacy=OFF
- **原定位**：`BODY-09B:2061`；真 Cell Id `CELL-f9d246f739b8`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L214，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：原Hermes tool/skill loader與worker fresh PID；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Hermes Agent/GENIE/GENIE.md/SWOF_CONNECTED/OFF：原Hermes tool/skill loader與worker fresh PID驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=journal cursor/lease_generation/worker_pid。
- NEG/first_fail：Hermes Agent此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Hermes Agent或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Hermes Agent若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Hermes原Journal/Worker Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Hermes Agent依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `f9d246f739b8` 的唯讀 Cell 產品設計候選。

<a id="current-416cd64f80e89f01662f"></a>
### CELL-8ed9eebf58e7｜GENIE/GENIE.md/SWOF_CONNECTED｜Codex｜legacy=ON
- **原定位**：`BODY-09B:2072`；真 Cell Id `CELL-8ed9eebf58e7`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L215，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Codex/GENIE/GENIE.md/SWOF_CONNECTED/ON：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Codex或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `8ed9eebf58e7` 的唯讀 Cell 產品設計候選。

<a id="current-589399e1af261bf76aea"></a>
### CELL-b6fc7bd2585b｜GENIE/GENIE.md/SWOF_CONNECTED｜Codex｜legacy=OFF
- **原定位**：`BODY-09B:2083`；真 Cell Id `CELL-b6fc7bd2585b`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L216，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Codex Host skill/plugin discovery＋乾淨chat/CLI session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Codex/GENIE/GENIE.md/SWOF_CONNECTED/OFF：Codex Host skill/plugin discovery＋乾淨chat/CLI session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=Host manifest/loaded SHA/trigger invocation。
- NEG/first_fail：Codex此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Codex或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Codex若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Codex Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Codex依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `b6fc7bd2585b` 的唯讀 Cell 產品設計候選。

<a id="current-f7b567bc7825b0ecd768"></a>
### CELL-ea0c6cc43029｜GENIE/GENIE.md/SWOF_CONNECTED｜Claude Code｜legacy=ON
- **原定位**：`BODY-09B:2094`；真 Cell Id `CELL-ea0c6cc43029`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L217，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：Claude Code/GENIE/GENIE.md/SWOF_CONNECTED/ON：Claude Code當期原loader＋乾淨session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Claude Code或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `ea0c6cc43029` 的唯讀 Cell 產品設計候選。

<a id="current-f3fd1cf896ca3e35a6ed"></a>
### CELL-425204fe1c0f｜GENIE/GENIE.md/SWOF_CONNECTED｜Claude Code｜legacy=OFF
- **原定位**：`BODY-09B:2105`；真 Cell Id `CELL-425204fe1c0f`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L218，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：Claude Code當期原loader＋乾淨session；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：Claude Code/GENIE/GENIE.md/SWOF_CONNECTED/OFF：Claude Code當期原loader＋乾淨session驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=原Host允許的manifest/permission/effective load。
- NEG/first_fail：Claude Code此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於Claude Code或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：Claude Code若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由Claude Code Host Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：Claude Code依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`OFF`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `425204fe1c0f` 的唯讀 Cell 產品設計候選。

<a id="current-b96d78735b0b9507ef87"></a>
### CELL-fc762041aa9d｜GENIE/GENIE.md/SWOF_CONNECTED｜DeepSeek Harness｜legacy=ON
- **原定位**：`BODY-09B:2116`；真 Cell Id `CELL-fc762041aa9d`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L219，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback。
- POS：DeepSeek Harness/GENIE/GENIE.md/SWOF_CONNECTED/ON：實際Harness adapter/capability reader；API_ONLY不能充loader驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：需provider時驗本cell原Policy允許的served Raw；provider缺件→NOFIT，不私fallback；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於DeepSeek Harness或provider行為違ON原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。

- **R2 生效隔離**：raw_token=`ON`；semantic_mapping_status=`UNBOUND_OWNER_CONFLICT`；host_provider_off_boolean=`null`；owner_ack_version=`null`；`runtime_effect_allowed=false`，不得使用同段舊 candidate 規則產生真正 Provider 呼叫；只能產 `fc762041aa9d` 的唯讀 Cell 產品設計候選。

<a id="current-09fd6697ba30c9d58e49"></a>
### CELL-5370fdd74e46｜GENIE/GENIE.md/SWOF_CONNECTED｜DeepSeek Harness｜legacy=OFF
- **原定位**：`BODY-09B:2127`；真 Cell Id `CELL-5370fdd74e46`（不得借其他 Host/Mode 之 receipt）。
- Trigger/input：此Kind需求在此Mode與此Host被要求；source v1:L220，SHA `41cdd5e5ab16bc2b44ab47155e6cd09e81eef98c56753ae7dd03d0484385a4cd`。
- route/HostCaps：實際Harness adapter/capability reader；API_ONLY不能充loader；原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT。
- input→behavior→typed output：source-bound input→原SWOF版本化GENIE reference/schema與Owner關聯讀回→CellOutcome(cell_id,host,session,capability,artifact_sha,actual_raw_sha,status)。
- effect/permission：ORIGINAL_SWOF_W3_ADMISSION+OPS/DEV_BY_EFFECT；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商。
- POS：DeepSeek Harness/GENIE/GENIE.md/SWOF_CONNECTED/OFF：實際Harness adapter/capability reader；API_ONLY不能充loader驗原SWOF版本化GENIE reference/schema與Owner關聯讀回；provider_off=UNBOUND_OWNER_ACK_REQUIRED：零provider網路呼叫；有離線實作才可完成，需模型但無離線runner→NOFIT，不換供應商；同cell/Host/session raw=harness ABI/tool_result/session identity。
- NEG/first_fail：DeepSeek Harness此cell拒任意GENIE.md冒正式生成或部署；若raw.host不等於DeepSeek Harness或provider行為違OFF原label對照則CELL_RECEIPT_SCOPE_NACK。
- NoFit：DeepSeek Harness若無原GENIE Compiler/Reader；便攜Host只read refs，無接口為NOFIT，由DeepSeek Harness Owner回NO_FIT_WITH_REASON；不借其它Host收據。
- exit/resume：DeepSeek Harness依此Kind原loader卸載/撤Profile或停止受影runner；Reader無effect只丟快照，UNKNOWN先reconcile；重新probe本Host能力與原Owner provider label map後再測。NATIVE_NOT_RUN。


---



## R2 四 Host 衝突的完整受影遷移候選（48/48，不覆寫原 CellID）


### PROPOSAL-CHATGPT-2738990e2c09｜`CLI_TOOL` × `STANDALONE` × legacy `ON`
- 源身份：`CELL-2738990e2c09` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-2738990e2c09` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-3869542dc2f7｜`CLI_TOOL` × `STANDALONE` × legacy `OFF`
- 源身份：`CELL-3869542dc2f7` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-3869542dc2f7` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-e78d746c7bf7｜`CLI_TOOL` × `PREW3_SHADOW` × legacy `ON`
- 源身份：`CELL-e78d746c7bf7` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-e78d746c7bf7` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-fabd535f6b8d｜`CLI_TOOL` × `PREW3_SHADOW` × legacy `OFF`
- 源身份：`CELL-fabd535f6b8d` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-fabd535f6b8d` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-f5c5147c11c1｜`CLI_TOOL` × `SWOF_CONNECTED` × legacy `ON`
- 源身份：`CELL-f5c5147c11c1` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-f5c5147c11c1` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-5bd80e6cf274｜`CLI_TOOL` × `SWOF_CONNECTED` × legacy `OFF`
- 源身份：`CELL-5bd80e6cf274` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-5bd80e6cf274` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-cb678bd208a8｜`AGENT_SKILL` × `STANDALONE` × legacy `ON`
- 源身份：`CELL-cb678bd208a8` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-cb678bd208a8` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-6e1c0fb8d36b｜`AGENT_SKILL` × `STANDALONE` × legacy `OFF`
- 源身份：`CELL-6e1c0fb8d36b` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-6e1c0fb8d36b` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-ae3081300a06｜`AGENT_SKILL` × `PREW3_SHADOW` × legacy `ON`
- 源身份：`CELL-ae3081300a06` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-ae3081300a06` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-79aa1ca6c95f｜`AGENT_SKILL` × `PREW3_SHADOW` × legacy `OFF`
- 源身份：`CELL-79aa1ca6c95f` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-79aa1ca6c95f` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-48757186c510｜`AGENT_SKILL` × `SWOF_CONNECTED` × legacy `ON`
- 源身份：`CELL-48757186c510` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-48757186c510` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-9df05458d74f｜`AGENT_SKILL` × `SWOF_CONNECTED` × legacy `OFF`
- 源身份：`CELL-9df05458d74f` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-9df05458d74f` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-f0a4964020d6｜`SIMPLE_AGENT` × `STANDALONE` × legacy `ON`
- 源身份：`CELL-f0a4964020d6` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-f0a4964020d6` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-8ba7cd2138c5｜`SIMPLE_AGENT` × `STANDALONE` × legacy `OFF`
- 源身份：`CELL-8ba7cd2138c5` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-8ba7cd2138c5` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-84fa01909649｜`SIMPLE_AGENT` × `PREW3_SHADOW` × legacy `ON`
- 源身份：`CELL-84fa01909649` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-84fa01909649` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-f77b24e32aaa｜`SIMPLE_AGENT` × `PREW3_SHADOW` × legacy `OFF`
- 源身份：`CELL-f77b24e32aaa` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-f77b24e32aaa` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-09c21bb6612b｜`SIMPLE_AGENT` × `SWOF_CONNECTED` × legacy `ON`
- 源身份：`CELL-09c21bb6612b` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-09c21bb6612b` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-9be3a648f57b｜`SIMPLE_AGENT` × `SWOF_CONNECTED` × legacy `OFF`
- 源身份：`CELL-9be3a648f57b` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-9be3a648f57b` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-ecca30d3d545｜`PLUGIN` × `STANDALONE` × legacy `ON`
- 源身份：`CELL-ecca30d3d545` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-ecca30d3d545` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-6acbaf567779｜`PLUGIN` × `STANDALONE` × legacy `OFF`
- 源身份：`CELL-6acbaf567779` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-6acbaf567779` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-bc4919027c0c｜`PLUGIN` × `PREW3_SHADOW` × legacy `ON`
- 源身份：`CELL-bc4919027c0c` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-bc4919027c0c` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-06bbd5e5ecb2｜`PLUGIN` × `PREW3_SHADOW` × legacy `OFF`
- 源身份：`CELL-06bbd5e5ecb2` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-06bbd5e5ecb2` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-8bf8d2ec3581｜`PLUGIN` × `SWOF_CONNECTED` × legacy `ON`
- 源身份：`CELL-8bf8d2ec3581` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-8bf8d2ec3581` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-085bc8fd7622｜`PLUGIN` × `SWOF_CONNECTED` × legacy `OFF`
- 源身份：`CELL-085bc8fd7622` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-085bc8fd7622` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-24e9aedd8086｜`PROFILE` × `STANDALONE` × legacy `ON`
- 源身份：`CELL-24e9aedd8086` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-24e9aedd8086` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-75540fe3412c｜`PROFILE` × `STANDALONE` × legacy `OFF`
- 源身份：`CELL-75540fe3412c` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-75540fe3412c` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-dd12df59427a｜`PROFILE` × `PREW3_SHADOW` × legacy `ON`
- 源身份：`CELL-dd12df59427a` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-dd12df59427a` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-5ce6176dde4b｜`PROFILE` × `PREW3_SHADOW` × legacy `OFF`
- 源身份：`CELL-5ce6176dde4b` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-5ce6176dde4b` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-44b29464a95a｜`PROFILE` × `SWOF_CONNECTED` × legacy `ON`
- 源身份：`CELL-44b29464a95a` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-44b29464a95a` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-db54604c0f5b｜`PROFILE` × `SWOF_CONNECTED` × legacy `OFF`
- 源身份：`CELL-db54604c0f5b` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-db54604c0f5b` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-9e3a12ad436c｜`AGENT_OS` × `STANDALONE` × legacy `ON`
- 源身份：`CELL-9e3a12ad436c` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-9e3a12ad436c` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-f18950ce731b｜`AGENT_OS` × `STANDALONE` × legacy `OFF`
- 源身份：`CELL-f18950ce731b` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-f18950ce731b` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-f93b6704ee69｜`AGENT_OS` × `PREW3_SHADOW` × legacy `ON`
- 源身份：`CELL-f93b6704ee69` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-f93b6704ee69` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-91838cb6a697｜`AGENT_OS` × `PREW3_SHADOW` × legacy `OFF`
- 源身份：`CELL-91838cb6a697` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-91838cb6a697` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-10cbe7b8ba17｜`AGENT_OS` × `SWOF_CONNECTED` × legacy `ON`
- 源身份：`CELL-10cbe7b8ba17` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-10cbe7b8ba17` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-95ae8bfac0e7｜`AGENT_OS` × `SWOF_CONNECTED` × legacy `OFF`
- 源身份：`CELL-95ae8bfac0e7` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-95ae8bfac0e7` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-f478ba7d0b9a｜`AI_SYSTEM` × `STANDALONE` × legacy `ON`
- 源身份：`CELL-f478ba7d0b9a` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-f478ba7d0b9a` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-057db0593627｜`AI_SYSTEM` × `STANDALONE` × legacy `OFF`
- 源身份：`CELL-057db0593627` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-057db0593627` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-9742bec81e5a｜`AI_SYSTEM` × `PREW3_SHADOW` × legacy `ON`
- 源身份：`CELL-9742bec81e5a` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-9742bec81e5a` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-237ac6308b3f｜`AI_SYSTEM` × `PREW3_SHADOW` × legacy `OFF`
- 源身份：`CELL-237ac6308b3f` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-237ac6308b3f` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-b85f95d3b255｜`AI_SYSTEM` × `SWOF_CONNECTED` × legacy `ON`
- 源身份：`CELL-b85f95d3b255` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-b85f95d3b255` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-1746d4d5a88d｜`AI_SYSTEM` × `SWOF_CONNECTED` × legacy `OFF`
- 源身份：`CELL-1746d4d5a88d` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-1746d4d5a88d` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-9af02fa9e8ed｜`GENIE/GENIE.md` × `STANDALONE` × legacy `ON`
- 源身份：`CELL-9af02fa9e8ed` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-9af02fa9e8ed` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-c38a7e723977｜`GENIE/GENIE.md` × `STANDALONE` × legacy `OFF`
- 源身份：`CELL-c38a7e723977` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-c38a7e723977` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-98d011df32e5｜`GENIE/GENIE.md` × `PREW3_SHADOW` × legacy `ON`
- 源身份：`CELL-98d011df32e5` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-98d011df32e5` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-880fcebbf48e｜`GENIE/GENIE.md` × `PREW3_SHADOW` × legacy `OFF`
- 源身份：`CELL-880fcebbf48e` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-880fcebbf48e` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-fc762041aa9d｜`GENIE/GENIE.md` × `SWOF_CONNECTED` × legacy `ON`
- 源身份：`CELL-fc762041aa9d` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-fc762041aa9d` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

### PROPOSAL-CHATGPT-5370fdd74e46｜`GENIE/GENIE.md` × `SWOF_CONNECTED` × legacy `OFF`
- 源身份：`CELL-5370fdd74e46` / `DeepSeek Harness`（保留，不改名）；產品要求另為 `ChatGPT`，本 ID **尚非 Original 192 Cell**。
- 原 Reader/Owner：SBL Product Owner＋ChatGPT Host Owner；input=原 ProductKind/Mode/SourceSHA/Token + HostCaps/Version/Effect；host_adapter=ChatGPT API-only under supported surface（未證實的 OS loader 原封不動 NOFIT）。
- 正例候選：只做唯讀 Source/Goal→ChatGPT supported UX result 或已證 Host SDK handler，記 requested Kind/Mode/ProviderOnOff 未核定；True Host Loader 功能等實機。
- 負例：假造 ChatGPT 擁有 DeepSeek 進程／host runner，或用 `CELL-5370fdd74e46` 的 Raw 當 ChatGPT → `HOST_IDENTITY_DRIFT`；`PREW3_SHADOW` 禁 World Write。
- 退出：Original ID untouched；未有核定版本/HostCaps/ProviderToken 就 `CR-HOST-192` 下 `MIGRATION_HOLD`；產品承諾仍列。

## STATIC-v1 Provider token 與執行布林的接線規則

本冊 192 原 Cell 的 ON/OFF 僅作原身份欄，沒有可呼叫 Provider 的推測轉換。`host_provider_off_boolean=null`、`runtime_effect_allowed=false` 直至原 Product/Provider Policy Owner 用同版本映射及原 Reader 完成綁定。POS：保留原 raw token、原 Host、原 CellID；在未知映射時可作文件／離線靜態處理而不外呼。NEG：從 ON 推定允許外呼、把 DeepSeek 48 Cell 改成 ChatGPT、借另一 Host Raw → 拒收。NoFit 只隔離需外呼的 Cell；恢復條件為同 Subject/PolicyEpoch 的有效映射與原 Host 收據。已批准 ProviderOff=true 時零 Provider 外呼是獨立安全義務，不受此 legacy label 衝突削弱。
