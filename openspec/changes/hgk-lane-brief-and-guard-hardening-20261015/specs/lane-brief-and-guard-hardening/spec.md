# lane-brief-and-guard-hardening

## ADDED Requirements

### Requirement: The guarded subject is the tracked file set, or ignoring VCS-ignored byproducts

The lane dispatcher SHALL define the guarded subject as the tracked (packet) file set when the
subject sits in a VCS tree, and SHALL treat VCS-ignored byproducts (e.g. `__pycache__/`, `*.pyc`) as
`added/removed — recorded, not fatal` rather than as verdict-voiding events. Where no VCS is
available the dispatch brief SHALL declare the ignored-pattern set explicitly and every change of an
ignored path SHALL still be recorded in the guard receipt.

#### Scenario: out-of-band hygiene does not void a verdict
- **WHEN** a lane completes cleanly over a guarded subject and an orchestrator afterwards deletes a gitignored byproduct inside it
- **THEN** the guard outcome is the recorded-not-fatal code
- **AND** the verdict is NOT voided

#### Scenario: the not-fatal class stays recorded
- **WHEN** any ignore-class path is added or removed during or around the turn
- **THEN** the guard receipt records the row
- **AND** nothing is silently dropped

#### Scenario: tracked-file removal still voids
- **WHEN** a path in the tracked subject set is removed or changed during the turn without an intra-turn disclosure
- **THEN** the guard voids the verdict exactly as before this change

#### Scenario: subjects without VCS keep the guard fail-closed
- **WHEN** the guarded subject is not in a VCS tree
- **THEN** the guard uses the ignored-pattern list declared in the dispatch brief
- **AND** the guard remains fail-closed on the un-ignored subject set

### Requirement: Guard marker matching uses command context, not bare words

The remote-write marker check SHALL require a shell-looking occurrence (a line beginning with
`git`/`gh`/`curl`/`ssh`/`winget`, or an argv-shaped form) and SHALL ignore matches inside
negative/prohibition sentences. The check keeps its declared `detection_only` semantics; the
dispatcher SHALL NOT refuse a dispatch on a prose-only match.

#### Scenario: prohibition prose does not refuse the dispatch
- **WHEN** a dispatch brief contains `do not git push …` / `do not publish …` inside `do not`/`never`/`must not`/`SHALL NOT` sentences and no command-shaped line
- **THEN** the marker detector records the words, does not emit `ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED`, and the dispatch proceeds

#### Scenario: the recorded refusal briefs clear on replay
- **WHEN** the recorded raw refusal briefs from round R7-0 (markers `git push`, then `publish`) are replayed through the classifier
- **THEN** both classify as prose and no refusal is produced

#### Scenario: an actual command line still refuses
- **WHEN** a brief carries a literal `git push <url>` line or an argv-shaped invocation
- **THEN** `ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED` is still emitted and the dispatch is refused

### Requirement: Intra-turn subject sampling

The guard SHALL sample the guarded subject digest during the turn (bounded sampler, capped sweep
size) instead of comparing only the pre-turn vs post-turn state, and SHALL record any mid-turn write
that is later restored as an intra-turn boundary violation marked `CLEAN_WITH_INTRATURN_WRITES`,
never as a silent `CLEAN`.

#### Scenario: a write-and-restore inside the turn is caught
- **WHEN** during a turn a lane writes N paths inside the guarded subject and restores them before the turn's end-state comparison
- **THEN** the guard records `CLEAN_WITH_INTRATURN_WRITES` with the intra-turn violation rows
- **AND** never reports plain `CLEAN` while intra-turn writes exist in the record

#### Scenario: a clean turn is unchanged
- **WHEN** no intra-turn writes occur
- **THEN** the guard outcome and receipt shape are as before this change (no new fields on the normal path)

### Requirement: Guarded subject paths are declared in the dispatch brief

The standing dispatch brief template SHALL list every guarded subject path explicitly, so a lane can
see what it must not write into, and SHALL name a writable output root outside every listed subject
for lane outputs.

#### Scenario: the brief names the subject
- **WHEN** a dispatch brief is generated for a guarded lane
- **THEN** it contains the explicit subject-path block and the writable-output-root declaration
- **AND** a lane can distinguish them without reading any receipt

### Requirement: Nonce-carrier attribution records the surface probed

For every dispatch attempt that reports `ok=false ERR_NO_ARM_EMITTED_NONCE`, the receipt SHALL
record, additively beside the existing `nonce_absent_arms` field, which nonce-carrier surface was
probed per attempt (wrapper echo path, relay path, none-probed), so a reader can distinguish
wrapper non-emission from relay loss without re-running a lane. The existing receipt contract
(`lane-dispatch-honest-declarations`) is unchanged; the dispatcher still SHALL NOT report `ok=true`
without a positively attested nonce carrier.

#### Scenario: the recorded receipts replay unchanged
- **WHEN** the recorded R6/R7 receipts (`usage_receipt_ok=true`,
  `nonce_absent_arms=[opencode-go/deepseek-v4.1-flash]` on EXECUTE,
  `opencode-go/glm-5.3-flash` on VERIFY) are replayed through the new record shape
- **THEN** the old fields keep their values and consumers matching only them keep working

#### Scenario: the per-attempt carrier surface is present
- **WHEN** any attempt returns without a nonce
- **THEN** the receipt names the carrier surface probed for that attempt (or `none-probed`)
- **AND** the repair owner can distinguish wrapper non-emission from relay loss from the record alone

### Requirement: PIPD mutation drivers take an explicit output destination

The PIPD mutation driver (`probe_mutations.py`) SHALL accept an explicit `--out-dir`/`DEST` for its
RAW receipts and records, SHALL refuse to run when its default destination would resolve inside a
declared guarded subject, and SHALL make writing into a subject possible only through an explicit
override flag that still refuses a guarded-subject destination.

#### Scenario: a re-run writes where it is told
- **WHEN** the driver is invoked with `--out-dir` outside every guarded subject
- **THEN** all RAW receipts and `mutation_records.json` land only under that out-dir
- **AND** no path of the guarded subject is written

#### Scenario: the defaulting destination is refused
- **WHEN** no `--out-dir` is given and the historical default would resolve inside a declared guarded subject
- **THEN** the driver refuses with a typed refusal
- **AND** zero writes occur anywhere

### Requirement: Every behaviour in this capability is deterministically test-covered

The tests for the requirements above SHALL be deterministic and SHALL NOT depend on the network, a
real model, the relay, a real credential value, or any live evidence tree being writable; recorded
raw receipts and briefs from the round serve as fixtures.

#### Scenario: the suite is the gate
- **WHEN** the named test command for this surface is run on the candidate bytes
- **THEN** the positive/negative/boundary cases for each requirement pass in full against the recorded fixtures
