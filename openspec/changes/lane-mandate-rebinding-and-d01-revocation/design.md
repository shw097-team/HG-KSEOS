## Context

HG-KSEOS is the sole control plane for model-lane routing. `config/lane-routing-registry.yaml`
(`schema: HGK-LANE-ROUTING-REGISTRY/1`, `status: CANDIDATE`, `epoch: 15`, `claim_ceiling: CANDIDATE_ONLY`)
is the single source of truth; `config/model-lane-assignment.json` (`revision: 16`,
`registry_epoch: 14`) is a projected site, and `src/hg_kseos/lane_policy.py::check_drift` compares each
declared pointer read-only. The registry carries the two facts this change acts on:

- `sod.plan_lane: "openai-codex / gpt-6.1-sol"` and `sod.verify_vs_plan_model_separation`, whose own
  text ends `Non-default operator-selectable alternate arm B still collides with PLAN and must be
  refused for PLAN-made artifacts.` A mandated checker on gpt-6.1-sol can therefore be legitimately
  refused against a PLAN-made artifact — the collision the owner's plan removes by rebinding PLAN.
- `wiring_feasibility.projection_drops_dual_arms.state: "DECLARED_GAP_NOT_FIXED"` with evidence
  `route_for_lane selects primary arm A. _compact_route still drops arms[] and selection_authority;
  fallbacks[] is empty under the zero-fallback invariant, so projected dispatch contains only the
  primary route.` The alternate arm is registry-declared but unreachable in a projected dispatch.

The D-01 deviation lives in the PIPD round `S4EXT-R1-20261012-external-challenge-repair` as two
byte-identical files: `verify/MODEL_SUBSTITUTION.txt` and
`evidence/09_CHALLENGE/MODEL_SUBSTITUTION.txt`, each `sha256
f54dec16d48d9432d61d3394b3468cfd2a12ddf5dfecf724a34922c8246e7fc2`. Their content declares
`declared_checker_model=gpt-6.1-sol (unserviceable: HTTP 400 model-not-supported on ChatGPT auth)` /
`actual_checker_model=gpt-5.6-sol` / `codex_cli=codex-cli 0.162.0-alpha.17.2` / `deviation_id=D-01`, and
the round's `evidence/09_CHALLENGE/lane_incidents.json` records D-01 as
`HTTP 400 invalid_request_error: "The 'gpt-6.1-sol' model is not supported when using Codex with a
ChatGPT account."`. The owner's single-variable A/B measurement — same isolated home, auth, model and
prompt — produced that HTTP 400 (exit 1) on Codex CLI build `0.147.0-alpha.6.5` and `OK` (exit 0) on
build `0.162.0-alpha.17.2`, so the blocker was a local toolchain artifact, not a provider refusal.

## Decisions

1. **PLAN rebinds to the owner-mandated identity.** `opencode-go / deepseek-v4.1-flash` is the PLAN
   binding, matching the owner's model plan. This removes the PLAN-vs-checker collision on
   gpt-6.1-sol by construction at the PLAN end, rather than by refusal text.
2. **Every stale PLAN site is enumerated, not hand-edited.** The change names each site (routes[PLAN],
   `lane_chains.PLAN[0]`, `sod.plan_lane`, the `projections[]` PLAN bindings, and the PLAN surfaces in
   `effective_wiring.plan_high`) so the rebinding is checkable by grep + drift gate rather than by
   memory. No site is left declaring gpt-6.1-sol for PLAN after the change applies.
3. **The publication counter advances.** The registry declares its own `epoch` as its publication
   counter and states it "must advance whenever the registry's committed content changes." Because C1
   and C2 change the committed content, the applied change MUST advance `epoch` (and the projected
   `main_agent`/source-of-routes binding it drives). This change records the requirement; it does not
   perform the edit.
4. **Arm reachability is a projection property, not a selection property.** The alternate arm already
   exists in the registry; the defect is that `_compact_route` drops it. C2 therefore requires the
   projection to carry `arms[]` and `selection_authority`, so a compiled dispatch exposes both arms.
   Preserving the arm AND surfacing it are both required — dropping the arm to "fix" the gap is
   rejected.
5. **The round's selected arm is additive.** The owner's mandate for THIS round
   (VERIFY/SECURITY = CODEX CLI, checker model `opencode-go/glm-5.3-flash`) is expressed as a NEW
   selection field (e.g. `selected_arm`) recorded beside the published arm history. The existing
   arm A / arm B records and the historical records are not rewritten; the round selection is a
   forward append, so the same registry can express a different owner mandate in a later round
   without falsifying this one.
