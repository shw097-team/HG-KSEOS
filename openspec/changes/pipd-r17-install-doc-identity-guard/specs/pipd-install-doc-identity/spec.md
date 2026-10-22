# pipd-install-doc-identity — delta for pipd-r17-install-doc-identity-guard

## ADDED Requirements

### Requirement: The install documentation SHALL be guarded against cross-release identity mixing

The repository test suite SHALL contain a check that fails when a single paragraph of the install SSOT
pairs one release's identifier with another release's target commit without marking that commit as
belonging to the other release, and when a documented build example's `--mount-pack`, `--release-id` and
`--release-commit` name different release generations. The check SHALL run inside the existing
continuous-integration suite, SHALL NOT require network access, and SHALL derive the release facts it
compares against from the repository's own release tuple or from git rather than from a hand-written
constant that the documents could silently contradict.

#### Scenario: a build example is edited back to a mixed identity

- **WHEN** a fenced build example in the install SSOT is edited so that its release id names one release
  while its release commit names another
- **THEN** the suite fails, naming the block's line and the two conflicting identities

#### Scenario: the check is not runnable offline

- **WHEN** the suite runs with no network available
- **THEN** the check still executes, because it reads only repository files

### Requirement: Every in-page link in the install documentation SHALL resolve

The repository test suite SHALL fail when `docs/install/README.md` or `docs/USER_GUIDE.md` contains a
same-file markdown link whose fragment does not match a heading in that file, or when either document
references a `dist/mount/` path that does not exist in the tree.

#### Scenario: a heading is renamed

- **WHEN** a heading that an in-page link points at is renamed or removed
- **THEN** the suite fails and names the document and the dangling fragment

### Requirement: The guard SHALL be falsifiable

Every check in the guard SHALL be exercised against a mutated copy of the document that makes that check
fail, so that a guard which cannot fail is rejected rather than trusted.

#### Scenario: the guard is gutted

- **WHEN** a check is changed so that it always passes
- **THEN** its paired mutation case fails, because the mutation no longer produces the required failure
