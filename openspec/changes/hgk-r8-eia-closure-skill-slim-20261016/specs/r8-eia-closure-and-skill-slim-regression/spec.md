# r8-eia-closure-and-skill-slim-regression

## Purpose

Define source-bound R8-0 skill-slim, validator and checker regression evidence, publication corrections and owner-gated claim ceilings without converting local observations into acceptance.

## ADDED Requirements

### Requirement: Skill-slim gate preserves capacity and host loader parity

The skill regression gate SHALL evaluate each AVR and HGK candidate against its explicitly bound live subject and SHALL require `SKILL.md` to be at most 100000 bytes, valid frontmatter beginning at byte 0, matching skill identity, and host loader/selection/trigger/nontrigger parity. It SHALL reject reconstruction wrappers preceding frontmatter, invalid loader metadata, missing nested references, unknown physical-file intake and stale subject bindings. It SHALL report each check and candidate separately. Reference counts above 60 SHALL produce a WARNING only and SHALL NOT independently reject a candidate (EIA-R6-09 / K-16 / ACC-RQ08).

#### Scenario: Reference soft-cap is not promoted to a hard gate
- **WHEN** a candidate has 90 references and all hard requirements succeed
- **THEN** the result contains the over-60 WARNING and does not reject solely for that count

#### Scenario: Capacity boundary remains exact
- **WHEN** otherwise valid main files of 100000 and 100001 bytes are evaluated
- **THEN** the first satisfies the capacity check and the second is rejected by that check

#### Scenario: Slice wrapper breaks actual loader intake
- **WHEN** a candidate places an SKCV-SLICE marker before its YAML frontmatter or the actual host cannot select its skill identity
- **THEN** the loader parity check rejects even if source text remains recoverable

#### Scenario: True loading and nontrigger behavior are tested
- **WHEN** valid candidate bytes are exercised through the actual host loader with trigger, nontrigger and forged-tool-text fixtures
- **THEN** the intended skill loads for the trigger, does not spuriously activate for nontrigger or forged text, and its nested references resolve under the declared intake rules

### Requirement: Absorbed references remain byte-lossless

The gate SHALL verify every declared absorbed reference against frozen source bytes using full SHA-256, byte length and exact start/end byte offsets in the destination, preserving the AVR 10 and HGK 6 source-block reconstructions and nested intake. Only explicit absorbed markers SHALL classify a reference as an absorbed stub; small ordinary references SHALL NOT become stubs by size alone. Missing bytes, stale source hashes, wrong offsets, unreachable stubs or absent source inputs SHALL prevent a successful hard-gate result. Negative controls SHALL independently exercise lost bytes, SHA mismatch and offset mismatch.

#### Scenario: Stale absorbed source is rejected
- **WHEN** `verifier-lane-handover.md` differs from its frozen absorbed source SHA or its destination slice
- **THEN** the losslessness check rejects and identifies that source and mismatch without treating zero lost long lines as proof of byte equality

#### Scenario: Ordinary short reference stays ordinary
- **WHEN** a small reference has no absorbed marker and remains resolvable
- **THEN** the gate treats it as a normal reference rather than demanding a fabricated absorbed-stub record

#### Scenario: Missing-source or tamper controls fail closed
- **WHEN** a required source is absent or one byte, offset or recorded SHA is independently changed
- **THEN** the corresponding check reports failure or inconclusive non-success, never a vacuous successful reconstruction

### Requirement: Skill apply is guarded and independently reversible

Any future skill apply SHALL default to dry-run and require separate apply authorization, exact target allowlist, frozen full-SHA pre-image for every replaced file, per-run non-overwriting backups, no unlisted deletion, post-write byte/hash and host-loader verification, and a receipt binding before/candidate/after bytes and hashes, command, exit codes, warnings and rollback references. Drift SHALL abort before writes. Rollback SHALL restore exact pre-image bytes and be tested in an isolated rehearsal before live apply. A maker receipt SHALL NOT constitute independent acceptance.

#### Scenario: Dry-run and pre-image drift cause no writes
- **WHEN** the apply tool is invoked without explicit apply authorization or the current target differs from the pinned pre-image
- **THEN** it performs no live write and records dry-run or drift refusal distinctly

#### Scenario: Authorized apply can be rolled back exactly
- **WHEN** a separately authorized apply passes its preconditions and an isolated rollback rehearsal runs
- **THEN** the receipt binds backups and readback to the changed targets and the rehearsal restores exact pre-image bytes without overwriting an earlier backup

### Requirement: Validator evidence binds the rebased candidate and all eighteen mutations

R8-0 validator evidence SHALL bind the candidate to the full commit resolving frozen `main` baseline `dba4b19`, not the R7 `9bd33a1` tree, and SHALL re-measure `M01..M18` on that same candidate. M04, M06 and M16 SHALL each produce REJECT under ASSURED veto, expected-oracle pin and trace-digest tamper respectively; adjacent valid fixtures SHALL remain accepted. Evidence SHALL name runner SHA, candidate/base, expected and actual result, raw output, exit code and first failure per mutation. Each of the eight historically NOT_RUN mutations SHALL retain its ID and receive an applicability decision, source rationale, prerequisite/owner and execution or explicit approved non-applicability disposition. NOT_RUN SHALL remain distinct from failure, detected and approved non-applicability; counts SHALL be derived from unique rows. Independent re-run on the frozen rebased candidate SHALL be required before reconsidering EIA-R6-04 closure.

#### Scenario: Historical-base success is insufficient
- **WHEN** evidence was produced only against `9bd33a1` or an unbound candidate
- **THEN** it cannot satisfy R8-0 re-measurement even if M04/M06/M16 rejected there

