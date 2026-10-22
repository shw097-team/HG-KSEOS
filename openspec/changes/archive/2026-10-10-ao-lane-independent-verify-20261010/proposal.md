# Proposal: make the AO/VERIFY CODEX-CLI lane a genuine independent check (round FAR-AO-INDEPENDENCE-20261010)

## Why

The round `FAR-AO-INDEPENDENCE-20261010` measured that handing VERIFY/SECURITY to the CODEX CLI did
NOT by itself produce an independent check, for three separable reasons:

1. `scripts/hgk-lane-dispatch.py` persisted only a 400-char stdout tail, so an AO verdict that did not
   land inside the tail was unrecoverable. Receipt `E3-ao-verdict.json` therefore had to be recorded as
   `ADVISORY_INCONCLUSIVE_FROM_RECORD` even though the turn itself exited 0 with a matching usage
   receipt.
2. Under the role-default sandbox on this host the checker's own shell commands are refused
   (`rejected: blocked by policy`), so the checker could not re-derive anything; it could only read
   what it was handed, which is not an independent check.
3. All three lanes resolve to the same model, so maker == checker is reachable by construction. This is
   NOT a harness defect and is not fixed by this change; it is recorded.

Measured in the same round: an escalated-sandbox checker CAN execute tools and re-derive a digest
(`certutil` returned the byte-exact sha256 of a subject file, 11.5 s, subject unchanged). So the fix is
to make that capability safe and to stop losing its output, not to forbid it.

## What changes

1. `hgk-lane-dispatch.py` persists each attempt's FULL stdout/stderr to
   `<json-out>.logs/attempt-<run-id>-<rank>-{stdout,stderr}.txt` with byte count and sha256 recorded in the
   receipt. The 400/300-char tails are retained for compatibility. The child's RAW BYTES are persisted
   (a decoded-and-re-encoded stream cannot be byte-exact), and the run id is in the filename so a
   re-run cannot overwrite the previous attempt's evidence.
2. A pre-spawn identity/health gate classifies every pool arm by `identity_requirement`
   (`none` | `cli_login` | `relay_pool`) and refuses BEFORE spawning with a typed code
   (`ERR_LANE_IDENTITY_NOT_PREAUTHORIZED`, `ERR_RELAY_OAUTH_NEEDS_REAUTH`). Health means
   REFRESHABILITY, not access-token expiry: an expired access token is normal because the relay
   refreshes single-flight.
3. `--require-arm provider/model` fails the run closed instead of silently degrading to another arm.
   Owner ruling 2026-10-10: the OAuth arm (`openai-codex/gpt-6.1-sol`) STAYS in the unattended pool, so
   the gate verifies it rather than excluding it.
4. `--guard-subject <file|dir>` snapshots digests before and after the turn; a removed or changed file
   voids the receipt (`ERR_CHECKER_MUTATED_SUBJECT`). Added files are recorded but not fatal, because a
   checker legitimately writes its own verdict outside the guarded roots. This is what makes an
   escalated-sandbox checker safe without trusting it.
5. `config/lane-route-slots.candidate.json` declares `identity_requirement` per CODEX-CLI arm so the
   gate is declarative and owner-visible instead of implicit in code.

## Impact

Additive. No `src/**` change, no registry rewrite, no relay restart, no credential operation, no
canonical-store write, no route promotion. The pool artifact stays `status: CANDIDATE` and remains
loadable by its own resolver (verified after the edit). `revision`/`supersedes_revision` are
deliberately NOT renumbered because an existing history entry already claims rev 7; the new entry is
recorded as rev 8 and the renumbering decision is left to the owner (disclosed in the round report).

## Iteration 2: what an adversarial review found and this change then fixed

An independent reviewer was asked to BREAK the three guarantees and did. Its findings were re-verified
by the author before being acted on, and each fixed one now has a regression test:

1. **`--no-identity-gate` also switched off `--require-arm`** (the require-arm block was nested inside
   the gate branch), so one flag could silently restore degradation to another arm.
2. **The pool's declared `identity_requirement` was dropped** when the dispatch built its candidate
   arms, so the declaration was decorative and only the provider heuristic was ever used; the
   misspelling case (`ERR_LANE_IDENTITY_UNKNOWN`) was unreachable end to end while the unit tests
   stayed green because they pass the field directly.
3. **The health probe was a substring test** (`"refreshToken" in raw`), so `refreshToken: null`, an
   empty string and an account marked needs-reauth all read as healthy.
4. **An escalated lane with no guard root was unbounded** while the receipt still reported success.
5. **The harness's own output could sit inside a guarded subject**, so its writes would register as
   subject changes.
6. **`text=True` + `errors="replace"` destroyed bytes before the file was written**, making
   "byte-identical" untrue for any non-UTF-8 output.
7. **Attempt logs collided across runs** (filename carried only the rank), so re-running with the same
   receipt path deleted the previous attempt's whole log.
8. A negative `--max-candidates` emptied the candidate list and crashed the gate with an `IndexError`
   instead of the typed refusal; its `[0]` access is now guarded and the argument is validated.

Residual findings that are NOT fixed and are disclosed instead: a before/after digest comparison
detects residue and not transient modification; a content-equivalent recreation of a guarded file is
indistinguishable; writes outside the declared guard roots are not measured; the required arm is
guaranteed ADMISSION-then-SERVICE but a runtime failure after a successful serve of the wrong arm is
only caught by the served-arm check; and the relay-health probe still does not contact the relay.

## Out of scope

- Cross-model maker/checker separation (the pool's `identity_overlaps_recorded_not_enforced` stands).
  Fixing it requires a model other than the owner-mandated `deepseek-v4.1-flash` in at least one lane.
- Moving the relay pool to a DEDICATED account. It needs one interactive browser/manual-code auth with
  a second ChatGPT account (`ocx account login codex`); the round prepares the runbook and the
  acceptance test but performs no credential operation.
- Auto-confirming an interactive login on the operator's behalf: that exceeds the authority gate,
  cannot work for a device-code or `refresh_failed` state, and is refused rather than approximated.
