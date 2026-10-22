# S4 R6 closeout: install-doc version identity and the same-`plugin_id` update route

## Why

The independent R6 report (`PIPD-S4-EXTERNAL-CHALLENGE-R6-20261016`) keeps the S4 core repair closed and
`v0.1.1-preview.4` published, and asks for **one bounded documentation pass** rather than another repair
cycle. Three defects block a normal user from safely finding, downloading, verifying and *updating* the
private Skills-only plugin:

1. `F-R6-01` — `docs/install/README.md` states one release as the version pin and then names a
   **different release's** build-source commit, and its Web-fallback build example points at a mount pack
   that does not exist in the tree. A reader who copies the example produces a mis-stamped artefact.
2. `F-R6-02` — `docs/USER_GUIDE.md` still carries the preview.3-era `Merge and release are HOLD`
   sentence and the claim that the published wheel cannot inherit the Trace repair. Users read the
   published `v0.1.1-preview.4` as held.
3. `F-R6-03` — the install SSOT has no path for a user who **already installed** the plugin under the
   same `plugin_id`. The host's refusal of a second Add under an existing id is currently
   indistinguishable, in the docs, from a corrupt ZIP.

The repository already has the single install SSOT and the single user guide; the correct change is a
minimal correction of those two files, not a new document.

## What changes

1. `docs/install/README.md` version pin: states the `v0.1.1-preview.4` tag object and its dereferenced
   target, and explicitly separates the `v0.1.1-preview.3` target commit, the preview.4
   `build_source_commit` **and its declared scope** (the wheel only).
2. `docs/install/README.md` Web-fallback example: relabelled as the **legacy preview.3 example**
   (preview.4 ships no mount pack), with the mount pack, release id and commit all naming the same
   generation.
3. `docs/install/README.md` hashes: the plugin ZIP gains its download entry and its sha256, with
   `SHA256SUMS` named as the sidecar of record, plus an explicit "do not press Add again" pointer.
4. `docs/install/README.md` gains **Updating a plugin you already installed**: identify the id first →
   same id means Manage/Update or Upload new version → no such option means back up, uninstall with the
   user's consent, add once → a **new** id is a derived candidate, never the release asset → rollback by
   keeping the previous ZIP.
5. `docs/USER_GUIDE.md` ceilings: the published-wheel claim is scoped honestly (it does not assert that
   the preview.4 wheel inherits the Trace repair), and the `HOLD` wording is replaced by the actual
   state — preview.4 published, `S4_FULL_PASS` / `HOST_QUALIFIED` / production still `NOT_GRANTED`.
6. `docs/USER_GUIDE.md` Web section points at the install SSOT's update route instead of duplicating it.

## What does NOT change

- No product code, schema, workflow, test or `dist/` artefact.
- No change to the published `v0.1.1-preview.4` tag, its seven assets or their digests.
- No new tag, no `.5`, no merge, no release, no public plugin directory submission.
- The D1 / D2 / ClaimCeiling repairs already merged on `main` are not reopened.

## Claim ceiling

`LOCAL + PACKAGE`. The change is a candidate on a controlled branch; merge, tag and release remain
owner-gated, and the S4 Preview MVP stage close stays `TEMP_CLOSED` pending an owner signature.
