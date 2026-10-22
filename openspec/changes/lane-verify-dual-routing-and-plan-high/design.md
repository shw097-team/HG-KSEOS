## Context

Round FAR-LANE-SOD-006 runs under the standing contract in `AGENTS.md`: HG-KSEOS is the sole control
plane, the canonical Hermes is its governed runtime, and completion requires implementation,
deterministic tests, evidence, rollback and an independent checker. The routing facts live in
`config/lane-routing-registry.yaml` with `config/model-lane-assignment.json` as a projected site, and
`src/hg_kseos/lane_policy.py::check_drift` compares each declared pointer read-only.

Two measured facts drive the decisions:

- **Effort is per model, not per lane.** `resolve_reasoning_config(cfg, model)` consults
  `agent.reasoning_overrides[<model>]` first and the global `agent.reasoning_effort` second. There is
  no per-lane effort key in `delegation`. Therefore a single model serving two lanes at two different
  efforts cannot be expressed by config alone.
- **The only per-dispatch effort surface is the kanban task row.**
  `hermes_cli/kanban_db.py` stores `reasoning_effort` per task and
  `hermes_cli/kanban_db_dispatch.py` passes `--reasoning <level>` to the spawned worker, so a pin
  there overrides the model-level default for that card.

## Decisions

1. **PLAN HIGH is a model-level default.** `agent.reasoning_overrides = {"gpt-6.1-sol": "high"}` is the
   one Hermes surface that reaches every PLAN consumer (delegation children,
   `auxiliary.kanban_decomposer`, `auxiliary.triage_specifier`, MoA reference models). The global
   `agent.reasoning_effort` stays `medium` so no other model is silently raised.
2. **`-HIGH` is an effort level, not a slug.** Measured: a model id `gpt-6.1-sol-high` resolves to
   `medium`, so introducing such a slug would silently deliver the wrong effort. The declaration
   therefore carries `reasoning_effort`, never a suffixed model name.
3. **The two VERIFY arms are co-equal.** Neither appears in `fallbacks`. The registry records both
   arms with `co_equal: true`, a `selection_authority`, and the OpenAI OAuth arm as the default. The
   machine-enforced surfaces are `delegation.provider/model` (the default arm) and the per-card
   `model_override`/`provider_override` (a specific selection); the co-equality itself is a
   declaration, and this change says so rather than implying enforcement.
4. **The collision is declared, not resolved.** `SOD006-C1` records that a PLAN maker checked by the
   default arm shares the model token. The coherent clause (EXECUTE vs both arms; PLAN vs arm A) runs;
   the conflicting pair is refused pre-dispatch and frozen for operator/HGK adjudication.
5. **One compensating control is mandatory.** Every VERIFY/ACCEPTANCE card carries an explicit
   `reasoning_effort` pin, because the model-level HIGH default would otherwise raise the medium
   requirement of the verification lanes on the shared model.
6. **Findings that are not in scope stay findings.** The `gpt-6.1-sol` tier-prefix mis-classification
   (the route resolves to the LEGACY effort set, so `max` is unreachable) and the legacy
   `codex_route` prose are reported with their evidence and are not repaired by this change.

## Risks

- Raising the PLAN default raises PLAN-lane latency and cost. Not measured here; the round records the
  per-card compensation rather than a latency claim.
- The co-equality of the two VERIFY arms is declared-only. A future dispatch that forgets the card
  override will silently use the default arm - recorded, with the card pin named as the control.
- The default arm shares a model with PLAN. Until `SOD006-C1` is adjudicated, any verification of a
  PLAN-made artifact MUST run on arm A (or an EXECUTE-independent lane), and the gate must refuse the
  colliding pair.
- `far-lane-sod-006` card overrides are coordination state on one board; a different board's card
  carries none of them.

## Rollback

- `config/model-lane-assignment.json` / `config/lane-routing-registry.yaml`: restore the byte preimages
  recorded beside the round (`var/far-lane-sod-006/backup/`).
- Live Hermes `config.yaml`: restore the pre-image
  (sha256 `c6e741e1aa8281c1c5504b259b55faf691b3b0a92b67c22a2c2b8528a2c135e4`), i.e. clear
  `agent.reasoning_overrides` and set `delegation.provider/model` back to `opencode-go/glm-5.3-flash`.
- Board: delete the `far-lane-sod-006` board.
- Nothing in `src/hg_kseos/**`, the Shared Spine or any acceptance receipt is mutated, so no
  compensating write is required.
