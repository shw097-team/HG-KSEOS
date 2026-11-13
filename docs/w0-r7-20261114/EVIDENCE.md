# FHS_PIPD-LS-PKG_W0_vNEXT 證據型附錄（r2）

> **配對正文**：`FHS_PIPD-LS-PKG_W0_vNEXT_2026-11-14_r2_實質正文.md`
> **本件僅供審計**，不是第二規範；規範仍以 `spec/FHS_PIPD-LS-PKG_W0_20261112_r8.md` 為 current。
> **Redaction**：不含 token、金鑰、口令、DB、WAL；憑證只留路徑與遮罩摘要。


## A｜來源 manifest（本輪實讀）

| 來源 | 路徑 | bytes | SHA-256 |
| --- | --- | --- | --- |
| L0 總藍圖 | FHS_vNEXT_總藍圖.md | 365153 | 33e49ca22872b135534e078661df32d6a2892058c8c0efae859540943731caf0 |
| L1 PLP 藍圖 | FHS_vNEXT_PLP_藍圖.md | 7256694 | bd2ab0b74f21da6b74cac2e1b1ffd2c8dcbde11daa6d22333a3c52d0675af060 |
| L2 全波次藍圖 | FHS_vNEXT_PLP_全波次藍圖.md | 2759509 | a6077aa208aa9cbcb2d37572e13be73de14125cd3f5881b3fa6320e34814c39b |
| Thin Prompt r1 | FHS_vNEXT_W0_HERMES_FHS_THIN_PROMPT_2026-11-13_r1.md | 14508 | 82d3def56bfd1f1df98d9489a42a0f65d22cded8387a4ab801d54e3a89f8021c |
| W0 baseline | FHS_vNEXT_W0_TRANSITION_BASELINE_AND_W1_ENTRY_20261112.md | 114616 | f1ee542923e3725b8d87040a2ba63f6dc0018a5d7c945a2674d706e13ff62237 |
| W0 As-Built | W0_AS_BUILT.md | 38379 | b6f1dbb61484ffbc52350119a91ac4b5fd6e597eb01a4bd4243c9232aa8b3102 |
| W0 SPEC r8 | FHS_PIPD-LS-PKG_W0_20261112_r8.md | 680998 | 42546311c3c62ae4c721403740ac675b748f3f66898157fca94c328af592ecc4 |

## B｜W0 gate 原始輸出

| gate | 結果 | Raw |
| --- | --- | --- |
| selfcheck | 15 PASS / 1 FAIL | out/SELFCHECK.txt |
|   └ FAIL | [FAIL] POS-02 — control/ seed is byte-identical to the spec-library origin | out/SELFCHECK.txt |
| gate_corpus | declared 31 / matched 31 / missing 0 | out/GATE_CORPUS.json |
| reregister_check | groups 41 / members 343 / PASS / 7.3s | out/REREGISTER.json |
| spec_identity | exit 0 (ok=true) | out/SPEC_IDENTITY.json |
| lane_pin --check | exit 0 | out/LANE_PIN.json |
| lane policy validate | exit 0 / CANDIDATE | out/LANE_POLICY.txt |
| POS-02b control pin | ok=True / 2 檔 / PASS_PIN_ONLY | out/POS02B.json |
| tree hygiene | exit 0 | out/TREE_HYGIENE.json |
| SourceFreeze candidate | 31 檔 / agg 1dacbb5e83f53525 / CANDIDATE_ONLY_AUTHORITY_READER_NOT_CALLED | out/SOURCEFREEZE_CANDIDATE.json |

### B.1 POS-02 的失敗脈絡（定位，不是內容）

`POS-02` 用 `SPEC_LIB_ROOT.rglob(檔名)` 定位 origin 再比位元。`SOURCE_IMPORT_MAP.json::control_seed` 宣佈的 `source_path` 是 `FHS_PIPD-LS-PKG/實作/FHS_NEXT/EXECUTION_CONTROL/…`，而 `實作/` 子樹在知識庫重組後已不存在（現有目錄：`FHS_NEXT_升級`、`FHS-MSC_PIPD-LS-PKG_BODY`、`PIPD-LS-PKG`、`藍圖`），深度 9 搜尋 0 命中。兩檔 on-disk bytes 仍等於 map 的 `target_sha256`，由 `ops/tools/pos02b_control_pin.py` 驗證為 `PASS_PIN_ONLY` / `source_absent=true`。判準更正候選：`out/POS02_LOCATOR_CANDIDATE.md`（待 owner 簽）。

## C｜W0 As-Built 全文（P0-01／P0-11 要求原文嵌入）

來源：`C:/Projects/Agent_Workspace/FHS_NEXT/_local/W0_AS_BUILT.md`　bytes=38379　lines=540　sha256=b6f1dbb61484ffbc52350119a91ac4b5fd6e597eb01a4bd4243c9232aa8b3102

