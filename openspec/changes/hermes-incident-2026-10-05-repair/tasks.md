## 1. Evidence and verification prerequisites

- [ ] 1.1 Re-run the store probe (`var/far-hermes-incident-rca-001/x_probes.py`) from a fresh context and confirm every digest and quick_check verdict in `evidence/store_probes.json` recomputes
- [ ] 1.2 Confirm the incident record's `state.db.snapshot-1755` hash binds an artifact whose `PRAGMA quick_check` is NOT ok, and record the raw error text as the falsification evidence
- [ ] 1.3 Confirm the rescue-export denominator (401 exported, 400 present, missing id 51395) with a read-only query on the live store
- [ ] 1.4 Enumerate both copies of the incident `state.db` subject with their own sha256 and integrity verdicts

## 2. Corrected incident record (candidate)

- [ ] 2.1 Author `INCIDENT_RECORD_2026-10-05_state-db-wal.v2.md` with per-artifact measured verdicts and an explicit withdrawal of the previous `INTACT / quick_check ok` claim
- [ ] 2.2 Restate the loss in **three tiers, never as a single total**: (i) PROVEN loss = 1 row (id 51395 — present in the rescue export, absent now); (ii) CANDIDATE gaps = 3 (ids 51396–51398 are id-sequence gaps and do **not** prove those rows ever existed); (iii) the earlier `~22 rows` estimate stays UNVERIFIED (neither confirmed nor refuted, because the rescue export ends at id 51395). Acceptance: the document contains no un-tiered total-loss number.
- [ ] 2.3 Keep the forensic WAL and both copies byte-identical; record their digests; refuse any in-place repair. Characterise the WAL by its **frame chain** — header valid (`0x377f0682`, page size 4096, frame size 4120), frames 1–51 verify, the chain breaks at frame 52, and the tail is not frame-aligned — and state that a **salvageable committed prefix exists**; do NOT use a blanket "not a WAL / no replay" claim.
- [ ] 2.4 Obtain an independent VERIFY lane verdict on the corrected record before it replaces the original as the cited artifact

## 3. Store restoration (candidate; CANONICAL class C — staging → gate → backup → readback; never a live-home write in one step)

- [ ] 3.1 Stage first: copy `verification_evidence.db` from the incident snapshot into `var/staging/verification_evidence.db` and read back `quick_check` + row counts (128 verification_state rows / 4 verification_events). No write to the live home.
- [ ] 3.2 Only through the gate: move the staged file into the canonical home with a timestamped backup of the (absent) target and a post-write readback; record rollback pointer `RB-VERIFICATION-EVIDENCE-DB`.
- [ ] 3.3 Acceptance: the live file must NOT exist before the gate approves; the staging digest is recorded in the evidence manifest.

## 4. Skill inventory integrity

- [ ] 4.1 Publish the 50-item removed-skill delta with per-skill sha256 (from `lanes/lane_a_drift.json`) as a candidate artifact
- [ ] 4.2 Stage the HGK-critical subset into `var/staging/skills/` with a curation tombstone naming the source digest for each skill. Adopting that staged tree into `$HERMES_HOME/skills` is a canonical class C action and happens only through the gate.
- [ ] 4.3 Add a skills shrink guard that refuses (fails closed with a finding) a bulk removal above a declared threshold instead of adopting the smaller tree as the new baseline
- [ ] 4.4 Verify the staged subset loads (skill_view / registry readback) and that the guard's negative case fires; assert the live skills count is unchanged before the gate approves

## 5. Binding and identity reconciliation

- [ ] 5.1 Repoint the pre-LLM and pre-tool-call gate hooks to scripts inside the canonical home (sanctioned CLI, backup first, readback after)
- [ ] 5.2 Add a startup self-check that surfaces a missing gate script as a loud diagnostic rather than a silent denial
- [ ] 5.3 Archive the second home with a per-entry digest receipt, or adopt it canonically and update the binding files — record the decision either way
- [ ] 5.4 Reconcile `HG-KSEOS/config/hermes.json` to the live runtime identity (0.21.5 / resolved MSIX home) with command evidence, and record the version delta
- [ ] 5.5 Resolve the 2026-10-06 failed update: complete or discard the parked stash with a recorded decision and a rollback copy

## 6. Update hardening, lane and gate repairs (R12–R16; added after the independent VERIFY verdicts)

- [ ] 6.1 R12 — updater must not `unlink` WAL sidecars before a consistent copy exists: take the copy with the SQLite backup API (or `VACUUM INTO`) first, verify it, and only then touch sidecars; every deletion emits a receipt.
- [ ] 6.2 R12 (negative) — simulate a non-atomic copy of a WAL-bearing database and PROVE the guard refuses it.
- [ ] 6.2b R12 acceptance oracle (data preservation, NOT integrity-only) — prove that a copy taken with the backup API / `VACUUM INTO` remains READABLE for rows that exist only in the WAL, on a purpose-built fixture; integrity-only (`quick_check ok`) is explicitly insufficient.
- [ ] 6.3 R13 — make the control-plane test suite hermetic: per-test spine/database; add a guard that FAILS any test which appends a `canonical_events` row to the canonical spine; CI pre/post check that the event count is unchanged (defect D15 proved this is currently violated: +2 events per run, reproducible).
- [ ] 6.4 R14 — repair the five red tests and reconcile declarations: `test_denominator_head_matches_git` (declared value must equal `git rev-parse HEAD`), guide/current-claim and `_final.md` projection tests, `test_r4_only_allowed_files_changed` scope check, and the COV-11-06 source-text test (defect D16; suite must end `OK`).
- [ ] 6.5 R15 — repair the crossed TaskSpec/WorkOrder binding in the spine (D17): create the correctly paired TS/WO via the domain API and record a supersede note, or record it explicitly as a disclosed one-WO-per-TS exception.
- [ ] 6.6 R16 — narrow the runtime pre-tool-call gate matcher so it inspects dangerous content patterns instead of input paths/whole payloads, and whitelist writes to an already-admitted run dir; keep blocking real secret-bearing payloads (D18). Negative + positive acceptance required.
- [ ] 6.7 Align `HG-KSEOS/config/hermes.json` to the **measured** HEAD `f97608f178d1ffeca59860195ab7da295f7c8e5f` (D8/D14), and explain the version-stamp divergence separately rather than adopting the stamp as the alignment value.

## 7. Coordination-state hygiene

- [ ] 7.1 Repair the stale `kanban_state` field to the live truth and record the small repair with a readback
- [ ] 7.2 Dispose of the 0-byte stale lock files only after confirming no live process holds them (quiescence procedure); otherwise disclose and leave them
- [ ] 7.3 Record the partial trigram-FTS coverage as a disclosed limitation or resolve it on a COPY

## 8. Closure and acceptance

- [ ] 8.1 Freeze the single evidence MD, mirror it byte-identically into the three review roots, and verify SHA-256 equality
- [ ] 8.2 Obtain the independent VERIFY/SECURITY lane verdict (gpt-6.1-sol, fresh context, read-only) with an explicit blockers count per round; keep every round's FAIL verbatim
- [ ] 8.3 Keep the claim ceiling honest: implementation vs locally+independently verified vs externally accepted, with what remains open listed item by item
- [ ] 8.4 Record every live metric with an as-of timestamp and an observed range; a live count must never be quoted un-stamped
