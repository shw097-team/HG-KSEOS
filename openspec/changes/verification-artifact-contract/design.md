## Context

The round's verification plane produced five lanes and zero acceptable verdicts. The measurements that
constrain any design are:

- the relay's per-request ledger (`opencodex-hermes/usage.jsonl`) records `provider`, `model`,
  `resolvedModel`, `status`, `durationMs` and `usage.inputTokens` per request. It shows the mandated
  checker model served **HTTP 200 on every request** of both decisive lanes (172 and 48 requests) — so
  the failure is not a model or provider failure;
- the two heavy lanes peaked at **114816** and **105974** input tokens on a single request, against the
  checker model's own declared `auto_compact_token_limit` of 115200 (`context_window` 128000). The
  catalogue holds 89 model entries, each with its own limits: reading the first
  `auto_compact_token_limit` in the file yields 334800, a different model's value;
- this Codex build exposes no `--max-turns`/output-budget knob, and the runner's own 2400 s timeout was
  never reached (the lanes ended at ~32 min and ~10.4 min of their own accord);
- the verdict was required as a *terminal* output, so both lanes' endings were destructive: one wrote a
  false PASS whose own comparator printed the frozen files as "extras", the other wrote nothing at all.

## Decisions

1. **Order the artifact, do not enlarge the budget.** A larger context is not available to us; the
   ordering is. Pre-creating the artifact converts every exhaustion from "the check vanished" into "the
   check is honestly partial". The skeleton carries `updated_by_checker: false` precisely so the
   pre-creation cannot become a new false green — the post-condition refuses it.
2. **Shard the audit rather than deepen one lane.** A lane that runs 172 requests to 99.7 % of the
   declared ceiling has no headroom left for judgement. Each shard is budgeted against the checker
   model's own catalogue entry, selected by slug — never by first match in the file.
3. **Pre-bake the discriminators.** Context spent constructing a fixture is context unavailable for
   deciding. The pack is content-addressed and rebuilt reproducibly so "the fixtures are the same ones
   the verdict refers to" is checkable.
4. **Isolate concurrent lanes.** The earlier global mutex was not protecting the provider: it guarded
   against a defect of ours — a pattern-scoped orphan sweep (`*exec --cd*`) that killed a concurrent
   sibling lane. That sweep is gone; cleanup is pid-scoped. With that fixed, concurrency is safe
   *provided* lanes do not share a mutable runtime home, so each lane materialises its own home.
5. **Keep the existing failure taxonomy.** `ERR_VERIFY_NO_VERDICT`, `SUBJECT_CHANGED`,
   `ERR_LANE_SHELL_BLOCKED` and the subject-boundary rules already caught real defects (a false PASS, an
   ineffective sandbox flag, a comparator that mis-attributed files). They are retained, not replaced.

## Rejected alternatives

- **Raise the timeout / add a bigger budget** — the lanes were not time-limited and the ceiling is the
  provider's, not ours.
- **Switch the checker model** — falsified by the provider's own ledger: every request was served 200 on
  the mandated model. Changing the model would have hidden the contract defect.
- **Tell the checker to "be concise"** — an instruction with no observable mechanism cannot be verified;
  an ordering contract can.
- **Remove the no-verdict post-condition to obtain a "verdict"** — that manufactures exactly the false
  green the round exists to eliminate.
- **Accept the void PASS from the fourth lane** — forbidden by the round's rules: promotion is not
  acceptance, and a verdict its own evidence contradicts is not a verdict.
