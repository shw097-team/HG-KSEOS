# MODEL MENU — READING CONTRACT (hard annotations)

> Machine-readable twin: the `reading_contract` block inside `config/lane-route-slots.candidate.json`
> (added at revision 37; epoch unchanged at 41). This file is the human-readable copy of the same rules.
> Aligned with `FHS_PIPD-LS-PKG_W0_r26` §25.7 — *FHS-3L&M: 硬入口契約，不是第四套路由*.

## 1. Which document is which

| Document | What it is | Authority |
|---|---|---|
| `config/lane-routing-registry.yaml` | lane → arm routing. **Only `routes[]` is authoritative.** | **the authority** |
| `config/lane-route-slots.candidate.json` | the **model menu**: what may be selected per lane, by rank (`DEFAULT/首選`, `FALLBACK1..5/備援1..5`) | what may be chosen |
| `config/model-lane-assignment.json` | operator-declared **projection** that the dispatcher reads. Its own note: *"Not an authority source; the runtime wiring named in `effective_wiring` is the machine truth."* | **not an authority** |
| `scripts/lane_policy_reconcile.py` | built projector: registry → menu + assignment `lane_chains` | tool, not policy |
| `scripts/lane_assignment_resync.py` | built projector: registry → assignment only | tool, not policy |

## 2. The six rules

1. **Never read the registry with a line-anchored grep.** The YAML carries historical blocks whose
   `- lane: PLAN` rows are *not* the authority. Read `routes[]` where `lane == <LANE>`.
   *A line-anchored read is exactly what produced the false conclusion "the registry puts PLAN on deepseek".*
2. **Same epoch or it is stale.** Menu and registry must report the same epoch (currently **41**).
   A projection naming an older epoch is stale by definition: `origin/main` is at revision 35 /
   `registry_epoch 34`, so `ERR_ARM_NOT_IN_ASSIGNMENT` measured there is a **stale-base error**, not a defect.
3. **No hand edits.** Never add or remove an arm by hand in the menu or the assignment. Edit the registry,
   then run `lane_policy_reconcile.py` (menu + assignment) or `lane_assignment_resync.py` (assignment).
   A hand-picked fallback set is an operator lane decision and is refused as such.
4. **Two planes.** The menu and the FHS-3L&M binding records are the **lane control plane**. A desktop-app
   session pin is a conversation setting and binds no lane. Only the binding record is read by
   `fhs_3lm.py --assert`.
5. **SoD is not enforced.** PLAN rank 1 and VERIFY_SECURITY rank 1 are both `openai-codex/gpt-6.1-sol`
   by owner order (**SOD006-C4, OPEN_OWNER_ORDERED**). Same-arm lanes are **recorded**
   (`same_arm_lanes`, `identity_overlaps_recorded_not_enforced`) and never refused; a run must not be
   failed for it.
6. **Selection semantics.** No session instruction → rank 1. A session instruction replaces rank 1.
   An entry outside the pool → `ERR_SLOT_NOT_IN_POOL`. A model failure advances in rank order.

## 3. Entry points

```text
tools/fhs_3lm.py --menu                 # renders this menu (reads menu + registry, read-only)
tools/fhs_3lm.py --bind LANE SLOT       # writes the lane-control-plane binding record
tools/fhs_3lm.py --assert <binding.json># fail-closed on epoch / pool / ledger drift
scripts/hgk-lane-dispatch.py            # mechanical routing; reads the assignment projection
```

## 4. Measured state at the time of writing

- `fhs_3lm.py --menu` → `policy_epoch 41 / IN_FORCE`, `slot_count 9`, `admitted_count 9`, `all_admitted true`.
- PLAN ordered pool: `1 gpt-6.1-sol (DEFAULT/首選)`, `2 deepseek-v4.1-flash`, `3 glm-5.3-flash`,
  `4 mimo-v2.6-flash`, `5 nvidia/z-ai/glm-5.3-flash`, `6 nvidia/deepseek-ai/deepseek-v4.1-flash`.
- `lane_assignment_resync.py` on the in-force clone → `changes 0`.
- `--bind`: PLAN → `gpt-6.1-sol` (`same_arm_lanes false`); EXECUTE → `deepseek-v4.1-flash` (`false`);
  VERIFY → `gpt-6.1-sol` (`true`, recorded, `sod_mandated false`).

## 5. Cost of editing this file

`pool_sha256` in every 3L&M binding is `sha256` of **this file's raw bytes**, so any edit here is a
**plane move**: existing bindings will fail `--assert` (exit 7) until they are re-bound. That is by design,
and it is why this annotation ships as a revision bump (`revision 36 → 37`, `supersedes_revision 36`) rather
than a silent comment.

**Line endings count.** `pool_sha256` is byte-based, so a checkout that converts LF→CRLF changes it without
changing a single arm: the same commit measured `d80b35d3…` before a `git stash`/`pop` round-trip and
`2d30cd67…` after it. Treat a digest mismatch as *plane bytes moved* and re-bind; do not conclude the arms changed.
