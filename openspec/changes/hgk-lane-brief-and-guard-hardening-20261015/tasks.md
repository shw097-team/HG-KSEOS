# Tasks

Task header convention: `[TF-nn|applicability]` where applicability is `NOW` (this change's lane
authority covers the edit) or `BLOCKED-owner` (control-plane or product-owner authorisation
required before the edit is applied). Every task names its acceptance evidence and every claim
carries a deterministic positive/negative/boundary test on recorded raw inputs.

## 1. Guard marker matching (TF-01) — `HG-KSEOS/scripts/hgk-lane-dispatch.py` — NOW

- [ ] 1.1 [TF-01|NOW] Classify a remote-write marker occurrence by command context, not bare words:
      require a shell-looking occurrence (a line beginning with `git`/`gh`/`curl`/`ssh`/`winget`, or
      an argv-shaped form) — evidence: new tests under `HG-KSEOS/tests/` on **recorded raw briefs**
      from the round (`lane_runs/EXECUTE_dispatch_receipt_attempt1.json` and the second refusal
      receipt); negative test: both recorded prose briefs classify non-marker and the dispatch
      proceeds; positive test: a literal `git push <url>` line and an argv form still classify as a
      marker; boundary test: `do not run git push` on its own line stays prose, but a prohibition
      sentence containing a command-shaped line is still a marker (fail-closed).
- [ ] 1.2 [TF-01|NOW] Keep `detection_only` semantics; the dispatcher stops REFUSING a dispatch on
      prose matches — evidence: same recorded briefs replayed through the classification table in a
      deterministic harness; the detection path still fires, the refusal code
      `ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED` is emitted only for context-matched markers.

## 2. Guard subject definition and intra-turn sampling (TF-08, TF-09) — same script — NOW

- [ ] 2.1 [TF-08|NOW] Define the guarded subject as the tracked (packet) file set where the subject
      sits in a VCS tree; treat ignored byproducts (`__pycache__/`, `*.pyc`, …) as
      `added/removed — recorded, not fatal` — evidence: recorded raw guard output from R7 attempt 2
      (`changed=0 removed=1`, `RUNNERS/__pycache__/probe_lib.cpython-311.pyc`) replayed: outcome is
      the recorded-not-fatal code, NOT a void verdict; negative test: a tracked-file removal still
      voids (fail-closed boundary); positive test: where no VCS is available, the brief's declared
      ignored-pattern list is consumed instead and the whole guard stays fail-closed.
- [ ] 2.2 [TF-08|NOW] Record every ignored-path add/remove in the guard receipt (hygiene leaves a
      trace) — evidence: receipt schema test asserting `ignored_*` rows survive the not-fatal path.
- [ ] 2.3 [TF-09|NOW] Sample the guarded subject digest during the turn (bounded sampler, capped
      iterations/sweep; no race-based comparators) instead of comparing only the end state —
      evidence: harness test using recorded receipts from R7 attempt 3 (13 in-place RAW writes
      restored by the checker): the guard outcome is `CLEAN_WITH_INTRATURN_WRITES` +
      `intra_turn_violation` rows, never a silent `CLEAN`; boundary test: no intra-turn writes
      reported produces no new fields and the plain `CLEAN` outcome is unchanged.
- [ ] 2.4 [TF-07/HG-KSEOS half|NOW] Make the standing dispatch-brief template state every guarded
      subject path explicitly and declare a writable output root OUTSIDE each subject (the R7-0
      practice, now standing text) — evidence: the brief template in the round's evidence records
      contains the subject-path block, checked by a static template test.

## 3. Nonce-carrier attribution (TF-06) — receipt record — NOW (root-cause fix BLOCKED-owner)

- [ ] 3.1 [TF-06|NOW] Record per-attempt the nonce carrier surface probed (wrapper echo path, relay
      path, none-probed) next to the existing `nonce_absent_arms` record — additive receipt fields
      only — evidence: receipt schema test; the recorded receipts from R6/R7 attempts
      (`ok=false ERR_NO_ARM_EMITTED_NONCE`, `usage_receipt_ok=true`,
      `nonce_absent_arms=[opencode-go/deepseek-v4.1-flash]` and the VERIFY lane's
      `opencode-go/glm-5.3-flash` row) replay through the new record shape unchanged (old consumers
      keep matching the old fields).
- [ ] 3.2 [TF-06|BLOCKED-owner] Root-cause fix of the wrapper/relay nonce echo path so
      `require==served` can be shown positively — control-plane surface, owner authorisation
      required before implementation; not claimed here. — evidence: an owner-signed rectification
      record naming the approved surface; absence of that record = task stays unexecuted.

## 4. Lifecycle admission correction (TF-02) — `hg_kseos.lifecycle` — BLOCKED-owner

