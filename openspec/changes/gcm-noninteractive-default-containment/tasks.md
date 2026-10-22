## 0. How to read this file (revised twice this session)

> **Revision note 1 — round `HGK-GCM-REPAIR-20261013`.** The checkboxes below were backfilled ONLY
> where in-repo evidence exists; every tick carries a one-line evidence reference (path + what it
> shows). Items that were never performed, or that require L2 activation / a collision-free
> measurement / an unviolated authorization cap, are kept as explicit `[ ] NOT DONE`.
>
> **Revision note 2 — round `HGK-GCM-REPAIR2-20261013` (nonce `REPAIR2-C-5a94`).** This file was
> revised a **second** time to reflect the true state after the two repair rounds. Revision 1 was
> the REPAIR-1 backfill; revision 2 (here) adds the repair-round items and their evidence (§7–§8),
> records the REPAIR-1 `FAIL` verdict as still on record, and states plainly where the session
> still failed. **Nothing was ticked that cannot be pointed to; no `[ ] NOT DONE` was silently
> converted to a tick.** The L2 activation, the collision-free measurement, and the positive control
> remain `[ ] NOT DONE`.
>
> `is_acceptance` is **false** for every round; the project is **NOT** complete and stays
> `EXECUTING`.

## 1. Research, admission and surface enablement

