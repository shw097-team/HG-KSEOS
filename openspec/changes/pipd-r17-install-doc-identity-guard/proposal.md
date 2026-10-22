# FAR-R17 residual closure: guard the install documentation's release identity and links

## Why

The independent S4 R6 review kept the S4 core repair closed and `v0.1.1-preview.4` published, and asked
for exactly one bounded follow-up on the documentation side: fix the release-identity confusion and
**add a single doc-link / release-identity check** (`F-R6-01`). The 2026-10-16 round repaired the prose.
What it did not do is make the prose *stay* repaired: the repair is enforced by nothing.

Measurement of the existing tree shows the guard is half-built, which is why this is a small change and
not a new framework:

- `tests/test_r5r3_install_route_identity.py` already re-derives tag facts from git and binds the served
  ZIP digest to the download paragraph it belongs to — the **release-identity** half exists.
- Nothing checks that an in-page link resolves, and nothing checks that a documented build example does
  not mix one release's id with another release's commit and a mount pack that does not exist — the
  **doc-link** half, and the exact defect `F-R6-01` names, is unguarded.

Running this as a governed audit also produced one new measurement: the published
`v0.1.1-preview.4` release **serves** a `PIPD_WEB_FALLBACK.md` whose own header declares the earlier
`v0.1.1-preview.3` provenance, and whose digest matches the committed file — a provenance drift inside
an immutable release, which therefore cannot be repaired in place.

## What changes

1. `tests/test_r6_doc_identity_guard.py` (new, stdlib + `unittest`, no network) guards, for
   `docs/install/README.md` and `docs/USER_GUIDE.md`: no paragraph pairs the preview.4 release id with
   the preview.3 target commit unless it marks that commit as preview.3; every fenced build example
   names one release generation; no documented `dist/mount/` path is missing from the tree; every
   same-file `#fragment` link resolves to a heading; the user guide keeps `S4_FULL_PASS` `NOT_GRANTED`
   and does not reintroduce the preview.3-era hold sentence.
2. That test ships **paired mutations**: for each of the guard's checks, a mutated copy of the document
   must make the check fail. A guard that cannot fail is not evidence.
3. `docs/install/README.md` gains a bounded note recording the served-document provenance drift and
   stating that it can only be corrected by a future release.

## What does NOT change

- No workflow file: the existing `ci` workflow runs `python -m unittest discover -s tests`, so a new test
  file is wired in by the repository's own convention.
- No `tools/` script, no second verification framework, no new gate outside the existing suite.
- No product code, schema, `dist/` artefact, tag or release asset.

## Claim ceiling

`LOCAL + PACKAGE`. The guard is a candidate on the controlled branch; merge, tag and release remain
owner-gated, and `S4_FULL_PASS` / `HOST_QUALIFIED` / production stay `NOT_GRANTED`.
