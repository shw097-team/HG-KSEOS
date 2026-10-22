# Change: hgk-cnv-evidence-archive-r7r11-20261016

## Why

The owner's commanding document `Fabric × Hermes × HG-KSEOS｜R7～R11 外部驗收後續作「指揮薄 PROMPT」`
(contract `CNV-EVIDENCE-ARCHIVE-R7R11-20261016`) and the external review
`EIA-FABRIC-CNV-R7-R11-20261016` both require this round to be executed as a SINGLE `EVIDENCE_ONLY`
ChangeSet: eight existing candidate-evidence pull requests (#4..#11) in `shw097-team/Fabric` are to be
preflighted one at a time, corrected only where a defect is actually measured, and — after a real
repository-maintainer approval — merged to `main` with remote readback, so that each candidate evidence
set either reaches `ARCHIVE_MERGED_READBACK_PASS` or reports an exact first-fail blocker.

This record exists so the work has a named-method route record under HG-KSEOS governance instead of
being executed maker-direct. It does not widen the round's authority: the round's ceiling is
`CANDIDATE_EVIDENCE_ARCHIVED_ONLY`, full convergence stays `TEMP_CLOSED_CHALLENGE`, and production stays
`FAIL_CLOSED`.

## What changes

- **Governance records only (no product code).** The change is an ADDITIVE, evidence-only record set:
  the round's source ledger, prompt-compiler receipt, HGK typed admission, Kanban/SWARM board evidence,
  per-PR preflight receipts, the ten-finding disposition matrix, and the convergence evidence return pack.
- **No canonical mutation.** `config/**`, product code, workflows, hooks, licences and the frozen source
  roots are untouched. Any later canonical change must ride its own typed WorkOrder.
- **Remote effect is bounded to evidence publication.** One new evidence branch plus one new pull request
  for this round; merging the eight existing evidence pull requests requires the separate, real
  maintainer approval recorded per PR.

## Impact

Affected surface: `_handover/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/**` (local round root) and
`EVIDENCE/CNV-EVIDENCE-ARCHIVE-R7R11-20261016/**` on a new branch of `shw097-team/Fabric`.
Unaffected: all previously merged/published evidence, the protected subject
`_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/`, both already-applied slim Skills, PIPD canonical main,
and every peer in-flight branch.
