# Tasks

Header convention: `[finding|class]` where `EXECUTED-CANDIDATE` means the work was done this round under the
round's admission and remains candidate-only, and `OWNER-BLOCKED` requires a named owner act.

## 1. R9-A — validator adaptation

- [x] 1.1 [R8-WS2|EXECUTED-CANDIDATE] Specify the two bounded hunks in `validate.py` (derive the binding from
  the bundle's own atoms only when no frozen context is supplied; guard the `risk_guard`/oracle mapping
  access) with exact before/after text, and dispatch them to the bounded-writer lane.
- [ ] 1.2 [R8-WS2|EXECUTED-CANDIDATE] Acceptance: `test_real_trace_link_is_legal_beside_its_endpoints` and
  `test_cli_smoke_runs` both pass on the adapted tree, **and** the M04/M06/M16 probes each still report
  `observed=REJECT`. Evidence: raw test output plus the probe JSON, in the round's `WS_A/`.
- [ ] 1.3 [R8-WS2|EXECUTED-CANDIDATE] Re-run the full local suite on the adapted tree and record the counts
  and duration; report a changed count rather than adopting it.

## 2. R9-B — guarded apply of the repaired skill candidate

- [x] 2.0 [R8-F5|EXECUTED-CANDIDATE] Refusal record: the first repaired candidate FAILED the round's own C6 gate
  in two independent runs (the bounded-writer lane and the orchestrator): `live_references: 113, lost: 1`, the
  missing file being `references/product-branch-write-set-gates.md` (4986 bytes). No canonical byte changed.
- [x] 2.1 [R8-F5|EXECUTED-CANDIDATE] Author and verify the successor candidate (`CANDIDATE_V2` = the first
  candidate plus that one file restored byte-identically); the round's own harness returns `overall PASS` with
  all of C1–C6 passing. The restore was authored by the ORCHESTRATOR (disclosed), additive and byte-identical to
  live.
- [x] 2.2 [R8-F5|EXECUTED-CANDIDATE] APPLIED: canonical `hgk-governed-execution` `SKILL.md` 105116 -> 21026 bytes
  by non-destructive overlay (zero deletions; 21 canonical-only paths retained), post-apply C1-C6 all PASS
  (113 live references, 0 lost) in the lane AND re-derived by the orchestrator, rollback drill OK on a copy,
  loader row `local / enabled`.
- [ ] 2.2b [R8-F5|EXECUTED-CANDIDATE] Apply the successor BY OVERLAY (no deletions) with a byte-for-byte pre-image,
  an `APPLY_RECEIPT.json`, a rehearsed rollback on a copy, a post-apply C1–C6 pass on the live tree, and a loader
  sanity row. Dispatched as `WS_R9B2_WRITER_BRIEF.md`.
- [x] 2.3 [R8-F5|EXECUTED-CANDIDATE] If the post-apply gate fails or the loader cannot select the skill, roll back,
  re-verify the pre-image digests and report the failure with its raw output.


## 2b. Independent verification (this round's checker)

- [x] 2b.1 [VERIFY|MEASURED] The R9 VERIFY/SECURITY turn ran on the mandated arm: receipt attempts[0] rank 1
  `openai-codex/gpt-6.1-sol` (768.19 s), identity gate listing only rank 1. The round's successor wrapper
  `dispatch_r9.py` pins rank 1 for the checker, unlike the R8 wrapper.
- [x] 2b.2 [VERIFY|ADJUDICATED] Checker overall `UNVERIFIABLE` (2 of 7 claims CONFIRMED). Every disagreement
  adjudicated in `R9_VERIFY/R9_VERDICT_ADJUDICATION.json`: 4 defects in THIS round's artifacts/brief corrected or
  accepted, 1 count explained, the checker's own self-reported temp-write breach recorded verbatim, and the
  checker-side limitation (its no-git guard cannot run a fixture that creates a git repository) recorded rather
  than rounded up.
