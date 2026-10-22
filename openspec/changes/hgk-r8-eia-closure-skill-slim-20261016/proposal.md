# Proposal: R8-0 EIA closure and skill-slim regression

## Why

R8-0 (`CNV-PIPD-LS-SP-20261015`, ChangeSet `R8-0-SKILL-SLIM-REGRESSION-AND-EIA-CLOSURE`, project `CNV-R8-SKILL-SLIM-EIA-CLOSURE`) needs source-bound regression and reconciliation contracts before any finding can be reconsidered. The local WS-A/WS-C/WS-D records expose loader/losslessness defects, a validator baseline mismatch, and absent checker write isolation; evidence publication corrections and owner decisions remain separate from implementation and acceptance.

## What Changes

- **A — EIA-R6-09 / K-16 / ACC-RQ08:** define the skill-slim gate for the 100000-byte main-file cap, frontmatter at byte 0 and actual host loader/selection/trigger parity, nested reference intake and absorbed-byte SHA-256/offset reconstruction. More than 60 references remains a **WARNING**, never a hard gate. Define dry-run-default, pre-image-pinned guarded apply, backup, rollback and receipt requirements for a separately authorized apply round.
- **B — EIA-R6-04:** require the R8-0 validator candidate to be rebased onto the frozen `main` baseline `dba4b19` (resolve and record its full commit identity before implementation), not the R7 `9bd33a1` base. Re-measure all `M01..M18`, require M04/M06/M16 to REJECT, and adjudicate the eight historical NOT_RUN individually without inflating the executed denominator.
- **C — EIA-R6-03:** encode evidence-of-absence and scratch deny-ACE mechanism proof while leaving actual guarded-root ACL changes proposal-only and owner-gated. A single shared Windows identity cannot separate maker from checker; distinct OS identities or a scoped sandbox are required. Output relocation and equal end-state hashes alone do not establish prevention.
- **D — EIA-R6-01/02 and nine-finding reconciliation:** propose a versioned R6 publication errata identifying the two declared-but-unshipped `__pycache__` `.pyc` paths, stale counts/SHA/UTC semantics, and fresh publication readback. Preserve the merged packet and failed historical receipts; never ship cache files to manufacture equality. Carry EIA-R6-06's local maintainer authorization without treating it as approval for a new packet.
- **E — EIA-R6-05/07/08:** retain explicit claim ceilings for Fresh G1, the original eight Gates, 221 planned cases, source #6 and the 20 quarantined KP `*-R04` clauses. Name the owner/authority prerequisites instead of creating substitute authority or automatic release eligibility.

## Capabilities

### New Capabilities

- `r8-eia-closure-and-skill-slim-regression`: one cross-surface evidence and regression contract for groups A-E. Design D1 explains why this is a separate flat capability rather than an implied modification of the unarchived R7 lane-guard proposal.

### Modified Capabilities

None. No canonical capability is modified by this proposal.

## Impact

- Intended future surfaces: skill candidates and regression/apply tooling; DOC-07 oracle/validator candidate and its 18-mutation runner; checker harness isolation and evidence; publication errata and finding/claim records. No API, dependency, authority, routing or product behavior changes are executed now.
- Inputs: `_handover/CNV-PIPD-LS-SP-20261015-R8/WS_A_REGRESSION_AVR.json`, `WS_A_REGRESSION_HGK.json`, `WS_A_LIBRARY_SCAN.json`, `WS_C/CHECKER_WRITE_ROOT_ISOLATION_EVIDENCE.json`, `WS_D/EIA_R6_RECONCILIATION.json`; attached PKG v2.0.0 (G-A Skills, ACC-RQ08) and external report §§4.1, 7-9. These are source records, not new acceptance verdicts.
- Governance context: admission receipt lists `WO-TS-CLOSURE-01..04`; this proposal neither re-admits nor resolves them. Task applicability and earliest owners are in tasks.md/design.md.

## Out of scope / Non-goals

No implementation, product/source/config/route edit, canonical/main-spec write, spine access or mutation, ACL application to an existing guarded subject, git write command, publication, merge, archive, promotion, release, SQP1 or Stage-3. The only authored paths are this new change directory and the authorized `WS_F/` receipt directory.

## NON-CLAIMS — this proposal is not an acceptance

This is a **PROPOSAL with zero implementation**. All implementation tasks remain unchecked. OpenSpec strict validation checks proposal structure only; it is not a regression result, Gate PASS, DOC-05 admission, independent acceptance or finding closure. No Fresh G1 certification, no G-A..G-H PASS, no execution of the 221 planned runtime cases, no AO verdict, no Product/Production claim and no permission escalation are asserted. Existing evidence is cited at its original LOCAL/candidate-only ceiling and is not re-run by authoring this change.

## Blocked items:

- Real guarded-subject ACL changes: HGK Checker Harness Owner plus explicit owner authorization; true role separation additionally needs distinct identities or a sandbox.
- Fresh G1 / runtime Gates / ECP / DOC-05 / 221 cases / AO: HGK and domain Gate Owners with fresh runtime admission and independent receipts.
- Source #6 classification and active denominator: PIPD Source/Authority Owner ruling.
- KP `*-R04` polarity correction and quarantine lifting: KP Policy Owner / DOC Owner, followed by safety-negative and cross-KP regression.
- Errata publication or any R8 merge: Fabric publication owner / Repo Maintainer authorization. R6's prior scoped authorization does not confer it.
