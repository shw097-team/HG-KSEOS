## Context

The candidates are already built and reviewed; the remaining work is evidence and ownership
transfer, not construction. The round runs under HG-KSEOS as the only normative control plane, with
canonical Hermes as the governed runtime and the Codex CLI lanes for bounded execution and
`VERIFY_ONLY` checking. The acceptance report explicitly forbids any new core repair round absent
one of five counterexamples, and the published prerelease must remain byte-identical.

## Goals / Non-Goals

**Goals:**
- One packet an external acceptance officer can audit without re-deriving anything from chat.
- Live identity freeze for `main`, both candidate pull requests, the annotated tag and the release assets.
- Four test denominators published side by side, unreconciled.
- Owner effects handed back with exact expected head SHAs.

**Non-Goals:**
- Any product source or schema change; any new tag or release; replacing the published `.4` assets.
- Four-host qualification, `S4_FULL_PASS`, `PRODUCTION`, public Directory submission.
- Claiming model-axis independence.

## Decisions

1. **Freeze by live readback, cite the report only as authority.** Reason: the report is a
   point-in-time review; a closeout must be reproducible after it. Alternative rejected: quoting the
   report's SHA table (unverifiable and stale-prone).
2. **Verify, do not merge.** The agent holds repository write capability, but the governance contract
   puts merge/tag/release behind the owner gate. Reason: separation of duties survives technical
   capability. Alternative rejected: "the tool can, so it may".
3. **One consolidated checker pass with an explicitly bounded scope.** Reason: the previous round
   showed four iterations each finding a genuinely new defect; the added value of a fifth pass is
   lower than the cost, so the residual is declared instead.
4. **Evidence on a scoped branch, never on the product branch.** Reason: the product write-set gate
   rejects round evidence, and evidence must not contaminate the candidate under review.

## Risks / Trade-offs

- **Same-model checker**: the verdict carries less independence than a cross-model one; mitigated by
  disclosing the limitation on every verdict and leaving ratification to the owner.
- **Hosted skip-count drift** versus local runs: mitigated by publishing both denominators rather
  than normalising them.
- **Log availability**: if a CI job log cannot be fetched, the row records the HTTP status instead of
  a reconstructed summary.