- [x] 2b.3 [VERIFY|CORRECTED] Corrections forced by the checker: the package byte count (2580690 -> 2689181);
  the stale PLAN-route claim (rebound by an act OUTSIDE this round at 2026-10-16T12:36:30, epoch 21); two defects
  in this round's own verifier brief (a non-existent FAR path and an undefined `evidence_ref` column); and the
  precision that the `r8-wt` delta includes the pre-existing R8-0 hardening files.

## 3. R9-C — record corrections

- [x] 3.1 [R8-F7|RESOLVED] Record that `ACC-RQ06` names AVR/10-piece and HGK/6-piece reconstruction, and that
  the measured partition is 6 HGK slices and 10 AVR markers; withdraw the "10/6 is inconsistent" reading.
- [x] 3.2 [R8-F4|EXECUTED-CANDIDATE] Recalibrate the size framing: no package clause states a cap;
  `MAX_SKILL_CONTENT_CHARS` (100,000 characters, LF-normalized) is the platform limit and is not the byte
  constant the R8 harness recorded.
- [x] 3.3 [R8-F6/R9-D1|MEASURED] Record that `check_drift` returns `[]` on the canonical registry and that the
  R8 `DRIFT_VALUE` claim does not reproduce as stated; keep the surviving fact (routes[].PLAN disagrees with
  the pool, the file's own SoD text and today's mandate — registered there as `F1-PLAN-ROUTE-ROW-OUTLIER`).
- [x] 3.5 [R9-F6|EXECUTED-CANDIDATE] Harness reporting defect recorded: the C1–C6 harness serialises its
  `subject_live` field before honouring `--live`, so a receipt can name the wrong live tree while the CHECKS used
  the right one.
- [x] 3.6 [R9-F8|MEASURED] The round's own dispatch wrapper pinned `VERIFY_SECURITY` to `--force-rank 2`
  (`opencode-go/glm-5.3-flash`), so the mandated rank-1 checker was never attempted; corrected in the round's
  successor wrapper `dispatch_r9.py` (rank 1 = `openai-codex/gpt-6.1-sol`), with the predecessor backed up and
  the deviation disclosed.
- [x] 3.4 [TF-06|CLOSED-WITH-CORRECTION] Arm attribution is recoverable from `attempts[]`; the missing nonce
  voids completion attestation only. Record that the R8 VERIFY turn ran on its lane's rank-2 fallback and that
  the standing failover rule permits it, with the verdict's provenance stated.

## 4. R9-D — FAR receipt and owner handover

- [x] 4.1 [FAR|EXECUTED-CANDIDATE] Produce the contract artifact set for
  `FAR-20261016-012-r9-residual-closure` including the rejected-alternative and open-question ledgers.
- [x] 4.2 [OWNER|OWNER-BLOCKED] Hand over the one-action records: the PLAN rebind (already proposed in
  `hgk-far-remediation-20261016` R1 — cite, do not duplicate), the checker identity/write root, the skill
  candidate's canonical-accept policy, and the taskspec-id derivation fix.

## 4b. Findings registered this round

- [x] 4b.1 [R9-F9|MEASURED] The checker cannot re-run a fixture that creates a git repository under its own
  no-git-write guard: the named two-test pair is UNVERIFIABLE from its seat (it ran a disclosed adapted fixture).
- [x] 4b.2 [R9-F10|CORRECTED] The package byte count recorded by this round was wrong (2580690 vs the measured
  2689181; the approved digest was unaffected).
- [x] 4b.3 [R9-F11|MEASURED] The dispatcher reported `ERR_NO_ARM_EMITTED_NONCE` for a turn that DID emit its nonce
  into its own artifacts; the receipt's `used_*` fields stay null, so the arm must be read from `attempts[]`.
- [x] 4b.4 [R9-F12|MEASURED] The canonical PLAN route was rebound to the mandated arm by an act outside this round;
  `VERIFY_SECURITY` `admission_status` remains UNPROVEN.

## 5. Not authorised this round

- [ ] 5.1 [221 cases / 8 Gates / Fresh G1|OWNER-BLOCKED] Human gates; not executed, not approximated.
- [ ] 5.2 [EIA-R6-03|OWNER-BLOCKED] A single Windows identity cannot separate maker from checker; the
  identity/sandbox decision belongs to the owner.
