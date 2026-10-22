## 1. FAR research and admission

- [x] 1.1 Admit the round through the typed Shared Spine API (`REQ-LANE-HEALTH-013` FROZEN v1, oracle fixed before the check, 2 TS/WO pairs: `TS/WO-LANE-HEALTH-013-EXEC` writer=codex, `TS/WO-LANE-HEALTH-013-VERIFY` writer=verifier)
- [x] 1.2 FAR research run `FAR-RUN-LANE-HEALTH-013` on the real harness (three channels + the runtime ledger), 24 KB + 24 memory rows in 9.52s, R0-R8 artifacts, synthesis with decisions D1-D4 and open questions OQ1-OQ3
- [x] 1.3 GSTACK named-method route check: 8 ACTIVE_SELECTED methods, 14 activation invariants all zero, review/security/release route GSTACK (`evidence/GSTACK_ROUTE_RESOLUTION.json`)
- [x] 1.4 KANBAN board `far-lane-health-repair-20261011` + SWARM graph (root `t_e6c5b9ec`, 4 workers, verifier `t_f611fb28`, synthesizer `t_91f2fd02`)

## 2. Candidate pack (writer = codex, via the sealed EXECUTE lane)

- [x] 2.1 D1: classify the receipt code at the single site; add `nonce_absent_arms` / `timed_out_arms`; keep the fallback
- [x] 2.2 D2a: complete the rank-2 declaration in both lanes with the measured state (artifact stays CANDIDATE, revision 7)
- [x] 2.3 D2b: skip declared-not-dispatchable arms with `_is_dispatchable()` before spawn, record `skipped_arms`, `--force-rank` overrides
- [x] 2.4 D3: fold the resolved home into the identity verdict; `ERR_LANE_HOME_NOT_ISOLATED`; `--allow-human-home-transport`; record `codex_home_is_declared_lane_home`
- [x] 2.5 D4: supersession record for the previous round's freeze (`evidence/review/FAR_LANE_HEALTH_REPAIR_20261011_SUPERSESSION_2026-10-11.json`)
- [x] 2.6 Scope check: the writer touched ONLY the three admitted files (measured: no file under `src/ scripts/ tests/ config/` other than the three has an mtime later than the writer's start)

## 3. Tests

- [x] 3.1 D1 positive: answered-without-nonce -> `ERR_NO_ARM_EMITTED_NONCE` + `nonce_absent_arms`
- [x] 3.2 D1 negative: all timeouts -> `ERR_ALL_ATTEMPTS_TIMED_OUT`, never the nonce code
- [x] 3.3 D1 boundary: another acceptable-turn failure -> the generic code is still emitted
- [x] 3.4 D2 positive: a declared not-dispatchable arm is skipped with zero attempts for that rank and a recorded reason
- [x] 3.5 D2 boundary: the same rank with `--force-rank` IS spawned
- [x] 3.6 D2 negative: a declared-dispatchable arm is not skipped
- [x] 3.7 D3 positive: non-isolated home without the flag -> exit 4, `ERR_LANE_HOME_NOT_ISOLATED`, zero attempts
- [x] 3.8 D3 negative: the same home WITH the flag proceeds and is recorded
- [x] 3.9 D3 boundary: the declared isolated lane home is never refused
- [x] 3.10 The suite `tests/test_lane_dispatch_ao_guard.py` passes as a whole: **47 passed** at pass 1, growing to **104 passed** by pass 6 (34 pre-existing)

## 4. Verification and closure

- [x] 4.1 Re-run the named acceptance commands on the writer's bytes (maker-side gate). Final: pytest **104 passed**; `probes/run_health_probes.py` **P1-P23, all PASS**
- [x] 4.2 Independent checker lane (VERIFY/SECURITY, `openai-codex/gpt-6.1-sol`) re-derives C1-C4 from the raw bytes — run **six** times over six successive candidate states: five FAIL, one no-verdict (provider content-policy refusal, disclosed). At pass 6: C1 (frozen classification) PASS, C2 PASS, C3 PASS, C4 PASS, C5/C6 UNVERIFIED, strict-evidence claim FAIL (K1-K5)
- [x] 4.3 Freeze the round (`var/far-lane-health-repair-20261011/FREEZE_MANIFEST.json`, 185 artifacts; the previous freeze is superseded, not rewritten)
- [x] 4.4 Evidence file + claim ceiling recorded (`evidence/FAR-LANE-HEALTH-REPAIR-20261011/`), no publication

## 5. The iterative repair loop (standing order: every new gap is FAR-researched and repaired)

- [x] 5.1 Pass 2 — F1-F5 (oracle's generic code, reason never null, home fields on every receipt, resolved home, blank nonce refuses) after checker FAIL 1
- [x] 5.2 Pass 3 — G1-G3 (nonce on preserved bytes, no manufactured text, empty guard root refuses) after checker FAIL 2
- [x] 5.3 Pass 4 — H1-H5 (byte-level nonce, strict status typing, shrunk-ledger refusal, per-root guard, typed refusal for a wrong-shaped carrier) after checker FAIL 3
- [x] 5.4 Pass 5 — I1-I3 (content-based rewrite detection, typed rejection for a wrong-shaped usage row, the frozen classification takes precedence) after checker FAIL 4
- [x] 5.5 Pass 6 — J1-J4 (strict decoding everywhere, only complete lines are evidence, exact typing, the requirement code-precedence table) **plus a whole-file sweep** after checker FAIL 5
- [x] 5.6 Every finding became a permanent probe (P1-P23); the false-green classes cannot return unnoticed

## 6. Open at closure (NOT done, recorded honestly)

- [ ] 6.1 **K1-K3** (in scope): an unterminated carrier, a non-strictly-UTF-8 carrier, and a U+2028-terminated carrier can each still produce a success
- [ ] 6.2 **K4-K5** (out of scope): the declaration is coerced by `int()`/`str()` in `src/hg_kseos/lane_route_resolver.py` — touching it needs an admitted write-set amendment (OQ11)
- [ ] 6.3 **C5/C6** UNVERIFIED; **OQ1-OQ11** open
- [ ] 6.4 The iteration was **stopped deliberately**: the same defect class was found by five consecutive independent reviews, which the owner's standing monitoring order treats as a repeated block requiring intervention rather than another pass
