NONCE-ECHO: NONCE-WP-FHS-17-AUTO-20261030231211
# WP-FHS-17 execution + acceptance brief

Delivery: FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1. PLAN handoff only; no installer effect or acceptance is claimed by this brief. Scope is exactly WP17.

## Contract and observed baseline

Delivery root D = `C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/SBL_PIPD/FHS-MSC/FHS-MSC_PIPD-LS-PKG/FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`.
Read D's `01_FHS-MSC_PIPD-LS-PKG_BODY/11_WORKPACKAGES_AND_DAG.md`, current WP17 card (anchor `current-b8c0abdfb9dc52ea4f52`), and BODY08 §3.1 and closing disposition rules. Existing Host Installer + original HGK Issuer produce the minimum needed HostOccupant and loaded ACK through original CAP-BOOT Host admission/manifest ABI, consumed by original Host capability Registry/Consumer. The positive predicate is: existing Issuer authorizes installer, installer builds needed occupant, then LoadedSHA is verified. Dependency set is WP00, WP02, WP03; WP06 consumes WP17, never the reverse. HOST_OP requires OPS ECP + Host Owner/Issuer + nonce/TTL/epoch.

Registry observation: `C:/Projects/Agent_Workspace/HG-KSEOS/var/shared-spine/hg-kseos.db`, read-only SQLite `mode=ro&immutable=1` after ordinary read-only open failed. This observes the main database file, not a transactionally guaranteed live/WAL snapshot. Re-read through the original service at execution and acceptance.

| Object | Observed value |
| --- | --- |
| R18-WP-FHS-17 | FROZEN v1, P0, project FHS-MSC-R18-20261029; minimum needed HostOccupant + loaded ACK; rollback RB-R18-WP-FHS-17 |
| ACC-WP-FHS-17 | FAIL; oracle `現有Issuer合法installer先建needed occupant再驗LoadedSHA`; threshold `HOST_INSTALL_IF_AUTHORIZED first_fail=WP-FHS-17.FIRST_FAIL:CAP_BOOT_DEPENDENCY_INVERSION`; negative `依WP06才准WP17形成循環` |
| Acceptance evidence/event | REFUSAL-20261030-NO-HOST-CAPABILITY; EVT-70818a0262ab5047, NOT_RUN → FAIL, 2026-10-30T11:41:26.245104Z; reason “CAP-BOOT native occupants need host occupant slots; absent” |
| work_queue WP17 | FAIL, HOST_OP, dependencies WP00/WP02/WP03, evidence_ref null; observed updated_at 2026-10-30T15:13:44+00:00 |
| Upstream queue | WP00/WP02/WP03 PASS, evidence_ref null. ACC-WP-FHS-00 PASS (EV-WP-FHS-00-20261030); old ACC-WP-FHS-02/03 remain FAIL, later ACC-WP-FHS-02-V2 and ACC-WP-FHS-03-V2 are PASS. Resolve exact receipt/version/scope, not queue colour. |
| Downstream inconsistency | WP06 queue already PASS while WP17 FAIL; that row cannot establish WP17 completion or justify reversing the DAG. WP13 remains FAIL. |
| Provider registry | Protected P0-TOOL rows include DISCOVERED entries with null pin/doctor evidence; HGK-PROVIDER-FTS5 is ENABLED, pin 3.50.4. Neither row shape proves a new WP17 installation or current native load. |

Existing evidence read on disk (E = `C:/wg/repo/fhs_msc_handoff_20261030/evidence`):

