# hgk-r11-session-handover-20261016 (spec delta)

## ADDED Requirements

### Requirement: Single-entry session handover
The mission SHALL produce one entry document that lets a NEW session resume the abandoned work without reading the
whole conversation, and it SHALL be published as candidate evidence.

#### Scenario: A fresh session resumes
- **WHEN** a new session reads the handover entry document
- **THEN** it finds the mission anchors (package, EIA report, claim ceiling), the measured state of every open
  governance record with its owner, one-action next steps, and the blocking items - each with a locator.

### Requirement: Measured open-record inventory
Every open change record SHALL carry a MEASURED status (counts, timestamps, validator result where run) and SHALL
NOT be annotated with a status this round did not measure.

#### Scenario: No stale claim survives
- **WHEN** a row's status is copied from an older record
- **THEN** it is marked as carried-over, not as re-measured, and names the source it was carried from.

### Requirement: Zero rollback and guard hands-off
This round SHALL NOT modify any published R6..R10 packet, the guard subject `R6_DELIVERY/`, or a peer round's
working tree.

#### Scenario: Publication is additive
- **WHEN** the round publishes
- **THEN** it does so from a NEW branch cut off `origin/main` in its own worktree, and the pre-existing prefixes
  are re-read afterwards and reported unchanged.
