# lane-sod-enforcement

## ADDED Requirements

### Requirement: Routing facts have one source of truth (D1, D9, D13, D14)

The system SHALL keep every active model-lane routing fact in a single registry and SHALL
derive each live projection from it, so that a partial or duplicated edit cannot remain valid.

#### Scenario: Duplicated routing fact drifts

- **WHEN** any live projection site (assignment tuple, sod string, lane chain, effective wiring)
  disagrees with the registry
- **THEN** the drift gate fails and names the exact path and JSON pointer of the disagreement

#### Scenario: Projection is deterministic

- **WHEN** the policy is projected twice from the same registry
- **THEN** the two projections are byte-identical and contain no wall-clock field

### Requirement: Maker and checker do not share a model (D1, D2, D9, D13)

The system SHALL refuse to dispatch a verification lane whose normalized model identity equals
the executor's, and SHALL NOT claim provider separation when the lanes share a provider.

#### Scenario: Verify model equals maker model

- **WHEN** the intended checker model normalizes to the maker model
- **THEN** the guard refuses with a SoD violation before any dispatch

#### Scenario: Shared provider is honest

- **WHEN** EXECUTE and VERIFY_SECURITY both use the opencode-go provider
- **THEN** the policy records provider separation as not required and relies on the model axis

### Requirement: Admission is lane-shaped, not a direct completion (D7, D8, D11, D12)

The system SHALL mark an arm ADMITTED only after a lane-shaped exercise completes a real model
call and tool round-trip through the lane engine, and SHALL record a bare direct completion
separately as never sufficient.

#### Scenario: Direct completion only

- **WHEN** an arm answers a direct completion with HTTP 200 but never completes a lane turn
- **THEN** the admission status remains UNPROVEN and is never ADMITTED

#### Scenario: Served identity mismatch

- **WHEN** a lane exercise completes but the runtime log shows a different served model
- **THEN** the admission is REFUSED and the guard blocks the dispatch

### Requirement: Dispatch fails closed on staleness (D14, D19)

The system SHALL refuse dispatch when the policy epoch or the recorded source digest is stale
relative to the live canonical policy.

#### Scenario: Stale epoch

- **WHEN** the admitted epoch differs from the live canonical policy revision
- **THEN** the guard refuses with a stale-epoch error

#### Scenario: Source digest changed

- **WHEN** the canonical policy bytes no longer match the recorded digest
- **THEN** the guard refuses and does not dispatch

### Requirement: The checker gate does not scan its own output (D23, D24)

The gate SHALL freeze its input set before reading, exclude its own output and registered
producer outputs, require an output path and an input digest, and produce semantic findings
that are identical over identical frozen inputs.

#### Scenario: Prior output exists

- **WHEN** the gate runs twice over identical frozen inputs with a leftover output file present
- **THEN** both runs emit identical findings and the same input digest

#### Scenario: Broken citation

- **WHEN** a required artifact is missing or a citation does not resolve
- **THEN** the gate fails with a named blocking finding and never reports PASS

### Requirement: Mutation and activation need an admitted envelope (D15, D16, D17, D18, D20, D21, D22)

The system SHALL treat all enforcement artifacts as CANDIDATE and SHALL require a separate
HGK-authorized generation binding before any is activated; no candidate may approve itself.

#### Scenario: Candidate self-activation

- **WHEN** a candidate registry is present but no authorized generation binding exists
- **THEN** the runtime is not activated and the change remains CANDIDATE

### Requirement: Named-method and denominator completeness (D24, D25)

The change SHALL enumerate the acceptance denominator explicitly and SHALL provide the named
OpenSpec adapter surface rather than a substitute.

#### Scenario: Empty denominator

- **WHEN** the gate finds no frozen input to check
- **THEN** it reports a blocking empty-denominator error rather than passing vacuously
