## Purpose

Define the externally observable behaviour of the CODEX-CLI lane dispatch path when it reports the
outcome of a turn: what a receipt is allowed to claim, which declarations it must consume, and which
identity properties it may not assert without measuring. This capability extends the surface defined by
`ao-lane-independent-verify`; it does not replace it.

## ADDED Requirements

### Requirement: A receipt distinguishes "no arm reachable" from "arms answered without the nonce"
The dispatch SHALL NOT report one code for both conditions. When at least one attempt returned
`exit == 0` with a valid usage receipt and none of those attempts emitted the nonce, the receipt SHALL
carry `ERR_NO_ARM_EMITTED_NONCE` and a non-empty `nonce_absent_arms` list naming those arms. When at
least one attempt was made and every attempt timed out, the receipt SHALL carry
`ERR_ALL_ATTEMPTS_TIMED_OUT` and a `timed_out_arms` list. In every other failing case the receipt SHALL
still carry `ERR_LANE_ALL_ROUTES_EXHAUSTED`.

#### Scenario: arms answered, no nonce
- **WHEN** every responding arm exits 0 with a usage receipt and none emits the nonce
- **THEN** the code is `ERR_NO_ARM_EMITTED_NONCE` and `nonce_absent_arms` names each such arm

#### Scenario: nothing reachable
- **WHEN** every attempt times out
- **THEN** the code is `ERR_ALL_ATTEMPTS_TIMED_OUT` and NOT `ERR_NO_ARM_EMITTED_NONCE`

#### Scenario: the acceptance rule is not relaxed
- **WHEN** any failing combination above occurs
- **THEN** the receipt still reports `ok: false` and the process still exits non-zero

### Requirement: A declared non-dispatchable arm is not spawned, and the skip is recorded
When the pool artifact marks an arm not dispatchable (`dispatchable: false`, or a `feasibility` value
beginning `UNREACHABLE` or equal to `CONFIG_COMPLETE_NOT_ACTIVATED`), the dispatch SHALL NOT spawn that
arm, SHALL record it in `receipt.skipped_arms` with its reason, and SHALL consume none of its timeout
budget. An explicit `--force-rank` naming that rank SHALL still spawn it. An arm not so declared SHALL be
unaffected.

#### Scenario: a declared-dead arm costs nothing
- **WHEN** a lane's ordered pool contains an arm declared not dispatchable
- **THEN** zero attempts are made for that arm and `skipped_arms` names it with its reason

#### Scenario: the measurement is overridable
- **WHEN** the same rank is requested with an explicit `--force-rank`
- **THEN** that arm IS spawned

#### Scenario: no over-blocking
- **WHEN** an arm is not declared not dispatchable
- **THEN** it is not skipped

### Requirement: A non-isolated Codex home cannot produce a "no human-attended identity" claim
The identity gate SHALL fold the resolved Codex home into its verdict. When the resolved home is not the
lane's declared isolated home and holds an `auth.json`, the dispatch SHALL refuse before spawning any
child with `ERR_LANE_HOME_NOT_ISOLATED` and a non-zero exit, unless `--allow-human-home-transport` is
passed. Every receipt SHALL record the resolved home and whether it is the declared lane home.

#### Scenario: the unsound combination is refused pre-spawn
- **WHEN** `--codex-home` resolves to a home holding `auth.json` that is not the declared lane home and
  the acknowledgement flag was not passed
- **THEN** the run is refused with `ERR_LANE_HOME_NOT_ISOLATED` and zero attempts are made

#### Scenario: the declared capability stays reachable deliberately
- **WHEN** the same home is used WITH `--allow-human-home-transport`
- **THEN** the run proceeds and the receipt records the acknowledgement

#### Scenario: the isolated lane home is never refused
- **WHEN** the resolved home IS the declared lane home
- **THEN** no refusal is produced by this requirement

### Requirement: Every behaviour in this capability is deterministically test-covered
The tests for the three requirements above SHALL be deterministic and SHALL NOT depend on the network, a
real model, the relay, or the developer's real Codex home. The pre-existing suite for this surface SHALL
continue to pass as a whole.

#### Scenario: the suite is the gate
- **WHEN** the named test command for this surface is run on the candidate bytes
- **THEN** it passes in full, including the pre-existing tests
