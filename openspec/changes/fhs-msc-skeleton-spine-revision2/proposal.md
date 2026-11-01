# Proposal: FHS-MSC Skeleton+Spine revision2 — native DAG execution (R18)

## Why

The FHS-MSC Skeleton+Spine package `FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2`
(85 files, 22-WP typed DAG, claim ceiling `AUTHOR_STATIC_ONLY; NATIVE_NOT_RUN; CHECKER_NOT_RUN;
RELEASE_NOT_RUN`) is a source-bound repair candidate for the Skeleton+Spine wiring of the FHS-MSC product
authority spine. It has never been executed as a governed DAG: its own 22 work packages carry
`native_status: NATIVE_NOT_RUN`, and no round has yet re-executed its author suites, mapped its receipts to
the MVS01–10 gate groups, or taken it through an independent checker.

The owner has issued a standing grant for this round: affected research, isolated tests, reversible repair on a
candidate branch, and branch/commit/PR publication. Native L2/L3/L4 effects still require a real Issuer PERMIT.

## What changes

1. **Source freeze is verified, not asserted.** Manifest rows, checksum rows, ZIP members and the 22-node /
   36-edge DAG are re-derived from bytes; the round binds its work to the outer archive sha256
   `4f5d6e93a7fb300da452f3807f2a2e2368b4e57f2b8b980fdd0e4706a4b773a5`.
2. **Governance binding.** One SharedSpine project (`FHS-MSC-R18-20261029`) with one frozen requirement per
   WP-FHS node, and a measured proof that the native admission gate refuses without signed Issuer references
   (`ERR_NATIVE_BUNDLE_REQUIRED`).
3. **L0/L1 execution with receipts.** WP-00/01/19/21/15/16/05/07/04 are re-verified against the candidate's own
   evidence; the affected L2/L3/L4 packages are typed PARKed per WP with a named owner, next legal action and
   resume predicate — never with a fabricated permit.
4. **Independent acceptance.** A different-principal checker lane reads a frozen subject; its verdict is
   recorded with the explicit ceiling `INDEPENDENT_AGENT_READBACK`, not a protected native checker.
5. **Delivery.** Candidate branch + commit + push + PR per affected repo; never `main`, never force-push,
   never merge/tag/release.

## Impact

- Affected specs: `fhs-msc-skeleton-spine` (new capability delta, below).
- Affected code: none in `main`; the round writes only under
  `C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029` plus per-repo candidate branches.
- Claim ceiling for this change: `CANDIDATE_VERIFIED` — local isolated verification plus independent
  agent readback. It is not a full-product claim, not a native host acceptance, and not a release.