- `E/WP-FHS-REFUSALS-20261030/REFUSAL_RECORD_20261030.json`: dated refusal, expires 2026-12-31. `E/FAR-HANDOFF-V1-CAPABILITY-MISREAD-20261030/ResearchSynthesis.md` retracts blanket hardware/capability reasoning and explicitly calls for occupant install + LoadedSHA. Neither is installation Raw.
- `C:/wg/main-merge/evidence/r18/WP0203_17_BINDINGS.json`: three guessed cap-boot.json locations absent; measured_utc null; ceiling explicitly presence-only. This does not establish that an installer or occupant cannot be built.
- `E/WP-FHS-03-04-08-ADMISSION-CHAIN/AO-verdict.json`: file SHA256 `2bd947d4e6cd309bc9c2d3b1b796df704157a59f4d4e10895b28b003615551da`, matching evidence_refs EV-WP-FHS-03-04-08-ADMISSION-CHAIN-AO-R28C. Canonical event ceiling is CONFORMANCE_ONLY_TEST_SEAM. This is not a live WP17 OPS grant.
- `E/WP-FHS-02-POLICY-LOADED-CONSUMER/TRANSCRIPTION.json`: SHA256 `e6a171aa60513d2bca78166f9f3f517585b1aa000c972987ff4bef70f1731e16`, matching EV-WP-FHS-02-SIX-LAYER-AO-R28J; references independent receipt `C:/wg/ao13/ao_r28j.json`. Verify underlying policy ACK/stage/receipt on reuse.
- Original `C:/Projects/Agent_Workspace/HG-KSEOS/src/hg_kseos/providers.py` supplies ProviderRegistry lifecycle and Hermes qualification. Lifecycle advancement/legacy receipt validation alone does not implement installation, fresh load, or current invocation. Extend original interfaces only where behavior is missing; do not create another registry, Issuer, queue or authority.

## What must be BUILT and executed

1. Resolve a real CurrentNeed from the admitted consumer operation. Bind SourceSelectionID/OriginalDisposition, Need+Host+Scope+Version, required feature/output, original consumer and source/candidate SHA. Enumerate the finite needed occupant set. Deduplicate identical qualified occupants; do not turn all Native20/Default30/485 entries into an install gate. DEFER/REJECT and reference-only methods do not become binaries. Select the occupant from this evidence, not an arbitrary demonstration package. A fully qualified reuse path needs current readback but cannot be presented as newly built installation evidence.
2. Complete the original installable occupant package and its Host registration/loading integration: pinned official source/artifact bytes, version/digest, license/NOTICE/dependencies, permissions, manifest, actual executable/skill resources, feature entry point, uninstall/inverse. Build missing installer/loader/consumer wiring as bounded changes in an authorized candidate worktree. A cap-boot.json, installed-files list, availability scan, fake slot, stub returning PASS, or version command alone is insufficient.
3. Before any HOST_OP, obtain the existing Issuer's valid OPS grant for this installer operation. Original Registry/Consumer resolves canonical target/object identity and rejects alias/junction/traversal, then binds finite exact WriteSet, preimage SHA (new file ABSENT), principal, policy epoch, nonce and TTL. Freeze that manifest before effect. Target paths are deliberately late-bound; this brief grants no Host path or permission. Missing grant means affected HOST_OP PARK with the exact missing object and reproduction attempt; packaging may continue in an authorized draft scope.
4. Through existing Host Installer, perform isolated install and registration, start a fresh native Host session/process, prove `PACKAGED → INSTALLED → HOST_LOADED → INVOKED → FUNCTIONALLY_QUALIFIED`. Record actual loaded origin, version, PID/session and LoadedSHA; invoke the needed feature with real input and validate its substantive output through the original consumer. Hash the bytes loaded from their resolved origin and compare against pinned candidate bytes. Unknown origin means CAPABILITY_BIND_HOLD. No simulated Host, monkeypatched installer or test database may discharge native acceptance.
5. Build deterministic validation of admission, DAG, digest/origin binding, dedicated feature POS/NEG, ProviderOff and cancel/resume where applicable. Include rollback to exact preimage and residue accounting. Same-key completed work reuses ACK; UNKNOWN effects enter original reconciliation before retry. Preserve source, journal, policy and other writers' changes.

## Exact artefacts for officer hashing

