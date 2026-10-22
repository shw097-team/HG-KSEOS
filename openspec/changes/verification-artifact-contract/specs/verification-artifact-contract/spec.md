# verification-artifact-contract

## ADDED Requirements

### Requirement: The verdict artifact exists before the expensive work begins

The verification harness SHALL pre-create the verdict artifact as a skeleton whose every item is
`INCONCLUSIVE` and whose `updated_by_checker` marker is false, and SHALL NOT accept that skeleton as a
verdict. The checker lane SHALL take the file over and update it in place as it resolves items, so that
exhausting a lane's budget can only downgrade items, never delete the artifact.

#### Scenario: A lane ends with the skeleton untouched

- **WHEN** a checker lane exits 0 and the verdict artifact still carries the runner's skeleton with
  `updated_by_checker` not true
- **THEN** the run fails with `ERR_VERIFY_NO_VERDICT` and a non-zero exit code, because a skeleton is
  not a verdict

#### Scenario: A lane's budget is exhausted mid-audit

- **WHEN** a checker lane is terminated or exhausts its budget after resolving some items
- **THEN** the artifact on disk still exists, contains at least one non-`INCONCLUSIVE` item if one was
  resolved, and carries explicit `INCONCLUSIVE` markers for the rest

#### Scenario: The artifact is absent at the end of a successful lane

- **WHEN** a lane exits zero and no verdict artifact exists
- **THEN** the harness fails closed rather than recording success

#### Scenario: A stale PASS survives a later downgrade

- **WHEN** an item is downgraded to `INCONCLUSIVE` after an earlier write recorded a stronger outcome
- **THEN** the on-disk artifact reflects the downgrade; a stale stronger verdict MUST NOT remain

### Requirement: Each checker lane runs under a declared, measured context budget

Each checker lane SHALL be dispatched with a bounded item set whose measured peak input tokens stay
below the ceiling declared by the checker model's OWN catalogue entry, and the harness SHALL fail closed
when a lane exceeds that budget.

#### Scenario: A lane exceeds its budget

- **WHEN** a lane's measured peak `usage.inputTokens` exceeds the budget recorded in its schedule
- **THEN** the run fails with `ERR_LANE_CONTEXT_BUDGET_EXCEEDED`

#### Scenario: The ceiling is read from another model's entry

- **WHEN** the budget is derived from the first `auto_compact_token_limit` key in the catalogue file
  rather than selected by the checker model's slug
- **THEN** the check is void, because that key belongs to a different model (measured: 334800 versus the
  checker's own 115200)

### Requirement: The audit item set is partitioned with no loss and no duplication

The shard schedule SHALL contain every audit item exactly once, and each shard SHALL carry its own
artifact and its own budget.

#### Scenario: An item is dropped or duplicated by sharding

- **WHEN** the union of the schedule's shards differs from the audit's item set
- **THEN** the schedule fails validation and no shard lane is dispatched

### Requirement: Discriminating fixtures are pre-baked, content-addressed and read-only

Fixtures that discriminate a required behaviour SHALL be built ahead of the lanes, content-addressed by
a manifest, reproducible from identical inputs, and presented read-only with their expected outcomes.

#### Scenario: The fixture pack is built twice from identical inputs

- **WHEN** the pack is rebuilt from the same inputs
- **THEN** the resulting pack digest is identical

#### Scenario: A fixture byte is modified

- **WHEN** any fixture file differs from the manifest digest recorded for it
- **THEN** the manifest check fails loudly, so the check cannot pass vacuously

### Requirement: Concurrent lanes do not share mutable runtime state

Lanes permitted to run concurrently SHALL each hold their own runtime home and their own lock, and
process cleanup SHALL be scoped to a lane's own process ids rather than to a command-line pattern.

#### Scenario: Two lanes run at the same time

- **WHEN** two lanes are dispatched concurrently
- **THEN** each has a distinct runtime home, a distinct lock, and a recorded declared write scope, and
  neither lane's cleanup terminates the other's process

### Requirement: A writer's self-report is never the verification

A lane's own statement about its artefact SHALL be recorded as non-authoritative, and acceptance SHALL
require an independent lane to reproduce the observation from raw evidence.

#### Scenario: A lane reports success with no reproducible evidence

- **WHEN** a lane's summary claims a passing result that the harness cannot reproduce
- **THEN** the claim does not count towards acceptance and the discrepancy is recorded as a finding

### Requirement: The post-condition validates the artifact's shape, not a takeover flag

A verdict artifact SHALL be accepted only when `updated_by_checker` is exactly `true`, a top-level
`verdict` is present and is one of `PASS`, `FAIL`, `INCONCLUSIVE`, and `per_requirement` is a non-empty
object whose every entry carries a `result` drawn from that same set. An overall `PASS` SHALL NOT be
accepted while any item is `INCONCLUSIVE` or `FAIL`.

#### Scenario: The takeover flag is set and no overall verdict is ever stated

- **WHEN** a lane exits 0 with an artifact whose `updated_by_checker` is true and which carries per-item
  results, but which has no top-level `verdict`
- **THEN** the run fails with `ERR_VERIFY_VERDICT_SHAPE` and a non-zero exit code, because an artifact
  with no overall verdict is not adjudicable

#### Scenario: An overall PASS is claimed over an unresolved item

- **WHEN** the artifact's overall `verdict` is `PASS` while at least one item's `result` is
  `INCONCLUSIVE` or `FAIL`
- **THEN** the run fails with `ERR_VERIFY_VERDICT_OVERCLAIM`, so a lane cannot upgrade an unresolved item
  into an overall pass

#### Scenario: The artifact is well-typed but empty of adjudicable items

- **WHEN** `per_requirement` is absent, is not an object, is empty, or any entry has no `result` in the
  allowed set
- **THEN** the run fails with `ERR_VERIFY_VERDICT_SHAPE`

#### Scenario: The takeover flag is truthy but not the boolean true

- **WHEN** `updated_by_checker` is `1`, or the string `"true"`, or otherwise not exactly `true`
- **THEN** the run fails with `ERR_VERIFY_VERDICT_SHAPE`, so a truthy proxy cannot stand in for the
  marker the contract names

#### Scenario: The artifact is still the untouched skeleton

- **WHEN** the artifact remains the runner's skeleton with `updated_by_checker` false
- **THEN** the run fails with `ERR_VERIFY_NO_VERDICT`, the original token, so fixtures and evidence
  recorded before this requirement stay valid
