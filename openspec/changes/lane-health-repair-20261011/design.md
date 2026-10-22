# Design: lane-dispatch-honest-declarations

## Context

`scripts/hgk-lane-dispatch.py` spawns a Codex-CLI turn through the relay and writes a receipt that other
surfaces (checker lanes, acceptance records) read as evidence. Three of its outputs were not tied to
anything it actually measured. The design question in each case was the same: what is the **lowest-friction
change that makes the output true**, and which change would be *too much*?

## D1 -- classify at the single code site

**Chosen.** Additive classification at the one assignment site. Two new codes plus the preserved
fallback. Rationale: one site (smallest possible diff), no semantics relaxed (`ok` stays false, exit stays
non-zero), and the diagnosis becomes machine-readable instead of requiring a human to diff smoke runs.

**Rejected:** relaxing the nonce requirement so an answered turn counts. That is exactly the vacuous-pass
class the same round's own rules forbid -- a run would report success for a check that never happened.
**Rejected:** emitting a distinct code from the caller instead of the harness; the caller is not the
surface that other rounds read.

## D2 -- give the declaration a consumer

**Chosen.** Both halves: (a) complete the declaration with the measured state, (b) skip declared-not-
dispatchable arms before spawn and record the skip in `skipped_arms`, with `--force-rank` overriding.
Rationale: a control is only a control if something consumes it; the measured cost of the missing
consumer is a full timeout on every fallback path.

**Rejected:** deleting the nvidia arm. It removes a declared capability without a measurement and leaves
the declaration mechanism still consumer-less -- the same defect would reappear on the next stale arm.
**Rejected:** silently reordering the pool. It hides the measurement instead of recording it.

## D3 -- fold the home into the identity verdict

**Chosen.** The identity gate's key-auth "no human-attended identity" claim is only sound when the
resolved home is the lane's own isolated home. So: refuse pre-spawn (`ERR_LANE_HOME_NOT_ISOLATED`) when
the home is non-isolated and holds `auth.json`, unless `--allow-human-home-transport` acknowledges it, and
record `codex_home_is_declared_lane_home` in every receipt.

**Rejected:** silently allowing the human home. That is the measured false green.
**Rejected:** removing `--codex-home`. The pool *declares* `REACHABLE_VIA_HUMAN_HOME_TRANSPORT` for the
EXECUTE lane's rank 3, so the capability is real; the defect is that it was unacknowledged and unrecorded,
not that it existed.
**Left OPEN (`OQ2`):** should the resolver carry a per-arm home/transport so a declared transport can be
honoured for the one arm that declares it, instead of the whole run sharing one home? That is a design
decision for the owner; this change only refuses the unsound combination.

## D4 -- supersession, never a rewrite

**Chosen.** A supersession record: superseded manifest id + digest, retired path digests, successor
freeze, and the rule that a freeze binds the bytes at its own time.

**Rejected:** editing the previous manifest or re-freezing the previous round. Both are self-referential
and rewrite history whose digest is already cited inside published documents.

## Test strategy

Deterministic only: the existing stub-child harness and a temp isolated home. No test may depend on the
network, a real model, the relay, or the developer's real Codex home. Positive, negative and boundary
cases for each of D1/D2/D3, plus the pre-existing suite staying green.

## Rollback

Every file under edit has a pre-change `.bak` and a pre-change sha256 in
`var/far-lane-health-repair-20261011/rollback/`. Reverting is a byte copy; nothing here writes the
canonical store, so rollback needs no spine action.