- [ ] 4.1 [TF-02|BLOCKED-owner] Derive `taskspec_id` from a full project-id digest (or a spine-wide
      counter) so two projects for the same mission no longer collide on the spine UNIQUE
      constraint — evidence: a deterministic spine test (local test spine, no production DB) binding
      the two colliding mission ids recorded in `HGK_TYPED_ADMISSION_R6R7.json` /
      `R7_BLOCKERS_AND_TASKS.json BLK-R7-08` and asserting distinct ids.
- [ ] 4.2 [TF-02|BLOCKED-owner] Resolve WorkOrder `base_head` from the project's declared
      `target_root` instead of the ambient process cwd — evidence: harness test invoking admission
      from a non-repo cwd against a recorded target_root fixture and getting a resolved head, not
      `ERR_WORKORDER_CRITICAL_FIELD_MISSING`.
- [ ] 4.3 [TF-02|BLOCKED-owner] On workorder-field failure, return a typed error instead of
      persisting a taskspec first — evidence: harness test asserting zero spine rows remain after a
      failed admission attempt.
- [ ] 4.4 Gating note: 4.1–4.3 may only be executed when an owner authorisation for a control-plane
      change is recorded in this change's evidence directory; the tasks remain unexecuted
      placeholders otherwise.

## 5. PIPD driver output isolation (TF-07, TF-09) — `probe_mutations.py` — NOW

- [ ] 5.1 [TF-07/TF-09|NOW] Add `--out-dir`/`DEST` to `probe_mutations.py` so a re-run writes its RAW
      receipts and `mutation_records.json` only where it is told; keep the historical default only
      behind an explicit flag that refuses to default into any declared guarded subject —
      evidence: harness test reading the recorded R7 attempt-3 flow (`RAW/mut_m*.json` written to a
      declared out-dir); negative test: a run with no `--out-dir` and a target defaulting inside a
      guarded subject refuses with a typed refusal instead of writing.
- [ ] 5.2 [TF-07|NOW] Cross-check: the driver's declared out-dir is validated against the brief's
      guarded-subject list (reject when it resolves inside a subject) — evidence: harness test with
      the R6_DELIVERY path from the round as subject and an out-dir inside it: refusal, zero writes.

## 6. PIPD provenance and test-fixture honesty (TF-03, TF-05) — NOW

- [ ] 6.1 [TF-03|NOW] Adopt the WriteSet + unified-diff pair as the standing provenance convention
      for this non-VCS tree (WriteSet: path/bytes/sha256 + pre-hash; diff via `diff -u` or
      `git diff --no-index`); record as standing convention text next to the writer-receipt —
      evidence: the convention record file existing in the round evidence and the R7-0 writer
      receipt (`R7_WRITER_RECEIPT.json`) satisfying it as its worked example.
- [ ] 6.2 [TF-05|NOW] Make `tests/test_publication_projection.py` and
      `tests/test_tooling_executes.py` skip with an explicit missing-ref reason when
      `r5-s4-candidate` is absent instead of failing — evidence: local pytest run on this host (257
      records not git-providing a ref today) asserting those tests report `skipped` with that
      reason; negative test: when a ref IS available the tests still run and exercise their normal
      path; the rest of the suite's counts unchanged apart from these skips.
- [ ] 6.3 [TF-05|NOW] Checker classification task (pre-existing vs introduced failures recorded
      separately, not relabelled) — evidence: the classification record existing in the round's
      evidence tree and naming the 7 pre-existing failures with their codes.

## 7. Operating guidance (TF-04) — documentation only — NOW

- [ ] 7.1 [TF-04|NOW] Record in the round's operating guidance: verify on-disk bytes before editing
      a credential-adjacent line — the terminal rendering may be a redaction (`Bearer ***`), not the
      file content — evidence: the guidance entry existing in `R7_NON_CLAIMS.md`-adjacent operating
      records (Hermes-display behaviour, no product change).

## 8. Closure gates

- [ ] 8.1 Deterministic tests only: no test in this change depends on the network, a real model, the
      relay, a real credential value, or the real R6/R7 evidence tree being writable — the recorded
      raw inputs are fixtures.
- [ ] 8.2 Candidate-only constants hold: no promotion, no archive, no main-spec write, no
      `config/` or route edit, no product-repo semantic change, no git write command, no host
      outside the workspace touched.
- [ ] 8.3 Each surface's implemented fix gets an independent checker lane before any verdict is
      recorded; maker self-check rows are never verdicts.
- [ ] 8.4 NON-CLAIMS boundary observed: implementing and even passing a test is not an acceptance —
      this change closes a finding only when its acceptance evidence exists AND an independent
      checker has run on that surface.
