# Proposal: R9-0 FAR residual closure

## Why

Round `CNV-PIPD-LS-SP-20261015` (ChangeSet `R9-0-FAR-RESIDUAL-CLOSURE`, project `CNV-R9-FARCLOSURE`) is
ordered to research every residual, gap and owner-decision item with FAR against the governing package, and
then execute the resulting engineering decision. This proposal carries only the deltas that are **not**
already proposed elsewhere: the PLAN-route rebind, the canonical promotion of the verified product candidate
and the SoD reclassification are already proposed in `hgk-far-remediation-20261016` (R1/R2/R3) with the same
target values, and the main-file cap is already proposed in `skill-mainfile-cap-remediation`. Duplicating them
would create two competing texts for one act.

## What Changes

- **R9-A — validator adaptation (executed, candidate).** The R8-0 hardening is not drop-in on `main`: a legal
  TraceLink fails closed with `UNBOUND_FROZEN_CONTEXT` when no frozen context is supplied even though the
  bundle carries the endpoints, and the CLI smoke path raises `AttributeError` where `derive_frozen_context()`
  assumes a mapping at `risk_guard` while the newer fixture submits a string. A two-hunk adaptation bounded to
  `validate.py` is specified and dispatched to the EXECUTE lane, with the M04/M06/M16 mutation probes as the
  negative control. This change **requires** the acceptance shape: two tests pass **and** each mutation still
  reports `observed=REJECT`.
- **R9-B — skill candidate guarded apply (candidate).** A first repaired candidate was REFUSED by the round's own
  C6 gate (one live reference absent: `references/product-branch-write-set-gates.md`, 4986 bytes) in two
  independent runs; a successor candidate restoring it byte-identically passes C1–C6 and is applied by overlay
  (no deletions). Restoring two live reference files verbatim into the
  slimmed `hgk-governed-execution` candidate makes the round's own C1–C6 harness pass with zero references
  lost (112 accounted: 89 byte-identical, 23 embedded; main file 21,026 bytes). The apply SHALL be guarded:
  pre-image, receipt, rehearsed rollback, post-apply re-measure, loader sanity.
- **R9-C — record corrections.** `R8-F7` is **resolved** by the package's own wording (`ACC-RQ06` names
  "AVR/10-piece" and "HGK/6-piece" byte reconstruction; measured HGK 6 slices, AVR 10 markers). `R8-F4` is
  **recalibrated**: the package states no size cap, yet a real platform limit exists —
  `MAX_SKILL_CONTENT_CHARS` = 100,000 **characters** enforced on the LF-normalized `len()`
  (`tools/skill_manager_tool.py:111/:192/:488`), which is not the byte-based constant the R8 harness
  recorded — and the stack's own SKILLCAP-20261007 research warns that both the disk-byte figure (105,116)
  and the raw-CRLF figure (101,219) misjudge it, 105,116 being precisely the live-size number R8-F4 cited. `R8-F6`/`R8-D1`'s claimed `DRIFT_VALUE` **does not reproduce**
  (`check_drift` returns `[]`); what holds is that a drift-clean registry is not a mandate-conformant one.
  `TF-06` is **closed with a corrected reading**: the served arm is recoverable from the dispatch receipt's
  `attempts[]`, and the R8 VERIFY turn was served by its lane's rank-2 fallback.
- **R9-E — independent verification.** The R9 checker turn is served on the mandated rank-1 arm and its verdict is
  adjudicated item by item: corrections this round accepted, explanation where the checker misread a count, and its
  own self-reported procedural breach recorded rather than discarded. The round's claim ceiling is unchanged by
  four confirmations.
- **R9-D — FAR run receipt.** `FAR-20261016-012-r9-residual-closure` under route `FAR_ROUTE_NATIVE_ARIS`, with
  the contract artifact set, the rejected-alternative ledger and the open-question ledger for the owner.

## Capabilities

### New Capabilities
- `r9-far-residual-closure`: the FAR decision surface and the executed-repair acceptance shape for this round.

### Modified Capabilities
None. No canonical capability is modified by this proposal.

## Impact
- Intended surfaces: the R8-0 hardening worktree (`validate.py` only), the canonical skill tree for one skill
  (guarded apply), and this round's evidence root. No route, registry, epoch, admission, spine or product
  release surface is edited by this change.
- Inputs: FAR run `runs/FAR-20261016-012-r9-residual-closure/` (21 artifacts), `R9_OWNER_READY_*.json`, the
  R8 records it corrects, and the receipts it re-reads. All at LOCAL / candidate-only ceiling.

## Out of scope / Non-goals
No registry or epoch edit, no spine access, no admission write, no git write command, no publication, no
merge, no acceptance, no Gate PASS, no AO verdict, no release. The already-proposed R1/R2/R3 of
`hgk-far-remediation-20261016` are cited, not re-authored, and are not applied here.

## NON-CLAIMS — this proposal is not an acceptance

A passing test pair, a green harness run, a completed FAR run and a validated proposal are **local candidate
evidence**. None of them is an independent acceptance, a DOC-05 admission, a Gate PASS, an AO verdict or a
release decision. The 221 planned acceptance cases remain unexecuted, the eight Gates remain unpassed, Fresh
G1 remains uncertified and the external report's `FAIL_CLOSED` production decision is unaffected.

## Blocked items
- Owner acts: the PLAN rebind (already proposed), the checker identity / write root, the skill candidate's
  canonical-accept policy, the taskspec-id derivation fix, the 221/Gate/Fresh-G1 applicability, source #6.
