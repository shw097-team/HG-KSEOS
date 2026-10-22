## 1. Contract freeze and baseline

- [ ] 1.1 Freeze the source package digests (`hgk_checker_upgrade` files) and the candidate base HEAD into the round evidence root
- [ ] 1.2 Record the pre-existing suite baseline (test count, failures, errors) before any candidate edit

## 2. Checker bridge package (candidate)

- [ ] 2.1 Create `src/hg_kseos/checker_bridge/runner.py`: snapshot digesting with symlink refusal, intake validation, staging/snapshot non-overlap, advisory verdict staging, post-run mutation detection
- [ ] 2.2 Create `src/hg_kseos/checker_bridge/watchdog.py`: pure `assess()` decision + `scan()` emitting diagnosis/pause requests
- [ ] 2.3 Create `src/hg_kseos/checker_bridge/binding.py`: candidate binding record + identity-field assertion
- [ ] 2.4 Create `src/hg_kseos/checker_bridge/advisory_verdict.schema.json` and a validator that rejects non-advisory tokens
- [ ] 2.5 Create `config/checker/checker-binding.candidate.json` and `config/checker/monitor-policy.json`

## 3. Bridge qualification (fail-closed)

- [ ] 3.1 Add the bridge preflight probe (loopback-only, positive-only, cannot promote)
- [ ] 3.2 Attempt live qualification of Codex CLI → bridge → OpenCode Go GLM-5.3-Flash and record the raw outcome
- [ ] 3.3 Record `BLOCKED_HITL` / `NO_CUTOVER` if the bridge is unsupported in the pinned environment

## 4. Tests

- [ ] 4.1 Positive: a mock checker stages an advisory verdict and leaves the snapshot untouched
- [ ] 4.2 Negative: candidate mutation, symlink snapshot, incomplete intake, digest mismatch, out-of-enum verdict, staging overlap
- [ ] 4.3 Watchdog: four repeats do not pause; the fifth after verified progress does; a different signature does not accumulate; stale heartbeat pauses; corrupt state fails closed
- [ ] 4.4 Security: poisoned repository instruction cannot escalate the checker role; permission escalation attempt fails closed

## 5. Detection and self-repair loop

- [ ] 5.1 Run the checker-bridge suite plus the full HG-KSEOS suite and diff against the frozen baseline
- [ ] 5.2 Repair any candidate defect through the tracked writer on a NEW commit and re-run
- [ ] 5.3 Confirm the failure set is a subset of the frozen baseline (no new failures introduced)

## 6. Independent verification

- [ ] 6.1 Freeze the candidate commit and snapshot canonical digests before/after the verify lane
- [ ] 6.2 Run an independent VERIFY_ONLY lane on a different model from the maker and capture the raw verdict
- [ ] 6.3 Adjudicate the verdict: re-measure every disputed fact from the raw artifact

## 7. Evidence and owner gate

- [ ] 7.1 Produce the single-file evidence MD with claim ceiling, binding, raw index, gates and nonclaims
- [ ] 7.2 Mirror the evidence MD byte-identically into the review roots and verify SHA-256 equality
- [ ] 7.3 Leave shadow/cutover as `BLOCKED_HITL` for the owner gate (COV-11-06); do not self-enable
