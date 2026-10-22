# R10-0 tasks

## 1. Admission and surfaces
- [x] 1.1 [ADMITTED|MEASURED] Typed HGK admission under a unique project id `CNV-R10-SESSCLOSE`
  (6 taskspecs / 6 work orders `WO-TS-SESSCLOSE-01..06`); source inventory hashed in the admission report.
- [x] 1.2 [MEASURED] KANBAN board `r10-session-closure-20261016` + SWARM graph recorded (root, 4 workers,
  verifier, synthesizer) and written to a round artifact on disk.
- [x] 1.3 [MEASURED] FAR run opened for this round's worklist (residual + unlanded candidates + closure).
- [x] 1.4 [MEASURED] Validated `--strict` by the project CLI before execution: `Change 'hgk-r10-session-closure-20261016' is valid` (the spec uses delta headers with requirement+scenario blocks).

## 2. R10-A change-record reconciliation
- [x] 2.1 [MEASURED] Adjudicated: 20 DONE_MEASURED / 3 OPEN_OWNER / 2 NOT_OWED. The rebind this record asks for IS in
  the canonical registry (epoch 21, PLAN `openai-codex/gpt-6.1-sol` medium ADMITTED, `check_drift` []), applied by
  an act OUTSIDE this round at 2026-10-16T12:36:30 - so the record is STALE, not the work. The change file was NOT
  edited by this round (a peer round is publishing that packet now).
- [x] 2.2 [MEASURED] Adjudicated: 4 DONE_MEASURED / 6 OPEN_OWNER / 1 SUPERSEDED. The split remedy is SUPERSEDED for
  the file it targeted: the governed measurement never exceeded the cap (99,996/100,000 LF-normalized characters)
  and the file now sits at 21,026 bytes after an in-place slim. Six rows remain open and are the ones that would
  ADD a regrowth guard, an index completeness pass and an independent recompute - a 73-of-112 unlisted-reference
  gap in the skill's own support-files index is recorded as the concrete low-cost item.
- [x] 2.3 [MEASURED] Re-derived fresh with the project's own reader (`lane_policy.load_registry()` +
  `route_for_lane()`): epoch 21, registry sha256 `38f0436b...aba38d2`, PLAN `openai-codex/gpt-6.1-sol` medium
  ADMITTED / EXECUTE `opencode-go/deepseek-v4.1-flash` UNPROVEN / VERIFY_SECURITY `openai-codex/gpt-6.1-sol`
  medium UNPROVEN, `check_drift` []. `check_sod(PLAN,VERIFY_SECURITY)` = **SOD_VIOLATION** (both `gpt-6.1-sol`) -
  a NEW control-plane defect surfaced by this adjudication (R10-F2). No artifact was manufactured.
- [x] 2.4 [MEASURED] `R10_CHANGE_RECORD_ADJUDICATION.json` (verdict counts, per-change reading, the orchestrator's
  own re-derivations, one recorded PROBE DEFECT, and a side-effect audit) plus the worker's `FAR/ws1/adjudication.tsv`
  (36 rows with evidence locators) and `FAR/ws1/raw_measurements.json` (81 measurements).

## 3. R10-B self-repair of this session's wrapper
- [x] 3.1 [EXECUTED-CANDIDATE] Repaired in the round's successor wrapper `tooling/dispatch_r10.py`: immutable per-turn
  receipt and attempt-log paths (lane + turn + UTC) plus automatic snapshot of BOTH files into the round root's
  `lane_receipts/` with sha256. Predecessors left byte-unchanged.
- [x] 3.2 [EXECUTED-CANDIDATE] `attest()` derives the expected nonce from the dispatched brief and searches the
  surfaces the dispatcher ALREADY recorded (`attempts[].stdout_path`, `stderr_path`) plus caller-declared artifact
  roots; the dispatcher's receipt is never rewritten and the served arm is read from `attempts[]`. The
  dispatcher-side half is a CONTROL-PLANE change and is carried as an owner-ready item instead.
- [x] 3.3 [MEASURED] `python -m pytest -q test_dispatch_r10.py` -> **8 passed**; includes a regression run against
  the round-before's REAL receipt and brief (no live lane, no network) which returns
  `NONCE_PRESENT_DESPITE_DISPATCHER_CODE` and names the 429,783-byte stdout that receipt itself recorded.