```markdown
# FHS_NEXT W0 — As-Built, round r1 (runtime acceptance)

Round: **2026-11-11, 18:00–20:00 +08:00** · Host: Hermes Agent **v0.23.1 (2026.9.24) · stable · local `3b4215785882`**
Claim ceiling for this document: **`SOURCE_READ` + `HOST_RAW` + `DRAFT` + `LOCAL_CHECK`**.
No `NATIVE_SIGNED`, no `INDEPENDENT_PASS`, no `RELEASE_GRANTED` is claimed. The previous round's
As-Built is preserved byte-identically at `_local/history/W0_AS_BUILT_r0_20261111.md`
(sha256 `ba697fec…`); this file supersedes it as the current state, not as its erasure.

> **Three corrections to the previous round are recorded first, because a reader who trusted it
> would otherwise be misled.** See §3 (H8 withdrawn), §4 (POS-07 was checking the wrong rule), §5
> (433 is an entry count, not a file count).

---

## 0. Identity, and the profile question the round asked

`hermes profile list` measured this round:

| profile | model | gateway | distribution |
|---|---|---|---|
| `default` | deepseek-v4.1-flash | running | — |
| **`fhs_next`** ◆ | deepseek-v4.1-flash | running | `fhs_next@0.1.0` |
| `hgk-governed` | deepseek-v4.1-flash | running | — |

**`fhs_nest` does not exist.** Per the control package the round therefore used the existing
`fhs_next` and created nothing: no `profile install`, no overwrite, no rename. `HERMES_HOME` =
`…\profiles\fhs_next`; configured and actual cwd = `C:\Projects\Agent_Workspace\FHS_NEXT`.

Host facts, measured (`_local/W0_R1_HOST_READBACK.json`):

| item | value |
|---|---|
| code sha (git HEAD of the install) | `3b421578588243f920886e6fe79a6faa87ea026e` |
| launcher `bin/hermes` sha256 | `66cc8b51818047727732d2eeb2f064414ad2a4d9cb9b4f37fcd618840bcb249f` |
| desktop `Hermes.exe` sha256 | `2ed0bc899b58832bc6ad9becb81855cd0646143b66ac5c15850ce0c0ee8c9e6d` |
| desktop PIDs | 3860, 11352, 14764, 19260 |
| runtime interpreter | Python **3.14.9**, cache tag `cpython-314` |
| tool interpreter (pinned) | Python **3.11.9**, cache tag `cpython-311`, `…\cache\scratch\fhs_next\venv311` |
| tree is a git repo? | **no** (`git rev-parse` fails) — as designed, W1 creates the repo |
| r26 baseline | 668,540 B, sha256 `0ea05544…3e0f` — **matches the pin**, recomputed |

**Skill plane, kept as three separate facts** (Installed ≠ Loaded ≠ Invoked ≠ Served):
origin `…\profiles\fhs_next\skills\fhs\SKILL.md` sha256 `eff4c7cc…e7b` · **Loaded**: `skill_view`
returned it in this session · **Invoked**: its documented runner `ops/selfcheck.py` was executed
(exit 0, 16/16) · **Served**: not a skill property; the *model* serving is §2.

---

## 1. V0 — tree, import map, and the "480 → 433" difference

`ops/r1_tree_hygiene.py` + `_local/W0_V0_TREE_READBACK.json`, both measured now:

| measurement | result |
|---|---|
| import-map entries | **433** (`provenance/SOURCE_IMPORT_MAP.json`, sha256 `1bae7892…4253`) |
| **distinct** target paths | **423** — 10 Fabric paths are listed twice |
| bytes as entry-sum | 3,787,417 |
| **bytes distinct** | **3,713,290** (74,127 B double-counted by the duplicates) |
| entries whose `target_sha256` matches the file on disk | **433 / 433** |
| entries whose `source_sha256 == target_sha256` | **433 / 433** |
| forbidden-class hits, after residue removal | **0 / 425 files** |
| exact set (tree − declared − allowed local) | **CLEAN**: 542 files, 423 declared, 0 extras, 0 missing |

**Residue found and removed (my own, not origin bytes):** executing the imported tools wrote
`__pycache__/*.pyc` into 8 directories of the imported trees plus one `.pytest_cache` (137 files);
they were never in the map and their mtimes are after the map's `generated_utc`. Removing them
restores the tree to its imported byte set. The scan that found them is the evidence that the scan
runs at all (26 bytecode hits + 1 filename-only hit, `SBL/integrations/pipd/tests/test_secret_patterns.py`,
classified `FILENAME_PATTERN_ONLY`).

**"480 → 433" — traced to a superseded map revision, not to a missing file set.** The figure is
real and it is quoted *inside the first FUO*: `_local/W0_FIRST_FUO/{pi,intent.card,bundle3}.json`
carry acceptance predicates `MUST: "files": 480` and `MUST: "bytes": 8970300`, and
`_local/W0_FIRST_FUO/MANIFEST.json` records `source_sha256: 669670593fbbbe7f…` — a manifest revision
that is **not** the current one (`1bae7892…`, 433 entries). So 480 was a *earlier map revision*
(480 files / 8,970,300 B) that the FUO was compiled against; the map was then rewritten to the
433-entry form at 16:13, after the FUO was built at 16:09. Two alternative hypotheses were tested and
rejected by measurement: dropping the evidence-prefix exclusion yields 551 files / 14,321,918 B, and
no directory in the clones holds 47 files / 5,182,883 B. The **itemised** filename-set difference
still cannot be produced — that revision is nowhere on disk (only one `SOURCE_IMPORT_MAP*.json`
exists on the host) — so this is recorded as `SUPERSEDED_REVISION_NOT_RETAINED`, with the count
delta (47) and the artefact that remembers it.

Consequence recorded as **H15**: the first FUO now asserts a MUST against a manifest revision that no
longer exists, so it is internally inconsistent with the current map. It must be recompiled against
`1bae7892…` or marked as bound to the superseded revision before anyone cites it.

**Arithmetic note (a subagent's figure corrected here).** One delegated readback reported
`double_counted_bytes = 148,254` and `distinct_bytes = 3,639,163`. Both subtract the duplicated bytes
**twice**: the ten duplicated paths contribute one redundant copy each, totalling 74,127 B, so
`3,787,417 − 74,127 = 3,713,290` is the distinct total, which `ops/r1_tree_hygiene.py` recomputes
directly from the files.

---

## 2. V3 — FHS-3L&M: the built stack, used as built

The stack was **used, not rebuilt**: `ops/tools/fhs_3lm.py` is the imported R13 tool
(sha256 `0c5fc663…`), run through `ops/tools/fhs_3lm_pathadapter.py`, which re-points its four path
globals at this tree and changes nothing else. Its contract (`FHS_W0_R13_ACCEPTANCE_20261108/out/FHS_3LM_CONTRACT.json`)
is the one honoured here: *menu → bind → assert*, the binding record is the only lane declaration,
`sod.mandated: false` (a shared arm is **recorded**, not refused by the contract), `retired_arms`
read from the control plane, exit codes 6/7/8/9.

### 2.1 Two planes, demonstrated rather than asserted

| plane | surface | measured value at the same moment |
|---|---|---|
| **conversation / session pin** | desktop picker, `state.db::sessions.model` | `deepseek-v4.1-flash` via `opencode-go` (host billing rows, real token counts) |
| **lane control plane** | `ops/lanes/bindings/*.json` + epoch digest | `PLAN/primary` = **`openai-codex/gpt-6.1-sol`**, `pool_rank 1`, epoch sha `811bf1a5…` |

The session stayed on DeepSeek while the PLAN lane was bound to GPT-6.1-SOL. Neither value is
derived from the other, and `--assert` reads only the binding record. This is the distinction the
round demanded: **a session pin is not a lane binding.**

Six bindings written and all re-assert clean at epoch 41:
`PLAN/{primary,opt1,opt2}`, `EXECUTE/primary`, `VERIFY/{primary,opt1}`.

### 2.2 Per-lane Requested → Selected → Dispatch → Usage → ActualServed

| lane | engine | requested (slot) | served arm (readback) | receipt |
|---|---|---|---|---|
| **PLAN** | hermes (in-session commander) | `PLAN/opt1` = deepseek-v4.1-flash | `deepseek-v4.1-flash` / `opencode-go` — host `session_model_usage` + a direct relay turn (HTTP 200, nonce echoed, usage 50/23) | `_local/lane_probes/plan_direct_probe.json` |
| **EXECUTE** | **Codex CLI** (`codex 0.167.0-alpha.3.2`) | `EXECUTE/primary` = deepseek-v4.1-flash | `opencode-go/deepseek-v4.1-flash`, `ok=true`, `usage_receipt_ok=true`, nonce echoed, 8.15 s | `_local/lane_runs/smoke/exc.json` |
| **VERIFY/SECURITY** | **Codex CLI** | `VERIFY/primary` = gpt-6.1-sol | `openai-codex/gpt-6.1-sol`, `ok=true`, `usage_receipt_ok=true`, nonce echoed, 127 s, frozen subject unchanged | `_local/lane_runs/verify5/ver.json` |

The owner mandate for this round was **all three lanes on OPENCODE GO / DEEPSEEK V4.1 FLASH**. That
mandate is *bound* (the binding records exist) but it cannot be *dispatched*: the guard refuses a
same-model maker/checker pair, measured exit **2** `ERR_LANE_SOD_VIOLATION`. The checker turn
therefore ran on the in-force `VERIFY` rank-1 arm. The deviation is recorded here rather than
hidden, and it is the owner's call whether to relax the guard or keep the separation.

### 2.3 Refusals, each from its own tool

| # | probe | exit | meaning |
|---|---|---|---|
| 1 | `fhs_3lm --assert-arm opencode-go/mimo-v2.6-pro` (live epoch 41) | **9** | `RETIRED_ARM`, replacement named |
| 2 | same probe, published epoch-33 copy | **0** | **admitted** — the divergence is real, and it is in the published repo |
| 3 | `lane_arm_retirement_check.py`, live trio | 0 | `PASS`, `retired_still_live: []` |
| 4 | same, with the retired arm injected into a live pool | **4** | the checker bites; #3 is therefore not vacuous |
| 5 | `hgk-lane-guard.py` same-model maker/checker | **2** | `ERR_LANE_SOD_VIOLATION` |
| 6 | `hgk-lane-guard.py --expected-epoch 33` | **4** | `ERR_LANE_STALE_EPOCH` (`live_epoch=35`) |
| 7 | dispatch of a live-epoch arm with the published pool | — | `ERR_LANE_REQUIRED_ARM_ABSENT`, then `ERR_ARM_NOT_IN_ASSIGNMENT` (see H10) |
| 8 | relay probe of the **retired** arm | **HTTP 200** | retirement is enforced at selection, **not** at transport (see H14) |

### 2.4 The GLM arms are not in the design, and not used

`FHS_PIPD-LS-PKG_W0_r26.md` contains **zero** occurrences of "glm" (measured: `grep -c -i glm` → 0),
so the governing design names no GLM arm. The live epoch-41 pool nonetheless still carries
`opencode-go/glm-5.3-flash` at PLAN rank 3 and VERIFY rank 4 — legacy drift between the spec and the
registry, owned by HG-KSEOS (H14), not repaired here. **No GLM arm was bound or dispatched this
round**: an attempt with `glm-5.3-flash` was refused `ERR_ARM_NOT_IN_ASSIGNMENT` before any spawn,
and the intended checker ran on `gpt-6.1-sol`.

---

## 3. Correction — H8 is withdrawn (the r26 mirror mismatch was a checkout artefact)

The previous round reported that `…/r26/GATE_R26.json` hashed to `231e2ac7…` while `SHA256SUMS` pins
`b9e7c2fc…`. Re-measured through the GitHub contents API:

| ref | bytes | sha256 |
|---|---|---|
| `a6f1fa89…` (the imported commit) | 6438 | `b9e7c2fc…` |
| `main` (today) | 6438 | `b9e7c2fc…` |

The stored blob **matches** its inventory. `231e2ac7…` is the same file after Windows
`core.autocrlf` expansion in a working tree: 6649 B with **211 CRLF**, and normalising `CRLF → LF`
reproduces the blob byte-for-byte (`n == gh` → True). The finding was produced by the measuring
environment.

Consequence: the 5 failures + 5 errors in the Fabric suite (51 tests, 41 pass, measured this round)
are `test_manifest_admission` reading a payload W0 deliberately did not import — **not** an upstream
defect. Fabric PR #56 carried the wrong finding; a correction commit (`b0431cd`) and a comment were
added to it; the PR is left open and unmerged for its receiver to close.

---

## 4. V2 — three SPs, and the POS-07 defect the round named

The previous oracle compared each SPEC's `Subject` row and passed when the three **subjects
differed**. That inverts the contract: three SPs are supposed to share one Goal/SubjectRef/Scope, and
differ in *what they produce*. The oracle was wrong even though it printed PASS.

Fixed in both places:

- The three files now carry an identical front-matter block — `Goal`, `SubjectRef`
  (`FHS-NEXT.W0.SUBJECT/1#sha256=1bae7892…`), `Scope` (`W0_SOURCE_BOUND`), `SourceManifestSHA`
  (`1bae7892…4253`) — and differ on `Artifact`, `OriginalConsumer`, `ACC`, and body bytes.
- A dedicated oracle `ops/tools/spec_identity_check.py` (written by the **EXECUTE lane**, 14.8 KB)
  implements the rule once. Its five self-controls fire (10 shared-drift, 11 artifact-collision,
  13 missing-field, 12 duplicate-body, 14 manifest-mismatch → `SELFTEST PASS`), the real directory
  returns exit **0** / `ok: true`, and a wrong manifest returns exit **14** with the declared-vs-actual
  digests. `ops/selfcheck.py` POS-07 now delegates to that oracle, so there is no second
  implementation to drift.

Independent corroboration (different tool, different lane): the VERIFY turn re-derived the same
invariants with PowerShell `Get-FileHash` / `Select-String` — `Goal`, `SubjectRef`, `Scope`,
`SourceManifestSHA` character-identical; `Artifact`, `OriginalConsumer` pairwise distinct; the
declared digest equal to the computed one. Its verdict on *execution* is **FAIL** for an honest
reason: the read-only checker sandbox cannot read the Python base install (`No Python at
…\Python311\python.exe`), so `--self-test` could not run there. That is H12, not a checker defect —
and it is reported as FAIL rather than smoothed into a pass.

**First FUO** (unchanged, re-verified): PI `PI-247c5d6c4fd9791b`, PD `PD-829e0f720f0ccf84`,
ECP `ECP-cb1a300f689e9ffd`, `validate` → `PASS checked 3 missing [TQAEP]`; `compile-tqaep` refuses
`TQ_SOD` (exit 2) — a maker still cannot attest its own independence.

---

## 5. V1 — six work packages, re-judged against r26's own words

> **Scope correction (added after a deep read of the R13 acceptance folder).** W0 *was* closed on
> 2026-11-09, and this table must be read against **that** closure, not against the full r26 WP text.
> `FHS_W0_R13_ACCEPTANCE_20261108/out/ACCEPTANCE_FINAL.json` records
> `completion_level: W0_AUTHOR_DESIGN_COMPLETE`, an owner semantic ACK `SIGNED_AND_VERIFIED`
> (ed25519, fingerprint `412b351937be72a1`, window `WIN-df9526589010` closed, verified by
> VERIFY/gpt-6.1-sol), gate `18/19 PASS, 0 blocking`, payload `13/13 PASS`;
> `CLOSEOUT_R26.json` claims `PUBLISHED / MERGED / LANE_REVIEWED` (SBL `1cb8abb0…`, Fabric `3b47570e…`);
> `GATE_R26.json` is `21 PASS / 0 blocking / 1 OPEN` (G16b `UNQUALIFIED_INCOMPLETE_SCAN`) on a
> `scope: full` run whose own `not_claimed` already lists `ORIGINAL_ACK`, `NATIVE_WORLDRAW`,
> `RELEASE_GRANTED`, `INDEPENDENT_PASS`.
> That closure **itself** assigns `EC-R24-009`: *"U0-U4, 96 Oracle and native world effects are W1-W4"*,
> and leaves `LICENCE`, `PIPD-15-VALUESET`, `R1-ISSUER-REV14`, principal separation and G16b open.
> So a `HOLD` below means **"W1–W4, per the W0 closeout"** — not "W0 was left undone". The earlier
> framing of this section implied the latter and is corrected here.

`_local/W0_V1_WP_RECHECK.json` / `.md` quotes the r26 passage for each WP and judges the actual
files. Three states moved **down**, which is the point of a second pass:

| WP | r26 asks for | state now | why it moved |
|---|---|---|---|
| WP-FHS-00 | source/currentness: the **31-volume physical manifest** (r26 L419–L449) with sha | **OBSERVED** | the r26 predicate is the 31 volumes, not the 433-file code ledger; all **31/31 are present and sha-exact** under the read-only root, independently re-verified here (`_local/W0_V1_PROBE_SRC31.json`) |
| WP-FHS-01 | U0–U4 / Parent / NEG register | **DRAFT** | AuthorityConflictLedger / QuestionLedger / ProfileBinding do not exist (`pi.json.profile_binding: null`); only a 5-row U0–U4 register |
| WP-FHS-15 | three substantively different SPs | **DRAFT** | 3 byte-distinct drafts, 7/7 cited `SourceSHA` verified, but **0** "Stage" mentions (18 Stage contracts absent) and the FUO is one row, not ten fields |
| WP-FHS-16 | 485 slots Qualified/NoFit | **HOLD** | **reason corrected**: the sources are *not* missing — `FHS-BODY-08` (`1df04680…`, the 485-item roster) and `SBL-DOC-06` (`64ea4977…`) hash-match and are on disk. The block is **production**, not availability |
| WP-FHS-19 | CI/License/NOTICE/SBOM | **HOLD** | r26 L1761/L1772 forbid a Spec standing in for the scan Raw; no CandidateSHA-bound Raw and no CI at all — two repos ship **no** licence file (exit 2 confirmed) |
| WP-FHS-21 | trace + five seams | **HOLD** | declared output is a 96-case plan; nothing carries `case_id` / `CasePlan` / `ExpectedEvidence` — SPEC-C §2 is a trace diagram |

22 WPs / 36 DAG nodes / OriginalID are untouched; no historical payload was imported.

---

## 6. V4 — capability register (what actually runs here)

`_local/W0_CAPABILITY_READBACK.md` + `_local/W0_CAPABILITY_REGISTER.json`: **57 rows** —
**44 PASS / 3 HOLD / 10 N/A_WITH_REASON / 0 NOT_RUN**, each row carrying
`ManualRef → Command/Host/Effect → PrimaryWave → ActualLocator(+sha256) → POS probe(exit) → NEG or
reason → Status`. Coverage: PIPD 13 verbs (13), 19 contract families + 8 `pipd-*` skills (27),
Fabric entry (4), FAR R0–R2 (4, all `N/A_WITH_REASON` — not in this tree), FDA (3), B1 (4), Hermes
direct/skill (2). A `PASS` there means *read-only probe behaved as documented at that scope*; it is
not a write-path or full-functionality claim.

Three findings from that register that change what W1 can assume:

- `compile-pi` reproduces the origin README pin byte-for-byte (`9cc0c1b1…`) and `intake` reproduces
  `f5a44e27…`; the chain `intake → compile-pi → bind-pd → compile-ecp` runs, and `compile-tqaep`
  still refuses `TQ_SOD`.
- `bind-pd` only binds against the read-only origin SBL clone; the W0 tree is not git, so an in-tree
  `--repo-root` is refused `REPO_CONTEXT_MISSING` — a W1 task, not a defect.
- the W0 FUO intent card **no longer recompiles** (`PI_SEMANTIC` collapse) because it carries compiled
  atoms rather than intake input — the same artefact as H15, seen from the compiler's side. Also:
  `export --dry-run` digests vary by design (`generated_at`), so they must never be used as a pin.

---

## 7. V5 — faults, classified, and the minimum repaired

Measured this round (not carried over): HGK suite **171 failed / 555 passed / 22 skipped / 4 xfailed
/ 17 errors** over 765 items, plus 10 module-level collection errors. 153 exception events classified
(`_local/W0_R1_V5_FAULT_CLASSES.json`, `ops/r1_fault_classify.py`):

| class | events | owner of the next action |
|---|---|---|
| `HISTORICAL_FIXTURE_EXCLUDED` | **123** | policy — evidence packs are not imported; re-run in the origin repo |
| `REAL_DEFECT` (assertion-level) | **16** | the owning repo; listed verbatim, none repaired here |
| `PATH_ABI` | **13** | this root / the host — e.g. `scripts/start-hgk-hermes.ps1` is not in the import |
| `ORIGINAL_OWNER_HOLD` | **1** | `ERR_NATIVE_BUNDLE_REQUIRED` — the issuer |

Repaired in this round, and nothing else: `__pycache__`/`.pytest_cache` residue (137 files, §1), the
POS-07 oracle (§4), and `ops/selfcheck.py` POS-07 delegation. No guard was disabled, no test was
skipped to make a colour, no fixture was invented. Same-first-fail retries stayed within the budget.

---

## 8. V6 — acceptance readback (POS / NEG, real exits)

`_local/W0_R1_TEST_READBACK.json`: **23 checks — 12 POS + 11 NEG — 23 pass, 0 fail**, each with
command, cwd, exit code, raw sha256 and head. Selected:

| id | check | exit |
|---|---|---|
| POS-01 | the 16-check self-check re-runs green | 0 |
| POS-02 | three SPs share the four identity fields, differ pairwise | 0 |
| POS-03 | the SPEC oracle's own five controls fire | 0 |
| POS-04/05/06 | bindings: deepseek under epoch 41 · gpt-6.1-sol while the session stays deepseek · all six re-assert | 0 |
| POS-09 | live GitHub `main` is still epoch 33, no retirement ledger | 0 |
| POS-10/11 | Codex lanes really served (`deepseek` / `gpt-6.1-sol`), usage receipts OK | 0 |
| NEG-01/02 | retired arm: exit 9 live **and** exit 0 published | 9 / 0 |
| NEG-04 | wrong manifest → SPEC oracle exit 14 | 14 |
| NEG-05/06 | guard: SoD exit 2, stale epoch exit 4 | 2 / 4 |
| NEG-07 | retirement checker exit 4 on the injected arm | 4 |
| NEG-08 | unknown task class → `HOLD_AFFECTED_WRITE` | 3 |
| NEG-10 | no positive `NATIVE_SIGNED`/`INDEPENDENT_PASS`/`RELEASE_GRANTED` in `_local/*.md` | 0 (`[]`) |
| NEG-11 | the non-mutation guard **voided** the writer receipt when the frozen subject changed mid-run | recorded, not synthetic |

NEG-11 is worth stating plainly: my own concurrent edit of `_local/W0_SPEC` invalidated the first
EXECUTE writer receipt (`ERR_CHECKER_MUTATED_SUBJECT`, `changed=3`). The guard caught a real
mutation; the receipt is kept as evidence that the guard bites, and the artefact was re-verified
afterwards by a clean VERIFY turn.

---

## 9. Owner authorisation — assessed, and **not** opened

The round required an assessment first. The instrument exists and was read:
`…\FHS\HG-KSEOS\ops\session-20261031\tools\owner_window.py` (tkinter prompt, `OwnerSigningWindow@1`,
effect ceiling `REPOSITORY_WRITE`, `FORBIDDEN_KINDS` including `release`/`sourcefreeze`/
`policy_authority`/`trust_anchor`/`owner_enrollment`). State measured: last window
`WIN-48977f9c3c57`, `state: OPEN`, `remaining_s: -30145`, `usable: false` — **expired, no live broker,
no port 2395**.

**Assessment: W0 r1 has no owner-key effect in scope** — no new ACK, no re-sign, no native issuance,
no release, no registry row signature. The control package also says the retired per-domain manual
ACK must not open a new owner window. So **no window was opened** and none was needed to finish:
`OWNER_WINDOW: NOT_OPENED / N_A_WITH_REASON`. GitHub writes used the owner-provided token, not the
owner key. If a genuine owner-gated effect appears, the command is
`python owner_window.py open --task <id> --ttl-hours <h> --max-ops <n>` — the passphrase is typed by
the owner in that window and never by an agent.

---

## 10. Fabric-first GitHub handover (what actually happened)

Token: read from `…\API KEY\GITHUB-REPO_SHW097-4.txt` by `ops/tools/ghsafe.py`, used only as an
in-memory `Authorization` header — never printed, never in argv, never in a URL, a log, a commit or
this document. Identity read back: `shw097`, `permissions` on Fabric = admin/maintain/push/triage/pull.

Fabric entry read **live from `main`** first: `INTEGRATION/FHS/README.md` (NAVIGATION_ONLY, L1
assisted use approved, `effect_permission: NONE`, unknown → HOLD the affected write) and
`repository-map.json` (`FHS-NAV/v2`, `source_state: PROPOSED_NOT_OWNER_RATIFIED`; note its sha is now
`c668fff4…`, not the `373120f5…` that was imported — main moved).

| PR | repo / branch | head | shape | state | CI as measured |
|---|---|---|---|---|---|
| [#19](https://github.com/shw097-team/HG-KSEOS/pull/19) | `HG-KSEOS` / `docs/fhs-w0-lane-routing-drift-20261111` | `dc1f028e` | 2 files, +179 | open, `mergeable: clean`, unmerged | `total_count 0` — **no check-runs configured** |
| [#56](https://github.com/shw097-team/Fabric/pull/56) | `Fabric` / `docs/fhs-w0-r26-mirror-digest-20261111` | `b0431cd` | 2 files, +133 | open, `mergeable: clean`, unmerged | 1 job `fhs-nav-static` → success (**one job**, not origin CI) |

Both received a measured note and a comment; neither is merged, neither touches `main`, neither
carries raw evidence, keys or history. HGK #19's branch advanced while this round ran
(`8495b0ab` → `dc1f028e`), so the earlier "head" recorded in the r0 As-Built is already history.

---

## 11. HOLD ledger (fail closed only on the affected effect)

| id | item | OriginalOwner | AffectedScope | FirstFail (measured) | ResumePredicate |
|---|---|---|---|---|---|
| H1 | published `main` is epoch 33 with no retirement ledger; live is 41 | HG-KSEOS owner | `config/lane-*`, assignment | `--assert-arm …pro` → 0 on main, 9 live | owner orders an epoch change (PR #19 documents it) |
| H2 | native admission / any protected HGK effect | HGK Native Issuer | native bundle, permits | `ERR_NATIVE_BUNDLE_REQUIRED` | issuer supplies bundle + permit |
| H3 | TQAEP closure | independent checker | checksum chain | `TQ_SOD` | checker execution receipt |
| H4 | WP-FHS-16 (485 slots) | original source owner | 31 source volumes | volumes absent from every import set | volumes delivered |
| H5 | publishing the assembled tree | owner / W1 | new `shw097-team/FHS` | no receiver repo exists | W1 authorises repo, then branch PR |
| H6 | owner-key signing window | Owner | signing capability | last window expired (`-30145 s`) | owner opens a window when a ceremony is scheduled |
| H7 | PLAN lane provider readback | host provider | `ACTUAL_SERVED` for PLAN | **partially closed**: EXECUTE and VERIFY have lane receipts; PLAN is proven by host billing rows + a direct relay turn, not by a lane receipt | run a PLAN lane dispatch on an arm the assignment admits |
| H8 | ~~r26 mirror digest mismatch~~ | — | — | **WITHDRAWN** — blob matches `SHA256SUMS`; CRLF artefact (§3) | closed |
| H9 | Codex toolchain pin no longer resolves | HG-KSEOS owner | `config/hermes-codex-lane.json` | `ERR_LANE_TOOLCHAIN_BINARY_MISSING` exit 3 (pin `0.165.0-alpha.1.2`; installed `0.167.0-alpha.3.2`) | owner refreshes the pin (documented repair pattern) |
| H10 | dispatcher assignment gate reads the **published** copy only | HG-KSEOS owner | `hgk-lane-dispatch.py` `ASSIGNMENT_FILE` | `ERR_ARM_NOT_IN_ASSIGNMENT` for a live-epoch arm | refresh `config/model-lane-assignment.json` or make the path epoch-aware |
| H11 | `VERIFY_SECURITY` row's stale `transport_model` admits the writer arm | HG-KSEOS owner | assignment row, SoD surface | guard exit 2 is the only thing refusing it | correct the row so the declaration cannot offer the writer's arm |
| H12 | the read-only checker lane cannot execute a Python interpreter | HG-KSEOS / FAR | checker sandbox read scope | `No Python at …\Python311\python.exe` inside the lane | grant the checker read access to the interpreter, or run execution checks in a scoped exec lane |
| H13 | import map counts entries, not files (10 duplicate paths) | this construction root | `provenance/SOURCE_IMPORT_MAP.json` | 433 entries / 423 distinct / 74,127 B double-counted | **recorded and corrected in the readback**; map itself left byte-stable, correction written beside it |
| H14 | the relay catalog still lists the retired arm, and serves it | HGK / relay config | `opencodex-hermes/config.json` `selectedModels`; registry GLM residue | retired arm → HTTP 200; `glm-5.3-flash` still in the epoch-41 pool while r26 names none | owner prunes the relay catalog and the registry pools |
| H15 | the first FUO asserts MUSTs against a map revision that no longer exists | this construction root | `_local/W0_FIRST_FUO/**` | PI carries `MUST: "files": 480` / `MUST: "bytes": 8970300`; MANIFEST `source_sha256: 66967059…` ≠ current `1bae7892…`; `intake` on it now refuses `PI_SEMANTIC` | recompile the FUO against `1bae7892…`, or mark it explicitly as bound to the superseded revision |

---

## 12. What this round did not do

Did not rebuild the P0–P6 tree, rename or delete the old `FHS` root, create `shw097-team/FHS`, touch
`hgk-governed` or any protected HGK state/key/DB/ReaderMap, merge or force-push, re-sign or re-issue
`FHS_ORIGINAL_ACK`, import an evidence pack, or claim native/independent/release status. Did not open
an owner window (§9). Did not relax a guard to reach a green number; where a check could not run, it
says so (H12).

**Files this round produced** (all local, none imported, none published except the two review notes):
`ops/r1_host_readback.py`, `ops/r1_lane_readback.py`, `ops/r1_test_readback.py`,
`ops/r1_fault_classify.py`, `ops/r1_tree_hygiene.py`, `ops/tools/ghsafe.py`,
`ops/tools/spec_identity_check.py` (EXECUTE lane), and the `_local/W0_R1_*` readbacks.

---

# Round r2 — the three open items, executed

## r2.1 R13 acceptance gate: re-run, and it does **not** reproduce 21/22 today

`tools/gate_r20.py` was executed **in place** against the R13 round (no copy, no edit):

| run | command | result |
|---|---|---|
| gate selftest | `--round . --selftest` | every mutation **FIRED** (G10…G29), i.e. the gate bites |
| gate full, no sources | `--round . --json out/_GATE_RERUN_R3.json` | 17/22 PASS, 3 blocking fail, 1 reporting open |
| gate full, **31-doc corpus view passed in** | `--sources <view> --json out/_GATE_RERUN_R4_sources.json` | 18/22 PASS, 2 blocking fail, 1 reporting open |
| gate full, **corpus view + the 26 archived roots restored as junctions** | `--sources <view> --json out/_GATE_RERUN_R5_roots.json` | **19/22 PASS, 1 blocking fail, 2 reporting open** |

**Root restore (found in the archive, not invented).** `G:\Projects\封存\FHS_封存_20261110_已分類可封存`
holds the deleted roots: `worktrees
4-hgk` (with its `pyproject.toml`), the other 16 worktrees, six round
directories (`FHS_W0W2_R4_20261107`, `FHS_W0_R6/R7/R9/R10_ACCEPT/R10_REPAIR_20261108`) and
`FHS_W1_Work_Final\FHS_W1_Work_Final\sources` (= `sources_31`). `ops/tools/restore_roots.py` linked 26 of
the 27 declared paths (the 27th is a relative `evidence` path the gate resolves against the round). Junctions,
not copies: no archive byte is touched and the restore is reversible by deleting the link. With the paths
back, **G16a passes by real re-derivation** (the artifact's per-subject dependency verdict now equals the
gate's own), G16b moved from ABSENT to OPEN, and G19 moved from `ROOT_ABSENT` (24/25) to
`MEMBER_ABSENT` (308/437). The 308 absent members are all under the old `知識庫/實作相關DOC/Fabric vNext/…` layout. That tree still
exists, reorganised, one level deeper (`…/FHS／FHS-MSC／SBL/Fabric/Fabric vNext`), and a digest scan of
all 8,105 files under `…/FHS／FHS-MSC／SBL` found **302 of the 308 members (103 of 106 distinct contents)
byte-identical**, living now under `FHS\FHS-MSC` (255), `Fabric\Fabric vNext` (43) and
`FHS\FHS_PIPD-LS-PKG` (4). Only **6 members / 3 distinct contents** are genuinely gone:
`FHS_PIPD-LS-PKG_W0_r4.md`, `FHS_PIPD-LS-PKG_W0_r6.md` and the `…HIGH_RETENTION…非規範性審計證據附錄.md`
appendix. So G19's red is **path drift, not data loss** — and it still fails, correctly, because it asks
whether the copy sits at its declared path. Mapping: `_local/W0_R2_G19_PATH_MAP.json`.

**G11 + G13 recovered.** The gate re-hashes the round's own declared 31 documents
(`lanes/A/SOURCE_LOCK_V3.json`, each with `file` + `declared.sha256`); those 31 files exist on this
host but split across **two** directories under different names (14 + 17). `ops/tools/gate_corpus.py`
builds a corpus view by matching **declared sha256 only** — 31/31 matched, 0 substituted — and the gate
then re-derives the line/byte totals from the documents themselves instead of trusting the artefact.

The two remaining blocking fails are absent inputs, not logic:

| check | why it cannot pass here |
|---|---|
| G16a/G16b `DEPENDENCY_*` | needs `…\Agent_Workspace\worktrees\r4-hgk\pyproject.toml`; no `r4-hgk` worktree exists anywhere on the host |
| G19 `COPY_REGISTER` | 24 of the 25 declared copy roots (`FHS_W0W2_R4_20261107`, `FHS_W0_R6_20261108`, …) have been deleted |
| G22 (OPEN) | a *consequence*: it reports the red rows above, documented=0 actual=1 |

So the honest statement is: **the R13 gate is re-runnable and its 21/22 verdict is not reproducible today — the delta is three deleted/moved input trees, and I could not manufacture them without importing history.** The gate's own `claim_ceiling` stays `GATE_VERDICT_NOT_ACCEPTANCE`.

## r2.2 Codex pin: refreshed per the R18 pattern, origin bytes untouched

`ops/tools/lane_pin.py` resolves the effective pin (overlay first, origin otherwise) and verifies the
binary against its own sha256 before any dispatch.

| | before | after |
|---|---|---|
| declaration | `HG-KSEOS/config/hermes-codex-lane.json` (origin) | `HG-KSEOS/config.live/hermes-codex-lane.live.json` (overlay) |
| path | `…\OpenAI\Codex\bin\0ab0e7a8f3779036\codex.exe` | `…\OpenAI\Codex\bin\5449c1f0f26f1f98\codex.exe` |
| version | 0.165.0-alpha.1.2 | **0.167.0-alpha.3.2** |
| binary exists | **false** | true |
| digest match | — | **true** (`4f91ae86…`) |
| sidecars (4-file layout) | — | **complete** |
| `lane_pin --check` exit | **3** | **0** |

Receipt: `provenance/PIN_REFRESH_R18_STYLE.json` (from/to, sidecars, rollback, and
`origin_declaration_sha256: ba357dcc…` so the untouched origin bytes are provable). Rollback = delete
the overlay.

## r2.3 Locator repair: 171 → 83 failures, measured one repair at a time

| step | repair | failed | passed |
|---|---|---|---|
| r1 | (baseline) | **171** | 555 |
| r2 | junction `C:\Projects\Agent_Workspace\HG-KSEOS` → `FHS\HG-KSEOS` (104 events pointed at the pre-move root) | **120** | 606 |
| r3 | junction `FHS_NEXT\TEST_RESULTS` → scratch (tests create temp dirs there) | **95** | 631 |
| r4 | junction `FHS_NEXT\PIPD` → read-only `FHS\SBL\PIPD\pipd-ls-sp` (50 events wanted `PIPD\skills\…\cases.yaml`) + addendum import of 3 worktree-only source files | **83** | **644** |

Errors 17 → 16, skipped/xfailed unchanged. **No imported origin file was edited** — and one mistake is
recorded rather than hidden: the addendum first included `HG-KSEOS/config/hermes.json`, which *was*
already a mapped entry, so it overwrote origin bytes. That was detected by POS-01, restored from the
import clone (`dde26bb4…`), and the addendum now refuses mapped paths
(`provenance/SOURCE_IMPORT_ADDENDUM.json` → `withdrawn`).

## r2.4 Fresh evidence, generated here

`ops/tools/evidence_producers.py` (written by the **EXECUTE lane**; attribution closed) runs the in-tree
producers and stamps every artefact `generated_this_round: true`:

| turn | receipt | result |
|---|---|---|
| attempt B | `execute_producers2/exc.json` | file written, but `ERR_NO_ARM_EMITTED_NONCE` — the turn is refused as an attribution |
| attempt C | `execute_producers3/exc.json` | **ok=true**, `served_arm == required_arm == opencode-go/deepseek-v4.1-flash`, usage receipt OK, **nonce present**, 243 s |

So authorship is now proven by a served turn, and the earlier refusal is kept beside it
(`_local/W0_R2_ARTIFACT_PROVENANCE.json` → `AUTHORSHIP_PROVEN_AFTER_RERUN`, with the
`ERR_NO_ARM_EMITTED_NONCE` record retained). Self-test PASS (7 controls) before and after the re-write.
`_local/evidence_generated/MANIFEST.json` → `lane_pin` exit 0, `spec_identity` exit 0, `selfcheck`
exit 0. Non-regenerable classes stay `N/A_WITH_REASON` (the classifier refuses to call a class
regenerable when no registered producer emits it). Known defect, stated: `--list` still writes
`HG-KSEOS/var/…/evidence_producers_list.txt`; the residue was removed and the defect recorded.

## r2.5 Lane planes, second pass (owner mandate: all three lanes DeepSeek)

| lane | receipt | served |
|---|---|---|
| EXECUTE | `_local/lane_runs/smoke/exc.json` | `opencode-go/deepseek-v4.1-flash`, ok, usage OK, nonce OK |
| VERIFY | `_local/lane_runs/verify_ds2/ver.json` | **`opencode-go/deepseek-v4.1-flash`**, ok, usage OK, nonce OK |
| PLAN | host `session_model_usage` + direct relay turn | `deepseek-v4.1-flash` / `opencode-go` |

The mandated checker model is therefore **served**. What that exposed: the dispatcher enforces SoD only
when the caller declares the maker — `hgk-lane-guard.py --maker-model …` refuses the same-model pair
with exit 2, but a dispatch that declares no maker runs the writer's model as the checker with no
refusal. Recorded as `SOD_UNDECLARED_MAKER` (H16), alongside the earlier `transport_model` finding
(H11). Two earlier attempts failed honestly and are kept: `ERR_LANE_ALL_ROUTES_EXHAUSTED` while the
relay was down, `ERR_ARM_NOT_IN_ASSIGNMENT` for arms the published assignment does not carry.


---

# Round r3 — the owner's ruling on G19, applied

**Owner decision (2026-11-12, in-session).** Two decisions, recorded verbatim in
`_local/rounds/W0_R2_REREG_20261112/ROUND_DECLARATION.json`:

- **OD-1** — the documents that could not be found were deleted **by the owner personally, to free local disk
  space**. They are historical records and must not be a blocking item.
- **OD-2** — the layout change is the owner's own optimisation, not drift. The register must be adapted to it
  and re-declared with a new denominator and new digests.

Applied, not merely acknowledged:

| step | artefact | result |
|---|---|---|
| re-declared the register over the current layout | `…/COPY_REGISTER_CURRENT.json` | **73 groups / 431 copies** (old: 90 entries by name-case, 437 copies) |
| verified every declared member by re-reading it | `ops/tools/reregister_check.py` → `G19_REREG_CHECK.json` | **431/431 re-read, V1–V5 all zero, PASS** (15.5 s) |
| recorded the three owner-deleted subjects | `owner_deleted_groups` in the register | `W0_r4`, `W0_r7`, `…HIGH_RETENTION…附錄`, each `OWNER_DELETED_20261112` |
| recorded the ruling and its limits | `…/OWNER_WAIVER_G19.md` | what it waives, and what it does not |

What it does **not** do — stated so the record cannot be read as more than it is:

1. **The R13 round keeps its own number.** Measured 2026-11-11 against the register as it stood then:
   19/22 with G19 `MEMBER_ABSENT`. Retro-fitting that verdict by editing `lanes/D/COPY_REGISTER_ALL.json` or
   `gate_r20.py` is exactly what the gate exists to prevent, so it was not done.
2. **It is not a digest-drift waiver.** OD-1 removes three *deleted* files from the denominator. It does not
   license substituting a different revision: the archive's `FHS_PIPD-LS-PKG_W0_r6.md` hashes to `69a08e7f…`,
   not the declared `9f9eb261…`, so it is not counted as a copy of the declared subject.
3. **It is not an acceptance.** The register states where documents live and what they hash to; it says
   nothing about whether their content is right.

Effective status: **G19 is no longer a blocking item** — by owner decision, with a re-declared denominator
that a reader can audit, not by weakening a check.
```

## D｜三車道 ActualServed 回執

| lane | ok | code | used_rank | arm | usage_rows | served_arm_assigned | 檔案 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EXECUTE | True | None | 1 | opencode-go/deepseek-v4.1-flash | 1 | True | out/LANE_EXECUTE.json |
| PLAN | True | None | 2 | opencode-go/deepseek-v4.1-flash | 1 | False | out/LANE_PLAN.json |
| VERIFY_SECURITY | True | None | 3 | opencode-go/deepseek-v4.1-flash | 1 | False | out/LANE_VERIFY_SECURITY.json |

usage 帳本：`%LOCALAPPDATA%/HG-KSEOS/opencodex-hermes/usage.jsonl`（lane home）。relay 必須以 `OPENCODEX_HOME=<lane home>` 啟動，否則 dispatcher 讀不到新列——這是前一回合 `ERR_LANE_ALL_ROUTES_EXHAUSTED` 的唯一根因。

## E｜NEG 矩陣（SoD 與退役臂）

### E.1 SoD（P0-06）

| 案例 | 注入 | 結果 | exit |
| --- | --- | --- | --- |
| MAKER_MISSING | 省略 --maker-* | REFUSE `ERR_MAKER_MISSING` | 3 |
| MAKER_FORGED | forged/none | REFUSE `ERR_MAKER_NOT_IN_ASSIGNMENT` | 4 |
| SAME_PRINCIPAL | maker=checker=deepseek | REFUSE `ERR_LANE_SOD_VIOLATION` | 2 |
| SAME_PRINCIPAL_EXEMPT | + --sod-exemption（業主 2026-11-12 裁決） | served，但 `ERR_NO_ARM_EMITTED_NONCE` | 6 |

回執：`out/SOD_SAME_PRINCIPAL_EXEMPT.json`（前三案在 dispatch 前即拒，無回執，屬預期）。

### E.2 退役臂（P0-07）

| 臂 | ok | code | attempts | 檔案 |
| --- | --- | --- | --- | --- |
| glm-5_3 | False | ERR_LANE_REQUIRED_ARM_ABSENT | 0 | out/RET_glm-5_3.json |
| minimax-m3_1-flash-free | False | ERR_LANE_REQUIRED_ARM_ABSENT | 0 | out/RET_minimax-m3_1-flash-free.json |
| opencode-go_mimo-v2_6-pro | False | ERR_LANE_REQUIRED_ARM_ABSENT | 0 | out/RET_opencode-go_mimo-v2_6-pro.json |
| z-ai_glm-5_3-flash | False | ERR_LANE_REQUIRED_ARM_ABSENT | 0 | out/RET_z-ai_glm-5_3-flash.json |

## F｜L1／L2 結構對帳

| 檔案 | bytes | lines | headings | H1 | H2 |
| --- | --- | --- | --- | --- | --- |
| FHS_vNEXT_PLP_藍圖.md | 7256694 | 34272 | 1268 | 50 | 826 |

| 檔案 | bytes | lines | headings | H1 | H2 |
| --- | --- | --- | --- | --- | --- |
| FHS_vNEXT_PLP_全波次藍圖.md | 2759509 | 16815 | 833 | 54 | 199 |

L1 50 CH 五段齊全：**50/50**

缺 §4（專屬 POS/NEG）章號：`[]`

## G｜原域 patch 候選（`_live_epoch`）

檔案：`HG-KSEOS/scripts/hgk-lane-guard.py:92-110`。現行回傳 `doc["revision"]`，而 `source_of_routes` 指向 assignment，其 epoch 欄位是 `registry_epoch`。

```diff
-    if isinstance(doc, dict) and "revision" in doc:
-        return int(doc["revision"])
-    return None
+    if not isinstance(doc, dict):
+        return None
+    for key in ("contract_epoch", "registry_epoch", "epoch"):
+        if key in doc:
+            return int(doc[key])
+    # Only the registry itself versions by `revision`; an assignment revision is not an epoch.
+    if "revision" in doc and "source_of_routes" in doc:
+        return int(doc["revision"])
+    return None
```

驗證方式：patch 後 `hgk-lane-guard.py --lane VERIFY_SECURITY --expected-epoch 41` 應回 `status=ALLOW`，且 `live_epoch=41`；再以 `--expected-epoch 44` 應回 `ERR_LANE_STALE_EPOCH`（負例）。本輪未改 origin，只提候選。

## I｜子代理台帳摘要（read-only）

`P1-02` 分帳：total_events=99、failed=83、errors=16

| class | count |
| --- | --- |
| REAL_DEFECT | 2 |
| HISTORICAL | 5 |
| ENV | 15 |
| ORIGINAL_OWNER | 55 |
| W1_WIRING | 22 |
| UNCLASSIFIED | 0 |

| 受影波次 | count |
| --- | --- |
| W0 | 17 |
| W1 | 32 |
| ORIGIN | 5 |
| W2 | 45 |

`P0-03` 台帳：{"state": "LEDGER_COMPLETE", "claims_supported": ["gate corpus 31/31 by sha256", "import map 433 entries / 423 distinct paths / 3,713,290 B with 74,127 B of double counting located to 10 named entries", "G19 current 41/343 PASS re-read independently", "73/394 superseded, not live", "431 located and demoted to a superseded run-1 copy count"], "claims_blocked": ["any citation of 429 as a count", "an

問答：73/394 與 41/343 是否可同時宣稱有效？ → **不可以。**（can_both_be_valid=False）

`L1` 結構：chapter_count=50、complete_5_of_5=50、missing_s4=[]、missing_consumer=[]

`P0-09` 六 WP Done 證據：

| WP | done_evidence | trace |
| --- | --- | --- |
| WP-FHS-00 | True | True |
| WP-FHS-01 | False | True |
| WP-FHS-15 | True | True |
| WP-FHS-16 | False | True |
| WP-FHS-19 | False | True |
| WP-FHS-21 | False | True |

缺失欄位 4 筆（見 `out/P0-09_SIXWP_TRACE.json::missing`）。

`Host` 讀回：blocked=[]；relay=`{"status":"ok","service":"opencodex","version":"2.11.0","uptime":773.1112659,"pid":7236,"p`；codex found=1


## H｜重現命令

```bash
PY="C:/Users/user/AppData/Local/hermes/cache/scratch/fhs_next/venv311/Scripts/python.exe"
cd /c/Projects/Agent_Workspace/FHS_NEXT
R="C:/Projects/Agent_Workspace/FHS_NEXT_Workspace/W0_R7_FULL_20261114"

# relay（必須 lane home，否則 usage 0 列）
export OPENCODEX_HOME="C:/Users/user/AppData/Local/HG-KSEOS/opencodex-hermes"
ocx start --port 10101

# gates
"$PY" ops/selfcheck.py
"$PY" ops/tools/spec_identity_check.py --spec-dir _local/W0_SPEC --manifest provenance/SOURCE_IMPORT_MAP.json
"$PY" ops/tools/gate_corpus.py
"$PY" ops/tools/reregister_check.py
"$PY" ops/tools/lane_pin.py --check
"$PY" HG-KSEOS/scripts/hgk-lane-policy.py validate

# lanes
"$PY" HG-KSEOS/scripts/hgk-lane-dispatch.py --lane EXECUTE --force-rank 1 --nonce N1 \
  --prompt "echo N1 then stop" --pool HG-KSEOS/config.live/lane-route-slots.candidate.json \
  --codex-executable "$CX" --json-out "$R/out/LANE_EXECUTE.json" --cwd "$R" --timeout 180

# SoD NEG
"$PY" "$R/../W0_R4_OWNER_RULINGS_20261112/tools/lane_dispatch_guarded.py" --lane VERIFY_SECURITY \
  --binding ops/lanes/bindings/VERIFY_opt1.json --workorder SOD-NEG --nonce N2 \
  --prompt "echo N2" --force-rank 3 --receipt "$R/out/SOD.json" --caller-record "$R/out/SOD_caller.json"

# guard epoch
"$PY" HG-KSEOS/scripts/hgk-lane-guard.py --lane VERIFY_SECURITY \
  --maker-engine opencode-go --maker-model opencode-go/deepseek-v4.1-flash \
  --target-engine opencode-go --target-model deepseek-v4.1-flash \
  --expected-epoch 41 --receipt "$R/out/GUARD_EPOCH41.json"
```
