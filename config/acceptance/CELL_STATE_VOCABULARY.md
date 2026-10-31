# Cell state vocabulary (FAR-042 §1.3, adopted)

A cell is one point of the delivery's product matrix: `Kind × Mode × Host × Provider`. Before this clause the matrix
had a size (192) but no operational definition of a cell, which made every cell's verdict a matter of opinion — and
made "192 PASS" look like the only honest target when 168 of the cells have nothing on this machine to measure.

## The rule

A cell MUST carry exactly one of these states. A cell with no state is a defect in the report, not a zero.

| State | Means | Counts toward |
|---|---|---|
| `PASS` | the cell was measured on the named host and both the positive and the negative held | the PASS denominator |
| `FAIL` | measured, and the positive or the negative did not hold | the FAIL denominator |
| `NO_HOST_SURFACE` | the host has no installable surface for this Kind; nothing exists to measure | reported separately, neither PASS nor FAIL |
| `NO_ARTEFACT_PROFILE_VETO` | the packager refuses to produce the artefact this cell would measure (e.g. ASSURED on a tree that declares no independent checker) | reported separately |
| `LOADER_PASS_MODEL_HALF_UNMEASURED` | the host's loader served the artefact and stopped after removal, but the model-half could not run | reported separately, **never counted as PASS** |
| `NOT_RUN` | no local runner for this host on this machine | reported separately |

## Why the separate states are not a loophole

The vocabulary exists so that "we could not measure this" and "this does not exist to measure" cannot be written as
success. The test of the rule is the arithmetic: if a report's PASS count plus its other states equals the matrix
size, and every other state names its reason, the report is complete. If any state is blank, the report is short.

## What a cell must name to be measurable

1. the host surface (a path or an API),
2. the positive criterion,
3. the negative criterion.

A Kind whose cells cannot name all three is `NO_HOST_SURFACE` — that is a finding about the matrix, and the fix is to
define the surface, not to invent one.

## Applied (2026-11-01)

```
WP-20  192 = 18 PASS + 168 NO_HOST_SURFACE + 6 NOT_RUN (DeepSeek Harness, no local runner)
WP-11    9 =  4 PASS +   3 LOADER_PASS_MODEL_HALF_UNMEASURED + 2 NO_ARTEFACT_PROFILE_VETO
```
