# Design: hgk-r8-eia-closure-skill-slim-20261016

## Context

See proposal.md for motivation and the five requirement groups. This is a planning-only companion to the admitted R8-0 project, not execution of its WorkOrders. The predecessor change's convention is preserved: `.openspec.yaml` contains only `schema: spec-driven` and `created: 2026-10-16`; Markdown artifacts begin with a title, not invented YAML metadata. Requirements use four-hash WHEN/THEN scenarios and tasks remain unchecked.

Authoritative local inputs read before authoring: HG-KSEOS `AGENTS.md`; all five artifacts of `hgk-lane-brief-and-guard-hardening-20261015`; R8 `WS_D/EIA_R6_RECONCILIATION.json`, `WS_A_REGRESSION_AVR.json`, `WS_A_REGRESSION_HGK.json`, `WS_A_LIBRARY_SCAN.json`, `WS_C/CHECKER_WRITE_ROOT_ISOLATION_EVIDENCE.json`; attachment PKG v2.0.0 targeted G-A/ACC-RQ08 material and external report §§8-9 finding table. `WS_A_REGRESSION_AVG.json` is not an input. These are observations at their recorded revisions, not a claim of current remote state.

## Goals / Non-Goals

**Goals:** define independently checkable future closure contracts; retain separate denominators and authority boundaries; make drift, unknowns and non-deployment visible.

**Non-Goals:** perform regression, repair candidates, change live skills, apply ACLs, rebase product code, publish errata, amend main specs, resolve acceptance or write any control-plane state. All such work requires a subsequent authorized execution; this proposal supplies no additional authority.

## D1 — one new flat capability

**Chosen:** `r8-eia-closure-and-skill-slim-regression`. The canonical `openspec/specs/` inventory currently contains only `ao-lane-independent-verify`; `lane-brief-and-guard-hardening` exists in the predecessor's unarchived change, not as a canonical capability. R8 adds a skill/apply and EIA/publication contract beyond that lane-dispatch surface. One new flat capability keeps the five groups together without implying the predecessor was applied or accepted. Its delta uses ADDED Requirements with a substantive Purpose; no existing requirement is replaced.

**Rejected:** silently extending the predecessor delta or labeling its requirements MODIFIED. That would make an unarchived proposal a canonical dependency and risk conflating its sampling/detection design with actual OS enforcement. This proposal supersedes no historical verdict.

## D2 — C1..C5 plus actual loader parity and guarded apply (group A)

**Chosen:** preserve WS-A's capacity, loader-shape, link-intake, losslessness and negative-control separation, but require actual host loader/trigger/nontrigger evidence rather than equating parsed YAML with loader parity. Hard cap is 100000 raw bytes (inclusive); reference count >60 is a non-gating WARNING under ACC-RQ08. Record recursive references and the frozen AVR 10/HGK 6 reconstruction source blocks; absorbed stubs require full source SHA-256 and exact byte offsets, not merely line presence or abbreviated digest displays.

Baseline records: AVR candidate 22091 bytes fails C2 (10 wrapper markers before frontmatter) and C4 (stale `verifier-lane-handover.md` source/offset); HGK candidate 21026 bytes passes the recorded C1..C5 and warns at 90 references. The library scan records live AVR 101488 bytes and HGK 105116 bytes with 118 references. These are historical input facts, not fresh regression results or readiness certification. WS_A_REGRESSION_HGK.json's top-level `subject_live` incorrectly points to the AVR root while its C2 identity reports HGK. Treat that binding inconsistency as an input-evidence limitation: future evidence must bind the actual HGK root and full digests before apply; never silently copy that field or reinterpret the old receipt as stronger evidence.

Guarded apply is a later, separately authorized act: dry-run default; explicit file allowlist and full pre-image SHA for each target; drift rejection before writes; per-run immutable backups; exact candidate materialization; readback and host-loader regression; receipt; isolated exact-byte rollback rehearsal. Re-running must not overwrite a pre-image backup with an already-slimmed stub. The gate has to be consumed by the apply path and tested in every supported mode before any prevention claim. A freestanding receipt without a consuming path is detection only.

**Rejected:** fixing only the main-file size, using zero lost long lines as byte-losslessness, requiring <=60 references, or applying a passing HGK summary with an inconsistent subject locator. Each hides a distinct acceptance condition.

## D3 — frozen main rebase and denominator-preserving mutations (group B)

**Chosen:** resolve `dba4b19` to its full commit in the authorized product repository in the future execution step, freeze it as the R8-0 main baseline, and bind the rebased candidate plus runner digest to every mutation row. Do not invent a full SHA or substitute the ambient HG-KSEOS HEAD. Historical R7 evidence on `9bd33a1` records 10 executed/detected and 8 NOT_RUN; it is insufficient for the rebased candidate.

