## ADDED Requirements

### Requirement: Three-lane model binding under a re-issued owner order

The system SHALL bind PLAN, EXECUTE and VERIFY_SECURITY to the models named by the governing
owner order, and SHALL record the binding in the pool, the registry, the assignment document
and the AGENTS.md owner chain as one change set.

#### Scenario: The owner re-issues the model order

- **WHEN** the owner names a model for each of PLAN, EXECUTE and VERIFY_SECURITY
- **THEN** the pool's rank-1 entry for each lane is that model with its provider-qualified
  transport id, the registry's route row for that lane is re-derived from the pool, the
  assignment document's lane chain is re-derived from the pool, and the AGENTS.md owner chain
  names the same three models

#### Scenario: A demoted arm is retained

- **WHEN** an arm that was rank 1 is demoted by a re-issued order
- **THEN** it remains in the pool as a reachable fallback at a contiguous rank
- **AND** no arm is deleted from the pool

#### Scenario: Prose fields agree with the data

- **WHEN** a re-issued order changes any lane's rank-1
- **THEN** the pool's `declared_by`, every lane's `selection_note`, the `placement_rationale`,
  the `change_log` and the AGENTS.md owner chain all name the same rank-1 for that lane
- **AND** no field names a rank-1 that contradicts the lane's `ordered_pool[0]`

#### Scenario: The maker and the checker are model-distinct

- **WHEN** the owner order names different models for EXECUTE and VERIFY_SECURITY
- **THEN** `check_sod("EXECUTE", "VERIFY_SECURITY")` reports separation
- **AND** the pair (PLAN, VERIFY_SECURITY), which shares a model, is declared explicitly rather
  than being hidden by a single global SoD flag

### Requirement: Governance identity and transport vocabulary stay distinct

A pool entry SHALL carry a governance identity (`provider`/`model`, compared by the drift gate)
and a transport vocabulary (`transport_model`, actually sent to the CLI), and the two SHALL
follow the per-provider spelling rule.

#### Scenario: An opencode-go arm

- **WHEN** an opencode-go arm is dispatched
- **THEN** the transport id is the provider-qualified `<provider>/<model>` spelling
- **AND** the bare id is not sent to the transport

#### Scenario: An openai-codex arm

- **WHEN** an openai-codex arm is dispatched
- **THEN** the transport id is the BARE model id
- **AND** the provider-qualified spelling is not sent to the transport

### Requirement: Admission before the order is treated as in force

A lane SHALL be treated as bound to a model only after a measured HGK admission receipt proves
that the lane's transport served that arm.

#### Scenario: A direct completion is not an admission

- **WHEN** a direct relay completion returns 200 for a model
- **THEN** the lane is NOT admitted on that basis
- **AND** the lane requires a lane-shaped dispatch whose served arm, nonce and usage receipt
  all match the required arm

#### Scenario: The admission receipt is evidence

- **WHEN** an admission is recorded
- **THEN** it carries the served arm, the nonce confirmation, the usage rows appended after the
  attempt started, and the tool-call count
