# Spec delta — far-residual-closure-admission

## ADDED Requirements

### Requirement: FAR round produces one ranked ruling with an explicit authority boundary

The round SHALL produce exactly one ruling artifact naming, for every residual item, its friction,
feasibility, engineering necessity, over-engineering ruling, alignment claim and the authority it needs,
and SHALL separate actions executable by an agent under the round's own authority from actions that are
structurally the owner's.

#### Scenario: an owner-gated item is encountered
- **WHEN** an item requires a merge, a release, a cross-repository code promotion, a canonical control-plane
  edit or a product-host ACL change
- **THEN** the round prepares it as a single-action form with its authority named and does not execute it,
  regardless of any pre-authorisation of the ruling

### Requirement: Executed items carry re-derivable receipts

Every action the ruling marks executable-now SHALL leave a raw receipt on disk produced by a script, and
SHALL NOT be reported as done on the strength of its own summary alone.

#### Scenario: a count is quoted in the ruling
- **WHEN** the ruling or any artifact states a count
- **THEN** that count SHALL be derivable from an artifact on disk, and an independent lane SHALL be able to
  re-derive it; a count that exists only in the report is not evidence

### Requirement: The checker lane is pinned to a different model axis than the writer

The verification lane SHALL be dispatched with a pinned required arm that is not the writer's own model, and
the served arm SHALL be recorded as equal to the required arm.

#### Scenario: the verification pool's rank-1 arm is the writer's model
- **WHEN** the pool's rank-1 arm equals the writer's arm
- **THEN** the checker is pinned by rank and by required arm, the registry is read and never edited, and a
  failure to serve the pinned arm is recorded as a blocking first-fail rather than silently falling back

### Requirement: Every probe can fail

Any probe or guard landed by this round SHALL be shown failing on a control case before it is shown passing,
and its stated rule SHALL be described behaviourally rather than as an exact description of the code.

#### Scenario: an OS write-denial claim
- **WHEN** the round reports that an OS-enforced write denial was demonstrated
- **THEN** the raw stdout/stderr of the denied attempt, the control case that must succeed, the exact ACL
  command forms and the cleanup receipts SHALL all be present, or the result SHALL be reported as
  `ACL_UNENFORCEABLE`/NOT_REPRODUCED instead

### Requirement: Session closeout and handover are first-class products

The round SHALL emit a handover checkpoint carrying the exact subject identity, the open tickets, the owner
decisions, the rollback pointer and the next legal action, plus a single evidence MD mirrored byte-identical
to the review roots with SHA-256 equality.

#### Scenario: a successor round resumes
- **WHEN** a successor round picks up this work
- **THEN** it can identify the frozen subject, the open items with their owners, and the exact next action
  without re-deriving any of them
