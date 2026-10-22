# git-credential-noninteractive-default

## ADDED Requirements

### Requirement: An unattended process MUST NOT be able to reach an interactive credential prompt

No git invocation issued by an unattended process on this host SHALL be able to present an
interactive credential prompt — whether a graphical account-selection window or a terminal prompt.
Authentication SHALL either be satisfied silently from the existing credential store, or fail
closed with an error, within a bounded time.

#### Scenario: No usable credential exists and no human is present

- **WHEN** a git invocation requires authentication for a host that the credential store cannot answer for
- **THEN** the invocation terminates with an error inside the bounded measurement window
- **AND** the host-measured instrument observes zero visible account-selection or credential windows
- **AND** it observes no GUI credential-helper child process

#### Scenario: A usable cached credential exists

- **WHEN** a git invocation requires authentication and the credential store can answer
- **THEN** the invocation succeeds silently with unchanged behaviour, so the containment has not
  over-reached by removing the cached-credential fast path

#### Scenario: The second prompt surface below the helper layer

- **WHEN** a configured credential helper returns no credential
- **THEN** the process environment or the default configuration additionally prevents git's own
  prompt fallback from waiting for a terminal, because a helper-level fix alone leaves that path open

### Requirement: The non-interactive posture MUST be a default, not an invocation-level opt-in

A control that must be remembered at every call site SHALL NOT be treated as a control. The
non-interactive posture SHALL hold for an ordinary invocation that carries no flags and no
specially prepared environment.

#### Scenario: A bare invocation with no flags

- **WHEN** an unattended session issues a bare git command with no `-c` overrides and no
  prepared environment variables
- **THEN** the effective credential-helper resolution does not reach a prompt-capable helper
- **AND** the reason is the higher-priority configuration, not the caller's discipline

#### Scenario: A dropped flag is not silently tolerated

- **WHEN** a previously working invocation is reconstructed by hand and a per-invocation flag is
  omitted
- **THEN** the committed default still prevents the interactive prompt, so the omission degrades
  authentication rather than blocking the session

### Requirement: The system-scope configuration SHALL NOT be mutated to achieve this

The containment SHALL be achieved without administrator rights and without editing the
installer-managed system configuration, so that the human's interactive credential path remains
available and the change stays reversible.

#### Scenario: Displacement without privilege

- **WHEN** the higher-priority configuration carries an empty helper value followed by a
  non-interactive helper
- **THEN** the lower-priority system-scope helper is not reached, and the system file's bytes are
  unchanged

#### Scenario: Rollback

- **WHEN** the user-scope preimage recorded before the change is restored
- **THEN** the effective resolution is byte-identically the pre-change state

### Requirement: The control MUST have a consumer, and the claim MUST match it

Any invariant introduced by this change SHALL have a component that reads it and refuses when it
is unsatisfied. Where that consumer has no caller, or where the broker cannot be activated within
this change's authority, the result SHALL be reported as `DETECTION_ONLY` or `NOT_ACTIVATED`
respectively, and SHALL NOT be reported as prevention.

#### Scenario: The invariant is unsatisfied at preflight

- **WHEN** the effective helper resolution reaches a prompt-capable helper of a form other than
  the admitted one
- **THEN** the preflight exits non-zero and names the unsatisfied check
- **AND** an absent or unreadable input yields `INCONCLUSIVE`, never a pass

#### Scenario: A present-but-unwired control

- **WHEN** the consumer exists but no caller outside this change's own worktree invokes it
- **THEN** the round records `DETECTION_ONLY` together with the callsite evidence, and does not
  claim the failure mode is prevented
