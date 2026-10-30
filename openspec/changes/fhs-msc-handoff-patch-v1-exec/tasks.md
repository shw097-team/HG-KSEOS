# Tasks — FHS-MSC HANDOFF-PATCH-v1 execution

## Intake and verification

- [x] Unpack the delivery and enumerate the tree (911 files, 909 declared payload rows)
- [x] Detect and repair the layout mismatch `01_FHS-MSC_PIPD-LS-PKG_BODY` → `01_SUBSTANTIVE_BODY` (F-02)
- [x] Verify all 909 payload rows on byte length and SHA-256 (0 mismatch, 0 missing)
- [x] Verify the nine delivery-manifest rows and name the three absences (F-01)
- [x] Verify the 30 relative links in the three entry documents
- [x] Seal a reproducible pair of archives with per-entry CRC32/bytes/SHA-256/UTF-8 readback
- [x] Prove seal idempotence by sealing twice into different directories

## First work WP-FHS-15

- [x] Re-run `prepare.py` in an isolated root and snapshot the four readers plus the TPM plugin
- [x] Re-run `first_work.py`: 24 functional clauses → 24 atoms, PI reader PASS, 3 SPECs
- [x] Run the delivered 35-check harness as shipped and record 34/35 (F-03)
- [x] Apply the two-line ordering repair and record 35/35
- [x] Compare every first-work artefact against the delivery and classify each difference
- [x] Prove the absolute-root identity mechanism and the root-relative repair (F-04)

## Structure

- [x] Verify the 22-WP DAG: node count, edge count, acyclicity, topological completeness
- [x] Compare the declared `dependency_closure` with the edge-derived ancestor set (F-05)
- [x] Verify 24 PI atoms carry source reference, owner, expected oracle and negative fixture
- [x] Verify the FUO ten fields and the three SPECs' own negatives
- [x] Verify 2,221 unique current-reader locators

## Lanes

- [x] Dispatch the EXECUTE lane with `--require-assigned-arms`, nonce and rollout identity
- [x] Record the served transport arm and the nonce echo in a typed receipt
- [x] Prove a bounded single-file write through the same lane
- [x] Repair the dispatcher receipt-builder `NameError` and record before/after SHA-256 (F-07)
- [x] Record the toolchain-pin absence and the explicit-executable bypass (F-06)
- [x] Record the `served_arm_assigned` false negative (F-08)
- [ ] Independent acceptance by the VERIFY lane (`openai-codex/gpt-6.1-sol`) — out of this change's
      authority; runs as a separate turn and its verdict is published with the PR, not inside this file
- [ ] Release, tag, merge — out of scope, not claimed

## Delivery

- [x] Stage a deterministic tree with a per-file SHA-256 inventory (`STAGED_MANIFEST.json`)
- [x] Write README, EXECUTION_REPORT, FINDINGS, REPRODUCE and EVIDENCE_INDEX
- [x] Register this OpenSpec change
- [x] Open a PR against `shw097-team/HG-KSEOS` on a dedicated branch, no merge, no tag
