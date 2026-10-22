## 1. Contract freeze and baseline

- [x] 1.1 Digest the file under edit before the change (`scripts/hgk-lane-dispatch.py` pre-change sha256 + a `.bak` copy in the round evidence root)
- [x] 1.2 Record the pre-existing suite baseline: full discovery fails 8 tests + 2 errors, and the SAME ten IDs fail with the two edited files reverted to their backups, so none of them is caused by this change

## 2. Harness hardening (candidate)

- [x] 2.1 `persist_attempt_logs()` writes full stdout/stderr byte-exactly (`newline=""` so Windows does not rewrite `\n` as `\r\n`) and returns path/bytes/sha256
- [x] 2.2 `default_identity_requirement()` + `identity_check()` + `probe_cli_login()` + `probe_relay_pool_health()`
- [x] 2.3 Pre-spawn gate in `main()` with a whole-lane refusal when no arm survives
- [x] 2.4 `--require-arm` fails closed instead of degrading; `ERR_LANE_REQUIRED_ARM_ABSENT` when the named arm is not in the pool
- [x] 2.5 `--guard-subject` pre/post digest snapshots + `ERR_CHECKER_MUTATED_SUBJECT` receipt voiding
- [x] 2.6 Declare `identity_requirement` per CODEX-CLI arm in `config/lane-route-slots.candidate.json` (additive; resolver re-validated)

## 3. Tests

- [x] 3.1 Positive: a key arm passes the gate with an empty lane home; an OAuth arm passes with refresh material; a declared `cli_login` arm passes with tokens
- [x] 3.2 Negative (end-to-end, spawns nothing): a required OAuth arm is refused with `ERR_RELAY_OAUTH_NEEDS_REAUTH` and no attempt log is created; an absent required arm is typed
- [x] 3.3 Boundary: an expired access token is NOT a failure; an unknown `identity_requirement` is typed, never ignored; an added file does not void while a changed or removed file does; a bare file root is snapshot-able
- [x] 3.4 Persistence: the stored stdout is byte-identical, larger than the 400-char tail, and digest-matches

## 4. Live lane evidence

- [x] 4.1 E5 negative: a checker ordered to mutate the guarded subject has its verdict VOIDED by measurement
- [x] 4.2 E6 positive: an escalated checker independently re-derives the digests of the changed artifacts
- [x] 4.3 E7: the OAuth arm runs unattended through the gate with `--require-arm openai-codex/gpt-6.1-sol`
- [x] 4.4 E8: an unhealthy relay home produces the typed refusal end-to-end

## 6. Hostile-review iteration (every item has a regression test)

- [x] 6.1 F1 `--require-arm` is enforced outside the gate branch, verified on its own when the gate is skipped, and judged against the PRE-gate candidate set
- [x] 6.2 F2 the pool's declared `identity_requirement` is carried into the evaluated arm; a typo now refuses end to end
- [x] 6.3 F3 health reads parsed content: non-empty refresh token required, re-auth marker refuses, empty CLI credential is not a login
- [x] 6.4 F4 an escalated lane with no guard root is refused unless the exception flag records it
- [x] 6.5 F5 (residual, disclosed) transient modify-and-restore is not detectable by a before/after comparison
- [x] 6.6 F6 harness output inside a guard root is refused (`ERR_GUARD_ROOT_CONTAINS_HARNESS_OUTPUT`)
- [x] 6.7 F7 the child's raw bytes are persisted and flagged byte-exact; non-UTF-8 round-trips
- [x] 6.8 F8 attempt logs carry the run id and no longer collide across runs
- [x] 6.9 F9 a negative `--max-candidates` is a typed refusal and the empty-candidate path cannot crash
- [x] 6.10 F11 the required arm must be SERVED (`ERR_REQUIRED_ARM_NOT_SERVED`), not merely admitted
- [x] 6.11 F12 the mode label no longer counts a synthetic injected-429 entry as the first attempt
- [x] 6.12 F13 (residual, disclosed) the gate probes the relay HOME while the turn uses the relay URL; the two are recorded but not cross-validated
- [x] 6.13 D-4 (found by this round's own probe E5b) a guard root that does not resolve is refused instead of yielding a vacuous "clean" snapshot

## 7. Regime-correct regression measurement

- [x] 7.1 The earlier baseline was taken WITHOUT `PYTHONPATH=src`, where three of the ten failures were only `ModuleNotFoundError`; the A/B is re-measured in both regimes against the repo's canonical runner


## 5. Disclosed, not done

- [x] 5.1 Cross-model checker separation NOT implemented (owner-mandated single model stands); recorded as a ceiling
- [x] 5.2 Dedicated relay-pool account NOT performed (needs one interactive auth); runbook + acceptance test prepared
- [x] 5.3 Independent verification of this change is dispatched to separate checker lanes; their verdicts are advisory and are reported with their own ceilings
