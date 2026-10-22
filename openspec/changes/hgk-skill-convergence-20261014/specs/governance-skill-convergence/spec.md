## Purpose

Preserve governed operating knowledge while reducing saturated entry loading and exposing full-current advisory findings without creating a second control plane or weakening independent verification.

## ADDED Requirements

### Requirement: Reversible source-preserving extraction
The migration SHALL preserve the exact original bytes, every original clause and locator, frontmatter identity and trigger, and the necessary inline authority/refusal/SoD/rollback core. Original content SHALL be reconstructible from the candidate and its ordered migration map, not from a hidden pristine source alone.

#### Scenario: Valid complete migration
- **WHEN** the nonempty frozen source and every candidate slice match the ordered map
- **THEN** reverse reconstruction equals the original bytes and digest exactly

#### Scenario: Changed or missing slice
- **WHEN** a slice is removed, reordered or altered
- **THEN** reconstruction validation fails and apply is refused

### Requirement: Topic navigation and alias compatibility
The candidate SHALL group operational/history content into bounded topic navigation, preserve old locators through compatible aliases, and introduce zero additional dangling references or unexplained orphans compared with the frozen baseline. Immutable historical counterexamples SHALL remain retrievable and SHALL NOT override current normative contracts.

#### Scenario: Old alias lookup
- **WHEN** a prior supported file or section locator is requested
- **THEN** the original clause is reachable through an explicit compatible mapping

#### Scenario: Target missing
- **WHEN** a migrated topic target or alias target is absent
- **THEN** validation rejects the candidate rather than reporting a healthy routing map

### Requirement: Full-current changed-skill advisory evidence
A successful supported changed-skill mutation SHALL expose the complete current lint findings separately from the existing delta-only warning field. Existing advisory severity and mutation outcomes SHALL remain unchanged. Lint evaluation failure SHALL be distinguishable from a clean evaluated result. Batch output SHALL preserve the additive evidence for successful operations.

#### Scenario: Standing oversized body changes
- **WHEN** an already oversized skill receives a small patch that introduces no new lint rule
- **THEN** full-current evidence still shows oversized-body while the delta warning retains its original semantics

#### Scenario: Linter unavailable
- **WHEN** evaluation cannot run
- **THEN** the result indicates unavailable or inconclusive evaluation, never evaluated-clean

### Requirement: Independent regression evidence and scope
Global convergence/regression review SHALL bind a frozen nonempty corpus denominator, distinguish changed and unchanged surfaces, and execute positive, negative, boundary, cross-role holdout, alias and rollback tests. Unexecuted model/profile/consumer surfaces SHALL remain NOT_VERIFIED. Maker SHALL NOT sign acceptance or repair the subject during independent review.

#### Scenario: Missing denominator or stale subject
- **WHEN** verification lacks a bound nonempty corpus or the subject changes
- **THEN** the verdict is invalid or inconclusive and canonical apply is blocked

### Requirement: Guarded apply and rollback
Local apply SHALL require a current admitted binding, independent exact-subject verdict and pre-image match. The operation SHALL retain immutable pre-images, restore touched files on partial failure, and verify live readback. Rollback SHALL refuse unrelated post-apply drift and restore exact original bytes on an unchanged applied generation.

#### Scenario: Stale pre-image
- **WHEN** a canonical target differs from its admitted frozen pre-image
- **THEN** apply refuses before any target is changed

#### Scenario: Roundtrip recovery
- **WHEN** a verified candidate is applied and rolled back without intervening drift
- **THEN** every target returns to the exact original bytes and no unrelated file is changed
