# FHS-MSC-ALLPASS-20261030 — closing report

Round: `FHS-MSC-ALLPASS-20261030`, under owner envelope `WIN-12cb9b954e99`.
Lanes: PLAN commander (gpt-6.1-sol) · EXECUTE bounded writers ×3 (opencode-go/deepseek-v4.1-flash) ·
VERIFY/AO ×2 (openai-codex/gpt-6.1-sol, nonces `NONCE-AO-20261030-E` and `-F`).

## The denominator, before and after

| | before | after |
|---|---|---|
| `ACC-WP-FHS-00..21` granted | 0 of 22 | **12 PASS** |
| refused by name, with expiry | 0 | **10 REFUSED_NAMED** (2026-12-31) |
| `NOT_RUN` among the 22 | 22 | **0** |
| delivery on `main` | no | **yes** — 151 files under `fhs_msc_handoff_20261030/` |
| first-work harness | 34/1 | **35/0 in the package's own tree** |

## What closed, and with what

| WP | artefact | how it was settled |
|---|---|---|
| 00 | `SourceManifest.json`, `RepoContext.json` | 24 corpus documents hashed individually (14 SBL + 10 PIPD); the reader's scalar `documents: 24` replaced by identities |
| 01 | `AUTHORITY_CONFLICT_LEDGER.json` | 13 declarations, 5 conflicting, each with file:line |
| 05 | `PI_PD_DEV_OPS_CANDIDATES.json` | 100 candidates (PI 56 / PD 31 / DEV-OPS 13), no promotion |
| 06 | `REVERSIBLE_DIFF.json` + one test | additive, revertible by one `git revert`; 3 tests pass |
| 07 | `PLAN_REVISION_ABC.json` | three revisions, one chosen, `NATIVE_NOT_RUN` stated |
| 09 | `PROTECTED_CHECKER_REQUEST.json` | claim, oracle, threshold, three negative fixtures, falsifier |
| 14 | `RELEASE_CANDIDATE.json` | release `fhs-msc-deliveries-20261030`, three assets, digests verified by download |
| 15 | `SPEC_18_STAGE.json` | 18 stages copied verbatim from the package table, with a gap analysis |
| 16 | `SLOT_TRANSLATION.json` | 24 slots / 25 methods, parity legend, unsourced counted |
| 18 | `BOUNDED_REPAIR_DIFF.json` | the MAX_PATH walk repair, measured before/after |
| 19 | `SBOM.json` | file inventory; no license file, no dependency manifest — **stated as unverified, not as clean** |
| 21 | `COVERAGE_MATRIX.json` | declared vs enumerated counts, discrepancy recorded rather than reconciled |

The ten that stay open are refused, not deferred: 02, 03, 04, 08, 10, 11, 12, 13, 17, 20 all need host
capability (policy-consumption trace, issuer principal, wake lease, worker cursor, three officers,
second host, fresh process tree, runtime capability broker, occupant slots, executable 192-cell matrix).
Each carries a reason and a review trigger in `evidence/WP-FHS-REFUSALS-20261030/REFUSAL_RECORD_20261030.json`.

## F-15 — the finding that took three attempts and one conviction

The harness failed `EXISTING_5_AFFECTED_TESTS`. First explanation: a bad loader. Second: the wrong
interpreter. Both were wrong, and the officer convicted the second one because it had been measured
against a **scratch copy of the tree**, not the package.

The actual cause: the harness put `READERS/PIPD/src` on `sys.path`, but the `tests` package sits at
`READERS/PIPD/tests` — one level above `src`. `loadTestsFromNames` raised, `wasSuccessful()` returned
`False`, and the case failed. One added line, measured in place:

```
unmodified package harness, pinned interpreter   → pass=34 fail=1
same harness + sys.path.insert(0, plain(E/'READERS/PIPD')) → pass=35 fail=0
```

The jsonschema preflight stays as a guard (a missing dependency must refuse, not produce a verdict), but it
was never the cause.

## Merge batch (OD-A)

| PR | result |
|---|---|
| #4 openspec-only | merged `91f47a50` |
| #6 publish/r20-subset | merged `da1d033b` |
| #7 this delivery | merged `1e98abf7` |
| #1, #2 | **blocked**: their branches share no ancestor with `main` (`git merge-base` empty; roots `a2389c13` vs `f6dfb1e5`), so git refuses with "unrelated histories" while GitHub still reports them mergeable |

#1 and #2 are not merged, and forcing them would attach an orphan history to `main`. Their 12 files
should be re-published from a branch cut off `main`; that is a decision for the owners of those
branches, not a merge to be forced here.

## Officer verdicts

- Pass 1 (`NONCE-AO-20261030-E`, 353.88 s): O1, O3, O4, O5, O6 PASS; **O2 FAIL**, conviction upheld.
- Pass 2 (`NONCE-AO-20261030-F`): O2 **PASS** — `unmodified pass=34 fail=1`, `with_one_line pass=35 fail=0`,
  `record_matches: true`, `root_cause_correct: true`.

## What remains true and is not claimed

- All twenty-two verdicts are lane verdicts. None is native; there is still no checker with its own
  principal and key.
- The release candidate is published, but Fabric and PIPD were not touched this round.
- Nine hundred and nine acceptances in the spine remain `NOT_RUN` — they belong to older rounds and are
  outside this delivery's denominator.
