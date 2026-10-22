# pipd-install-doc-identity — delta for pipd-s4r6-closeout-doc-identity-and-update-route

## ADDED Requirements

### Requirement: The install SSOT SHALL attribute each release identity to that release only

The install SSOT SHALL present a release id, its tag object, its dereferenced target commit and any
`build_source_commit` as fields of the SAME release entry, and SHALL state a `build_source_scope` wherever
that scope does not cover every artefact of the release. It SHALL NOT pair one release's id with another
release's commit, and SHALL NOT offer a build example whose `--mount-pack`, `--release-id` and
`--release-commit` name different generations. Where a release ships no mount pack, the page SHALL say so
rather than referencing a pack path that does not exist.

#### Scenario: a reader copies the documented build example

- **WHEN** a reader copies the Web-fallback build example from the install SSOT
- **THEN** every argument of that example names one release generation, and the example is labelled as
  the legacy example when the pinned release ships no pack

#### Scenario: a mixed pin is re-introduced

- **WHEN** the `v0.1.1-preview.4` id is re-paired with the `v0.1.1-preview.3` target commit
- **THEN** the round's doc-identity detector reports a failure rather than passing

### Requirement: The install SSOT SHALL define the update path for an already-installed `plugin_id`

The install SSOT SHALL define, in one place, what a user does when the plugin is already installed under
the same `plugin_id`: identify the installed id first; use the host's own Manage/Update or
Upload-new-version flow when it exists; when it does not, back up, uninstall with the user's consent and
add the newly downloaded ZIP once. It SHALL state that a same-id Add refusal concerns the id already being
present and SHALL NOT be read as evidence that the ZIP is damaged. A package re-issued under a
**different** `plugin_id` SHALL be described as a derived candidate, never as the published release asset,
and the SSOT SHALL NOT instruct anyone to create a new id automatically.

#### Scenario: a user with an earlier install downloads the current ZIP

- **WHEN** a user who already installed the plugin downloads the current release ZIP
- **THEN** the SSOT directs them to Update/Upload-new-version first, and to a consenting
  uninstall-then-add only when no such flow exists

#### Scenario: a renamed rebuild is presented as the release

- **WHEN** a package carrying a different `plugin_id` is presented as `pipd-ls-sp-public-skills.zip`
- **THEN** that presentation is a defect: the released asset keeps its own digest and the renamed package
  stays a derived candidate

### Requirement: The user guide SHALL state the measured publication state, not a superseded hold

The user guide SHALL NOT assert a release hold that the measured state contradicts, and SHALL NOT assert
that a published wheel inherits a source repair unless that inheritance is established. Where a
publication exists, the guide SHALL name it and SHALL keep `S4_FULL_PASS`, `HOST_QUALIFIED` and production
as separately `NOT_GRANTED`.

#### Scenario: a reader checks whether the pinned release is held

- **WHEN** a reader consults the user guide's ceilings
- **THEN** the guide reports the release as published while keeping full-pass and production gated

#### Scenario: the stale hold sentence returns

- **WHEN** the preview.3-era hold sentence is re-introduced into the guide
- **THEN** the round's currentness check reports a failure rather than passing