- [x] 1.1 FAR Gate-1 research run: re-survey the CURRENT on-disk assets (system gitconfig, the GCM binary, `scripts/cred/`, the askpass shim, the skill's `push_branch.sh`), the callable skills, and the vendor/open-source documentation; produce `plan/FAR_GATE1_RESEARCH.json` with the option matrix and the challenge block — evidence: `var/hgk-gcm-containment-20261013/plan/FAR_GATE1_RESEARCH.json` (option matrix + challenge block present).
- [x] 1.2 Run the deterministic, model-free seams and record raw output: S1 (`credential.helper` reset displaces a lower-priority helper) and S2 (git's own prompt fallback below the helper layer) — evidence: `var/hgk-gcm-containment-20261013/execute/artifacts/seam_probe.json` and `win_selftest.jsonl` (S1 reset + S2 fallback observations).
- [x] 1.3 Admit the change through the typed Shared Spine API (project `HGK-CHU-20261009`, requirement frozen before the check, TaskSpec/WorkOrder, writer=codex) — evidence: `var/hgk-gcm-apply-20261013/admission/hgk_gcm_apply_admission.json` (requirement FROZEN, errors 0; amendment added). REPAIR2 re-admitted under `REQ-HGK-GCM-REPAIR2-001` — evidence: `var/hgk-gcm-repair2-20261013/admission/hgk_gcm_repair2_admission.json` (state FROZEN, errors 0).
- [x] 1.4 GSTACK named-method route check: read `named_methods.py` fresh, record the ACTIVE_SELECTED set and the `route(flow)` decisions to `evidence/GSTACK_ROUTE_RESOLUTION.json` — evidence: `var/hgk-gcm-apply-20261013/evidence/GSTACK_ROUTE_RESOLUTION.json` (ACTIVE_SELECTED count 8, route decisions).
- [x] 1.5 OpenSpec change created and `openspec validate --strict` passes — evidence (this session): ran `openspec validate gcm-noninteractive-default-containment --strict` -> output `Change 'gcm-noninteractive-default-containment' is valid`, EXIT=0.
- [x] 1.6 KANBAN board created and the SWARM graph materialised; write the returned root/worker/verifier/synthesizer ids to disk (an id that lives only in the transcript cannot be re-verified) — evidence: `var/hgk-gcm-containment-20261013/evidence/KANBAN_SWARM_EVIDENCE.json` (root `t_c58b2a09`, workers, verifier `t_4b92a9c8`, synthesizer `t_5609c47e`). NOTE: the verifier/synthesizer cards are left open and are SUPERSEDED by this repair round, not retro-closed.

## 2. L1 — the non-interactive default (the only new artefact)

- [x] 2.1 Capture the `~/.gitconfig` preimage (bytes or a recorded ABSENT) with sha256 before any change — evidence: `var/hgk-gcm-apply-20261013/execute/artifacts/X1_preimage.json` (87 B, sha256 `34781bc5...`).
- [x] 2.2 Author the applier with the seven required properties: dry-run default, full-digest preimage guard, per-run timestamped backup, post-write verification, receipt, rollback, and no key deletion (append-only) — evidence: `scripts/gcm-containment/apply_gitconfig_default.py` (all seven properties present in the applier).
- [x] 2.3 `--apply` adds exactly the `[credential]` block: an empty `helper` reset, `helper = manager --no-ui`, and `interactive = false`; the system-scope `manager` entry is untouched — evidence: `var/hgk-gcm-apply-20261013/execute/artifacts/X1_apply_receipt.json` (`block_added` = the 3-line credential block; system entry untouched). Live re-read this round: `C:/Users/user/.gitconfig` sha256 `3a2d8f61...`, 158 B, carries the 3-line block; system scope mtime `2026-02-12` (untouched).
- [x] 2.4 Verify by EFFECTIVE resolution (`git config --show-origin --get-all credential.helper` plus a request-level probe), not by reading the candidate file's own contents — evidence: `var/hgk-gcm-apply-20261013/execute/artifacts/X1_effective_resolution.json` (raw resolution + preflight PASS) and the request probe.
- [x] 2.5 `--rollback` restores the preimage byte-identically and prints before/after sha256 — evidence: `var/hgk-gcm-apply-20261013/execute/artifacts/X1_rollback_proof.json` (`3a2d8f...` -> `34781bc5...`, byte_identical_restore=true).

## 3. L2 — activate the already-admitted broker for the governed write lane

- [x] 3.1 Prove the broker's `NOT_ACTIVATED` state and the exact activation seam the lane actually calls — evidence: `var/hgk-gcm-apply-20261013/execute/artifacts/X4_l2_status.json` (measured_state NON_ACTIVATED; seam_exists_today=false).
- [x] 3.2 Wire the governed write lane's invocation to the broker, OR record `NOT_ACTIVATED` with the reason and the missing seam if the wiring is out of this change's authority — evidence: `var/hgk-gcm-apply-20261013/execute/artifacts/X4_l2_status.json` (the RECORDING branch is met: NON_ACTIVATED with reason + missing seam; the WIRE branch was out of authority and was NOT performed).
- [ ] NOT DONE — L2 activation / broker wiring (3.2 wire branch): never performed. The broker remains NON_ACTIVATED; there is no seam in the governed write lane to invoke it. REPAIR2 was forbidden to activate it and did not — evidence: `var/hgk-gcm-repair2-20261013/evidence/ROUND_LEDGER.json` (prohibition list) and `var/hgk-gcm-repair2-20261013/closure/SESSION_CLOSEOUT_20261013.md` §3.3.
- [x] 3.3 Prove the caller by grep OUTSIDE this change's own worktree — evidence: `var/hgk-gcm-apply-20261013/execute/artifacts/X4_l2_gitgrep_scripts_cred.txt` (0 executable references to the broker outside `scripts/cred/`).

## 4. L3 — the consumer and the second prompt surface

- [x] 4.1 Ship the fail-closed preflight that asserts the effective `credential.helper` resolution and exits non-zero when the invariant is unsatisfied (three-valued: PASS / FAIL / INCONCLUSIVE, with INCONCLUSIVE never counted as verification) — evidence: `scripts/gcm-containment/credential_preflight.py` + `X2_gate_broken_scratch.json` (FAIL/BLOCK exit 89), `X2_gate_inconclusive.json` (INCONCLUSIVE warn-continue), `X2_gate_good_scratch.json` (PASS/CONTINUE).
- [x] 4.2 Add `GIT_TERMINAL_PROMPT=0` to the lane environment so git's own prompt fallback (seam S2) is closed — evidence: `var/hgk-gcm-apply-20261013/execute/artifacts/X2_lane_env_readback.json` (child's own env read-back shows `git_terminal_prompt="0"`).
- [x] 4.3 Prove a real caller; a consumer with no caller is reported DETECTION_ONLY, never PASS — evidence: `var/hgk-gcm-apply-20261013/execute/artifacts/X2b_caller_proof.txt` + `config/hermes-codex-lane.json:155` (`lane_dispatch_script` wired). Classification: WIRED_ON_DECLARED_DISPATCH_PATH / NOT_INDEPENDENTLY_ENFORCED (checker V6) — NOT a flat DETECTION_ONLY, and NOT a claim that prompts are prevented.

## 5. Measurement — the only real oracle

- [x] 5.1 Author the host-measured instrument: sample visible windows and new console/GUI-hosting processes (`GitCredentialManager.UI` and the git child) over a bounded window — evidence: `scripts/gcm-containment/win_instrument.py` + `var/hgk-gcm-apply-20261013/execute/artifacts/X3_win_selftest.json` (instrument self-test).
- [x] 5.2 Instrument the PRE-fix state on a forced unauthenticated request, bounded by a hard timeout (this is the defect capture) — evidence (cited, NOT re-run this round): `var/hgk-gcm-containment-20261013/execute/artifacts/PRE_FIX_INSTRUMENTATION.json` (window observed over a 25.1 s bounded window).
- [x] 5.3 Instrument the POST-fix state on the same request: expect a fast typed failure, zero visible windows, zero GUI child processes — evidence: `var/hgk-gcm-apply-20261013/execute/artifacts/_collision_snapshot/X3_post_apply_measurement.json` (discriminative dev.azure.com run: 1.442 s, exit 128, 0 windows). CAVEAT: this is a RE-DESIGNATION of the snapshot copy; the top-level `X3_post_apply_measurement.json` is the `.invalid`-host run and is INCONCLUSIVE.
- [ ] NOT DONE — the collision-free post-fix measurement was never obtained. The round's post-fix runs collided (X3 and X3b wrote the same paths); the discriminative result survives only in the collision snapshot, not as an uninterrupted single-writer stream. Still open after REPAIR2 (the round issued 0 live requests) — evidence: `var/hgk-gcm-repair2-20261013/closure/SESSION_CLOSEOUT_20261013.md` §3.2/§3.3.
- [ ] NOT DONE — 5.4 Positive/no-over-reach control: a push satisfied from the credential store still succeeds silently, with unchanged behaviour. The prior round's control was DECLARATIVE / NOT_MEASURED_NO_SECRET_READ; a behavioural control would require reading a real credential, which is forbidden — evidence: `var/hgk-gcm-repair2-20261013/closure/SESSION_CLOSEOUT_20261013.md` §3.3.

## 6. Independent verification and close-out (original round)

- [x] 6.1 Dispatch an independent checker lane in a SEPARATE process on the frozen candidate, read-only, fail-closed, and require it to RE-DERIVE every decisive claim (re-run the seams, recompute the digests, re-grep the call sites) rather than restate the writer's report — evidence: `var/hgk-gcm-apply-20261013/verify/verdict/checker_verdict_20261013T053309Z.json` (separate process, read-only, rederived; verdict PARTIAL, is_acceptance:false).
- [x] 6.2 Record the owner-mandated EXECUTE/VERIFY same-model deviation, the named failure mode it hedges, and what is NOT claimed because of it — evidence: `var/hgk-gcm-apply-20261013/verify/verdict/checker_verdict_20261013T053309Z.json` (sod_axis_model NOT_SATISFIED_BY_OWNER_MANDATE; hedged_failure_mode: correlated blind spots).
- [x] 6.3 Freeze the round evidence: single evidence MD written LAST, mirrored byte-identically to the review roots, claim ceiling stated — evidence: `var/hgk-gcm-apply-20261013/closure/CONSOLIDATED_STATUS_20261013.md` (evidence mirror `4179978877147ff7...`, 14715 B, stated claim ceiling CANDIDATE_ONLY). NOTE (REPAIR2): the frozen CONSOLIDATED status carries a stale headline figure; it is superseded additively — see `var/hgk-gcm-repair2-20261013/closure/ADDENDUM_TO_CONSOLIDATED_STATUS.md` (the mirrored file is NOT edited; its sha256 is `13da4e3c...`, unchanged).
- [ ] NOT DONE — 6.4 Close out: kanban cards completed, checkpoint recorded, and every side effect disclosed. The apply board is 7/7 done, but the containment board's verifier/synthesizer cards remain ready/todo; those leftover items are SUPERSEDED by this repair round, NOT retro-closed.
- [ ] NOT DONE — authorization cap: the round-level live-measurement cap was violated (2 live credential requests issued vs. 1 authorized). Recorded as a carried round-level defect; not cured by this repair — evidence: `var/hgk-gcm-repair2-20261013/closure/SESSION_CLOSEOUT_20261013.md` §3.2 (APPLY-G10).

## 7. Repair of the checker's fail-open defects (rounds REPAIR-1 -> REPAIR2)

The containment checker's first repair (`HGK-GCM-REPAIR-20261013`) was itself checked by a
**different model** (`gpt-6.1-sol`, native OAuth) and returned **`FAIL`** — 5 HIGH, 2 MEDIUM, 2 LOW
defects `D1`–`D9`. That `FAIL` verdict **stays on record and is NOT superseded** — evidence:
`var/hgk-gcm-repair-20261013/verify/verdict/checker_verdict_20261013T070511Z.json` (`verdict: FAIL`,
`is_acceptance: false`). `HGK-GCM-REPAIR2-20261013` took up `D1`–`D7` as a bounded repair in two
writer lanes (`Z1`, `Z2`); each fix has a deterministic counterexample that fails on the preimage and
passes on the current file. The REPAIR2 checker runs a **same-model** lane (`sod_axis_model:
NOT_SATISFIED`, owner mandate) and therefore **cannot** supersede the different-model `FAIL`.

- [x] 7.1 D1 (HIGH) later/higher-precedence `credential.interactive` was ignored -> fail-open. Fixed: `resolve_interaction_effective()` resolves the effective value by scope precedence; a re-enable, a conflict at the deciding scope, or an unrankable scope yields UNKNOWN, never a proof of non-interaction — evidence: `var/hgk-gcm-repair2-20261013/execute/Z1_REPORT.md`; preimage `scripts/gcm-containment/assertions.py.bak-z1-20261013T073320Z` (`58c17212...`, 13846 B). Reproduction `D1` now returns `FAIL` (was `PASS`).
- [x] 7.2 D2 (HIGH) unvetted executable accepted by basename/family alone. Fixed: positive path+digest allow-list from the actually-installed helper; `C:/unvetted/manager.exe` now `FAIL`; the real installed `git-credential-manager.exe` still `PASS` — evidence: `Z1_REPORT.md`.
- [x] 7.3 D3 (HIGH) a FAILED `core.askPass` read became a safety PASS. Fixed: `read_context()` carries `askpass_ok`/`interactive_ok` outcomes; a failed read yields UNKNOWN -> whole context INCONCLUSIVE; an adjacent failed `credential.interactive` read was fixed the same way — evidence: `Z1_REPORT.md`.
- [x] 7.4 D4 (HIGH) authorization was reusable and never consumed by dispatch. Fixed: durable `:consumed` tombstone on the existing `leases` table; the dispatcher acquires before spawning and consumes after a successful spawn; a second dispatch refuses `ERR_AUTHORIZATION_ALREADY_CONSUMED` — evidence: `Z2_REPORT.md`; preimage `scripts/gcm-containment/authorization_claim.py.bak-z2-20261013T072923Z` (`79655ff7...`, 8615 B).
- [x] 7.5 D5 (HIGH) repair dispatch accepted a missing liveness proof (3 insufficient variants). Fixed: a real host pid-liveness check on a known pid is required; the three insufficient variants now REFUSE; a genuine prior-gone case still proceeds — evidence: `Z2_REPORT.md`.
- [x] 7.6 D6 (MED) a test relaxed to hide a real extraction defect. Fixed: `detect_publication_workorder("WorkOrder: WO-PUB-9")` -> `WO-PUB-9`; the boundary suite uses `assertEqual` again — evidence: `Z2_REPORT.md`; falsifier `var/hgk-gcm-repair-20261013/verify/test_relaxation.json` (`current_bytes` 20257 vs reconstructed original 20260).
- [x] 7.7 D7 (MED) a writer report claim was false as written. Fixed **additively**: `var/hgk-gcm-repair-20261013/execute/Y3_REPORT.md` §8 quotes the false sentence, names the falsifier, and gives byte evidence; the original sentence is preserved — evidence: `Z2_REPORT.md`; preimage `Y3_REPORT.md.bak-z2-20261013T072923Z` (`bb30aed1...`, 17027 B).
- [x] 7.8 D8 (LOW) uncontrolled `AttributeError` on a scalar `interactive`. Fixed: `classify()` returns a typed `ERR_CLASSIFY_BAD_ARGUMENT` INCONCLUSIVE dict; Z3 re-derived `classify([{'value':'manager'}], interactive='false')` -> typed INCONCLUSIVE dict — evidence: `Z1_REPORT.md`.
- [x] 7.9 D9 (LOW) non-mutation discipline described as enforcement. Corrected in REPAIR-1: `var/hgk-gcm-repair-20261013/evidence/ROUND_LEDGER.json` now records `danger-full-access` and states that non-mutation is evidenced only by the before/after subject hash. REPAIR2 confirms (this round's `$R/evidence/ROUND_LEDGER.json` carries the same); recorded additively in `$R/closure/ADDENDUM_TO_REPAIR-1_EVIDENCE.md` §A2 — evidence: `var/hgk-gcm-repair-20261013/evidence/ROUND_LEDGER.json`.
- [x] 7.10 Bounded suites re-run by Z3 (not quoted from the lane reports): `scripts/gcm-containment/tests/test_credential_preflight.py` -> **34 passed**; `scripts/gcm-containment/tests/test_authorization_boundary.py` -> **33 passed**; `tests/test_lane_dispatch_ao_guard.py` -> **136 passed** — evidence: `var/hgk-gcm-repair2-20261013/execute/Z1_REPORT.md`, `Z2_REPORT.md`, `$R/evidence/SCRIPT_DIGEST_INDEX.json`.
- [ ] NOT DONE — model-axis SoD is **NOT** satisfied in REPAIR2 (writer and checker both `opencode-go/deepseek-v4.1-flash`, owner mandate). The repair therefore carries a correlated-blind-spot caveat and the verdicts of this round cannot supersede the `gpt-6.1-sol` `FAIL` — evidence: `$R/evidence/ROUND_LEDGER.json` (`sod_axis_model: NOT_SATISFIED`).

## 8. Session close-out (round REPAIR2)

- [x] 8.1 Author the session close-out: every round + verdict, the claim ceiling, defect disposition, what stays open and who decides it, and the exact host state with the revert command — evidence: `var/hgk-gcm-repair2-20261013/closure/SESSION_CLOSEOUT_20261013.md`.
- [x] 8.2 Additive corrections to the two frozen/mirrored evidence documents (quoted + corrected, never edited) — evidence: `var/hgk-gcm-repair2-20261013/closure/ADDENDUM_TO_REPAIR-1_EVIDENCE.md` and `ADDENDUM_TO_CONSOLIDATED_STATUS.md` (both quote the superseded sentence; the mirrored files still hash `316a0b9e...` / `13da4e3c...`).
- [x] 8.3 Record every script this session changed with its current sha256/bytes/git state and its preimage (or an honest `preimage: null`) — evidence: `var/hgk-gcm-repair2-20261013/evidence/SCRIPT_DIGEST_INDEX.json` (schema `HGK-SCRIPT-DIGEST-INDEX/1`).
- [ ] NOT DONE — the close-out is a docs/data close-out only; it does **not** produce an independent different-model verdict on the REPAIR2 result. The `gpt-6.1-sol` FAIL remains the last different-model verdict; whether to re-run it on REPAIR2 is the owner's call — evidence: `SESSION_CLOSEOUT_20261013.md` §4.
- [ ] NOT DONE — no independent acceptance: `is_acceptance` is `false` for all rounds; the project stays `EXECUTING`; L2 remains `NON_ACTIVATED`; the collision-free measurement and the positive control were never obtained.