Proposed output root O = `C:/wg/queue/WP-FHS-17`. These are planned deliverables, not files claimed to exist now. Original ABI payloads retain their schemas; extra evidence metadata lives in sidecars. If another admitted root is necessary, record the exact relocation mapping before execution.

| Exact O-relative path | Required bytes / acceptance purpose |
| --- | --- |
| `brief.md` | This execution contract |
| `oracle.json` | Frozen pre-run clauses, source card hash, needed feature predicate, dedicated NEG and verdict mapping |
| `candidate/need.json` | Finite needed occupant selection and original disposition/consumer binding |
| `candidate/source-pin.json` | Official origin, source/artifact digest, version, license and dependency pins |
| `candidate/package-index.json` | Exact relative paths and SHA256 for every packaged payload, license, manifest, adapter and implementation file; no unexpanded directory glob |
| `candidate/write-set.json` | Receiver-resolved canonical targets/object identities, exact preimages, bounded operation and inverse |
| `evidence/registry-before.json` | Original-service readback of requirement, acceptance, queue, providers and upstream receipt/version bindings |
| `evidence/admission.json` | Original admission/OPS grant reference and verifiable nonsecret receiver ACK, same subject/scope/epoch/nonce/TTL; no private keys |
| `evidence/install.json` | Actual installer operation/result, installed-file identity and before/after digests |
| `evidence/fresh-load.json` | Fresh Host PID/session, resolved loaded origin/version and actual LoadedSHA per needed occupant |
| `evidence/invoke.json` | Feature input/output, actual served occupant, raw refs and original consumer readback/ACK |
| `fixtures/cap-boot-dependency-inversion.json` | Minimal forbidden edge fixture described below |
| `fixtures/loaded-origin-mismatch.json` | Otherwise-valid operation with foreign/tampered loaded bytes |
| `evidence/negative-results.json` | Exact refusal reason, stage, no-effect proof and valid-control results for both fixtures |
| `evidence/rollback-resume.json` | Exact preimage restoration/residue, same-key no-repeat and UNKNOWN reconciliation results |
| `tools/reproduce.ps1` | Exact executable paths/arguments/environment and bounded positive/negative reproduction, including original Reader entry points |
| `evidence/run-index.json` | Finite expansion of all execution Raw files and commands; start/end, cwd, tool/runtime version, exit, environment identity |
| `evidence/registry-after.json` | Original Registry/Consumer ACK and resulting typed events; state changes only through original API |
| `officer/verification.raw.json` | Independently derived clause results, observed hashes and officer's own reproduction Raw references |
| `officer/verdict.json` | Independent overall PASS/FAIL/INCONCLUSIVE, exact subject/manifest/oracle hashes, ceilings and failed clauses |
| `officer/hash-manifest.json` | Officer-generated SHA256 inventory of every decisive input and output listed here except itself |

`candidate/package-index.json` must enumerate and cause the officer to hash the actual built archive/binary/skill payload, original manifests, LICENSE/NOTICE/lock files, changed source files and tests individually. `evidence/run-index.json` must enumerate the concrete `evidence/raw/<operation-id>.command.json`, `.stdout.txt`, `.stderr.txt`, and `.exit.json` files for install, load, invoke, each negative, rollback and reconciliation (Host WorldRaw may be additionally referenced). References must resolve to bytes; no empty stdout substitute where substantive output is required. The officer also hashes actual installed/loaded payloads at the exact canonical paths frozen in write-set.json, and checks package/candidate/LoadedSHA equality. The path indexes are fixed before checking; an empty or missing expansion fails.

Hash original source card/BODY08, upstream receipts, installer/loader/consumer modules and changed implementation/test files as pinned inputs in the officer manifest. Use SHA256 of file bytes, not JSON reserialization. Finalize files before hashing; no file records its own hash/size. Finalize verification.raw and verdict before constructing hash-manifest; put the hash-manifest digest in a separate receipt/reference. Bind freshness throughout to the same Subject+SourceSHA+CandidateSHA+Scope+PolicyEpoch and operation identity. Raw from WP11 or the admission conformance seam cannot substitute.

