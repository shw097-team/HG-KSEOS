# VOID NOTICES — which numbers in this directory are superseded

Read this before quoting any file in `evidence/r19/`. Every item below was measured twice: once wrongly, once
correctly. The wrong value is still on disk because deleting it would erase the record of the error.

| Artifact | Superseded statement | Correct value | Where |
|---|---|---|---|
| `SUBJECT_INTEGRITY.json` | "44/44 files byte-identical" | the package is **85 files / 145,944,348 B**; the 44-file figure is a `pathlib` MAX_PATH truncation (longest relative path 289 chars). Integrity of 44 files is true but says nothing about the other 41, including a 112,296,081 B `source_keyword_hits.jsonl` | `FAR_R19B` §A4 |
| `receipts/WP19_SUPPLY_CHAIN_R19.json` | "delivered set scanned, 0 secret" | scope was **8% of bytes**; the secret scan did not open the 112 MB jsonl nor the self-embedded 13,326,288 B ZIP | `FAR_R19B` §A4 |
| `receipts/WP21_ORACLE_RERUN_R19.json` | "27 actual CLI process invocations" | 27 is a **fixture declaration**; the rerun replays stored raw and spawns none (elapsed 0.019 s). The 679/0 and 50/46/0 counts stand | `FAR_R19B` §2 |
| `RESUME_HERE.md` §1.3 (as first written) | same 44-file scope | idem | `FAR_R19B` §A4 |
| TT-R19-LANE-SANDBOX (raised, then withdrawn) | "the dispatcher sandbox blocks the VERIFY lane" | the 1223 launch failure belongs to the **sealed lane home**; the human home runs `workspace-write` fine. Withdrawn; replaced by `TT-R19-SEALED-HOME-HELPER` | `receipts/VERIFY_LANE_R19.json` |
| `DISAGREEMENT_LEDGER_R19.json` item R-3 | "challenge rejected: the package's report is not stale green" | **the challenge was right**: the shipped `03_TESTS_AND_READBACK/static_validation_result.json` records `passed 2789 / failed 0` while a fresh run on the same bytes gives `2788 / 1` | `FAR_R19B` §A5 |

## What is NOT void

- `receipts/WP18_CAUSAL_REPAIR_R19.json` — the red→patch→green→unpatch→red sequence and the 29 exact-hash locator
  rewrites (26 into `OLD`, 3 into `AUDIO`) are reproducible and were independently re-verified.
- `receipts/WP15_16_ID_LEDGER.json` — 80 per-ID rows, 0 doc-only INSTALLED claims.
- `receipts/VERIFY_LANE_R19.json` `.mandated_arm_rerun` — the `gpt-6.1-sol` turn: `ok=true`, `served_arm ==
  required_arm`, 205.4 s.
- `EVIDENCE_ATTESTATION.json` — the owner signature is real, but it covers the tree as enumerated at that commit
  (268 entries, with the attestation and its manifest excluded); files added later are outside it by construction.

## Rule for the successor

Publish a denominator only after a long-path-safe enumeration that asserts **file count** and **max path length**.
If a number cannot be reproduced that way, it is a guess, not a measurement.
