# hygiene-and-readme-closure

## ADDED Requirements

### Requirement: The repository homepage states its claim ceiling

The root `README.md` SHALL state, on the homepage itself, that the repository is a governance projection mirror
whose control plane is HG-KSEOS, and SHALL name what is NOT claimed (independent acceptance, AO acceptance,
DOC-05 effect admission, production release), so that an external reader cannot mistake archived candidate
evidence for an accepted release.

#### Scenario: An external engineer opens the repository for the first time
- **WHEN** the reader opens the repository homepage
- **THEN** the positioning, the evidence-prefix map and the explicit non-claims are visible without following a
  link, and the reading order for the evidence tree is stated

### Requirement: Branch hygiene removes only verified-merged branches

Deleting a remote branch SHALL be gated on having verified, from the live API, that the branch's pull request is
merged; every deleted branch's tip SHA SHALL be recorded in the round's receipt so the ref can be restored.

#### Scenario: A branch's pull request is still open
- **WHEN** the hygiene pass finds a branch whose pull request is not merged
- **THEN** that branch is KEPT and named in the receipt with the reason, and no ref is deleted

### Requirement: Destructive local cleanup is owner-gated

Cleanup of local evidence-preserving artefacts (database copies, worktrees, runtime caches) SHALL be recorded
with path, size and the exact minimal command, and SHALL NOT be executed by the round that measured it.

#### Scenario: The audit finds a large database copy under var/
- **WHEN** the round proposes to reclaim that space
- **THEN** the proposal is written as an owner-gated candidate and no file is deleted
