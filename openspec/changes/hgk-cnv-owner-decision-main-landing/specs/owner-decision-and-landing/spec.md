# owner-decision-and-landing Specification

## ADDED Requirements

### Requirement: A landing candidate must be additive before it is merged
A candidate change to the default branch SHALL be additive or explicitly justified, and SHALL be measured
against the default branch's own file conventions before any merge is recommended.

#### Scenario: line ending drift
- **WHEN** a candidate rewrites whole files although its text change is small
- **THEN** the drift SHALL be repaired on the candidate branch and the diff SHALL be shown to be insertion-only
  before a merge is recommended

### Requirement: Only previously verified candidates may land
The default branch SHALL only receive candidates whose contents were already verified and read back, and whose
merge is gated on a check by a different model than the one that wrote them.

#### Scenario: the gate
- **WHEN** a candidate's blobs read back byte-identical and an independent checker passes
- **THEN** the candidate may be merged, with the merge commit and a revert command recorded

#### Scenario: the round's own pack
- **WHEN** a round publishes its own delivery pack
- **THEN** that pack SHALL be left open for the owner and SHALL NOT be merged by the round

### Requirement: An owner decision is prepared, never taken
An item awaiting an owner decision SHALL be reduced to one minimal action form with its prerequisites prepared,
and SHALL NOT be signed, accepted or closed by any agent.

#### Scenario: bulletin
- **WHEN** a round reports items awaiting the owner
- **THEN** it SHALL state, per item, what is already prepared and what only the owner can supply
