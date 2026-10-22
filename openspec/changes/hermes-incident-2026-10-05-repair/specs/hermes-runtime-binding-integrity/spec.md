## Purpose

Define what the governed runtime must prove about where it lives: that its declared home, its gate-hook bindings
and its data stores resolve to the runtime root it actually executes from, that foreign or missing gate bindings
are surfaced as defects, and that a recovery-created second home is either archived with a receipt or adopted
canonically in one recorded decision.

## ADDED Requirements

### Requirement: Single resolved runtime root
The runtime SHALL resolve exactly one home as the runtime root, and governance binding files SHALL be reconciled to
that resolved root before any durable change is claimed against the runtime.

#### Scenario: Second home detected
- **WHEN** a second home directory exists that holds a configuration file and a skill tree but no session store
- **THEN** it is classified as either recovery residue (archive candidate) or an adopted root, with the classification and its evidence recorded before any file is moved or removed

#### Scenario: Binding file drift
- **WHEN** a binding file declares a home or database path that differs from the path the runtime resolves
- **THEN** both paths are recorded with the resolving command and the drift is registered as a defect with a bounded repair candidate

### Requirement: Recovery residue is archived, never silently deleted
A directory produced by a recovery action SHALL be added to the archive with a content digest before disposal.

#### Scenario: Disposal without receipt
- **WHEN** a recovery residue directory is a disposal candidate
- **THEN** an archive artifact naming every top-level entry with its digest exists first, and the disposal is recorded as a separate, revertible step

### Requirement: Partial update is resolved or disclosed
An update that stops part-way (for example a parked stash restore) SHALL be either completed or disclosed with the
pre/post identity delta recorded.

#### Scenario: Failed stash restore
- **WHEN** an update receipt shows a failed local-changes restore with identical pre- and post-update revisions
- **THEN** the round records the mixed/partial state, names the surviving stash reference (or records that none is resolvable), and emits a repair task rather than re-running the update blindly
