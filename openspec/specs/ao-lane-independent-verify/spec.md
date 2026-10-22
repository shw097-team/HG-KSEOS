# ao-lane-independent-verify Specification

## Purpose
Define the externally observable behaviour of the CODEX-CLI lane dispatch path when its VERIFY/SECURITY
role is used as an independent check: what must be refused before a turn is spawned, what evidence must
survive the turn, how non-mutation is established for a checker that needs a writable sandbox, and which
limits remain out of scope.
## Requirements
### Requirement: A required arm is enforced independently of the gate
The dispatch SHALL enforce a named required arm whether or not the identity gate ran:
`--no-identity-gate` SHALL switch off the gate and SHALL NOT switch off this
guarantee. The named arm SHALL be verified on its own when the gate was skipped,
and a run SHALL fail closed if the named arm is not in the lane's pool
(`ERR_LANE_REQUIRED_ARM_ABSENT`) or does not survive verification.

#### Scenario: disabling the gate does not disable the required arm
- **WHEN** the gate is skipped by flag and the named required arm cannot run
  without a human
- **THEN** the run is refused with that arm's typed refusal and nothing is spawned

#### Scenario: pool membership is judged against the pre-gate candidate set
- **WHEN** the named required arm is in the lane's pool but refused by the gate
- **THEN** the refusal names that arm's own code rather than reporting it absent

### Requirement: A declared identity requirement is carried, not decorative
When the pool artifact declares `identity_requirement` for an arm, the dispatch
SHALL carry that value into the arm it evaluates, so the declaration takes
precedence over the provider heuristic and a misspelled value is refused
(`ERR_LANE_IDENTITY_UNKNOWN`) on the end-to-end path.

#### Scenario: the pool's declaration overrides the provider default
- **WHEN** the pool declares an arm needing a login in its own home and the lane
  home holds no credential
- **THEN** the run is refused with `ERR_LANE_IDENTITY_NOT_PREAUTHORIZED`

#### Scenario: a misspelled declaration is refused end to end
- **WHEN** the pool declares a value outside the three classes
- **THEN** the refusal is `ERR_LANE_IDENTITY_UNKNOWN`

### Requirement: Health reads credential content, not a substring
The identity probes SHALL decide from parsed credential content: a relay
credential is usable only if a non-empty refresh token is present somewhere in
the document, an explicit re-auth marker makes it unusable, and a CLI home needs
a non-empty credential string. A literal null, an empty string or an account
marked for re-authentication SHALL NOT read as healthy.

#### Scenario: null or empty refresh material is unhealthy
- **WHEN** the relay credential carries `refreshToken: null`, an empty or
  whitespace-only token
- **THEN** the gate reports the arm unusable

#### Scenario: a re-auth marker is unhealthy
- **WHEN** the credential document marks the account as needing re-authentication
- **THEN** the gate reports the arm unusable even if a token string is present

### Requirement: An escalated lane must be bounded by a guard
An escalated sandbox SHALL require declared guard roots, because an escalated
sandbox has no sandbox root and the guard is the only bound on the subject. The
exception SHALL require an explicit flag and SHALL be recorded in the receipt.

#### Scenario: escalation without a guard root is refused
- **WHEN** a lane is escalated above its role default with no guard root and no
  explicit exception flag
- **THEN** the run is refused with `ERR_GUARD_REQUIRED_FOR_ESCALATED_CHECKER`

#### Scenario: the exception is recorded, not silent
- **WHEN** the exception flag is supplied
- **THEN** the receipt states that the escalation was unguarded

### Requirement: Harness output never lies inside a guarded subject
The dispatch SHALL refuse when any of its own output paths (the attempt log
directory, the receipt, the attempts trail) lies inside a declared guard root,
because those writes would otherwise register as subject changes.

#### Scenario: a guard root containing harness output is refused
- **WHEN** a guard root contains the receipt or attempt log path
- **THEN** the run is refused with `ERR_GUARD_ROOT_CONTAINS_HARNESS_OUTPUT`

### Requirement: A declared guard root that does not resolve is refused
A guard root that does not resolve to an existing file or directory SHALL be
refused rather than producing an empty snapshot that reads as an unmodified
subject.