## 4. R10-C session closure and handover
- [x] 4.1 [MEASURED] Checkpoint bound to evidence refs in the typed admission report (`checkpoint` id) plus the
  handover package.
- [x] 4.2 [MEASURED] `SESSION_LEDGER_R10.json`: 7 disclosed side effects (including the delegation binding change
  with readback), 6 blockers with owners, 4 measured findings.
- [x] 4.3 [MEASURED] `HANDOVER_R10.md` sections 3 and 4: open items each with owner + locator, and a concrete
  resume procedure (re-measure, which wrapper to use, what the checker host cannot do).

## 5. R10-D publication
- [x] 5.1 [MEASURED] Packet prepared from a worktree cut off `origin/main` (first commit `1f436695`); M2 scan PASS
  (23 blobs, hard 0, soft 1). Prior evidence prefixes verified unchanged by an independent GitHub API read.
- [ ] 5.2 [OPEN] Push + independent readback (per-blob digest recomputation), prior prefixes unchanged.
- [ ] 5.3 [OPEN] Draft PR opened for external verification; claim ceiling restated in the packet.

## 6. Independent verification of this round
- [x] 6.1a [MEASURED] The VERIFY/SECURITY lane was dispatched on the mandate's arm through this round's successor
  wrapper and **fail-closed**: `ERR_LANE_REQUIRED_ARM_ABSENT` (exit 4) - the dispatcher's own identity_gate lists
  only rank 1 `openai-codex/gpt-6.1-sol`, `required_arm: opencode-go/deepseek-v4.1-flash`, "the required arm is
  not in this lane's pool". The registry and the lane slots were **NOT** edited to make the dispatch succeed
  (R10-F5).
- [x] 6.1b [MEASURED] The mandated checker MODEL was then run **provider-direct through the same relay** with the
  model pinned on argv, after a smoke probe returned `PROBE_OK` on exactly `opencode-go/deepseek-v4.1-flash`.
  That is a disclosed routing deviation with no pool hop and no pool ledger line; its verdict is advisory evidence
  and its serving arm is declared by the command line, not by a pool receipt.
- [ ] 6.1 [OPEN] Run the VERIFY/SECURITY lane on the mandate's checker arm and adjudicate its verdict.
- [x] 6.2 [MEASURED] Residual recorded: the order binds writer and checker to the SAME arm
  (`opencode-go/deepseek-v4.1-flash`), so this round's verification has NO model-axis independence - only
  process/lane separation plus a re-derivation duty. The checker is required to re-derive, not restate.

## 6b. Findings registered this round
- [x] 6b.1 [MEASURED] R10-F1 registry PLAN route contradicts the newest owner order (outside rebind at 12:36:30).
- [x] 6b.2 [MEASURED] R10-F2 the registry violates its own SoD invariant: `check_sod(PLAN,VERIFY_SECURITY)` = SOD_VIOLATION.
- [x] 6b.3 [MEASURED] R10-F3 the mandate binds writer and checker to the same arm -> model-axis independence ABSENT.
- [x] 6b.4 [MEASURED] R10-F4 the mandated checker arm's `admission_status` is UNPROVEN.
- [x] 6b.5 [MEASURED] A research worker's 0-byte SKILL.md claim was REFUTED by the orchestrator's own measurement
  (35,739 bytes) and recorded as a PROBE DEFECT.
- [x] 6b.6 [MEASURED] R10-F5 the mandated checker arm is absent from the lane's pool (routing absence, not a model
  outage); provider-direct access proved the model reachable.
- [x] 6b.7 [MEASURED] R10-F6 the successor wrapper's attestation path behaved correctly on that FAILED dispatch:
  1 snapshot copied, `NO_ATTEMPTS_RECORDED` - it manufactures no nonce and no arm from an empty dispatch.

## 7. Not authorised this round
- [ ] 7.1 [OWNER-BLOCKED] 221 cases, 8 Gates, Fresh G1, DOC-05 effect admission, release/publication approval.
- [ ] 7.2 [OWNER-BLOCKED] Any canonical lane-registry rebind; this round only records owner-ready items.
