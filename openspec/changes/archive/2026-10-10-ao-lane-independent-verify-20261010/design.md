# Design: pre-spawn identity gate + measured non-mutation for the CODEX-CLI lane

## D1. Why the gate must not be "refuse the OAuth arm"

An earlier draft of this fix proposed removing the `openai` arms from the unattended pool and seeding a
credential into the lane home instead. Both halves were wrong, and the round measured why:

* an arm routed with `-c openai_base_url=<relay>` consumes the RELAY's subscription credential, not the
  lane home's CLI login, so seeding the lane home would not have pre-authorised it;
* the owner ruling is the opposite: the unattended window must keep `gpt-6.1-sol` available.

So the gate does not exclude anything. It verifies, and it refuses only when the arm cannot work without
a human. Refusing BEFORE the spawn is what turns "a login window appears at 03:00 and the run hangs"
into "the run stops with a named blocker that is recoverable".

## D2. Health = refreshability, not expiry

`probe_relay_pool_health` looks for refresh material in the relay's credential files and deliberately
does NOT look at `expiresAt`. Measured: the relay serves turns while the human home's access token is
already expired, because refresh is single-flight and automatic. A gate that treated expiry as failure
would refuse healthy runs — a false refusal that would look exactly like the popup it is meant to
prevent.

## D3. Why the verdict is voided by measurement instead of prevented by a sandbox

On this host the role-default (read-only) sandbox refuses the checker's own shell commands, and
`workspace-write` was previously measured to degrade to read-only while still reporting success. That
leaves only `danger-full-access` if the checker is to re-derive anything. Since no sandbox can then
bound it, the bound is moved to MEASUREMENT: digest the guarded subject before and after, and void the
verdict if a file was removed or changed. This is the same shape the existing checker-bridge capability
already uses (`Read-only candidate subject`), reused here at the dispatch layer so the two cannot drift.

An `added` file is recorded but not fatal: a checker legitimately writes its own verdict file, and the
guard roots are chosen to exclude it. The residual hole (a checker could delete-and-recreate a subject
file with identical content) is disclosed rather than claimed closed; a same-content recreation is
content-equivalent, and any content difference is caught.

## D4. Why the full output is persisted

The receipt's tail is a convenience view, not evidence. The change keeps the tails for compatibility
and adds the artifact: path, byte count and sha256 of the complete stream. `newline=""` is required,
not stylistic: without it Windows rewrites every `\n` as `\r\n` and the stored digest would describe
bytes the CLI never emitted.

## D5. Ceilings stated with the change

* **Same-model SoD is unresolved.** All three lanes resolve to `deepseek-v4.1-flash` on owner
  instruction, so maker == checker is reachable by construction. This change makes the check
  *executable and recoverable*, not *diverse*. A verdict from this lane is advisory.
* **The dedicated-account cutover is not performed.** It requires one interactive auth with a second
  account; the round documents the exact operator steps and the acceptance test instead.
* **The gate is cheap, not proof.** The relay-health probe reads credential files and does not make a
  live completion call by default, so it can pass while the upstream account is quota-blocked; the lane
  then fails at the turn, which the receipt records.

## D7. What iteration 2 changed and why (hostile review)

The reviewer's mandate was to break G1/G2/G3, and it succeeded eight times; each fix has a regression
test named after the finding. Two of the fixes are worth naming as design changes rather than bug edits:

* **The bound moved from "enabled by flags" to "conditionally required".** The first version made the
  guard opt-in, so the safest configuration was also the one you had to remember. Now escalating a lane
  WITHOUT a guard is itself a refusal, and the override has to be stated explicitly and is recorded in
  the receipt. A safety property that depends on the caller remembering it is not a property.
* **"Byte-identical" was withdrawn and made true.** It cannot be achieved by decoding with replacement
  and re-encoding, so the capture path now keeps the child's bytes and only decodes for parsing. The
  claim is now backed by a test that round-trips invalid UTF-8.

The residual limits in the spec's last requirement are not oversights: a two-point digest comparison
cannot see a transient modification, and no non-sandbox mechanism in this harness can measure writes
outside the declared roots. Those are stated as DETECTION with the unmeasured paths named, which is the
same posture the existing checker-bridge capability takes.

## D6. Rollback

Restore `scripts/hgk-lane-dispatch.py` from `var/far-ao-independence-20261010/backup/` (pre-change
sha256 recorded) and `config/lane-route-slots.candidate.json` from its `.bak-rev8-ao-identity-*`
sibling; delete `tests/test_lane_dispatch_ao_guard.py`. The change is additive and the pool artifact
stays `CANDIDATE`, so no promoted state depends on it.
