# Round R18 evidence index — FHS-MSC Skeleton+Spine revision2

Publishable index only. Raw receipts, databases, credentials and host-specific paths stay in the local
round directory (`var/R18-FHS-SKELETON-SPINE-20261029/`), which is not published.

## Subject

`FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2` — 85 files, byte-frozen and read-only
for the whole round. Every check below ran against an isolated copy whose 83 in-package digests were
re-derived and matched before any test was run.

## Measured results

| Check | Result |
|---|---|
| Source freeze | 82 manifest rows, 83/83 digests, 84 ZIP members byte-identical, 22-node / 36-edge DAG |
| Candidate `tools/validate.py` as delivered | 2788 PASS / 1 FAIL (`SOURCE-BYTES-UNCHANGED`) |
| Same validator after repairing 29 stale source pins | 2789 PASS / 0 FAIL |
| 96-cell semantic oracle | 50 PASS_LOCAL_ORACLE / 46 HOLD / 0 FAIL, 679/0 author checks — matches the claim |
| WP-level oracle traceability | 22/22 WPs have no backing case for either their positive or negative oracle |
| Supply chain | 0 secret findings with a canary-validated detector; 9 files embed absolute host paths |
| Declared holds | 11 (HOST 3, ABI 4, SOURCE 2, CHECKER 1, RELEASE 1), each with a named owner and resume predicate |

## Defects found and their disposition

| Id | Defect | Disposition |
|---|---|---|
| D-R18-01 | `source_manifest.json` pins 29 inputs in the superseded `_SKELETON_SPINE_DRAFT` tree, so the author's own `SOURCE-BYTES-UNCHANGED` check asserts that revision2 never happened | repaired in the isolated copy (data only, validator untouched); the shipped package still carries it |
| FAR-R18-05 | `wp_graph.json` declares per-WP oracles that no case, cell or runner binding grounds | recorded, not papered over; author-side mapping required |

## Claim ceiling

No native qualification, no independent acceptance, no release. The candidate's own scope string says
`AUTHOR_LOCAL_ORACLE_ENGINE_AND_ACTUAL_PRIVATE_CLI_RAW; NOT_NATIVE_QUALIFICATION` with `native_case_pass = 0`
and `independent_verdict = NOT_RUN`, and this round does not raise that ceiling.

## Spec delta

`openspec/changes/fhs-msc-skeleton-spine-revision2/` — proposal, tasks and capability delta covering the
source-freeze, evidence, hold and delivery invariants this round actually exercised.
