## Why

HG-KSEOS delegates semantic repository analysis to LLM checkers today, but the
repository has no bounded, isolated *process-level* checker execution path: the
`hgk_checker_upgrade` P0 admission candidate (2026-10-09) provides the design and
runnable examples for an independent Codex-CLI checker driven by GLM-5.3-Flash
through OpenCode Go. Reviewing and repairing that candidate outside HG-KSEOS
governance would leave the capability unadmitted, unbound against the Shared
Spine, and unverifiable by an independent lane.

## What Changes

- Introduce a bounded **independent checker execution** capability: a
  read-only-snapshot checker runner whose verdict is advisory
  (`CANDIDATE_PASS` / `CANDIDATE_FAIL` / `CANDIDATE_INCOMPLETE`) and can never
  be an HGK `OracleReceipt` PASS.
- Add a **checker role binding** that is mapped through the existing
  `RP002-EXECUTION-BINDING/2` schema — no new normative schema, no second state
  machine, no new task DB, no new reducer.
- Add an **observational watchdog** with a 10-minute tick, a
  "strictly more than 4 repeats after the last verified progress" pause trigger,
  and a **pause request that only the owning runner may honour**. The watchdog
  never mutates canonical truth.
- Add **offline negative/security fixtures** proving the runner fails closed on
  candidate mutation, symlink in the snapshot, intake digest mismatch,
  out-of-enum verdict, poisoned repository instruction and permission escalation.
- Non-goals (unchanged, carried in every artifact): no deployment, no cutover,
  no canary activation, no promotion, no production claim, no Stage-3/SQP1.

## Capabilities

### New Capabilities
- `independent-checker-execution`: bounded, isolated, read-only checker execution
  over a frozen candidate snapshot with advisory-only verdicts, a typed checker
  role binding, a candidate-source-mutation guard, and an observational
  pause-request watchdog.

### Modified Capabilities
<!-- none: no existing capability's requirements change -->

## Impact

- New package `src/hg_kseos/checker_bridge/` under the admitted candidate
  write-set; new tests under `tests/checker_bridge/`; new candidate config under
  `config/checker/`.
- Consumes, unchanged: Shared Spine typed API, `Fabric/control/SOD_POLICY.yaml`,
  `Fabric/control/ACCEPTANCE_POLICY.yaml`, `Fabric/control/AUTHORITY_MATRIX.yaml`.
- Runtime: a fresh isolated `CODEX_HOME` and a loopback-only bridge; the sealed
  EXECUTE lane (Codex CLI → opencode-go/deepseek-v4.1-flash) is not modified.
- No change to the canonical database schema, no release path change.
