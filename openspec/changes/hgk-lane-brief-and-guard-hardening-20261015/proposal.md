# Proposal: lane brief and guard hardening — remediating the nine R7 tooling findings (TF-01..TF-09)

## Why

Round R7-0 (mission `CNV-PIPD-LS-SP-20261015`, changeSet `R7-0-VALIDATOR-AND-CHECKER-ISOLATION`)
recorded nine defects in the governed tooling itself, each with raw evidence, impact, owner and a
low-friction fix (`_handover/CNV-PIPD-LS-SP-20261015-R7/R7_TOOLING_FINDINGS.json`,
claim ceiling: LOCAL observation, not a product defect verdict). Three properties recur across them:

1. **The dispatch guard false-positives on prohibition prose and false-greens on end-state
   comparison.** `scripts/hgk-lane-dispatch.py` refused two legitimate EXECUTE dispatches because the
   brief contained the words `git push` / `publish` inside `do not …` sentences (TF-01), while the
   same guard reported `CLEAN (added=0 removed=0 changed=0)` during a turn in which the mutation
   driver wrote 13 RAW receipts in place into the frozen subject and the checker had to restore them
   (TF-09) — the guard compares only the subject digest before vs after the turn. Separately, the
   guard voided a checker verdict because the orchestrator deleted a gitignored `__pycache__/*.pyc`
   byproduct out-of-band (TF-08). Of three checker attempts in the round, two were spent voided —
   50+ minutes of lane budget on receipt plumbing instead of verification.
2. **The dispatch surface does not isolate the checker's writes.** The mutation driver kept defaulting
   its output into the frozen tree (TF-07, TF-09), and the recurring
   `ERR_NO_ARM_EMITTED_NONCE` verdict defect on Codex-CLI lanes leaves model attribution resting on
   recorded usage rows instead of a nonce (TF-06, third occurrence this round).
3. **The governance admission path fails for reasons unrelated to authority, and the product tree
   cannot answer provenance questions.** `taskspec_id` collides on the spine for two projects of the
   same mission, and `create_workorder` resolves git HEAD from the ambient process cwd instead of the
   project's target_root, stranding three admission attempts at `PLAN_READY` (TF-02). The PIPD
   product tree is not a git repository, so the WriteSet + unified diff pair is the only
   reproducibility handle (TF-03); the product test suite depends on a git ref the tree does not have
   and cannot tell pre-existing from change-induced failures (TF-05).

TF-04 is an operator-display artefact (Hermes redacts a credential-shaped literal on screen while the
on-disk bytes contain the real placeholder); it needs operating guidance, not a product change.

## What Changes

This is a tooling-and-convention change only. It touches lane tooling under `HG-KSEOS/scripts/`,
the PIPD mutation driver, and the standing brief template. It does **not** change lane routing,
model chains, or any authority surface.

### Surface A — HG-KSEOS lane dispatch and guard (`scripts/hgk-lane-dispatch.py`)

- **TF-01 — match command context, not bare words.** The remote-write marker check requires a
  shell-looking occurrence (a line beginning with `git`/`gh`/`curl`/`ssh`/`winget`, or an argv-shaped
  form) and ignores matches inside negative/prohibition sentences (`do not`, `never`, `must not`,
  `SHALL NOT`, …). `detection_only` semantics are kept; the dispatcher stops refusing a dispatch on
  prose. Acceptance evidence: a deterministic table-driven test on recorded raw briefs — the two
  refusal briefs from the round classify as prose (dispatch proceeds), and an actual
  `git push <url>` line classifies as a marker (dispatch refused unchanged).
- **TF-08 — guard subject = the tracked file set, or ignoring VCS-ignored byproducts.** Where the
  subject sits in a VCS tree the guarded subject is normalised to the tracked (packet) file set before
  the turn opens; ignored byproducts (`__pycache__/`, `*.pyc`, …) are treated as
  `added/removed — recorded, not fatal` instead of voiding the verdict. Where no VCS is available the
  brief declares the ignored-pattern set explicitly. Every change of an ignored path is still
  recorded, so out-of-band hygiene leaves a trace.
- **TF-07 — intra-turn subject sampling.** The guard samples the subject digest during the turn (a
  bounded-background sampler iterations capped, one digest sweep per sample), not only before vs
  after; a mid-turn write that is later restored is recorded as an intra-turn boundary violation and
  the verdict is marked `CLEAN_WITH_INTRATURN_WRITES` (still fail-closed, never silently green).
- **TF-06 — nonce-carrier attribution honesty.** The lane tooling keeps the receipt contract already
  declared in `lane-dispatch-honest-declarations` (`ERR_NO_ARM_EMITTED_NONCE` +
  `nonce_absent_arms`), and additionally records per-attempt the nonce carrier surface it probed, so
  an owner can distinguish "the wrapper never echoes the nonce" from "the relay dropped it" without
  re-running a lane. Genuine fix of the wrapper/relay echo path remains **owner-gated** (relay is a
  control-plane surface; see Blocked items).
- Intra-turn subject sampling and subject-path **declaration**: the dispatch brief lists every
  guarded subject path explicitly, so a checker lane can see what it must not write into (the TF-07
  brief fix, already applied ad hoc in round R7; here it becomes standing template text).

### Surface B — Lane lifecycle admission (`hg_kseos.lifecycle`, spine)

