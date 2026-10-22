# archive-evidence-merge

## ADDED Requirements

### Requirement: Per-PR evidence archive merge
The archive stage SHALL merge each candidate evidence pull request normally at its approved exact head
SHA, and SHALL read the merged prefix and blobs back from `main`.

#### Scenario: Approved head is merged
- **WHEN** a maintainer approval names the PR's exact head SHA, prefix and rollback
- **THEN** the PR is merged with `sha=<approved head>` and the merge commit SHA is read back from the API

#### Scenario: Head drifted after approval
- **WHEN** the live head no longer equals the approved SHA
- **THEN** that PR is HELD, no merge is attempted, and its first-fail is recorded

### Requirement: Evidence-only scope enforcement
The round SHALL refuse any PR whose changed paths leave its single allowed `EVIDENCE/**` prefix, and
SHALL hold only that PR.

#### Scenario: Prefix escape
- **WHEN** a changed path lies outside the allowed prefix
- **THEN** the PR is HELD with `PREFIX_ESCAPE` and the other PRs keep their independent gating

### Requirement: Trusted scoped secrets scan
The round SHALL scan the content each PR adds with a scanner proven to fire on a positive control and
silent on a clean control, and SHALL hold any PR with a real secret.

#### Scenario: Positive control fires
- **WHEN** the scanner is run against a fixture containing a synthetic credential
- **THEN** it reports a finding, proving the scan is not vacuous
