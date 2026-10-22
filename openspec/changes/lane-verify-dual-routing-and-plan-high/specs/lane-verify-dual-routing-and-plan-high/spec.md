# lane-verify-dual-routing-and-plan-high

## ADDED Requirements

### Requirement: Reasoning effort is declared per lane and drift-checked

The system SHALL carry an explicit `reasoning_effort` at every active declaration site of the PLAN
route and of each VERIFY_SECURITY arm, and SHALL fail the drift gate when any site loses or changes it.

#### Scenario: A declaration site loses its effort

- **WHEN** a projected site stops carrying the declared `reasoning_effort` for a lane
- **THEN** the drift gate reports the exact path and JSON pointer as a hard error

#### Scenario: An effort is expressed as a model slug

- **WHEN** a lane's effort is encoded by suffixing the model id instead of declaring `reasoning_effort`
- **THEN** the change is rejected, because a suffixed slug resolves to the global default rather than the declared level

### Requirement: The PLAN effort default is model-level and does not raise other models

The system SHALL make the PLAN effort a model-level default for the PLAN model only, leaving the
global effort unchanged for every other model.

#### Scenario: Another model is resolved

- **WHEN** the effective reasoning config is resolved for a model other than the PLAN model
- **THEN** it resolves to the global effort, unchanged by the PLAN declaration

### Requirement: VERIFY/SECURITY is a user-selected dual model-AND-provider route

The system SHALL declare two co-equal VERIFY/SECURITY arms that differ on both the model and the
provider axis, SHALL name the operator's instruction as the selection authority, and SHALL use the
OpenAI OAuth arm when the instruction names neither arm.

#### Scenario: Operator names an arm

- **WHEN** the operator's instruction names one arm at dispatch time
- **THEN** that arm serves the lane and the other arm is not configured as its fallback

#### Scenario: Operator names neither arm

- **WHEN** the dispatch carries no arm selection
- **THEN** the OpenAI OAuth arm (gpt-6.1-sol / openai-codex) is used

#### Scenario: Co-equality is not claimed as enforcement

- **WHEN** the co-equality of the two arms is reported
- **THEN** it is reported as a declaration, and the machine-enforced surfaces (the delegation default and the per-card override) are named separately

### Requirement: The maker/checker model collision is declared and refused

The system SHALL declare the model-axis collision created by the default arm sharing the PLAN model,
SHALL refuse to dispatch the colliding pair, and SHALL NOT silently resolve the conflict.

#### Scenario: PLAN-made artifact checked on the default arm

- **WHEN** the checker arm normalizes to the same model token as the PLAN maker
- **THEN** the pre-dispatch gate refuses, and the collision remains declared for adjudication

#### Scenario: EXECUTE-made artifact checked on either arm

- **WHEN** the maker is the EXECUTE lane and the checker is either VERIFY arm
- **THEN** the model-axis separation holds on both arms

### Requirement: The shared model's non-default lane is pinned per dispatch

The system SHALL pin the verification lanes' effort per dispatch whenever the verification lane runs
on a model whose model-level default is higher than the lane's declared effort.

#### Scenario: A verification card on the shared model

- **WHEN** a VERIFY or ACCEPTANCE card is created on the shared model whose model-level default is HIGH
- **THEN** the card carries an explicit task-level effort pin of the lane's declared level

### Requirement: Reported defects outside the change are not silently repaired

The system SHALL report any defect it measures but does not fix, with its evidence and status, and
SHALL NOT let an out-of-scope repair change the declared routing.

#### Scenario: An unrelated routing defect is measured

- **WHEN** a defect is found in a routing surface this change does not own
- **THEN** it is recorded as a named finding with raw evidence and an open status
