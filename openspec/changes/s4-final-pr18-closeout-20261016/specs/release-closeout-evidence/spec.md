## Purpose

Define a read-only, reproducible freeze-and-return procedure that lets an external acceptance
officer verify a published prerelease closeout from one self-describing packet, without the maker
performing any merge, tag or release effect.

## ADDED Requirements

### Requirement: Frozen subject identity readback

The closeout SHALL freeze the live identity of every release subject from an authoritative live
source, and SHALL NOT substitute the text of a governing report for that readback.

#### Scenario: Subjects match the frozen values
- **WHEN** the readback is executed for `main`, the candidate pull requests, and the published tag
- **THEN** each subject's SHA, tree, file count and asset digests are recorded next to the expected
  value, with a per-field match flag and one overall verdict

#### Scenario: A subject drifted
- **WHEN** any recorded identity differs from the frozen expected value
- **THEN** the packet records the drift explicitly and only the affected checks are re-run

### Requirement: Test denominators stay separate

The closeout SHALL report each execution environment's test result as its own denominator, and SHALL
NOT reconcile or rewrite a skip count to make the numbers agree.

#### Scenario: Hosted and local results differ
- **WHEN** the hosted CI reports a different skipped count than the local run
- **THEN** both numbers are published as-is with their environment named

### Requirement: Immutable published release

The closeout SHALL NOT modify, re-tag, re-upload or in-place replace any asset of an already
published release, and SHALL distinguish the tag target, the build-source scope and any later
commits that are not part of the release.

#### Scenario: A defect is found in a published asset
- **WHEN** a residual such as a stale provenance header inside the published document is confirmed
- **THEN** it is disclosed as a non-blocking observation with its locator, and its correction is
  deferred to the next release that is built from scratch

### Requirement: Owner-only external effects

The closeout SHALL return every merge, tag, release and phase-ratification effect as an explicit
owner action request carrying the expected head SHA, and SHALL NOT report such an effect as done
until an owner readback shows it complete.

#### Scenario: The agent has repository write capability
- **WHEN** the credentials could technically perform a merge
- **THEN** the merge is still not performed, and the packet reports `OWNER_ACTION_REQUIRED`

### Requirement: Checker basis disclosure

Every checker verdict in the packet SHALL state whether the checker is a different model axis from
the maker, and SHALL state that independence rests on process, lane and evidence path when the same
model serves both roles.

#### Scenario: Same model serves maker and checker
- **WHEN** the writer and the checker resolve to the same provider and model
- **THEN** the verdict reads `PARTIAL` on the model axis and no cross-model independence claim is
  published
