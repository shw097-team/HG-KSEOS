## 1. T1 — C1: verdict artifact contract (pre-creation + skeleton refusal)

- [ ] 1.1 Confirm the runner pre-creates `<workdir>/VERDICT.json` with every item `INCONCLUSIVE` and `updated_by_checker: false` BEFORE the checker turn is dispatched
- [ ] 1.2 Confirm the post-condition refuses a missing artifact, an unparsable artifact, and an artifact whose `updated_by_checker` is not true — each with `ERR_VERIFY_NO_VERDICT` and a non-zero exit
- [ ] 1.3 Record the receipt fields that expose the distinction (`verdict`, `verdict_updated_by_checker`, `verdict_is_skeleton_only`)
- [ ] 1.4 Build the deterministic stand-in checker (no model calls) that simulates: full verdict, no write, skeleton-only, and kill-after-k-writes
- [ ] 1.5 Prove the three acceptance classes: POSITIVE (truncated budget still leaves a partial verdict), NEGATIVE (pre-creation removed -> nothing; untouched skeleton -> refused; exit 0 with no file -> refused), BOUNDARY (kills at k = 0, 1, mid-list, after a final PASS write)
- [ ] 1.6 For every negative case, state why it discriminates — a case that would also pass with the defect present counts for nothing

## 2. T2 — C2: bounded shard schedule and per-lane budget

- [ ] 2.1 Import the audit's item ids from the verification brief and assert the schedule carries each exactly once
- [ ] 2.2 Read the ceiling from the checker model's OWN catalogue entry selected by slug; record the first-match value (334800) as the trap it is
- [ ] 2.3 Record per-shard predicted peak input tokens and the headroom rule applied
- [ ] 2.4 Implement `ERR_LANE_CONTEXT_BUDGET_EXCEEDED`: measure a lane's own peak `usage.inputTokens` from the relay ledger inside the lane's window and fail closed above budget
- [ ] 2.5 Keep each shard's artifact, log and receipt separate from every other shard's

## 3. T3 — C3: pre-baked fixture pack

- [ ] 3.1 Build the discriminating fixtures: declared≠served identity; body-mentions-but-header-agrees (false-positive control); unreadable header (no vacuous pass); untouched artifact after a truncated budget; out-of-boundary sibling directory
- [ ] 3.2 Emit `MANIFEST.sha256` plus a single `pack_digest` over the sorted file digests
- [ ] 3.3 Prove determinism (two builds, identical digest) and non-vacuity (one modified byte fails the check)
- [ ] 3.4 Present the pack read-only to consumers and state the portable check a checker lane runs

## 4. T4 — C4: parallel lane isolation

- [ ] 4.1 Give each concurrent lane its own runtime home materialised from the sealed config (no shared mutable home)
- [ ] 4.2 Replace the global mutex with a per-lane lock and keep orphan cleanup scoped to the lane's own process ids, never a command pattern
- [ ] 4.3 Record each lane's declared write scope in its receipt so a collision would be detectable afterwards
- [ ] 4.4 Verify no credential is copied when a lane home is materialised

## 5. T5 — Automated detect / repair / verify loop

- [ ] 5.1 Drive EXECUTE -> post-condition check -> typed failure -> repair -> re-dispatch as a bounded loop with an explicit stop condition
- [ ] 5.2 Classify each failure and count it PER CLASS, not per session; stop and report rather than retry an unmitigated class a fifth time
- [ ] 5.3 Report the loop's terminal state honestly: `PARTIAL` when no acceptable verdict exists, never rounded up to done

## 6. T6 — Independent verification (GLM-5.3-Flash checker lanes)

- [ ] 6.1 Dispatch at least one shard lane under the new budget and pre-creation contract
- [ ] 6.2 Require a verdict artifact with `updated_by_checker: true`, per-item outcomes and explicit `INCONCLUSIVE` markers
- [ ] 6.3 Treat the verdict as an advisory independent check; owner acceptance remains `NOT_RUN`
- [ ] 6.4 Record the checker's identity evidence from non-introspective sources only (relay model field, anchored run header, config)

## 7. T7 — F11: shape validation of the verdict artifact (bounded repair lane 11, decided by FAR `DEC-018-1`)

- [x] 7.1 Re-measure the defect: execute the runner's own post-condition against every shard verdict file and show an artifact accepted with no overall verdict (measured: 1 of 7 lanes, S8)
- [x] 7.2 Rewrite the post-condition to require an exact-`true` flag, an enumerated top-level `verdict`, a non-empty `per_requirement` with usable item results, and no overall `PASS` over an unresolved item; three distinct tokens (`ERR_VERIFY_NO_VERDICT` preserved, `ERR_VERIFY_VERDICT_SHAPE`, `ERR_VERIFY_VERDICT_OVERCLAIM`)
- [x] 7.3 Prove it with positive/negative/boundary cases plus a discrimination run against the verbatim pre-repair predicate, under two encodings (lane 11: 40 tests; PLAN re-check: 13 independent cases + the real S8 artifact now refused)
- [x] 7.4 Do not disturb any pinned artifact: the edit is outside lane 10's `F5-LANEHOME-RESOLVE` digest-pinned region and outside the file `c1` pins (measured: `disturb=false` for both)
- [x] 7.5 Provide a tested rollback (`candidate/w6/c2/repair11/rollback_f11.py --check`): restores the 722-byte original region (sha256 `019828d9…`, body `1e981579…`) and is verified by `bash -n` and by the old behaviour returning on S8
- [x] 7.6 Record this requirement in the spec so the contract is not narrower than the implementation
- [x] 7.7 INDEPENDENT CHECK: performed by an `opencode-go/glm-5.3-flash` checker lane (`verify/shards/S11`, attempt 2): 8/8 items PASS, `verdict: PASS`, exit 0, identity read from the startup header; the PLAN plane re-measured the verdict and corrected one evidence line (F11E's F5-region digest span) — see `verify/shards/S11/PLAN_RECHECK_S11.md`. On F11's own scope the contract's elements are now all present (implementation, discriminating tests, evidence, tested rollback, independent check). Owner acceptance remains `NOT_RUN`; F9 / F10 / F13(b)(c) remain open outside this scope
