# RESUME_HERE — R18 FHS-MSC Skeleton+Spine

Read in this order. Do not re-derive what is measured.

1. `FAR_R18_11_WHY_IT_STOPS.md` — why the round kept stopping and what replaced it (driver + cron).
2. `FAR_R18_10_CONCURRENT_SESSION_RECHECK.md` — the duplicate owner key and the diverged branches.
3. `FAR_R18_07_STOP_REVIEW_AND_OWNER_ENVELOPE.md` — the delegation design (T1/T2/T3).
4. `STATUS_HANDOFF.md` — measured results and ceilings.
5. `SESSION_STATE.json` — machine-readable state.

## Current facts (verified)

- ledger: {"DONE": 7, "PARTIAL": 11, "HOLD": 1, "PARKED": 7}
- owner delegation: `R18-CANON-6733b6bb`, canonical owner `412b3519…`, window `WIN-796b69117680`.
- gate: 7/7 POS permits, 6/6 NEG refusals (`receipts/DELEGATION_GATE_MATRIX_CANONICAL.json`).
- delivery: `candidate/r18-openspec-only` @ `b2159b09`, PR #4.
- unattended driver: `tools/r18_autodriver.py`, cron `2897733e2ca1` every 30m, gateway PID 23508.

## Do not do this again

- do not treat PARTIAL as terminal; that is what made the round look finished while 18 rows were open;
- do not create a second owner key: the canonical one is `~/.hgk-owner/owner.key.enc`;
- do not delete or force-push the other candidate branch — it diverges, it is not stale;
- do not present a signature over a payload as an Issuer PERMIT.
