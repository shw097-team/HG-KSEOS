## Purpose

Define what the governed Hermes runtime must be able to prove about its own on-disk state after an agent-caused
integrity incident: a re-derivable integrity verdict for every forensic artifact it names, a measurable (not
estimated) data-loss bound, a skill inventory whose bulk shrink is detectable, and a gate binding that resolves to
the live runtime root and fails loudly when it does not.

## ADDED Requirements

### Requirement: Re-derivable forensic integrity verdicts
Every forensic artifact named by an incident record SHALL carry its own measured integrity verdict, and the record
MUST NOT assert an integrity state that a fresh read-only check of that artifact contradicts.

#### Scenario: A bound artifact fails its declared verdict
- **WHEN** an incident record declares a snapshot artifact as intact by hash, and a fresh `PRAGMA quick_check` on that exact artifact returns malformed page errors
- **THEN** the record is reported as containing a falsified claim, the artifact is recorded in the defect register, and the claim is corrected rather than restated

#### Scenario: Subject identity of twin copies
- **WHEN** two copies of an incident subject exist with the same size but different content digests
- **THEN** each copy is enumerated with its own digest and integrity verdict, and no single hash is presented as covering both

### Requirement: Measured data-loss accounting
A data-loss statement in a governed incident record SHALL be derived from a named source artifact and a reproducible
query, and MUST report both the numerator and the denominator.

#### Scenario: Rescue export reconciliation
- **WHEN** a rescue export of rows visible before the loss is replayed against the live store
- **THEN** the record reports present/total counts and the exact identifiers that are absent, and any earlier estimate that disagrees is withdrawn

### Requirement: Detected skill-inventory shrink
The runtime SHALL be able to enumerate its skill inventory with per-skill content digests, and a bulk removal SHALL
be detectable rather than silent.

#### Scenario: Bulk shrink is detected
- **WHEN** the number of skill directories in the live home drops by more than a declared threshold relative to a recorded inventory
- **THEN** the runtime records a shrink finding naming the removed skill paths and digests, and does not treat the new inventory as the baseline

### Requirement: Gate binding resolves to the live root
Pre-LLM and pre-tool-call gate hooks SHALL resolve to scripts inside the resolved runtime home, and a gate script
that is missing or foreign MUST fail closed with a recorded, user-visible reason.

#### Scenario: Foreign gate binding
- **WHEN** the canonical home's configuration references a gate script that lives outside the resolved runtime root
- **THEN** the binding is reported as a defect with both the referenced and the resolved paths, and the round records that deleting the foreign directory would fail-close the guarded tool surface

#### Scenario: Missing gate script
- **WHEN** a configured gate script does not exist at the referenced path
- **THEN** the guarded tools fail closed AND the failure is surfaced as a startup diagnostic rather than as an unexplained tool denial

### Requirement: Declared identity equals resolved identity
A governance binding file that declares a runtime home, version or database path SHALL match the identity the
runtime resolves at execution time, or the mismatch MUST be recorded as a defect.

#### Scenario: Declared versus live version
- **WHEN** a binding file declares release version X but the runtime reports version Y
- **THEN** the delta is recorded with the command evidence for Y, and a repair candidate is emitted that does not mutate the runtime without a gate