Re-measure all 18 registered IDs; M04 ASSURED veto, M06 expected-oracle pin and M16 trace-digest tamper must REJECT at their first intended failure, while adjacent valid fixtures still ACCEPT. Retrieve the eight historical NOT_RUN IDs from the actual mutation register before execution; this proposal does not guess their identities. Give each an applicability decision, source, owner/prerequisite, raw execution or owner-approved N/A. Preserve historical and new statuses separately, compute counts from unique rows, and require an independent re-run against the same frozen rebased candidate.

**Rejected:** cherry-picking the three successful R7 negatives as complete R8 evidence, or counting eight applicability judgments as eight detected mutations. Evaluation of all 18 IDs is not a claim all 18 executed.

## D4 — isolate the checker without claiming scratch ACL deployment (group C)

**Chosen:** retain three distinct states: evidence-of-absence at the real root, mechanism proof on scratch, deployment pending owner authorization. WS-C reports inherited Authenticated Users Modify, no deny ACE, scratch write rc=0, deny-W write rc=1/Permission denied/no file, and successful writing after removal. It reports the guarded set as 300 files with digest `3588d5d51a4941cf1c9425beee9dcf3f4162fe23bcdd276bc1dd3939af86f16c`. These are producer observations, not this proposal's rerun.

WS-C's exact proposal uses Windows command-shell expansion: `icacls "C:\Projects\Agent_Workspace\_handover\CNV-PIPD-LS-SP-20261015\R6_DELIVERY" /deny "%USERNAME%:(W)"`, rollback `/remove:d "%USERNAME%"`. They are quoted as unexecuted source proposals, not safe universal commands: Bash does not expand `%USERNAME%`; the recorded deny lacks inheritable `(OI)(CI)` flags and only demonstrates scratch file creation denial. It does not establish denied writes/deletes/renames to all existing descendants. Before any authorized real application, the harness owner must select the actual checker SID, freeze/save the original ACL, qualify parent/child/replace/delete/rename behavior and exact ACL restore on a disposable equivalent tree. Restoring the saved ACL is the rollback contract; indiscriminate `/remove:d` could remove pre-existing denials and is not sufficient by itself.

Maker and checker presently share one Windows identity. A deny on that identity can constrain both, not distinguish their roles. True separation requires a different checker OS identity or a scoped process sandbox; approve the mechanism in a later security change. Require an outside writable output root plus successful allowed-write and denied-subject-write tests in the same deployed context. Read back the complete frozen subject set, not just a historical 299-file subset. Equal end hashes cannot prove absence of transient write-and-restore; procedural output relocation and sampler detection are not OS prevention.

**Rejected:** applying ACLs now, claiming one re-login creates a distinct identity, or presenting a W-only scratch probe as full descendant/role isolation. EIA-R6-03 remains open.

## D5 — versioned publication errata and finding-by-finding ledger (group D)

**Chosen:** propose a separate versioned errata artifact (v1, subject and observation timestamps, original/current head locators, exact excluded paths, declared/shipped sets and fresh readback) for later authorized publication. Do not edit the merged packet or failed receipts. WS-D observes R6 head `b8ff81043e47e4b652522be34444bf52fcf4d65e`, 583 declared versus 581 shipped, no only-in-Git rows, and exactly these manifest-only rows:

1. `EVIDENCE/CNV-PIPD-LS-SP-20261015/R6_CHECKER/COPIES/probes/RUNNERS/__pycache__/probe_lib.cpython-311.pyc`
2. `EVIDENCE/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/RUNNERS/__pycache__/probe_lib.cpython-311.pyc`

The errata must distinguish report-time 567/569, stale 566 figures and WS-D's later 583/581 observation, and explain that generated UTC is an observation timestamp, not commit-order authority. Fresh publication readback must derive the exact shipped set for the chosen immutable revision; do not present a historical observed head as today's head. R7's reported 306/306 equality cannot fix R6's mismatch.

