# fhs-msc-skeleton-spine — spec delta (revision2 native DAG execution)

## ADDED Requirements

### Requirement: Source freeze SHALL be re-derived from bytes, not asserted

The round SHALL recompute every manifest row, every checksum row and every outer-archive member digest from the
canonical package root before any dependent work, and SHALL record the outer archive sha256 as the round's source
binding.

#### Scenario: A tampered or incomplete package

- **GIVEN** the declared MANIFEST.md and artifact_checksums.sha256 for the revision2 package
- **WHEN** any member's bytes differ from its declared digest, or a member is missing, or an on-disk payload is
  listed in neither register
- **THEN** the round verdict is FAIL and no WP may be marked DONE on that basis.

### Requirement: A work package SHALL be closed only against a resolvable receipt

Every WP-FHS-00..21 row SHALL carry a status plus at least one evidence path that resolves on disk; a row whose
evidence does not resolve is a claim, not a record.

#### Scenario: Ledger audit

- **GIVEN** the round ledger with per-WP statuses
- **WHEN** the driver runs its audit
- **THEN** every closed row's evidence paths are checked to exist, and any unresolved reference fails the audit.

### Requirement: Native-gated packages SHALL be parked with a named owner, never fabricated

Any WP whose `effect_class` is REPO_WRITE, HOST_OP, USER_OP, REMOTE_WRITE or RELEASE and which lacks a native
Issuer PERMIT bound to this exact request SHALL be parked with `owner`, `next_legal_action` and
`resume_predicate`.

#### Scenario: Missing Issuer bundle

- **GIVEN** a WP requiring HOST_OP and no signed Issuer references
- **WHEN** admission is attempted
- **THEN** the gate refuses with a typed code, the refusal is recorded as evidence, and the WP is parked rather
  than downgraded to a document claim.

### Requirement: Maker and checker SHALL be different principals

The independent acceptance of this round's candidate SHALL be produced by a lane whose principal differs from the
maker, and its verdict SHALL state its ceiling: an agent readback is not a protected native checker pass.

#### Scenario: Verdict ceiling

- **GIVEN** a frozen subject and an independent reader
- **WHEN** the verdict is recorded
- **THEN** the receipt names the reader principal, the frozen subject digest, and the exact claim it does and does
  not support.

### Requirement: Delivery SHALL be candidate-only

Publication SHALL go to per-repository candidate branches with commits and pull requests; `main` SHALL NOT be
written, no branch SHALL be force-pushed, and no merge, tag or release SHALL be created.

#### Scenario: Publication review

- **GIVEN** a pushed candidate branch
- **WHEN** the publication is verified
- **THEN** the destination branch differs from the default branch, the tarball excludes raw data, databases, keys
  and credentials, and the PR body carries the claim ceiling verbatim.