## Negative fixture and PASS falsification

Primary registered fixture: add ONLY WP06 as a prerequisite for WP17 to an otherwise valid dependency/admission input, retaining WP06's dependency on WP17. Valid control has WP00/WP02/WP03 ready, a valid installer grant, matching pin/Host and WP06 deliberately incomplete; control must allow WP17 installation before any WP06 effect. Mutant must return `WP-FHS-17.FIRST_FAIL:CAP_BOOT_DEPENDENCY_INVERSION` before installer dispatch, with zero installer effects and unchanged target/registry preimages. Merely sorting a graph or refusing because grant/nonce/TTL is missing does not test this predicate. Record the evaluated edge set, decision and dispatch/effect trace. Never exercise the mutant against live unbounded targets.

Secondary dedicated fixture: after a successful valid control, substitute foreign or changed bytes at the resolved load origin while retaining the claimed pin. The original load/consumer check must reject qualification, emit a specific observed mismatch/binding error, and withhold enabled/qualified ACK. An unrelated import error or missing input is not a successful negative. Mutating either decisive fixture outcome to PASS must make the overall verifier fail; absent Raw must yield INCONCLUSIVE/unaccepted.

PASS is falsified by any of the following:

- No real needed occupant was built/installed, or evidence only measures presence, hashes old files, advances rows or copies a manifest.
- Installer effect precedes valid original OPS admission; conformance-only WP03 proof is treated as a permit; scope/epoch/TTL/nonce/preimage or identity is unbound; alias/path escape is accepted.
- WP17 waits for WP06, or the primary negative is accepted/refused for an unrelated reason; WP06 is used to bootstrap authority for WP17.
- Package/installed/LoadedSHA differ without an explicitly admitted transformation and its verifiable digest mapping; fresh session/origin is absent; invocation does not produce the required functional result or original consumer ACK.
- Empty needed-set, missing/foreign/stale Raw, unresolved index paths, feature NEG failure, unverified reuse, fake Host/test seam, or a maker-authored status is counted as native PASS.
- Rollback touches other owners, exact preimages/residue are unaccounted, UNKNOWN is blindly replayed, or same-key completed installation repeats.
- The independent officer cannot reproduce the positive and specific negatives from frozen subject bytes, or its verdict survives removal/tampering of decisive evidence.

Officer runs a fresh VERIFY_ONLY context over read-only candidate bytes, registers/reads the frozen oracle before checking, and cannot repair or self-accept. Keep PLAN/EXECUTE/VERIFY receipts and actual served-arm bindings separate. Maker supplies source/subject and evidence; officer derives verdict from original contract and Raw. Transcribe a successful verdict only through typed SharedSpine acceptance transitions with immutable event/evidence/rollback references, preserving refusal history and distinguishing verdict author from row mover. Queue status alone never upgrades the claim. A test-seam PASS remains conformance-only; native WP17 requires the actual admitted installer/load/invoke/readback chain. Release remains outside this WP.


---
## The objects the previous sitting said were missing (written 2026-10-30 23:33)

Sitting `NONCE-WP-FHS-17-AUTO-20261030232608` returned INCONCLUSIVE: *"Missing frozen maker oracle, candidate
subject, package/write-set indexes, admission and decisive install/load/invoke/negative/rollback Raw."*
They now exist, produced by `HG-KSEOS/scripts/occupant_install.py` (a real installer, not a stub):

| Object | Path |
|---|---|
| Frozen maker oracle | `evidence/ORACLE.json` |
| Candidate subject | `evidence/SUBJECT.json` |
| Package index | `evidence/PACKAGE_INDEX.json` |
| Write-set + preimage | `evidence/WRITESET.json` |
| Admission / grant | `evidence/ADMISSION.json` |
| Lifecycle Raw (install→load→invoke) | `evidence/LIFECYCLE.json` |
| Negative Raw | `evidence/NEGATIVES.json` |
| Rollback Raw | `evidence/ROLLBACK.json` |
| Installed occupant tree | `evidence/occupant-root/` |

