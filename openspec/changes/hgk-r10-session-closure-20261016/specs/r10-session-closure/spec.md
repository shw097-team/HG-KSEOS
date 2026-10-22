## ADDED Requirements

### Requirement: stale change records are adjudicated, not ticked

A change record whose tasks were executed by an outside act, or whose premise no longer holds, MUST be
adjudicated row by row against freshly measured state. Each row carries exactly one of `DONE_MEASURED`,
`SUPERSEDED`, `OPEN_OWNER`, `NOT_OWED`, and each verdict cites the locator that decides it.

#### Scenario: a row whose work an outside act performed

- **WHEN** the row's artifact already exists in the measured state
- **THEN** the verdict is `DONE_MEASURED` with the measurement and the outside act named as its cause

#### Scenario: a row whose premise no longer holds

- **WHEN** the governed measurement shows the remedy is unnecessary
- **THEN** the verdict is `SUPERSEDED` with the measurement, and no artifact is manufactured to close it

### Requirement: this session's own tooling is repaired where it damaged evidence

The round wrapper MUST NOT destroy an earlier turn's dispatch provenance, and its nonce gate MUST read
the lane's own artifact root.

#### Scenario: two turns of the same role in one round

- **WHEN** a second turn of the same role dispatches
- **THEN** the earlier turn's receipt and attempt log survive at their own immutable paths

#### Scenario: the lane writes its nonce into its artifacts but the transcript is truncated

- **WHEN** the nonce exists in the lane's artifact root
- **THEN** the receipt records that nonce rather than reporting the arm as nonce-absent

### Requirement: closure leaves a resumable handover

The round MUST deliver a checkpoint, a ledger of side effects and a next-round residual worklist.

#### Scenario: a successor session picks the work up

- **WHEN** the successor reads the handover package
- **THEN** every open item has a locator and its claim ceiling, without needing this session's context