#### Scenario: a vacuous guard is refused
- **WHEN** a declared guard root does not exist for the running process
- **THEN** the run is refused with `ERR_GUARD_ROOT_MISSING`

### Requirement: Persisted streams are the child's own bytes
Where the child's raw bytes are available, the dispatch SHALL persist those bytes
and SHALL record that the artifact is byte-exact. A stream reconstructed by
decoding with replacement SHALL NOT be described as byte-identical to the child's
output.

#### Scenario: a non-UTF-8 byte survives
- **WHEN** the child emits a byte sequence that is not valid UTF-8
- **THEN** the persisted file contains the bytes the child emitted and the
  recorded digest matches them

### Requirement: Attempt evidence is addressable per run
An attempt's persisted stream SHALL be addressable per run, so that re-running
with the same receipt path cannot overwrite a previous attempt's evidence.

#### Scenario: two runs at the same rank keep both logs
- **WHEN** two runs of the same rank write to the same log directory
- **THEN** both attempts' streams remain readable at distinct paths

### Requirement: The required arm must be served, not merely admitted
When a required arm is named, the receipt SHALL be not-ok unless that exact arm
served the turn (`ERR_REQUIRED_ARM_NOT_SERVED`), because surviving the gate does
not guarantee being used.

#### Scenario: a runtime failure cannot silently serve another arm
- **WHEN** the required arm passes the gate but another arm serves the turn
- **THEN** the receipt is not-ok and names both the required and the served arm

### Requirement: Residual limits are disclosed with the capability
The capability SHALL disclose that (a) a before/after digest comparison detects
residue and not transient modification, (b) content-equivalent recreation of a
guarded file is not distinguishable, (c) writes outside the declared guard roots
are not measured, and (d) the relay-health probe reads credential files and does
not contact the relay, so the turn's usage receipt remains the operative verdict.

#### Scenario: detection is not described as prevention
- **WHEN** the non-mutation guard is described
- **THEN** it is classified as detection, with the unmeasured write paths named

