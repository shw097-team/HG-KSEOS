## Purpose

Define the externally observable behaviour of bounded, isolated independent
checker execution inside HG-KSEOS: what a checker run may read, what it may
produce, what it may never become, and how a stalled or repeated-failure run is
paused without granting or withholding canonical authority.

## ADDED Requirements

### Requirement: Advisory-only verdict ceiling
The checker execution path SHALL emit only advisory verdict values
(`CANDIDATE_PASS`, `CANDIDATE_FAIL`, `CANDIDATE_INCOMPLETE`) and SHALL NOT
produce, promote or impersonate an HGK `OracleReceipt` or any canonical
acceptance status. Any other verdict token SHALL be rejected before it is
staged.

#### Scenario: verdict outside the advisory enum is rejected
- **WHEN** a checker run returns a decision token that is not one of the three
  advisory values
- **THEN** the run fails closed, no advisory verdict file is staged, and the run
  state records a failure

#### Scenario: an advisory PASS never becomes a canonical PASS
- **WHEN** a checker run returns `CANDIDATE_PASS`
- **THEN** the staged output is an advisory receipt only and canonical
  acceptance remains with the existing HGK authorized path

### Requirement: Read-only candidate subject
The checker SHALL read the candidate subject only from a read-only snapshot
whose file digests are captured before the run, and SHALL fail closed if any
snapshot file digest differs after the run.

#### Scenario: candidate mutation during the run fails closed
- **WHEN** a checker run modifies any file inside the snapshot it was given
- **THEN** the run fails closed, no advisory verdict is staged, and the state
  record carries a failure event

#### Scenario: symlinked snapshot entry is refused
- **WHEN** the snapshot contains a symlink
- **THEN** the digest pass refuses the snapshot instead of following the link

### Requirement: Exact subject binding
A checker run SHALL reject any intake that does not carry a non-empty
`workorder_id`, `subject_digest` and `evidence_manifest_digest`, and SHALL
reject a verdict whose subject or evidence-manifest digest differs from the
frozen intake.

#### Scenario: incomplete intake is refused
- **WHEN** the intake document is missing `workorder_id`, `subject_digest` or
  `evidence_manifest_digest`
- **THEN** the run refuses to start and stages nothing

#### Scenario: mismatched digest is refused
- **WHEN** the checker returns a `subject_digest` that differs from the frozen
  intake
- **THEN** the run fails closed rather than staging the verdict

#### Scenario: staging may not overlap the snapshot
- **WHEN** the requested staging path is the snapshot path or a parent/child of
  it
- **THEN** the run refuses to start

### Requirement: Observational pause request with a bounded repeat trigger
The watchdog SHALL be observational only: it SHALL NOT write canonical task
truth, and it SHALL express a stall as a pause request that the owning runner
honours cooperatively. A run that is older than the overrun inspection interval
SHALL be paused when the same normalized blocker signature occurs strictly more
than four times since the last verified progress, when the heartbeat is stale,
or when no verified progress has occurred for twenty minutes. Four repeats SHALL
NOT trigger a pause.

#### Scenario: four identical failures do not pause
- **WHEN** the same blocker signature has occurred four times since the last
  verified progress and the run is past the inspection interval
- **THEN** the watchdog returns an investigate disposition, not a pause request

#### Scenario: fifth repeat after verified progress pauses
- **WHEN** the same blocker signature occurs five times after a verified
  progress event
- **THEN** the watchdog emits a pause request naming that signature

#### Scenario: verified progress resets the repeat window
- **WHEN** a verified progress event occurs after four failures
- **THEN** the earlier failures no longer count toward the trigger

#### Scenario: a different signature does not accumulate
- **WHEN** four failures carry one signature and a fifth carries a different one
- **THEN** no signature has exceeded the threshold

#### Scenario: corrupt or incomplete state fails closed
- **WHEN** a status snapshot cannot be parsed or is incomplete
- **THEN** the watchdog emits a pause request rather than skipping the run

#### Scenario: pause is cooperative, never canonical
- **WHEN** the watchdog emits a pause request
- **THEN** the runner stops co-operatively and the canonical lifecycle state is
  left pending or blocked, never accepted

