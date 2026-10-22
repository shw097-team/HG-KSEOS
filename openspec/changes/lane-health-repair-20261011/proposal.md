# Proposal: make the lane dispatch path stop reporting what it did not measure (round FAR-LANE-HEALTH-REPAIR-20261011)

## Why

Round `FAR-LANE-HEALTH-REPAIR-20261011` FAR-researched the findings of the lane-health diagnosis
(`var/lane-health-20261011/LANE_HEALTH_DIAGNOSIS.md`) and measured that the reported "the VERIFY/SECURITY
lane is abnormal" reduces to **one mechanism with four faces: a declaration was written and nothing
consumed it.** The OAuth arm itself is healthy (three live probes `ok: true`, served
`openai-codex/gpt-6.1-sol`, nonce present, usage receipt 200, guard clean).

1. **One code, two conditions.** The receipt's code is assigned at a single site
   (`scripts/hgk-lane-dispatch.py`, `receipt["code"] = "ERR_LANE_ALL_ROUTES_EXHAUSTED"`). A run in which
   every responding arm returned `exit 0` with a valid usage receipt but **no nonce** (measured: another
   session's smoke, candidates `[1,2,3,4]`, rank 4 exit 0 in 16.22 s with `usage 200 openai-p6a1fe3`,
   `nonce_present: false` on all) reads identically to a run in which **nothing was reachable**
   (measured: this round's bounded rank-2 probe, `exit TIMEOUT`, 90.03 s).
2. **A declared capability with no consumer.** The pool artifact declares the nvidia arm
   `CONFIG_COMPLETE_NOT_ACTIVATED` (`relay_http: 400`, "unblock: one relay restart"). The relay **has**
   since restarted (pid 15656 -> 2052, 08:32:28 2026-10-11) so the declaration is stale, and nothing in
   the dispatcher reads `feasibility` at all, so the arm is still spawned and burns its full timeout
   (240.04 s in another session's smoke; 90.03 s in this round's probe) on every fallback path.
3. **A gate asserting a property it never measured.** `identity_check(...)` certifies key-auth arms as
   `"no human-attended identity"` **without reading the resolved Codex home**. Another session's receipt
   shows `identity_gate.lane_home = C:\Users\user\.codex`, a home that holds `auth.json`. The pool
   declares transports **per arm**, but `--codex-home` is a **per-run** flag, so reaching one arm via the
   human home silently gives every key-auth arm in the run the human credential while the receipt still
   certifies them as non-human-attended. That is a false green.
4. **A frozen manifest made stale by design.** The previous round's freeze binds
   `scripts/hgk-lane-dispatch.py`'s digest and that manifest's own digest is cited inside documents
   already published to a public repository, so any repair makes the binding stale. The record must stay
   honest without rewriting history.

## What changes

1. The single receipt-code site classifies additively: `ERR_NO_ARM_EMITTED_NONCE` (with a
   `nonce_absent_arms` list) when arms answered without a nonce, `ERR_ALL_ATTEMPTS_TIMED_OUT` (with
   `timed_out_arms`) when no attempt returned, and `ERR_LANE_ALL_ROUTES_EXHAUSTED` remains the fallback.
   `ok` stays `false` and the non-zero exit is unchanged -- the acceptance rule is not relaxed.
2. The pool declaration is completed with the measured state and given a **consumer**: an arm the
   artifact declares not dispatchable is skipped before spawn, recorded in `skipped_arms` with its
   reason, and an explicit `--force-rank` still reaches it (the measurement is overridable, not hidden).
3. The resolved Codex home is folded into the identity verdict: a non-isolated home holding `auth.json`
   refuses pre-spawn with `ERR_LANE_HOME_NOT_ISOLATED` unless `--allow-human-home-transport` is passed,
   and every receipt records `codex_home_is_declared_lane_home`.
4. A **supersession record** names the superseded freeze and digest, the retired path digests, the
   successor freeze, and the rule that a freeze binds the bytes at its own time.

## Non-goals

- Not a promotion. The pool artifact stays `status: CANDIDATE`; the change is a candidate pack.
- Not a fix for the nvidia arm itself, and not a removal of it: this change makes its measured state
  honest and gives it a consumer. Whether the arm should exist at all is the owner's call.
- Not a redesign of the resolver to carry a per-arm home/transport (left OPEN as `OQ2`).
- Not an acceptance. Acceptance requires the independent VERIFY/SECURITY checker lane.

## Risks and limits

- The skip rule must not over-block: a declared-dispatchable arm must be completely unaffected, and a
  `--force-rank` pin must still reach a skipped arm. Both are test-covered.
- The classification is additive but changes which code a previously-generic failure reports; any
  consumer matching on the old code keeps working because the fallback is preserved.
- A guard/identity refusal is still a refusal: no new path may spawn after a refusal.
