# repo-surface Specification

## ADDED Requirements

### Requirement: Front page and evidence must agree
The repository front page SHALL describe the state that the archived evidence already records, and SHALL NOT
claim a state that no evidence supports.

#### Scenario: status line and merge wave
- **WHEN** a round merges pull requests into the default branch
- **THEN** the front page status section SHALL be refreshed with those merge commits, and the earlier dated
  status lines SHALL be kept as history rather than deleted

#### Scenario: non-claims survive the refresh
- **WHEN** the front page is refreshed
- **THEN** every explicit non-claim SHALL remain explicit: no independent acceptance, no acceptance-officer
  acceptance, no effect admission, no production or runtime release, no passed continuous-integration status

### Requirement: Branches must be advertised only while they are unfinished
A remote branch whose pull request is merged SHALL NOT continue to be advertised as outstanding work.

#### Scenario: merged branches are removed with a rollback record
- **WHEN** a branch's pull request is merged
- **THEN** the branch SHALL be removed from the remote, and its tip commit SHALL be recorded so the reference
  can be restored

#### Scenario: open and orphan branches are kept
- **WHEN** a branch's pull request is still open, or the branch has no pull request at all
- **THEN** the branch SHALL be kept

### Requirement: The round must publish what a stranger can re-check
Every claim of this round SHALL be re-checkable from the published pack alone.

#### Scenario: per-blob readback
- **WHEN** the round publishes its pack
- **THEN** each published blob SHALL be read back from the remote and compared byte for byte before the round
  reports success