### Requirement: Disclosed non-isolation and residual risk
The capability SHALL state in the artifact that a post-run digest comparison is
a detection guard and NOT a substitute for operating-system level read-only
mounts, and SHALL disclose the residual bypasses (direct binary invocation,
other write paths) rather than claiming prevention.

#### Scenario: a detection guard is not reported as prevention
- **WHEN** the capability is described or accepted
- **THEN** the description classifies the post-run digest comparison as
  DETECTION and names the bypasses that remain out of scope

### Requirement: The runner produces the verified-progress marker it is judged by
A checker run SHALL advance its verified-progress marker whenever the checked
child produces a non-failure event, and SHALL persist that advance in its local
state record. A run SHALL NOT be pause-eligible solely because it has been
running for longer than the no-verified-progress interval while it continues to
make observable progress.

#### Scenario: a long healthy run is not paused for lack of progress
- **WHEN** a checker run exceeds the no-verified-progress interval while it
  continues to emit non-failure events
- **THEN** its verified-progress marker is later than its start time and the
  watchdog does not pause it for lack of progress

#### Scenario: the marker is exercised through the runner, not a fixture
- **WHEN** the verified-progress behaviour is tested
- **THEN** the test drives the runner itself and reads the persisted state
  record, rather than hand-constructing a state record for the watchdog alone

### Requirement: Run identity is contained inside the state directory
A run identity SHALL be refused if it contains a path separator, a parent
directory marker, a drive-relative or absolute prefix, or any reserved
filesystem character. After the state path is formed, the run SHALL verify that
the resolved path lies inside the state directory and fail closed otherwise.

#### Scenario: a drive-relative run id is refused
- **WHEN** a run id such as `D:evil` is supplied while the state directory is on
  another volume
- **THEN** the run is refused before any path is formed or written

#### Scenario: containment is asserted, not assumed
- **WHEN** a state path is formed from a run id
- **THEN** the path is checked to be inside the state directory rather than
  trusted because the character list looked safe

### Requirement: Operator-facing text distinguishes raw from bounded evidence
Any message that directs an operator to evidence SHALL name the artifact
accurately: a verbatim child stream SHALL NOT be described as sanitized, and a
bounded signature log SHALL be named as such.

#### Scenario: a raw stream is not called sanitized
- **WHEN** a checker run fails because the child exited nonzero
- **THEN** the message does not describe the verbatim stream as sanitized

### Requirement: The shipped bridge configuration serves one request
The capability SHALL ship a proxy configuration that can serve at least one
responsible request for the checker model on a loopback interface, and SHALL
state the constraints the chosen proxy version imposes instead of referring to a
merely "pinned compatible" version. Credentials SHALL be environment references;
no key value SHALL appear in configuration or code.

#### Scenario: the shipped configuration is startable
- **WHEN** the shipped bridge configuration is started with the documented
  command on a loopback interface
- **THEN** the proxy starts and a request for the checker model returns a
  structured response object rather than an authentication or routing error

#### Scenario: provider-required routing is declared
- **WHEN** the configured provider requires an additional routing header
- **THEN** the shipped configuration carries it and the preflight names the same
  header, so the two cannot drift apart

### Requirement: Tests assert behaviour rather than source text
The capability's tests SHALL assert observable behaviour and SHALL NOT read
production source text to assert on its formatting or on a literal extracted
from it.

#### Scenario: a behaviour-preserving reformat does not fail a test
- **WHEN** a production module is reformatted without changing behaviour
- **THEN** no test fails

## MODIFIED Requirements

### Requirement: Isolated checker identity and credentials
A checker run SHALL use a dedicated isolated Codex home and SHALL NOT inherit
maker credentials, the maker session, editor/agent plugins with write authority,
git credential helpers or release authority. Every provider credential present
in the parent environment SHALL be removed from the child environment, not only
the credentials of the provider the maker lane happens to use, because the child
reaches the model only through the loopback proxy, which holds the provider
credential server-side.

#### Scenario: maker credentials are not inherited
- **WHEN** a checker run starts
- **THEN** every provider credential the parent environment carries is absent
  from the child environment, and the run's declared credentials are the
  checker's own

#### Scenario: the child's environment is checked, not assumed
- **WHEN** the credential isolation is tested
- **THEN** the environment actually handed to the spawned child is inspected and
  asserted to contain no provider credential
