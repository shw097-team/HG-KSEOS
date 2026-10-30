# r4 — receiver revision

This directory is **additive**. The sealed delivery bytes are not touched, re-sealed or reinterpreted:
`01_SUBSTANTIVE_BODY/` and `03_HANDOFF_EVIDENCE/` keep the digests the delivery declares, and both archives
still rebuild byte-exactly (AO O2/O3, `P13`).

## What r4 closes

| Former defect | Disposition in r4 |
|---|---|
| `PACKAGE_READBACK.json` absent (`F-01`) | `RECEIVER_READBACK.json` — a **receiver-side** readback. Deliberately not named after the author artefact: that one embeds author-run results (`minimal_static`, `one_light_global`, `link_count`) that cannot be re-derived from the tree, and impersonating it would be worse than its absence. |
| Harness import order (`F-03`) | `tools/check_first_work.py` — one statement (`sys.path.insert(0, .../READERS/PIPD)`) moved **before** `loadTestsFromNames`. The shipped file in `03_HANDOFF_EVIDENCE/QA_TOOLS/` is untouched. |
| Layout prefix (`F-02`) | Measured and cited (`P14`): 31 rows, 0 resolving as declared, 31 resolving through the alias. No payload edit. |
| Seal reproducibility (`F-01c`) | Withdrawn. Both archives byte-exact under the shipped packer rule. |

## Hashes

| File | SHA-256 |
|---|---|
| `tools/check_first_work.py` (fixed) | `5b1a606fe8ca97f2701413c2b6c11e231ae87251cf392296dce39199e68261bc` |
| `03_HANDOFF_EVIDENCE/QA_TOOLS/check_first_work.py` (shipped) | `e075611a7313c6c27514a79fe446e6d90bd7c4ee423e1a5f035e45aa8bb0a3a2` |
| `RECEIVER_READBACK.json` | `84d2c95fe9b34cfc632962d67e6442fa8245d45196b8ed020fa6296be8470c0d` |

## Two honest caveats

1. **`F-13` stays open.** `prepare.py` does not carry `tests/fixtures` into the READERS snapshot, so a clean
   rebuild can still miss fixtures. r4 does not guess at a patch for a snapshot list it has not seen.
2. **`F-15` (new).** The harness needs `jsonschema` in the interpreter that runs it. Without it three
   validation cases fail with `ValidationFail:jsonschema unavailable` and the run scores below the recorded
   35/35 — an undeclared dependency of the delivery. Measured 2026-10-30 on Python 3.11.17.

## What r4 does **not** do

No re-seal, no digest rewrite, no manifest surgery, no claim promotion. `Native`, `Release` and
per-workpackage acceptance remain `NOT_RUN`.
