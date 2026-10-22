## Context

HG-KSEOS is the sole control plane; Hermes is its governed runtime. Every routing fact must be
established from authoritative records and must survive restart, concurrency and provider
failover. Round FAR-LANE-SOD-003 measured that a global delegation pin is shared with other
workstreams (boards fda-repair-20261007, gstack-repair-20261007, skillcap-20261007) and was
empty at start, so it is not a durable mechanism; and that a direct completion HTTP 200 can
coexist with a lane that never completes a Hermes child turn. Both facts drive the decisions
below.

## Decisions

1. **One registry, one projection.** Routes live only in `config/lane-routing-registry.yaml`.
   Every other file is a projection checked by exact JSON pointer. This closes the duplication
   family (D1, D9, D13, D14) because a partial edit now fails the gate instead of remaining
   silently valid.
2. **Model axis, not provider axis.** SoD is enforced on the normalized model identity. EXECUTE
   and VERIFY share the opencode-go provider, so provider separation is explicitly NOT required
   and never claimed (D9, D13). Failover that swaps provider while keeping the model preserves
   the separation.
3. **No per-lane runtime surface is assumed.** The registry declares zero fallback arms
   (D3, D4, D5, D8); adding fallbacks can only weaken separation. Historical fallback arms remain
   in the immutable revision-8 snapshot, never dispatchable.
4. **Admission is lane-shaped.** A bare direct completion is recorded separately and never
   yields ADMITTED (D7, D11, D12). ADMITTED requires >=1 completed model call AND >=1 completed
   tool AND a served identity that matches the requested arm, read from the runtime log line.
5. **Fail closed on staleness.** The guard refuses on a stale epoch or a source-digest mismatch
   (D14, D19). The canonical-policy revision is the epoch source; the registry digest binds the
   exact bytes.
6. **The gate excludes itself.** The artifact gate freezes its input set before reading and
   excludes its own output and registered producer outputs by resolved, case-insensitive
   identity; findings are semantic-stable regardless of a prior output file (D23, D24).
7. **Candidate ceiling.** Everything in this change is CANDIDATE. Activation is a separate
   HGK-authorized generation binding; the registry cannot confer authority on itself (D15,
   D16, D18, D21).

## Risks

- A live (non-dry) lane-shaped probe dispatches through the sealed lane; it is therefore staged,
  not run by this kit. Running it is an admitted execution WorkOrder step.
- The `config/hermes.json` binding still names the pre-MSIX AppData install and an older model
  slug; this is recorded as `PROJECTION_DEBT` (warn), never a PASS, until an authorized
  generation migrates it (D19).
- Deep process-tree write-denial for a checker is a Windows primitive that has not been
  qualified here (U2); containment claims stay BLOCKED until measured.
- Provider-internal weights are not cryptographically attested by a model string (U7); only
  requested/resolved/served runtime labels are claimed.

## Rollback

Delete the new candidate files (`config/lane-routing-registry.yaml`, `src/hg_kseos/lane_policy.py`,
`src/hg_kseos/lane_admission.py`, the five scripts, the test, and the OpenSpec change). None of
them is imported by the live runtime; removing them restores the pre-change tree. No live file,
canonical policy byte, or spine row was modified, so no compensating write is required. If any
candidate is later staged into a live integration point, revert by restoring the recorded
preimage of that single file.
