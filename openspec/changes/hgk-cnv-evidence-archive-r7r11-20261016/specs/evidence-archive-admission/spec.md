# Spec delta — evidence archive admission (round CNV-EVIDENCE-ARCHIVE-R7R11-20261016)

## ADDED Requirements

### Requirement: An evidence-archive round is admitted before any remote effect

The round SHALL obtain an HGK typed admission (requirement, TaskSpec, WorkOrder lineage) and a
successful local prompt-compiler compile for THIS round before any remote publication or merge is
attempted. A compile receipt issued for an earlier round SHALL NOT be reused as this round's compile
result (the round's own contract carries the rule at `/source_scan/normative_claims/NC-006`).

#### Scenario: No fresh compile receipt exists

- **WHEN** the round has no `PROMPT_COMPILE_PASS` receipt whose `task_id` equals this round's contract id
- **THEN** the round performs read-only source positioning only and makes no remote write

### Requirement: Each evidence pull request is frozen individually

Each of the eight candidate-evidence pull requests SHALL be frozen separately on
`repo/base/head/prefix/diff/approval/rollback`, and SHALL NOT be presented as one atomic transaction.
A pull request that fails its preflight SHALL be checkpointed alone with a typed first-fail reason.

#### Scenario: One pull request drifts while others are clean

- **WHEN** a pull request's live `head` differs from the `head` frozen in its preflight record
- **THEN** only that pull request's preflight is invalidated and re-run; the other seven retain their
  records

### Requirement: The changed-file set of every evidence pull request stays inside one evidence prefix

A preflight SHALL derive the exact changed-file set from the live head and SHALL refuse the
evidence-only exception if any path escapes `EVIDENCE/<round>/`, or if any path is a product, control,
CI, hook, submodule, symlink or credential path.

#### Scenario: A pull request adds a file outside its own prefix

- **WHEN** the changed-file set contains a path whose first two segments are not the pull request's own
  evidence prefix
- **THEN** the round records `PREFIX_ESCAPE`, suspends that pull request's evidence-only approval and
  requires a newly compiled ChangeSet before any merge

### Requirement: The remote merge is a human power node

The merge of any evidence pull request SHALL require a real repository-maintainer approval covering the
single prefix, the actual head at merge time, the candidate-only/no-auto-execute condition and a
rollback pointer. The maker, the external reviewer and the round's own records SHALL NOT self-sign it.

#### Scenario: No maintainer approval is recorded

- **WHEN** a pull request satisfies every technical preflight but carries no maintainer approval
- **THEN** the pull request stays Draft/Open, the round reports `ARCHIVE_EVIDENCE_CANDIDATE_READY`, and
  the merge is not attempted

### Requirement: K-ledger semantics are corrected additively

The round SHALL introduce the distinction between `source_linked` (20/20) and `same_run_retested` (0/20)
in NEW metadata only, and SHALL NOT rewrite the historical upstream snapshot or its status counts.

#### Scenario: A local candidate repair is confused with a source status change

- **WHEN** a candidate remediation exists for a ledger row whose upstream status is `PARTIAL`
- **THEN** the row keeps its baseline status and gains a separate candidate-remediation field
