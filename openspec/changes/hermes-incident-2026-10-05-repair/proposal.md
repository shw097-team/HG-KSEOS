## Why

On 2026-10-05 the Hermes runtime (bound to HG-KSEOS as its governed Runtime/Orchestration Plane) suffered an
integrity incident whose **MECHANISM IS UNCONFIRMED**: the accident record attributes it to an agent-triggered
credential-leak scan that rewrote `state.db-wal` as text-mode content, but source-level review did not locate such a
same-path lossy sanitizer (LANE C: M1 = NOT_FOUND; M2/M3/M8 = PARTIAL), so the cause is carried here as a
**hypothesis consistent with the physical evidence**, not as an established root cause. A FAR research round over the 20:49 incident snapshot (round
`FAR-HERMES-INCIDENT-2026-10-05-RCA-001`, admission `REQ-HERMES-INC-20261005-RCA-001`) then measured that the
incident record's own integrity claim does not reproduce, that the loss must be stated in **three tiers, never as a
single total** (proven 1 row, id 51395; candidate 3 id-sequence gaps, 51396-51398, which do not prove those rows ever
existed; the earlier roughly-22-rows estimate left unverified), that the verification
store and 50 skill directories are absent from the live home, that a second dataless Hermes home exists, and that
the canonical runtime's tool gate is bound to that second home. The environment therefore carries **unrepaired,
measurable integrity and binding defects** that will recur on the next update, curation pass, or leak scan.

## What Changes

- Publish a **corrected incident record (v2)** for `INC-2026-10-05-HERMES-STATE-WAL` whose integrity verdicts are
  re-derived from the artifacts (sha256 + raw `PRAGMA quick_check`) instead of repeated, and which discloses that
  the record's previous `state.db INTACT / quick_check ok` claim is falsified by the artifact it binds.
- Restate the **data-loss bound** as measured: exactly 1 of the 401 rescued message rows (id 51395) is absent from
  the live store; the loss is stated in three tiers and never as a single total: PROVEN 1 row (id 51395, present in the rescue export and absent now), CANDIDATE 3 id-sequence gaps (51396-51398, which do not prove those rows ever existed) and the earlier roughly-22-rows estimate left UNVERIFIED (neither confirmed nor refuted, because the rescue export ends at id 51395).
- Restore the missing **verification evidence store** (`verification_evidence.db`) from the incident snapshot as a
  candidate, with a readback and rollback path.
- Restore the **HGK-critical subset of the 50 missing skills** from the incident snapshot as candidates with a
  curation tombstone record, and add a shrink guard so a silent bulk removal cannot happen again.
- **Repoint the runtime's pre-LLM/pre-tool-call gate hooks** to scripts inside the canonical home, and add a
  startup self-check so a missing gate script fails loudly instead of silently disabling (or, worse, blocking) the
  governed tool surface.
- **Resolve the second home**: either archive it with a receipt (recovery residue) or adopt it canonically and
  update the HGK binding in the same change. No deletion before the archive receipt exists.
- Reconcile **declared-vs-resolved identity**: HGK `config/hermes.json` (0.20.0 / declared home under
  `%LOCALAPPDATA%\hermes`) against the live 0.21.5 / MSIX-resolved runtime; and resolve the 2026-10-06 failed
  update whose stash-restore was parked.

## Capabilities

### New Capabilities
- `hermes-runtime-incident-integrity`: the governed runtime must carry a re-derivable integrity verdict for every
  forensic artifact it names, must never rewrite a binary/SQLite file in place, and must expose a skill/skill-store
  inventory whose shrink is detectable.
- `hermes-runtime-binding-integrity`: the runtime's declared home, gate-hook bindings, and tool-gate closure must
  resolve to the live runtime root; a missing or foreign gate binding must fail closed AND loudly.

### Modified Capabilities
<!-- none: openspec/specs/ is empty in this repository; no existing capability requirements change -->

## Impact

- Runtime home `%LOCALAPPDATA%\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes` (`config.yaml` hooks,
  `skills/`, `verification_evidence.db`, stale lock files) and the second home `%LOCALAPPDATA%\hermes`.
- HGK control-plane binding files: `HG-KSEOS/config/hermes.json`, `HG-KSEOS/config/hermes-codex-lane.json`.
- Evidence surfaces: `var/incident-2026-10-05-state-db-wal/`, `HG-KSEOS/var/far-hermes-incident-rca-001/`,
  `Fabric|HGK|SQS evidence/review/`.
- No production, release, live-trading or remote-deployment effect. No HG-KSEOS source mutation in this change.
