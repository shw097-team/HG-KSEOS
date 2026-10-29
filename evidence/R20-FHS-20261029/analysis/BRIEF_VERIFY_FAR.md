# VERIFY brief — FAR_CLOSURE_AND_PROMOTION_20261029 (advisory falsification)

You are an independent checker. You did NOT write the document. Your job is to FALSIFY its numeric claims
by measuring them yourself. Do not trust any number in the document; re-derive it.

## Inputs (absolute paths, read-only)

- FAR document: `C:\Projects\Agent_Workspace\_handover\R20-FHS-20261029\FAR_CLOSURE_AND_PROMOTION_20261029.md`
- Shipped archive: `C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric\SBL_PIPD\FHS-MSC\FHS-MSC_PIPD-LS-PKG\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision3.zip`
- Receipts: `C:\Projects\Agent_Workspace\var\R20-FHS-20261029\receipts\`
- Repo: `C:\Projects\Agent_Workspace\HG-KSEOS` (git, read-only: do not commit, do not checkout, do not merge)
- Work tree for tests: `C:\Projects\Agent_Workspace\wt-r19-delivery`

Long paths are DISABLED on this host (260 char limit). If you must extract the archive, extract to `C:\r20chk`
(short root) and delete nothing outside it.

## Expected values (verify these, do not assume them)

| Claim | Expected |
|---|---|
| C1 archive sha256 | `ee0091173c3a5df96b48c469eeb2294e500c7bd1122f46a696e166e9baa6081f` |
| C2 archive bytes / entries | `13578117` / `89` entries, `0` directory entries |
| C3 validator on a fresh extract | `2789` passed / `0` failed, `scope=AUTHOR_STATIC_FIXTURES_ONLY` |
| C4 checksum list rows verified | `88` rows, `0` mismatch (list must NOT contain itself) |
| C5 HOLD_DISPOSITION rows by reader | CALIBRATION 11, HUMAN_DECISION 11, HUMAN_JUDGE 11, TWO_VERSION 8, PERFORMANCE 5 = 46 |
| C6 STAGE18 rows | `18` rows, all `status=ABSENT`, owners = ProductOwner 6 / ArchitectureOwner 6 / ProgramOwner 6 |
| C7 package holds.json | `11` rows, classes SOURCE 2 / ABI 4 / HOST 3 / CHECKER 1 / RELEASE 1 |
| C8 repo topology | `main` has 4 commits; `candidate/r19-fhs-implementation` has 214 commits; `git merge-base main candidate/r19-fhs-implementation` FAILS (rc=1, no common ancestor); `candidate/r18-fhs-skeleton-spine-20261029` IS an ancestor of r19 |
| C9 tree diff main↔r19 | `941` files changed, `+121019 / -5438`; narrow subset `scripts config tests evidence/R20-FHS-20261029 docs` = `207` files, `+42745 / -723` |
| C10 gate tests | `pytest tests/test_lane_dispatch_r20_gates.py -q` in the work tree = `9 passed` |

## What to produce

Write `FAR_CHALLENGE_20261029.json` in the current working directory:

```json
{"claims":[{"id":"C1","verdict":"PASS|FAIL|HOLD","measured":"...","method":"..."}],
 "disagreements":["..."],
 "overall":"PASS|PASS_WITH_FINDINGS|HOLD",
 "claim_ceiling":"advisory only; you are not an acceptance authority"}
```

Rules:
- One claim the document makes that you could NOT test must be `HOLD` with the reason, never `PASS`.
- Any mismatch between the document and your measurement goes in `disagreements`, with both values.
- Do not fix the document, do not write inside the archive, do not touch git state.
- End your final message with exactly one line: `NONCE=<the nonce you were given>`.