6. **Revocation is additive and byte-preserving.** The D-01 revocation is a new companion artifact
   that names the ORIGINAL path plus its `sha256`, so the frozen bytes and any manifest binding them
   remain valid. The revocation records the falsifying evidence and binds the checker lane to the
   currently mandated model. The original artifact is never mutated — a revocation that edited the
   original would invalidate the very digest that proves which bytes were revoked.
7. **Exclusion is an invariant, not a one-off edit.** C4 states the rule that a family excluded by the
   owner for a round cannot be re-entered by a registry default or an inherited child setting. Without
   it, a rebinding default (or a `delegation` inheritance) could silently restore the excluded family,
   which is exactly the failure mode the plan/checker collision and the near-exhausted GPT quota make
   material.

## Risks

- **Projection change touches a shared function.** `_compact_route` is on the dispatch path; carrying
  `arms[]`/`selection_authority` must not change the primary route that existing consumers resolve.
  Mitigation: the change requires the primary field to be byte-identical pre/post and adds the arms
  fields additively; the drift gate plus a projection test pin both.
- **Publication counter coupling.** Advancing `epoch` without synchronizing the `source_of_routes`
  revision/digest binding would make the drift gate flag a stale pointer. Mitigation: C1/T1 treat the
  epoch advance and the projection-binding synchronization as one edit.
- **History rewrite is the tempting shortcut.** Re-editing arm records to "make the round mandate
  true" would falsify prior rounds. Rejected by decision 5; the round selection is additive only.
- **Revocation can be mistaken for a mutation.** A reviewer may expect the original D-01 file to change.
  The change states explicitly that it must NOT; the revocation is a companion keyed by the original
  digest.

## Rollback

Every piece is additive or a named single-site edit, so rollback is a byte restore of the touched
file:

- `config/lane-routing-registry.yaml`: restore the pre-change byte-preimage (backups exist beside the
  registry as `config/lane-routing-registry.yaml.bak-*`); the `epoch` reverts with the bytes.
- `config/model-lane-assignment.json`: restore the revision-16 byte-preimage
  (`sha256 7c1fa5f25d67799f82650621b5194e8ac7a6739a219cf8bc5cf1ded379298d13`) from
  `config/model-lane-assignment.json.bak-final-route-20261008T071211Z`.
- D-01 revocation record: delete the additive companion; the original artifact and its `sha256` are
  untouched by construction.
- The projection function: revert to the pre-change revision; no data is stored in it.
- No credential, route, `src/**` (other than the named projection function) or evidence byte is
  changed by this change's candidate scope, so no compensating write is required.

## Decision 8 — the encoding is reconciled, not the models (C5)

The registry was internally contradictory: `sod_invariants.pairs` declared `{maker: EXECUTE,
checker: PLAN, distinct_required: true}` while the SAME registry's `declared_conflicts` recorded
`SOD-APPLY-01` with `pairs: [[EXECUTE, PLAN]]` and `status: OPEN` — an overlap declared accepted and
enforced as a refusal at the same time. The owner's own slot declaration of 2026-10-10 settles which
side wins: `selection_semantics.sod` reads "NOT enforced at this revision (owner D1). Identity
overlaps are recorded as facts only, not as refusals."

So C5 removes the un-reconciled strict pair, keeps `SOD-APPLY-01` recorded as a fact, and names the
compensating control in the record itself. It does **not** change any model: PLAN remains on the
owner's rank-1 default (`opencode-go/deepseek-v4.1-flash`). Re-pointing PLAN at a third model to
satisfy the encoding would have been rework that overwrote the owner's own rank-1 declaration — it
was considered and rejected.

**Named compensating control.** With the strict pair removed, the maker/executor overlap is held by
(a) structure — PLAN and EXECUTE are both maker/executor routes and never check each other; (b) the
artifact contract — the acceptance verdict comes from the dedicated VERIFY/SECURITY lane under the
C1 verdict-artifact shape (no top-level `verdict` key or a mismatched shape is rejected as overclaim);
(c) the per-card reasoning pin; and (d) for THIS round task-scoped checker, the disclosure that the
checker's independence rests on lane/role/harness separation (separate process, separate CODEX_HOME,
separate brief, separate log) rather than on model distinctness, since the checker model equals the
maker/executor model.

**Known residual (F18).** The projected site still declares
`/wiring_feasibility/projection_drops_dual_arms/state = FIX_READY_IN_CANDIDATE_PROJECTION_NOT_APPLIED_TO_LIVE_SRC`
while the fix IS now applied to live `src/`. The drift gate passes because the registry's expectation
and the site's value agree with each other — the pair is internally consistent and externally stale.
No gate catches declaration-vs-reality drift of this kind; it is recorded rather than silently
corrected, because correcting it means another registry edit and another `epoch` advance.

