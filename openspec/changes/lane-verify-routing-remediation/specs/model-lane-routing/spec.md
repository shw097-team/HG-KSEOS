# model-lane-routing

## ADDED Requirements

### Requirement: A lane's model is established from authoritative records

A governed round SHALL establish which model served each lane from the runtime's own log
records and configuration, not from a delegation banner or a declared policy value.

#### Scenario: Verify lane routing evidence

- **WHEN** a verify lane is dispatched under a changed delegation route
- **THEN** the round records the runtime log line naming that session's model and provider
- **AND** the round restores the previous route and reads the restored values back

#### Scenario: Declared but unexercised arm

- **WHEN** an arm is declared configured but has never returned a verdict
- **THEN** the round records the arm as declared and unexercised rather than as wired

### Requirement: An arm is probed before it is used

A round SHALL probe every arm it intends to use on both the catalogue read and a bounded
completion attempt, and SHALL treat a listed model that does not answer as unavailable.

#### Scenario: Non-Flash sibling hangs

- **WHEN** the plain sibling model exceeds the probe timeout with no response while the
  mandated variant answers
- **THEN** the round keeps the mandated variant, records the sibling as unreachable, and
  names the difference rather than generalising it to the provider

### Requirement: The claim ceiling enumerates writes

A round SHALL state its ceiling as no mutation of the subject store, accompanied by an
enumeration of every write it caused, and SHALL NOT claim that no canonical write occurred.

#### Scenario: Suite appends events to a shared store

- **WHEN** a suite run appends rows to a shared canonical store
- **THEN** those rows are enumerated in the write ledger and the round's ceiling names the
  store as written

### Requirement: Repair precedes canonical re-verification

A round SHALL NOT re-verify a non-hermetic suite against the canonical store before the
hermeticity repair has landed, unless it discloses the write that the run itself causes.

#### Scenario: Ordering of repair and re-verification

- **WHEN** the hermeticity repair is still a candidate
- **THEN** the canonical re-verification is either deferred or run against an override store
  with the deviation stated in the handoff
