## Context

HG-KSEOS is the sole normative control plane; Hermes is the governed
runtime/orchestration plane; Codex CLI is the bounded implementation worker. The
`hgk_checker_upgrade` package (P0 admission candidate, 2026-10-09) specifies an
independent checker executed as a fresh, isolated Codex CLI process with
GLM-5.3-Flash served by OpenCode Go through a Responses→Chat-Completions
bridge, plus a 10-minute observational watchdog.

This change lands that specification as a **candidate** capability inside the
repository under an admitted WorkOrder, with the parts that cannot be qualified
in this environment reported as blocked rather than claimed.

## Goals / Non-Goals

**Goals**
- Materialize the checker runner, its candidate role binding, the watchdog and
  the negative fixtures as repository artifacts with tests.
- Keep the verdict advisory; keep canonical authority with the existing HGK
  authorization path.
- Make every claim ceiling explicit, including what was NOT qualified live.

**Non-Goals**
- Deploying, cutting over, enabling a canary or promoting anything.
- Building a second state machine, reducer, task database or orchestrator.
- Replacing the existing deterministic HGK checks: only semantic repository
  analysis is delegated to the checker.

## Decisions

### D1 — The adapter is a thin bounded layer, not a new engine
The checker adapter resolves (intake, snapshot, staging, codex home) and
delegates execution to a Codex CLI child process. State that the existing
lifecycle already owns stays with the lifecycle: the adapter records run state
only in a local state directory and never writes canonical tables.

*Alternative rejected*: emitting `OracleReceipt` rows directly. The canonical
acceptance transition has exactly one entry point
(`SharedSpine.resolve_acceptance` + `TRANSITIONS['acceptance']`); a checker that
writes acceptance state would be a second authority.

### D2 — Advisory verdict schema is a distinct type from `OracleReceipt`
The candidate verdict schema keeps `CANDIDATE_*` tokens and forbids the
canonical PASS/PARTIAL/FAIL/TEMP_CLOSED vocabulary. Status such as
`BLOCKED_HITL` belongs to the project lifecycle, not to an invented oracle
verdict.

### D3 — The checker role binding is a *candidate* declaration
`config/checker/checker-binding.candidate.json` carries
`status: CANDIDATE_NOT_ADMITTED` and names the identity fields required by
`RP002-EXECUTION-BINDING/2` (`workorder_id`, `candidate_digest`,
`acceptance_oracle_digest`, `evidence_manifest_digest`,
`checker_distribution_digest`). It binds nothing until an admitted binding
consumes it. A control is only a control if something consumes it, so the
consumer shipped in this change is the runner's identity assertion, and the
claim is scoped to it.

### D4 — Isolation is layered, and the layers are named
1. Fresh `CODEX_HOME` for the checker.
2. Credential scrubbing of the child environment.
3. Read-only Codex sandbox mode in the spawned command.
4. A pre/post snapshot digest comparison as a last-resort DETECTION guard.

Layers 1–3 are the isolation attempt; layer 4 only *detects* breach and is
explicitly not a substitute for operating-system level read-only mounts. The
residual bypasses (`direct binary invocation`, any write path that does not go
through the launcher) are named in the capability description.

### D5 — The watchdog is observational and the pause is cooperative
Failure signatures are grouped by normalized class after the last verified
progress. Five occurrences of one signature pause; four do not. Pause requests
are emitted as files that the owning runner polls and honours by terminating the
child; canonical state stays with the lifecycle owner. No automatic resume.

### D6 — Bridge qualification is fail-closed and reported
`scripts/qualify_bridge.py` style preflight is positive-only and cannot promote.
If the Responses↔Chat-Completions bridge cannot be qualified in the current
pinned environment, the disposition is `BLOCKED_HITL` / `NO_CUTOVER`, recorded
as such, and the adapter is still delivered as a candidate with its verification
predicates intact.

## Risks / Trade-offs

- **Detection is not prevention.** A post-run digest diff cannot stop a write;
  it only reports one. Mitigation: state the ceiling and name the bypasses.
- **Bridge availability is environmental.** The checker model route may be
  unqualifiable here. Mitigation: fail closed, report the exact blocker, and do
  not let the unqualified path read as enabled.
- **Windows sandbox helper availability.** The Codex Windows sandbox helper is
  absent on this host, so `workspace-write` can degrade. Mitigation: the checker
  path is `read-only`; the degradation and any deliberate bypass must be
  disclosed in the run receipt, never silent.

## Migration Plan

Additive only. Rollback = remove `src/hg_kseos/checker_bridge/`,
`tests/checker_bridge/` and `config/checker/`; the sealed EXECUTE lane, the
canonical database schema and the existing checker path are untouched.

## Open Questions

- Which consumer will own the checker's *promotion* decision (owner gate,
  COV-11-06) — unresolved by design; shadow/cutover remains `BLOCKED_HITL`.
