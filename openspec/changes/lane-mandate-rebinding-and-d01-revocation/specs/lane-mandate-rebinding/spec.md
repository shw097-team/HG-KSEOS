# lane-mandate-rebinding

## ADDED Requirements

### Requirement: The PLAN lane is bound to the owner-mandated model

The registry SHALL bind the PLAN lane to `opencode-go / deepseek-v4.1-flash`, so that no registry site declares `openai-codex / gpt-6.1-sol` as the PLAN binding.

#### Scenario: A registry site still binds PLAN to the old model

- **WHEN** any PLAN site (`routes[PLAN]`, `lane_chains.PLAN[0]`, `sod.plan_lane`, or a PLAN entry in the projection bindings) resolves to `gpt-6.1-sol`
- **THEN** the change is incomplete, and the drift gate reports the exact path and JSON pointer as a hard finding

#### Scenario: The rebound PLAN model is resolved

- **WHEN** the PLAN route is resolved after the change applies
- **THEN** it resolves to `opencode-go / deepseek-v4.1-flash` with `canonical_identity: deepseek-v4.1-flash`

### Requirement: Every affected projection is synchronized and the publication counter advances

The registry SHALL advance its declared publication counter (`epoch`) and SHALL synchronize every affected projection binding whenever its committed content changes.

#### Scenario: Committed content changes

- **WHEN** the registry's route content changes by the rebinding
- **THEN** the `epoch` advances and the projected site and `source_of_routes` binding agree, so the drift gate reports no stale pointer

#### Scenario: A binding is left stale

- **WHEN** a `projections[]` binding still expects the pre-change value
- **THEN** the drift gate fails on that pointer rather than passing silently

### Requirement: The VERIFY/SECURITY alternate arm is reachable in the projected dispatch

The system SHALL preserve the VERIFY/SECURITY alternate arm and SHALL carry it, together with the selection authority, into the projected dispatch, so the declared gap `projection_drops_dual_arms` is closed.

#### Scenario: A dispatch is projected

- **WHEN** a route is projected for a VERIFY/SECURITY dispatch
- **THEN** the projection contains both arms and the `selection_authority`, not only the primary route

#### Scenario: The alternate arm is dropped to close the gap

- **WHEN** the fix would remove the alternate arm instead of projecting it
- **THEN** the change is rejected, because preservation AND reachability are both required

#### Scenario: The gap is still declared open

- **WHEN** the projection function still drops `arms[]` and `selection_authority`
- **THEN** `wiring_feasibility.projection_drops_dual_arms.state` remains `DECLARED_GAP_NOT_FIXED` and the change is incomplete

### Requirement: The round's selected arm is expressible without rewriting history

The registry SHALL express the owner's per-round arm selection as an additive field recorded beside the published arm history, and SHALL NOT rewrite or delete any existing arm or historical record.

#### Scenario: The owner names the round's checker model

- **WHEN** the owner mandates this round's checker as `opencode-go/glm-5.3-flash` under CODEX CLI
- **THEN** the selection is recorded in the additive round-selection field and serves the lane, while the arm A / arm B records and every historical field remain byte-unchanged

#### Scenario: A later round names a different arm

- **WHEN** a later round selects a different arm
- **THEN** the later selection is added forward and the earlier round's selection is still readable

### Requirement: The D-01 model substitution is revoked additively against its frozen bytes

The system SHALL record an ADDITIVE revocation of deviation `D-01` that names the original artifact path and its `sha256` and its falsifying evidence, and SHALL NOT mutate the original artifact.

#### Scenario: The revocation is written

- **WHEN** the D-01 revocation is recorded
- **THEN** it names the original artifact path plus its `sha256` (`f54dec16d48d9432d61d3394b3468cfd2a12ddf5dfecf724a34922c8246e7fc2`) and the falsifying A/B result, so the frozen bytes and any manifest binding them stay valid

#### Scenario: The original artifact would be edited

- **WHEN** a proposed revocation would modify the original D-01 artifact's bytes
- **THEN** the change is rejected, because a revocation must be keyed by the digest of the bytes it revokes

#### Scenario: The revoked blocker is re-checked

- **WHEN** the declared blocker is re-measured
- **THEN** the same isolated home, auth, model and prompt is recorded as producing HTTP 400 exit 1 on Codex CLI `0.147.0-alpha.6.5` and `OK` exit 0 on `0.162.0-alpha.17.2`, confirming the blocker was a local toolchain artifact

### Requirement: The revoked substitution's checker lane is rebound to the mandated model

The revocation SHALL bind the checker lane to the currently mandated model, replacing the revoked substitution's binding for the forward mandate.

#### Scenario: The forward checker lane is resolved

- **WHEN** the checker lane is resolved after the revocation
- **THEN** it binds the currently mandated model `opencode-go/glm-5.3-flash`, not the revoked `gpt-5.6-sol` substitution

### Requirement: An owner-excluded model family cannot be restored by a default or an inherited child setting

The system SHALL refuse to restore, for a round, any model family the owner excluded, whether the candidate source is a registry default, a fallback arm, or an inherited child setting.

#### Scenario: A registry default names an excluded family

- **WHEN** a registry default or fallback arm would select a family the owner excluded for the round
- **THEN** the dispatch refuses, and the family is not restored

#### Scenario: A child setting inherits an excluded family

- **WHEN** a delegation child would inherit an excluded family from a parent setting
- **THEN** the exclusion holds, and the child does not dispatch on the excluded family

#### Scenario: An excluded family is silently downgraded

- **WHEN** a dispatch names an excluded family and the system would substitute a permitted model without recording it
- **THEN** the silent downgrade is rejected, because the refusal and the substitution must both be recorded

### Requirement: The SoD encoding is reconciled with the owner's recorded-overlap semantics

The registry's static separation-of-duties encoding SHALL NOT declare a strict pair that the same registry records in `declared_conflicts` as an accepted identity overlap. Where an overlap is recorded, it SHALL stay recorded as a fact together with a named compensating control, and SHALL NOT be enforced as a refusal.

#### Scenario: A strict pair contradicts a recorded conflict

- **WHEN** `sod_invariants.pairs` requires `maker != checker` for a pair that the same registry records in `declared_conflicts` as an accepted overlap (`SOD-APPLY-01`, `pairs: [[EXECUTE, PLAN]]`)
- **THEN** the encoding is internally contradictory, and the conformance suite fails on the maker/checker identity — so the strict pair is removed and the overlap remains recorded

#### Scenario: The reconciled encoding is exercised

- **WHEN** the reconciled encoding is exercised by the conformance suite
- **THEN** every remaining declared pair resolves without a violation, the recorded conflict is still present and readable, and the model bound to each lane is unchanged by the reconciliation

### Requirement: A round-scoped checker override is declared and its independence stated

Where the owner scopes a single round's checker to a model that is not one of the registry's published arms, the round SHALL record the override additively, SHALL state that the checker's independence then rests on lane/role/harness separation rather than on model distinctness, and SHALL NOT rewrite the published arm records.

#### Scenario: The round's checker is overridden

- **WHEN** the owner mandates this round's checker as `opencode-go/deepseek-v4.1-flash`
- **THEN** the override is recorded as a round-scoped deviation with its compensating control, the published arm selection (`selected_arm: A`, `selected_arm_identity: glm-5.3-flash`) remains readable as the round's previously declared arm, and no historical record is rewritten

#### Scenario: The override is mistaken for an applied registry change

- **WHEN** a task-scoped checker override would be written into the registry as the published arm
- **THEN** it is rejected, because a one-round override is not a registry arm and must not rewrite the arm model

