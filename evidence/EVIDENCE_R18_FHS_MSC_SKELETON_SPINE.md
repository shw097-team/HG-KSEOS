# R18 evidence index — FHS-MSC Skeleton+Spine

Round `R18-FHS-SKELETON-SPINE-20261029` against the frozen subject
`FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`.

Subject identity: `sha256` over 83 sorted (path, sha256) pairs = `5a06d8ddfcfaeefdda4430a0fcd0677e5ca036ac9e10072b5f00e141824f430d`.
The working copy was verified byte-identical: 83/83 declared entries match, 0 drift, 0 missing.

## What was measured (locally, candidate-only)

- source / manifest / ZIP / DAG currentness: 82 manifest rows, 83 checksum entries, 84 ZIP members,
  22 WP nodes, 36 typed edges (`DATA_OR_ADMISSION` 34, `CAPABILITY` 2 — the DAG has **no acceptance edges**)
- candidate author validator re-run on an isolated copy: **2789 PASS / 0 FAIL** after a data-side pin
  repair (before: 2788 PASS / 1 FAIL; the 29 stale pins pointed at an abandoned `_SKELETON_SPINE_DRAFT` tree)
- 96-cell oracle re-run: **50 PASS_LOCAL_ORACLE / 46 HOLD / 0 FAIL**, 192 negative fixtures all refused
- WP contract harness: 6 mechanical checks per WP over the DAG's own declared fields → **22/22 CONTRACT_OK**
  (`WP_CONTRACT_RESULTS.json`); the prose invariants are explicitly **not** evaluated
- owner delegation: signed by the canonical owner key (`412b3519…`) through the existing owner window
  (`WIN-796b69117680`, 8 h / 40 ops), scope-bounded to 7 WPs and 2 effect classes, valid 30 days
- gate enforcement: **7/7 POS `PERMIT_DERIVED`, 6/6 NEG refused** (native, release, denied class,
  non-candidate target, expired, non-allowlisted WP)

## Independent challenge

The VERIFY_SECURITY lane produced a verdict under the required arm (`gpt-6.1-sol`, rank 2, nonce-bound):
**HOLD** — fixture consistency does not establish native qualification or authenticated execution
provenance. Not upgraded, not reinterpreted.

## What is NOT claimed

No native bundle, no Issuer PERMIT for HOST_OP/RELEASE, no acceptance signature, no release, no merge.
11 WPs are host-effect or release class and stay gated. Nothing here is an independent acceptance.

Reading order: `evidence/r18/FAR_R18_07_STOP_REVIEW_AND_OWNER_ENVELOPE.md`,
`FAR_R18_09_CLAIM_RECHECK.md`, `FAR_R18_10_CONCURRENT_SESSION_RECHECK.md`,
`DELEGATION_SIGNED_CANONICAL.json`, `DELEGATION_GATE_MATRIX_CANONICAL.json`.
