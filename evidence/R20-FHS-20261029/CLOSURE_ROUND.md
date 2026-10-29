# R20 closure round — authorization, execution, and the six falsification rounds

This document is the closure record for the owner-authorized execution of the FAR plan
(`analysis/FAR_CLOSURE_AND_PROMOTION_20261029.md`, `analysis/CLOSURE_PLAN.json`).

Claim ceiling for everything here: **AUTHOR_SIDE_LOCAL**. The VERIFY lane's verdicts are advisory. The owner
receipt is an owner act, not an independent verification. Nothing here is external acceptance.

## 0. What was authorized, and by whom

- Owner message, 2026-10-29: "用戶授權 & 簽章執行FAR提出的全部最佳「裁決、授權、簽章」建議，和全部的建議執行方案".
- Envelope opened for this task: `WIN-7d092fd95ffc`, task `R20-FHS-CLOSURE`, scope
  `registry_row_sign` + `merkle_root_sign`, 24 ops, ceiling `REPOSITORY_WRITE`, owner fingerprint
  `412b351937be72a1`. The R19 window (`WIN-254a1c9fbe72`, 3/40 ops) was closed first and its before-state
  recorded in `owner_receipts/WINDOW_R19_STATUS_BEFORE_CLOSE.json` — one window at a time is the tool's
  fail-closed rule, not a preference.
- Anchor signature: merkle root `40a9fd30…` over 18 artifacts, Ed25519 `31f8f347…`, verifiable from
  `owner_receipts/OWNER_AUTHORIZATION_R20.summary.json` alone (the file carries `body_json` verbatim and
  `owner_public_hex`; sha256 + signature both check without any key file).
- The receipt states what the signature does **not** authorize: OR-6 separation of duties, OR-8 external
  acceptance, release/tag, and any merge to main.

## 1. Machine items (A1..A8)

| item | defect being closed | measured result |
|---|---|---|
| A1 | bare `pytest tests` reported 2 collection errors (781 collected) | **809 collected, 0 errors**; sibling import is relative-only — a fallback was removed after the checker proved it could load a different module |
| A2 | receipts could not name their producer | `producer.script_sha256` + `producer.git_head` on every attempt and receipt; `nonce_present_anywhere` / `nonce_in_agent_message` split; `tools/compare_lane_receipts.py` refuses cross-producer comparison (exit 4) |
| A3 | assignment drift was prose | `tools/config_drift.py`: 10 fields, `lanes_with_identity_change=[]`, `affects_issued_evidence=false`, never rewrites evidence |
| A4 | no representable fallback chain | `primary_arms` / `fallback_arms` / `declared_fallbacks` separated; primary COMPOSED; overlap refused with `ERR_ASSIGNMENT_PRIMARY_FALLBACK_OVERLAP` (exact, case-variant and alias shapes) |
| A6 | 75 residues with no decision surface | 8 packets, `ids_across_packets=75` (46 cells + 18 stages + 11 holds), each with signer, fill fields, verify command, ceiling |
| A7 | document numbers unchecked | `tools/evidence_reconcile.py`: 17 checks, 0 mismatches; negative mutation → 1 mismatch, exit 3 |
| A8 | `--require-arm` only checked after the call | selection filtered pre-spawn (alias-equivalent); production receipt: 4 candidates → 1, single attempt, `ok=true` |

## 2. Defects this round found in its own work

TT-R20-12 codex pin named a deleted binary (repaired, previous triple recorded) · TT-R20-13 `_producer` bound
in the wrong scope (61 green tests red, fixed) · TT-R20-14 a checker row asserted a local variable · TT-R20-17
verdict compared served/required by string while selection used aliases (a correct serve was refused after
210.09 s; alias pair now declared in `config/lane-arm-aliases.json`, verdict uses `arm_served_equivalent`) ·
TT-R20-18/19 my "primary excludes fallbacks" test was a tautology (replaced by a runtime refusal) · TT-R20-20
the overlap check ignored case variants and declared aliases.

Open: TT-R20-15 (2 lineage deletions deliberately not replayed onto the subset — owner decision) and TT-R20-16
(**74 pre-existing failing tests** repo-wide; 0 new ids vs `6086908`, 14 previously-failing now pass).

## 3. Six falsification rounds (VERIFY lane = `openai-codex/gpt-6.1-sol`, served via declared alias)

| # | nonce | seconds | checker verdict | consequence |
|---|---|---|---|---|
| 1 | `fc46244ad592fff4` | 210.09 | harness refused (TT-R20-17); content 1 PASS / 6 HOLD / 3 FAIL | brief C3 wording, C6 missing `--archive`, C10 count |
| 2 | `bd3363ae01fb3a1c` | 156.10 | 5 PASS / 3 HOLD / 3 FAIL | C1 fallback import, C4 tautology, C10 363 vs 364, C11 bare-model widening |
| 3 | `cda911cd8fe19bc8` | 193.82 | 5 PASS / 4 HOLD / 1 FAIL | C4 replaced by runtime refusal; C8 projection made self-verifying |
| 4 | `ec06c324068b7fce` | 212.36 | 6 PASS / 4 HOLD / 1 FAIL (C10 blob ids) | overlap made alias/case aware; manifest blob source fixed |
| 5 | `cedd03b119d0d07f` | 208.66 | 5 PASS / 3 HOLD / 1 FAIL (C10, 3 stale blobs) | `git hash-object` of the working tree |
| 6 | `a52ce6085a28497d` | 226.24 | **6 PASS / 4 HOLD / 0 FAIL — overall HOLD** | nothing outstanding to fix |

The four HOLDs in round 6 are structural, not evasive: C1/C4/C7/C9 all require executing tests or spawning the
dispatcher, and this lane's sandbox is read-only by design (escalating it VOIDS the verdict by contract). In
each case the checker's own read confirmed the property and it said so.

Full receipts: `lane/CLOSURE_VERIFY_R20_R6.json` (round 6), the per-round log directory it names, and
`var/R20-FHS-20261029/lane/receipts_attempt1_FAIL3.json` (round 1).

## 4. What is genuinely left

1. **75 residues need owner signatures** — `owner_requests/OR-1..OR-8.json` (machine) and `.md` (human). One
   signature per decision maker; each packet carries its own verify command and ceiling.
2. **OR-6 (separation of duties) and OR-8 (external owners)** cannot be satisfied by any agent, by design
   (DOC-00:504, DOC-02:10643).
3. **74 pre-existing failing tests** repo-wide — attributable to nothing in this round; a separate round.
4. **Merge of `publish/r20-subset` (PR #6) to main** — the owner's press. 366 paths, every one listed with a
   working-tree blob id in `SUBSET_MANIFEST.json`; two lineage deletions deliberately not replayed.
