# Tasks — pipd-s4r6-closeout-doc-identity-and-update-route

## 1. Version identity (F-R6-01)

- [ ] 1.1 `docs/install/README.md`: the version pin names the `v0.1.1-preview.4` tag object
      `0618d73c725da0d8c3280f99ef369d13741b5197` and its dereferenced target
      `cc6c1930765160697e7e51d6e37735b9220a30db`, and no longer presents any other release's commit as
      a preview.4 identity.
- [ ] 1.2 `docs/install/README.md`: the preview.4 `build_source_commit` is stated together with its
      `build_source_scope` (the wheel only, not the plugin ZIP).
- [ ] 1.3 `docs/install/README.md`: the Web-fallback build example is labelled the legacy preview.3
      example, and its `--mount-pack` / `--release-id` / `--release-commit` name one generation.
- [ ] 1.4 No reference to a `pipd-ls-sp-s4-chatgpt-mount-v0.1.1-preview.4` directory (it does not
      exist; preview.4 ships no mount pack).

## 2. User-guide currentness (F-R6-02)

- [ ] 2.1 `docs/USER_GUIDE.md`: the `Merge and release are HOLD` sentence is removed and replaced by the
      measured state (preview.4 published 2026-10-14; full S4 / host qualification / production
      `NOT_GRANTED`).
- [ ] 2.2 `docs/USER_GUIDE.md`: the published-wheel Trace claim is scoped without asserting that the
      preview.4 wheel inherits the repair.
- [ ] 2.3 `docs/USER_GUIDE.md`: the CLI section no longer contrasts a "candidate branch" against a
      "published wheel" as if the published line were frozen.

## 3. Same-`plugin_id` update route (F-R6-03)

- [ ] 3.1 `docs/install/README.md` gains the `Updating a plugin you already installed` section with
      identify → Update/Upload new version → consent back-up + uninstall + single Add → derived-candidate
      rule for a new id → rollback.
- [ ] 3.2 The section states that a same-id Add refusal is about the id already being present and is
      **not** evidence of a damaged ZIP.
- [ ] 3.3 `docs/USER_GUIDE.md` points at that section rather than copying it.

## 4. Download entry and digest (F-R6-04 / REQ-04)

- [ ] 4.1 The plugin ZIP bullet carries the release download entry and the sha256
      `545e359a5ca6abc7bcbbaa2316f8e062244ad4a132ae1ae839bc9a8e17d95d75` (68,357 bytes).
- [ ] 4.2 `SHA256SUMS` is named as the sidecar of record; the page does not become a second sidecar.
- [ ] 4.3 The `NOT_SUPPORTED_FOR_ACCOUNT` downgrade to `PIPD_WEB_FALLBACK.md` (`DOC_MOUNT_ONLY`) is
      preserved.

## 5. Verification

- [ ] 5.1 The round's doc-identity detector passes with 0 errors.
- [ ] 5.2 Every detector check has a paired mutation that makes exactly that check fire (non-vacuity).
- [ ] 5.3 `python -m pytest tests/test_r5r3_install_route_identity.py` passes on the candidate.
- [ ] 5.4 The affected regression subset passes with raw counts recorded.
- [ ] 5.5 `git diff --check` is clean and the changed path set is a subset of the authorized set.
- [ ] 5.6 A non-maker checker replays 5.1–5.4 on the frozen candidate and issues its own verdict.

## 6. Publication and closeout

- [ ] 6.1 The candidate is committed and pushed to the controlled branch; the remote head equals the
      local candidate SHA.
- [ ] 6.2 No secret appears in the diff, the branch, the commit message or the evidence pack.
- [ ] 6.3 `S4_R6_CLOSEOUT_RETURN/` is emitted with `CK-01..CK-14` dispositions.
- [ ] 6.4 Owner closeout ratification is requested; `TEMP_CLOSED` is not written as `FULL_PASS`.
