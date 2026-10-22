# Design — Hermes incident repair (round FAR-HERMES-INCIDENT-2026-10-05-RCA-001)

## Context

- Sole governance control plane: HG-KSEOS (typed Shared Spine API; `REQ → TS → WO`, canonical events on an
  append-only stream). Governed runtime: the canonical Hermes desktop runtime, home resolved to the MSIX
  `LocalCache\Local\hermes` path; a second home exists at `%LOCALAPPDATA%\hermes`.
- Evidence for this design: `HG-KSEOS/var/far-hermes-incident-rca-001/evidence/store_probes.json` (measured store
  probes), `lanes/lane_a_drift.json` (file-level drift), `lanes/lane_b_timeline.json` (log-reconstructed timeline),
  `lanes/lane_c_mechanism.json` (source-level mechanism), the incident record
  `var/incident-2026-10-05-state-db-wal/INCIDENT_RECORD_2026-10-05_state-db-wal.md`, and the FAR synthesis.
- Model segregation (user-mandated SoD): PLAN and VERIFY/SECURITY on `gpt-6.1-sol` (openai-codex); EXECUTE on
  `deepseek-v4.1-flash` (opencode-go); the Codex CLI lane is the tracked writer for code deliverables.

## Goals / Non-Goals

Goals: leave the runtime environment with (a) true, reproducible integrity verdicts, (b) a measured loss bound,
(c) no silently-missing governed capabilities, (d) gate bindings that resolve inside the canonical home, and
(e) declared identity equal to resolved identity.

Non-Goals: no repair of the destroyed WAL bytes (impossible and not needed), no rewrite of a live SQLite file, no
HG-KSEOS source mutation, no production/release/live claim, no deletion of any recovery artifact.

## Decisions

1. **Repair class discipline.** Each defect is classified additive/reversible (executable with backup + readback)
   or canonical/durable (candidate + independent validator + rollback + gate). Nothing canonical is applied by
   this round. Rationale: the acceptance contract forbids maker self-acceptance and forbids direct writes to
   canonical stores.
2. **Never in-place on binary or live files.** Any database work happens on a copy. Rationale: the accident record
   attributes the incident to exactly such an in-place text rewrite of a binary file - a mechanism that source-level
   review could NOT confirm (LANE C M1 = NOT_FOUND). That is itself the reason to forbid the class categorically
   instead of relying on an established cause.
3. **Skill restoration is surgical, not a wholesale overwrite.** Only the HGK-critical subset is proposed for
   restore, each with a content digest taken from the incident snapshot, plus a tombstone record; the shrink guard
   is preventive. Rationale: a bulk re-materialisation of 50 skills would re-introduce skills that a curator may
   have legitimately pruned.
4. **Gate binding stays fail-closed but must fail loudly.** Repoint the hook scripts into the canonical home and add
   a startup self-check. Rationale: `fail_closed: true` on a foreign path is a single point of failure for the
   whole governed tool surface, and a silent denial is indistinguishable from a policy decision.
5. **The second home is evidence first.** Archive-or-adopt is a recorded decision with digests; disposal is a
   separate revertible step. Rationale: it is the only surviving copy of some recovery-era state.
6. **Ordering proof uses the spine's append-only stream, never wall-clock.** Admission precedes mutation by
   construction (the admission script cannot write candidate source; the apply step asserts the permit exists).
   Rationale: the control plane requires an ordinal the writer cannot choose or backdate.

## Risks / Trade-offs

- Restoring skills from a 2026-10-05 snapshot could restore skill text that a later curator intentionally removed
  → mitigated by the tombstone record and by restoring only the HGK-critical subset.
- Repointing hooks changes the gate that governs this very session's tool calls → the change must be applied
  outside a governed round, with a rollback copy, and re-verified by a fresh lane.
- The 400/401 reconciliation depends on the rescue export being the authoritative window → disclosed as a bound,
  not a proof of zero loss outside that window.

## Migration / Rollback

Every candidate carries a pre-state digest and an explicit rollback position (`RB-<artifact>`); config changes go
through the sanctioned CLI with a timestamped backup; deletions are forbidden until an archive receipt exists.

## Open Questions

1. Is the 59-skill tree in the second home a subset of the incident snapshot's 109, or does it carry skill text
   that exists nowhere else? (Drift lane enumerates it; the archive decision depends on the answer.)
2. Is the partial trigram FTS coverage (20,695 of 52,404 live rows; both figures as-of the EXECUTE-lane probe 2026-10-06T17:16:03.955280+00:00, and the live denominator is an unstable metric in the 52,047-52,595 range) a normal rolling window or an indexing defect?
3. Does any other consumer resolve the second home at runtime (gateway service, scheduler) apart from the
   configured hooks?
4. Which curator/update step removed the 50 skill directories, and was that removal recorded anywhere?
