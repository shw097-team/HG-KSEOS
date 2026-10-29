# Withdrawn claims (SWARM deleg_20715b47)

Three read-only subagents audited this round. Their measurements overrode three of my own claims.

| Claim I made | Measured | Status |
|---|---|---|
| "validate.py reproduces 2789 PASS / 0 FAIL on the isolated copy" | Pristine subject gives **2788 passed / 1 failed of 2789**; the single failure is `SOURCE-BYTES-UNCHANGED`. Cause: 29 external source documents were relocated after the freeze into `..._SKELETON_SPINE\OLD\` (26 byte-identical there, 3 unlocated). | **WITHDRAWN** for the pristine copy. 2789/0 is only reachable after a data-side pin repair in a working copy, which is not the delivered artefact. |
| "WP-FHS-18 DONE (bounded repair red→green)" | The cited file was the contract harness, whose own ceiling says it is not an execution. The real repair receipt (`WP18_D_R18_01_REPAIR.json`) is an isolated-copy repair and states the delivered candidate still carries the defect; `D-R18-02`'s negative control has no receipt at all. | **DOWNGRADED** to PARTIAL |
| "WP-FHS-06 DONE" | The cited artefact proves the delegation gate (7/7 permits, 6/6 refusals), not a candidate write. No diff or raw is tied to the row. | **DOWNGRADED** to PARTIAL |
| "WP-FHS-19 DONE" | Supply scan is real (85 files, 0 secrets, planted canary fired) but its SBOM no longer recomputes: 5/85 entries drift and `bytes_scanned` differs — it captured a transient tree state. | **DOWNGRADED** to PARTIAL |

## Upheld (independently reproduced)

- **83/83 byte integrity** of the frozen subject, 0 drift, 0 missing, re-verified after all runs.
- **96-cell oracle: 50 PASS_LOCAL_ORACLE / 46 HOLD / 0 DENY**, recomputed through `evaluate()` rather than read from fixtures; 679/0 internal checks.
- **Delegation**: signature valid over canonical bytes, subject digest reproduced from 83 pairs, 7/7 enforcement cases as expected, retired second key refused (`REFUSED_NONCANONICAL_OWNER`).
- **Gate hardening after the audit**: the record's public key is now pinned to `~/.hgk-owner/owner.key.enc`, so a forged record can no longer self-label the canonical fingerprint (`REFUSED_OWNER_PUBKEY_MISMATCH`).

## Counts

`ledger.json` (26 rows): DONE 4 · PARTIAL 14 · HOLD 1 · PARKED 7.
`receipts/FINAL_WP_STATE.json` covers the 22 WP rows only; the four round-level rows (ADMIT, MVS, DELIVER, HANDOFF) are reported separately. Do not quote 5/9/7/1 as ledger totals.