| Finding | Original class / severity | WS-D local disposition retained | Earliest owner / closure prerequisite |
|---|---|---|---|
| EIA-R6-01 | CONFIRMED_DEFECT / MEDIUM | OPEN_PARTIAL | Fabric publication owner; versioned exact-path errata and authorized publication/readback |
| EIA-R6-02 | CONFIRMED_DEFECT / LOW | OPEN_PARTIAL | Fabric publication owner; same errata with SHA/count/UTC currentness |
| EIA-R6-03 | EVIDENCE_GAP / HIGH | OPEN | HGK Checker Harness Owner; real isolation authorization and same-subject independent proof |
| EIA-R6-04 | EVIDENCE_GAP / HIGH | IN_FLIGHT | DOC-07 Oracle/Validator Owner; rebased 18-row measurement and independent re-run |
| EIA-R6-05 | EVIDENCE_GAP / HIGH | BLOCKED_AUTHORITY | HGK/domain Gate Owners; separately admitted runtime and AO evidence |
| EIA-R6-06 | EVIDENCE_GAP / MEDIUM | CLOSED_LOCALLY | Fabric Repo Maintainer; R6 authorization recorded, zero GitHub review objects, new approval for any R8 merge |
| EIA-R6-07 | EVIDENCE_GAP / MEDIUM | OWNER_GATED | PIPD Source/Authority Owner; source #6 ruling then active-denominator recomputation |
| EIA-R6-08 | ORACLE_DISAGREEMENT / MEDIUM | QUARANTINED_CONFIRMED | KP Policy Owner / DOC Owner; polarity correction and safety/cross-KP regression |
| EIA-R6-09 | NON_BLOCKING_OBSERVATION / LOW | MEASURED_AND_IN_TREATMENT | Skill Owner; loader/losslessness repair and guarded apply with independent rerun |

These are local reconciliations, not new closures. 01/02 block publication-side claims conditionally; 03 blocks independent-acceptance claims; 04 remains open pending its execution/checker; 05 blocks full Product/Production claims; 07 blocks full PI/PD; 08 is non-blocking only while unrepaired clauses remain unconsumed; 09 stays non-blocking as an observation but candidate hard-gate defects block that candidate's apply. Preserve check/source/observed/blocking/authority fields in any successor machine ledger.

**Rejected:** adding `.pyc` files to make the count match, rewriting historical failures, borrowing the R6 merge approval for R8, or declaring closure just because errata text exists.

## D6 — original gate catalog and owner boundaries (group E)

**Chosen:** retain Slot 14's original eight Gates only: G-A Skills, G-B G1, G-C Hermes, G-D Trace, G-E FS/DB/API/Desktop, G-F SoD, G-G GitHub and G-H Release/Handoff. A local C1..C5 machine result is not G-A PASS; strict OpenSpec validation is not an additional acceptance Gate. Fresh G1 requires competent recertification. Runtime effects require authorized WorkOrder/RepoContext, applicable DEV/OPS ECP/TQAEP and effect-time DOC-05 admission; independent raw receipts and AO authority are separate steps. R8 proposal execution count for the 221 planned runtime cases is zero; NOT_RUN is never PASS.

Source #6 stays FAIL_CLOSED until the PIPD Source/Authority Owner issues a versioned active-normative versus superseded-history ruling; no local agent classification or silent denominator shrink. All 20 KP `*-R04` polarity conflicts stay quarantined from automatic policy/release intake until KP Policy Owner / DOC Owner correction and safety-negative/cross-KP checks. Do not execute contradictory MUST NOT clauses as written. No self-certification, second control plane or release authority is introduced.

**Rejected:** interpreting evidence merge, proposal validation, hashes, row counts, quarantine or local machine successes as acceptance.

## Risks / Trade-offs

- [Producer evidence may evolve or misbind a subject] → bind full source hashes in the receipt and treat observations as dated; re-derive candidate/root identities before future apply.
- [ACL hardening may block the maker too] → choose distinct identities or sandbox; test allowed and forbidden operations before an owner-approved deployment; retain original ACL backup.
- [N/A reduces apparent scope] → retain all 18 IDs and require owner applicability decisions, never erase NOT_RUN rows.
- [Publication changes remote currentness] → immutable subject pin plus fresh exact-target readback; errata does not rewrite historical receipts.

## Migration Plan

No deployment occurs in this task. Future apply requires a new explicit implementation authorization and per-target admission: freeze sources/baselines; repair in bounded candidates; run deterministic positive/negative/boundary checks; independent re-run; guarded skill apply only after dry-run and rollback rehearsal. ACL deployment and publication remain distinct owner-authorized actions. Rollback must restore skill pre-images exactly and restore saved ACLs, with receipts and no original evidence deletion. Any new stronger acceptance request goes through its original owner and typed governance path, outside this proposal's write scope.

## Non-claims

PROPOSAL ONLY; zero implementation, zero live effects, no ACL applied to the real root, no publication performed, no control-plane writes, no source/config/spine changes, no git writes. This document upgrades no finding or Gate and issues no acceptance. Future tasks are not permission to execute now.