### Requirement: Pre-spawn identity refusal
The dispatch path SHALL classify every candidate arm by the identity it needs
(`none` for a key-auth arm whose credential the relay holds, `cli_login` for an arm
that needs a login in its own home, `relay_pool` for an arm that consumes the
relay's subscription credential) and SHALL refuse the arm BEFORE spawning a turn
when that identity is not usable without a human. A refusal SHALL be typed
(`ERR_LANE_IDENTITY_NOT_PREAUTHORIZED`, `ERR_RELAY_OAUTH_NEEDS_REAUTH`,
`ERR_LANE_IDENTITY_UNKNOWN`) and SHALL be reported in the receipt. A refused arm
SHALL NOT be spawned.

#### Scenario: an OAuth arm without refresh material is refused before the spawn
- **WHEN** a candidate arm requires the relay's subscription credential and the
  relay home carries no refresh material
- **THEN** the dispatch refuses with `ERR_RELAY_OAUTH_NEEDS_REAUTH`, spawns no
  turn, and creates no attempt log

#### Scenario: every arm refused refuses the whole run
- **WHEN** no candidate arm survives the gate
- **THEN** the run exits with a typed refusal stating that nothing was spawned,
  rather than proceeding with an empty candidate list

#### Scenario: an undeclared or misspelled requirement is refused, not ignored
- **WHEN** an arm declares an `identity_requirement` value outside the three
  classes
- **THEN** the arm is refused with `ERR_LANE_IDENTITY_UNKNOWN`

#### Scenario: an undeclared requirement falls back to a provider rule
- **WHEN** an arm declares no `identity_requirement`
- **THEN** an `openai-codex`/`openai` arm is treated as `relay_pool` and any other
  provider as `none`

### Requirement: Health means refreshability, not expiry
The relay-side health probe SHALL report healthy when refresh material is present
and SHALL NOT treat an expired access token as a failure, because refresh is
single-flight and automatic. The probe SHALL read credential files and SHALL NOT
require an interactive login to decide.

#### Scenario: an expired access token does not refuse a healthy arm
- **WHEN** the relay credential carries an `expiresAt` in the past together with
  refresh material
- **THEN** the gate reports the arm usable

#### Scenario: a missing relay home is a typed refusal
- **WHEN** the relay home does not exist or carries no credential file
- **THEN** the gate reports the arm unusable with `ERR_RELAY_OAUTH_NEEDS_REAUTH`

### Requirement: A required arm fails closed instead of degrading
The dispatch SHALL accept a named arm that must survive the gate. When the named
arm is refused, or is absent from the lane's pool, the run SHALL fail closed
(`ERR_RELAY_OAUTH_NEEDS_REAUTH` or `ERR_LANE_REQUIRED_ARM_ABSENT`) instead of
silently running a different arm.

#### Scenario: a refused required arm does not degrade to a key arm
- **WHEN** the named required arm is refused by the gate while other arms survive
- **THEN** the run exits with the required arm's refusal code and no turn is
  spawned, even though a usable arm exists

#### Scenario: a required arm outside the pool is distinguished from a refused one
- **WHEN** the named required arm does not appear in the lane's pool at all
- **THEN** the run exits with `ERR_LANE_REQUIRED_ARM_ABSENT`

### Requirement: Full attempt output survives the turn
Every attempt SHALL persist its complete stdout and stderr, with a byte count and
a content digest recorded in the receipt and on the attempt's ndjson trail. The
persisted stream SHALL be byte-identical to what the child emitted, and the
receipt's bounded tail SHALL remain a convenience view rather than the evidence.

#### Scenario: a verdict outside the receipt tail remains recoverable
- **WHEN** an attempt produces a verdict, digest or refusal text that does not fall
  inside the receipt's bounded tail
- **THEN** the complete stream is readable from the recorded path and its digest
  matches the recorded digest

#### Scenario: the stored stream is not newline-translated
- **WHEN** the child emits a line feed inside its output
- **THEN** the stored bytes and the recorded digest describe exactly the emitted
  bytes on a platform whose default text mode would rewrite line endings

#### Scenario: no attempt log is claimed when none was written
- **WHEN** the dispatch runs without an attempt log directory
- **THEN** the receipt records no stdout/stderr path for the attempt

### Requirement: Measured non-mutation for an escalated-sandbox checker
When guard roots are declared, the dispatch SHALL digest every file under them
before and after the turn and SHALL void the receipt
(`ERR_CHECKER_MUTATED_SUBJECT`) when any guarded file was removed or changed. It
SHALL record added files without treating them as a violation, because a checker
legitimately writes its own verdict outside the guarded roots.

#### Scenario: a checker that modifies the subject has its verdict voided
- **WHEN** a checker turn changes a file under a guarded root
- **THEN** the receipt reports not-ok with `ERR_CHECKER_MUTATED_SUBJECT` and names
  the changed file

#### Scenario: an added file does not void the verdict
- **WHEN** a checker turn creates a new file under a guarded root and changes
  nothing else
- **THEN** the added file is recorded and the verdict is not voided

#### Scenario: a removed file voids the verdict
- **WHEN** a guarded file is deleted during the turn
- **THEN** the receipt is voided

#### Scenario: the guard is declared, not assumed
- **WHEN** no guard root is declared
- **THEN** the receipt records the mutation state as not guarded rather than
  claiming a clean subject

### Requirement: Disclosed limits travel with the capability
The capability SHALL state, in the artifact and in the receipt, that (a) the
checker verdict is advisory and not an acceptance, (b) cross-model separation is
not provided when the pool resolves every lane to the same model, (c) a
post-run digest comparison is DETECTION and not an operating-system level
read-only boundary, and (d) the relay-health probe reads credential files and
does not make a live completion call.

#### Scenario: an advisory verdict is not reported as acceptance
- **WHEN** a checker turn completes successfully
- **THEN** the receipt states that this proves the lane served the turn with a
  matching usage receipt and is not an acceptance of any subject

#### Scenario: the same-model overlap is named where it applies
- **WHEN** every lane in the pool resolves to the same provider and model
- **THEN** the round's record names that the checker's independence is process-only
  until a different model occupies at least one lane

