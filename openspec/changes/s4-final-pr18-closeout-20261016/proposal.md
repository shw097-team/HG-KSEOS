## Why

The external independent acceptance report `PIPD-LS-SP-S4-EXTERNAL-FINAL-20261016` closed the S4
Preview MVP engineering question: PR #18 is `MERGE_APPROVED_SCOPE_ONLY`, `v0.1.1-preview.4` is
`PUBLISHED_PASS_SCOPED`, the private ZIP is `FORMAT_PASS / ONE_ACCOUNT_PARTIAL`, and the phase is
`TEMP_CLOSED_CHALLENGE`. Its STOP RULE forbids opening another S4 core repair round without one of
five named counterexamples. What is missing is not more product code: it is one auditable,
read-only evidence return that lets an external acceptance officer check the frozen identities and
lets the Owner perform the two merges and the phase ratification.

## What Changes

- Add a governed, read-only **release-closeout evidence return** procedure: freeze `main`, PR #18,
  PR #17, the annotated tag, the release assets and the CI raw logs; publish one lightweight,
  self-describing packet under `S4_FINAL_PR18_EXECUTION_RETURN/`.
- Record every detection row with source locator, expected/actual, evidence id, checker and
  candidate SHA, and keep the four non-interchangeable test denominators separate
  (hosted CI 635/6-skipped, local 635/4, R6 baseline 624/6, evidence branch 633/6).
- Return the Owner effects — merging PR #18 and PR #17, and signing
  `S4_PREVIEW_MVP_PHASE=TEMP_CLOSED` — as `OWNER_ACTION_REQUIRED` with `expected_head_sha`, instead
  of performing them.
- Disclose, in every checker verdict, that maker and checker are the same model arm (registry
  `SOD006-C3`), so no model-axis independence is claimed.

Explicitly **not** changed: no product source, no `schemas/`, no `.4` tag or asset, no new tag or
release, no ninth Skill, no MCP/Apps/Actions/Hooks, no public Directory work.

## Capabilities

### New Capabilities
- `release-closeout-evidence`: the read-only, reproducible freeze-and-return procedure (identity
  readback, denominator separation, owner hand-back, immutability guarantee) for a published
  prerelease closeout.

### Modified Capabilities
<!-- None: this change adds a closeout procedure and does not alter existing spec-level requirements. -->

## Impact

- Round root `_handover/S4-FINAL-PR18-CLOSEOUT-20261016/**` (planning, contract, checks, evidence).
- One scoped evidence branch in `shw097-team/PIPD-LS-SP`; no product branch and no `main` write.
- Owner effects are requested, never performed: merge and release remain `OWNER_GATE_ONLY`.
