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

## Second correction — the causal repair proof failed (my procedure, not the theory)

I attempted red → patch → green → un-patch → red inside a throwaway copy. It produced **2789/0 in all three
phases** (`causal: false`), and the reason is my own bug: `tools/repair_stale_pins.py` hardcodes
`SUBJ = .../subject`, so the "repair" ran against the frozen copy instead of the copy under test. The three
phases were therefore the same tree with nothing changed between them.

What that also revealed, and this part matters more than the bug:

- today, three consecutive runs of `validate.py` on `subject/` return **2789 passed / 0 failed**;
- the SWARM child at 15:39 returned **2788 / 1** on its own copy, failing `SOURCE-BYTES-UNCHANGED`;
- the difference tracks whether the 29 relocated external source documents resolve at that moment.

So `SOURCE-BYTES-UNCHANGED` is **environment-dependent and not deterministic on this host**. That makes
2789/0 *and* 2788/1 both true statements about different moments, and neither one a property of the
delivered artefact. The headline number must therefore be quoted as "2789 checks, 1 of which depends on
external source paths that moved after the freeze", never as a bare PASS count.

WP-18 stays PARTIAL: repair causality is **NOT PROVEN** (procedure mis-targeted), and the underlying check
cannot be made deterministic from inside this round.

WP-19 is the one that improved: `receipts/WP19_SBOM_RESCAN.json` scanned the frozen subject twice with
identical hashes and byte totals (85 files), so the SBOM is now recomputable.

## Third correction — the repair is not causal; the "defect" is time-dependent

`receipts/WP18_CAUSAL_REPAIR.json` (v3) ran three phases in three separate copies, parsing the report that
`validate.py` writes rather than its indented stdout:

| phase | passed | failed |
|---|---|---|
| pristine copy | 2789 | 0 |
| same copy after `repair_stale_pins.py --target` | 2789 | 0 |
| pristine copy again | 2789 | 0 |

`causal = false`, `deterministic = true` (the three runs agree with each other).

Consequences, stated plainly:

1. The pin repair **does not cause** the pass — the pristine copy passes without it. So D-R18-01's "2788/1 → 2789/0"
   narrative is not a repair story at all; it was two observations taken in different environments.
2. The single failure the SWARM child saw at 15:39 (`SOURCE-BYTES-UNCHANGED`) is **not reproducible right now**
   and was not reproducible in three fresh copies, so the check depends on whether the 29 relocated external
   sources resolve at that moment. It is an unstable check, not a defect of the package bytes.
3. WP-18 therefore closes as **NOT PROVEN** (no bounded repair can be demonstrated), and the honest headline
   for the validator is: *2789 mechanical checks; one of them depends on external source paths that moved
   after the freeze; today it passes, at 15:39 it failed.*
