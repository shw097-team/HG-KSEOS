# FHS-MSC HANDOFF-PATCH-v1 execution record

## Why

The FHS-MSC product package `FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1` declares a single claim,
`PIPD_CONSTRUCTION_HANDOFF_READY`, and hands off one first work (`WP-FHS-15`). Nobody had executed that
handoff on the receiving side: the package was delivered, described and left. This change records the
execution — what verifies, what does not, and what the next team inherits.

## What changes

Additive only. No existing file, policy, requirement or job is modified.

- `fhs_msc_handoff_20261030/` — execution record: receipts, the four verifiers, the reproduced
  first-work artefacts, the seventeen current books, the package manifests, and the narrative documents
  (`README`, `EXECUTION_REPORT`, `FINDINGS`, `REPRODUCE`, `EVIDENCE_INDEX`).
- `openspec/changes/fhs-msc-handoff-patch-v1-exec/` — this proposal, its tasks and the requirement
  delta.

Nothing is moved into a normative path: the seventeen books stay under the delivery directory, not under
`docs/`, because this repository is not their writer.

## What it establishes

| Statement | Basis |
|---|---|
| the delivered payload is intact | 909/909 manifest rows match byte length and SHA-256, once the canonical directory name is restored |
| the delivery seal is not | three of nine delivery-manifest rows are absent, including both archives and the readback |
| the first work is reproducible | three SPECs, `SourceReadback` and the 22-WP DAG reproduce byte-identically; PI/TaskSpecSeed differ only through an absolute-root identity |
| the package's own harness fails as shipped | 34/35, `EXISTING_5_AFFECTED_TESTS` import-order defect; 35/35 after a one-line move (`lines_changed: 2`), conditional on the delivered READERS snapshot (F-13) |
| the graph and the declaration disagree | declared closure `{00,01,15}` versus edge-derived `{00,15}` |
| one lane works and says so, one fails closed | EXECUTE served `opencode-go/deepseek-v4.1-flash` with nonce echo; VERIFY returned an upstream 401 and no fallback existed, so independent acceptance did not run (F-10); receipt defects F-07/F-08 recorded |

## Impact

- **No runtime effect.** No permit, WorkOrder, lease, host operation, user-data effect, remote write or
  release is performed or claimed.
- **No control-plane mutation.** The only write outside this directory is an OpenSpec change; the live
  HG-KSEOS working tree is untouched except for the one-line dispatcher repair documented in F-07, which
  is recorded with its before/after SHA-256 and its backup.
- **For the next team**: 14 numbered findings (F-01..F-14), each with one next action, plus a reproduction path that a reviewer
  can run in five minutes.

## Claim ceiling

`PIPD_CONSTRUCTION_HANDOFF_READY`. `NATIVE_ADMITTED`, `NATIVE_VERIFIED`, `INDEPENDENT_ACCEPTED` and
`RELEASE` remain `NOT_RUN`; independent acceptance is a separate lane and its verdict is not part of this
change's authority.
