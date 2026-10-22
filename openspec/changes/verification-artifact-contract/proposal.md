# verification-artifact-contract

## Why

Round `HGK-SOLUTION-APPLY-20261012` opened five independent checker lanes against the W5/W3 artefacts and
obtained **zero acceptable verdicts**. FAR run `FAR-RUN-VERIFY-LANE-NOVERDICT-017` (round
`FAR-VERIFY-LANE-NOVERDICT-20261012`) established, from the provider's own per-request accounting, that
the checker model was never the problem: the relay ledger records the mandated
`opencode-go/glm-5.3-flash` resolved and served **HTTP 200 on every request of both decisive lanes** —
172 requests in the lane that produced a false PASS and 48 in the lane that produced nothing.

The two load-bearing defects are contract defects, not model defects:

- the verdict was a **terminal** artifact of an **unbounded** audit, so budget exhaustion deleted it;
- the audit ran against a **fixed** ceiling the harness neither measured nor budgeted — the checker
  model's own catalogue entry declares `context_window 128000` / `auto_compact_token_limit 115200`,
  and the two heavy lanes peaked at **114816** and **105974** input tokens.

A harness that can silently lose its own verdict is not a verification harness: it is a harness whose
failure mode is indistinguishable from "nothing was checked".

## What Changes

Five checkable pieces. All are candidate declarations; none of them is applied to a governed store by
this change.

- **C1 — Verdict artifact is pre-created and incrementally updated.** Before dispatch the runner
  pre-creates `<workdir>/VERDICT.json` as a skeleton with every item `INCONCLUSIVE` and
  `updated_by_checker: false`. The post-condition **refuses the skeleton**: a lane that exits 0 without
  the checker taking the file over fails with `ERR_VERIFY_NO_VERDICT`. Exhaustion may **downgrade**
  items to `INCONCLUSIVE`; it may never remove the artifact — and the skeleton may never be mistaken
  for a verdict.
- **C2 — Bounded shard budget.** The audit item list is partitioned into shards small enough that each
  lane's measured peak `usage.inputTokens` stays under the checker model's declared
  `auto_compact_token_limit`, read from **that model's own catalogue entry**. A lane that exceeds its
  budget fails closed with `ERR_LANE_CONTEXT_BUDGET_EXCEEDED`.
- **C3 — Pre-baked, content-addressed fixture pack.** Discriminating fixtures are built once, ahead of
  time, presented read-only with their expected outputs, so a lane's context is spent judging rather
  than constructing.
- **C4 — Parallel lane isolation.** Lanes that run concurrently must not share a mutable `CODEX_HOME`,
  and orphan handling must be scoped to a lane's own process ids rather than to a command pattern —
  the pattern-scoped sweep used earlier killed a concurrent sibling lane.
- **C5 — No self-report as verification.** A writer's own claim about its artefact stays
  non-authoritative until an independent lane reproduces the observation.

## Non-goals

- This change does not run any lane, does not apply, promote or archive anything, and makes no
  acceptance claim. It writes only planning artifacts under
  `openspec/changes/verification-artifact-contract/`.
- No edit to `config/`, `src/**`, `PIPD/**`, `verify/subject-copy/**`, or any frozen evidence byte.
- No claim about model quality, provider liveness, or the correctness of any audited artefact. A
  verdict produced under this contract remains an **advisory independent check**, not acceptance.

## Impact

Affected (once applied, outside this change): the round's verification harness
(`verify/run_verify_lane_v2.sh` and its shard successor), the runner's post-condition, the shard
schedule, the fixture pack, and the parallel-lane runner's lane-home materialisation.

Not affected: the freeze manifest and the subject bytes, the sealed front door's sanctioned pair, the
D-01 deviation record, and every existing lane's raw log.