#### Scenario: Critical negative and adjacent valid fixtures are distinguished
- **WHEN** the rebased candidate processes M04, M06 and M16 and their registered neighboring valid fixtures
- **THEN** each mutation rejects at its named oracle and valid fixtures remain accepted with raw outputs bound to that candidate

#### Scenario: Historical NOT_RUN rows are not manufactured into executions
- **WHEN** any of the eight missing runs lacks its fixture, authority or applicable runtime
- **THEN** the corresponding ID remains NOT_RUN with owner/prerequisite rationale unless a competent owner approves non-applicability, and it is never counted as executed or detected

### Requirement: Checker isolation distinguishes absence mechanism and deployment

Checker isolation evidence SHALL separately record effective guarded-root ACL/identity, evidence-of-absence, a scratch positive-write/denied-write/rollback-write mechanism proof, and whether that mechanism is applied to the real subject. Real-root ACL application SHALL remain proposal-only until explicitly owner-authorized. Scratch deny-ACE success SHALL NOT prove child overwrite/delete/rename protection or deployment to the subject. A shared Windows identity SHALL NOT be represented as maker/checker separation: distinct OS identities or a scoped checker sandbox SHALL be required to prove that separation. The checker SHALL have a writable output root outside the frozen subject; prevention claims SHALL require deliberate forbidden writes, subject-digest readback and demonstration that permitted output writes still work.

#### Scenario: Scratch proof does not close the finding
- **WHEN** a scratch deny-W ACE blocks file creation and rollback restores writing but the real subject has inherited Modify and no applied deny
- **THEN** the record states mechanism proven and isolation not fixed, retaining EIA-R6-03 as open

#### Scenario: Shared-identity deny is not separation
- **WHEN** maker and checker share a Windows identity and the same deny ACE applies to both
- **THEN** evidence describes only the demonstrated immutability scope and requires distinct identities or a sandbox before any maker/checker separation claim

#### Scenario: Scoped checker demonstrates both allowed and denied paths
- **WHEN** a separately authorized checker isolation deployment is tested
- **THEN** create/overwrite/delete/rename attempts against existing subject files and descendants are denied, permitted external output writes succeed, raw errors are retained, and the complete guarded-subject digest set is re-read unchanged

### Requirement: Reconciliation and publication errata preserve historical evidence

The reconciliation record SHALL retain EIA-R6-01 through EIA-R6-09 separately with original class/severity, observed source, local disposition, earliest owner, authority prerequisite, blocker and claim ceiling. EIA-R6-01/02 remediation SHALL use a new versioned errata, not a rewrite of the merged R6 packet or failed receipts. The errata SHALL identify both excluded paths exactly, distinguish manifest-declared and shipped path sets, bind historical and freshly observed publication heads/counts with observation UTC semantics, and mark stale 566/569 claims as superseded observations rather than repaired historical execution. Publication SHALL require its own publication authorization and exact-target readback; prior R6 maintainer authorization SHALL NOT approve an R8 merge or become a GitHub review object.

#### Scenario: Declared cache files are corrected without shipping them
- **WHEN** the recorded R6 manifest declares 583 paths but the historical tree ships 581
- **THEN** the versioned errata identifies `EVIDENCE/CNV-PIPD-LS-SP-20261015/R6_CHECKER/COPIES/probes/RUNNERS/__pycache__/probe_lib.cpython-311.pyc` and `EVIDENCE/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/RUNNERS/__pycache__/probe_lib.cpython-311.pyc` as the two excluded paths, preserves original evidence and never adds them merely to match the declared count

#### Scenario: A later publication head is observed rather than invented
- **WHEN** an authorized publication step reads a head different from the WS-D observation `b8ff81043e47e4b652522be34444bf52fcf4d65e`
- **THEN** it retains that historical observation and records the fresh exact head, unique path set, counts and observation time separately before checking equality on the corrected declared shipped set

### Requirement: Runtime source and policy claims remain owner-gated

R8-0 outputs SHALL state that Fresh G1 is not certified, G-A..G-H have no newly claimed PASS, the 221 runtime cases are not run by this proposal, and AO acceptance is not issued. Future stronger claims SHALL require legitimate RepoContext, owner-authorized WorkOrder, DEV/OPS ECP and TQAEP as applicable, effect-time DOC-05 admission, fresh independent raw receipts and the competent gate/AO authority. Source #6 SHALL remain FAIL_CLOSED without PIPD Source/Authority Owner classification of active normative versus superseded history; only after that ruling SHALL the active denominator be recomputed. The 20 KP `*-R04` polarity-conflict clauses SHALL remain quarantined from automated policy/release consumption until KP Policy Owner / DOC Owner correction and safety-negative/cross-KP regression. Quarantine SHALL not be counted as policy repair, and affected gates SHALL block if they consume unrepaired clauses.

#### Scenario: Planning validation does not lift runtime ceilings
- **WHEN** this proposal validates strictly or a local regression receipt is produced later
- **THEN** neither event becomes a Fresh G1 certificate, an eight-Gate PASS, a 221-case execution result, an AO verdict or release permission

#### Scenario: Source authority is missing
- **WHEN** source #6 lacks a competent owner ruling
- **THEN** it stays FAIL_CLOSED and full PI/PD/source coverage cannot be claimed by silently changing its classification or denominator

#### Scenario: Quarantined polarity conflict reaches a release path
- **WHEN** an automated policy or release checker attempts to consume an unrepaired KP `*-R04` clause
- **THEN** that consumption is blocked and referred to the policy owner rather than executing the contradictory MUST NOT polarity
