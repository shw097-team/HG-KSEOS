# hgk-cnv-far018-far019-archive

## Why
Three candidate evidence pull requests (#12 R7R11 archive, #13 FAR-018, #14 FAR-019) are frozen and
independently reviewed (`EIA-FABRIC-FAR018-FAR019-ARCHIVE-20261016`).  The archive stage can be closed
without promoting any product code, but only under a bounded maintainer authorisation, a trusted scoped
secrets scan, and a per-PR merge at an approved exact SHA.

## What changes
Evidence only: the three existing `EVIDENCE/**` prefixes are merged normally into `main`, and this round's
own return pack is added under `EVIDENCE/CNV-FAR018-FAR019-ARCHIVE-20261016/`.

## Impact
- Capability: archive-evidence-merge (new, evidence-only).
- No product, runtime, config, hook or workflow change.
- Rollback: `git revert <merge_sha>` per PR.