- **TF-02 — taskspec ids and head resolution.** Replace the last-dash-segment derivation with a full
  project-id digest (or a spine-wide counter) so two projects for the same mission cannot collide on
  the spine's UNIQUE constraint, and resolve the WorkOrder's `base_head` from the project's
  declared `target_root` instead of the ambient process cwd. On workorder-field failure, return a
  typed error instead of persisting a taskspec, so failed admission leaves no partial spine residue.
  This is a **control-plane change** — applicative only after owner authorisation (see Blocked).

### Surface C — PIPD product tooling

- **TF-03 — WriteSet + diff as the standing provenance convention.** Adopt the R7-0 writer-receipt
  practice as the standing convention for this non-VCS tree: every bounded write to the product ships
  a `WriteSet` (path / bytes / sha256 + pre-hash) plus a unified diff produced with
  `diff -u` / `git diff --no-index`. Placing the tree under version control is an alternative, but
  requires the PIPD Product Owner / Fabric Repo Maintainer and is not assumed here.
- **TF-07/TF-09 (PIPD half) — the mutation driver writes where it is told.** Add
  `--out-dir`/`DEST` to `probe_mutations.py` so a re-run never defaults its RAW output into a frozen
  tree; the R7-0 ad-hoc isolation call becomes a declared flag.
- **TF-05 — the suite skips, not fails, when its fixture ref is absent.**
  `tests/test_publication_projection.py` and `tests/test_tooling_executes.py` require
  `r5-s4-candidate`; make the required-ref skip (`pytest.skip` with the missing-ref reason, recorded
  as such) so missing-fixture failures separate from change-induced ones. The R7 round's classification
  of its 7 pre-existing failures is recorded separately and is a checker task, not this change's.

### Surface D — Operating guidance only

- **TF-04 — verify bytes before editing secret-adjacent lines.** Record in the round's operating
  guidance: a credential-shaped literal rendered as `Bearer ***` on screen may be a display
  redaction; read the on-disk bytes before editing. No product change; no Hermes runtime change
  proposed here (that surface's owner is the Hermes operator, not this repo).

## Capabilities

### New Capabilities

- `lane-brief-and-guard-hardening`: the guard-subject definition, the marker classification,
  intra-turn sampling, and the driver output isolation contract for dispatched lanes.

### Modified Capabilities

- `lane-dispatch-honest-declarations` (existing): the nonce-carrier record `nonce_absent_arms`
  gains a per-attempt carrier-surface probe record (additive).

## Impact

- Files: `HG-KSEOS/scripts/hgk-lane-dispatch.py` (marker match, subject normalisation, intra-turn
  sampler, nonce record); `HG-KSEOS/src/hg_kseos/` lifecycle admission (taskspec id + head resolution,
  owner-gated); `PIPD` mutation driver `probe_mutations.py` (`--out-dir`);
  `PIPD/tests/test_publication_projection.py` + `tests/test_tooling_executes.py` (skip-on-missing-ref);
  standing brief template text.
- Tests: each claim above carries a deterministic positive/negative/boundary test on recorded raw
  inputs; no test depends on network, model, relay, or credentials.
- Runtime: no lane routing, no model chain, no authority rebind; additive fields only.
- Risk: false-negative risk from TF-01's prose-tolerant matching is bounded by requiring a
  shell-shaped occurrence; a boundary test asserts an actual command line still refuses.

## Out of scope / Non-goals

- No change to `config/lane-routing-registry.yaml`, `config/model-lane-assignment.json`, any model
  chain, or any authority surface.
- No product repo (Fabric, PIPD product code) semantic change: PIPD work is tooling (the driver's
  output destination) and test-fixture honesty.
- No claim that TF-06's relay/wrapper echo path is fixed by this proposal; only its attribution
  record is.
- No runtime store, spine schema, or promotion change beyond the TF-02 admission correction (which
  is owner-gated).

## NON-CLAIMS — this proposal is not an acceptance

- **An openspec proposal is a proposal, never an acceptance.** Nothing here records an Acceptance
  Officer verdict, a DOC-05 admission, or a canonical acceptance status; each of the nine findings is
  re-derived on its own acceptance lane after the change is applied.
- **Existing, it changes no runtime behaviour.** An adopted-but-unimplemented proposal has no
  effect on any dispatch, guard, lane, product, or store; its tasks are unexecuted placeholders
  until implemented and independently checked.
- No promotion, no archive, no main-spec write, no `config/` or route edit, no product repo change,
  no git write command, no host outside this workspace is touched.
- Maker self-checks inside any future implementation are, per AGENTS.md, maker artifacts — not
  verdicts; each surface gets an independent checker lane.
- Claim ceiling of the nine findings themselves: `LOCAL observation`, not a product defect verdict;
  this proposal inherits that ceiling and adds nothing stronger.
- Task status at proposal time: **0/13 tasks done, applicability declared per finding** (see
  tasks.md); "applicative now" means this change authorises the edit on this lane's authority, not
  that the finding is fixed.

## Blocked items:

- **TF-06 root-cause fix (relay/wrapper nonce echo)** — blocked on owner authorisation for a
  control-plane change; this change authorises only the attribution-record side.
- **TF-02 lifecycle admission correction** — a control-plane change; applicative only with owner
  approval recorded in the change record, not silently shipped.
- **TF-03 alternative (place the PIPD tree under version control)** — requires PIPD Product Owner /
  Fabric Repo Maintainer authorisation; WriteSet+diff convention is the proposal's default.
- **TF-04 vendor-side display fix (Hermes rendering)** — outside this repo's authority; recorded as
  operating guidance only.