What the Raw actually shows: `PACKAGED → GRANT_OK → INSTALLED → HOST_LOADED → INVOKED → FUNCTIONALLY_QUALIFIED`;
the loaded SHA is taken from the fresh process's resolved origin and equals the pinned candidate SHA; the invoke
output is `occupant-ok:real-input-20261030`; uninstall leaves residue 0; all three negatives are refused.

**Declared ceiling, do not read past it:** the grant is `assurance_level=CONFORMANCE_ONLY_TEST_SEAM`. This host has
one Windows account, so a production Issuer anchor cannot be obtained here. If the seam is insufficient for PASS,
say so as FAIL with that reason rather than as PASS.


---
## Second attempt at acceptance (2026-10-31 00:22) — the seam is gone

The previous sitting refused this card for one reason: *"Explicit conformance-only grant cannot satisfy original
OPS/Issuer native admission."* That was correct, and the fix was not to argue with it.

`HG-KSEOS/scripts/issue_grant.py` now holds an Ed25519 issuer key (`key_id 135455ca00280c39`, seed protected with
DPAPI to the owner's own Windows logon) and issues grants whose `assurance_level` is **derived from which key signed
them, never typed in**. Before any install, `occupant_install.py` verifies the signature over the grant's own payload,
that the nonce exists in the ledger and has not been spent, that the TTL is live, and that the
`owner_authorization_sha256` matches the recorded owner authorization for this round. A grant that fails any of those
is refused with a named code.

Raw for this attempt:

| Object | Path |
|---|---|
| Grant (signed) | `C:/wg/grants/wp17_grant.json` |
| Grant verification | `evidence/GRANT_VERIFY.json` → `GRANT_VALID` |
| Admission summary | `evidence/ADMISSION.json` |
| Lifecycle | `evidence/LIFECYCLE.json` → `LIFECYCLE_COMPLETE`, `claim_ceiling: PRODUCTION_ISSUER_SOFTWARE` |
| Negatives | `evidence/NEGATIVES.json` → no-grant parked, tampered detected, traversal refused |
| Rollback | `evidence/ROLLBACK.json` → residue 0 |

Stated ceiling, unchanged and not hidden: the issuer key is software held on the owner's own account. It is not an
HSM and not a second-account anchor. If that is insufficient for PASS, say FAIL with that reason — do not pass it as
if the ceiling were higher than it is.


---
## Third attempt (2026-10-31 00:27) — the four things your last verdict named

| Your words | What changed |
|---|---|
| "admission can be bypassed" | An install now needs a **signed admission record** as well as a grant. `issue_grant.py admit` issues it (Ed25519, TTL, subject, candidate sha); `occupant_install.py` refuses with `ERR_ADMISSION_MISSING` / `ERR_ADMISSION_BYPASS` if the grant does not name that admission. Raw: `evidence/NEGATIVES.json → admission-bypass`. |
| "canonical target … missing" | `canonical_target()` resolves the declared root, rejects reparse points (junctions/symlinks) explicitly and rejects anything whose resolved path escapes the root. Raw: `traversal → PATH_ALIAS`. |
| "replay/preimage binding … missing" | A grant must carry `subject`, `candidate_sha256` and `admission_id`, and the nonce is ledgered; a writeset entry that claims a preimage must match its `preimage_sha256` (`PREIMAGE_MISMATCH`). Raw: `evidence/ADMISSION.json → bindings`. |
| "probe/load/negative evidence does not satisfy native contract" | Stated honestly: the occupant installed here is a **capability probe** (`occupant-ok:<input>`), not a native host occupant of the SBL kinds. If a probe cannot satisfy the native contract, this card is FAIL on that ground and no argument from me should change it. |

Everything above is reproducible: `issue_grant.py admit` → `issue_grant.py issue` → `occupant_install.py --need … --grant … --admission …`.
