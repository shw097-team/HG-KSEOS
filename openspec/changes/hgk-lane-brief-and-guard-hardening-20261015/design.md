# Design: hgk-lane-brief-and-guard-hardening-20261015

## Context

Nine tooling findings (TF-01..TF-09) were recorded in round R7-0 while the round's lanes were
executing; two of three checker attempts were voided by the guard interacting with a driver that
kept writing into the frozen subject, and two legitimate dispatches were refused by prose matching.
The design question: what is the smallest set of typed, fail-closed corrections that stops spending
lane budget on receipt plumbing, without weakening any guard and without touching any authority
surface?

## D1 — classify markers by command context (TF-01)

**Chosen.** Require a shell-looking occurrence (line-initial `git`/`gh`/`curl`/`ssh`/`winget`, or
argv-shape) and require the match NOT be inside a prohibition sentence (`do not`, `never`,
`must not`, `SHALL NOT`, …). Keep `detection_only`; prose-only matches no longer refuse dispatch.

**Rejected:** deleting the marker check. The check's failure mode in the round was false positive,
not absence; removing it would trade a nuisance for an unguarded remote-write lane.
**Rejected:** matching only argv arrays. Briefs are free text; a plain command line on its own line
is a true positive and must keep refusing (fail-closed boundary).

## D2 — guard subject = tracked set / declared ignored set (TF-08)

**Chosen.** In a VCS tree the subject normalises to the tracked file set before the turn opens;
ignored paths become `recorded, not fatal`. Without VCS, the brief declares the ignored-pattern set
and the guard consumes it. Every ignored-path change is recorded either way.
**Rejected:** ignoring `__pycache__` by hardcoded pattern lists in the script. The pattern set is an
environment fact; declaring it in the brief (and reading it) keeps the guard honest in both worlds.

## D3 — intra-turn sampling (TF-09)

**Chosen.** A bounded background digest sampler during the turn; any intra-turn write (even one
restored before the end comparison) is recorded and the outcome becomes
`CLEAN_WITH_INTRATURN_WRITES`. The end-state comparison stays as the final verdict gate.
**Rejected:** a read-only mount / deny ACE. It is stronger but requires filesystem/OS control the
lane tooling does not have on this host; declared as a possible hardening later, not here.
**Rejected:** trusting the lane's own disclosure. The disclosure requirement stays in the brief (it
worked), but a control that depends on the subject's honesty is not a control.

## D4 — one output destination for re-runnable drivers (TF-07/TF-09, PIPD half)

**Chosen.** `--out-dir`/`DEST` on `probe_mutations.py`; a destination resolving inside a declared
guarded subject is refused with zero writes; the historical default survives only outside subjects.
**Rejected:** a "safe default" computed at runtime from the brief. The driver may run outside a lane;
an explicit flag is auditable, a computed default is neither stable nor attributable.

## D5 — nonce-carrier attribution (TF-06)

**Chosen (record-only here).** Additive per-attempt "surface probed" record beside
`nonce_absent_arms`. The root-cause fix of the wrapper/relay echo is a control-plane change and stays
owner-gated, as this proposal's NON-CLAIMS and Blocked items declare.
**Rejected:** treating the attribution record as the fix. AGENTS.md rule 7: a record is not a
verdict; rule: Promotion requires the owner gate.

## D6 — admission corrections (TF-02), owner-gated

**Chosen.** Full project-id digest for `taskspec_id` (collisions land as typed errors, not UNIQUE
failures); `base_head` resolved from the declared `target_root`; no taskspec insert before the
workorder field check passes. Implementation is BLOCKED on recorded owner authorisation — the spine
and lifecycle are control plane.
**Rejected:** correcting only the cwd/HEAD resolution. The id collision alone re-strands admission
the next time two projects share a mission.

## D7 — provenance convention for a non-VCS product tree (TF-03) and fixture honesty (TF-05)

**Chosen.** WriteSet + unified diff as standing convention (the R7-0 practice, already proven as a
writer receipt); suite-level `skip(reason)` when `r5-s4-candidate` is absent, so pre-existing
environment failures separate from change-induced ones.
**Rejected:** git-init the PIPD tree as the default. Requires the product owner / repo maintainer
and adds a VCS to a tree whose existing convention is already recorded and reproducible; kept as
the declared alternative.

## D8 — TF-04 as operating guidance only

The rendering redaction is a display artefact of the agent harness, outside this repo's authority.
Recorded as guidance ("read bytes before editing secret-adjacent lines"); no product change.

## Receipt / record deltas (additive only)

- Guard receipt: `ignored_*` rows; `intra_turn_violations[]`; outcome value
  `CLEAN_WITH_INTRATURN_WRITES`; per-attempt `nonce_carrier_surface` on nonce-absent attempts.
- Dispatch receipt: refusal code `ERR_LANE_REMOTE_WRITE_NOT_AUTHORIZED` now emitted only on
  context-matched markers; unchanged name, narrowed trigger.
- Driver: new `--out-dir`/`DEST` flags and typed refusal `ERR_DRIVER_DEST_INSIDE_GUARDED_SUBJECT`.

## Rollback

All deltas are additive code paths plus one narrowed refusal trigger. Revert is restoring the prior
script versions; no spine, config, registry, or authority mutation is involved (the TF-02 items are
owner-gated and unexecuted in this change).

## Non-claims

- A proposal is not an acceptance and changes no runtime behaviour by existing; every task here is
  unexecuted at proposal time.
- No claim that any finding is closed by this document; closure requires implementation, the
  declared deterministic tests, and an independent checker result per AGENTS.md.
- No claim about TF-06's relay/wrapper behaviour beyond what the recorded receipts show.
- Claim ceiling inherited from `R7_TOOLING_FINDINGS.json`: LOCAL observation, not a product defect
  verdict.
