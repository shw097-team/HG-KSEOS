# Advisory audit — three independent read-only processes

**What this is not.** It is not the VERIFY lane. That lane was dispatched (`VERIFY_SECURITY`, assigned arm
`openai-codex/gpt-6.1-sol`) and returned `ERR_LANE_ALL_ROUTES_EXHAUSTED` with an upstream `401` before any
model ran (`receipts/P5C_LANE_VERIFY_BLOCKED.json`). No verdict exists, nothing here closes a box in
`tasks.md`, and the claim ceiling stays `PIPD_CONSTRUCTION_HANDOFF_READY`.

**What it is.** Because the gate was blocked, three processes with no context from the writing session were
told to attack the work. They were right about most of what they hit. This file records which findings I
could reproduce, which I could not, and what changed — including two claims withdrawn from earlier commits
of this branch.

## What held up

| Finding | Re-measured here | Change |
|---|---|---|
| The seal published in the first push covered 17 body files and excluded 14 declared files (29,121,570 B) | Confirmed: the collector is `01_SUBSTANTIVE_BODY/*.md`, non-recursive | Seal withdrawn; **F-12**; replaced by `P7` |
| The declared BODY archive *is* reproducible, so "not reconstructible" was false | **Confirmed first-hand**: using the payload manifest's own partition and the pinned recipe, BODY rebuilds to 114 entries / 4,007,065 B / `5e722cfb…` — the declared digest exactly. EVIDENCE rebuilds to 797 entries / 25,909,480 B, 4,801 B short | Phase 2 rewritten; **F-01** restated as BODY PASS / EVIDENCE FAIL; the false sentence retracted |
| `EVIDENCE_INDEX` described `P1_PACKAGE_INTEGRITY_VERIFIED.json` as "PASS … independent re-derivation" | Confirmed: its own verdict is **FAIL**, with C/E/F/G/H failing and I skipped. Its `F` check is nonetheless the first evidence that the BODY digest was checkable | Row rewritten to FAIL, decisive for F-01 |
| `RUN/FUO.json` also differs, and by `elapsed_ms` only — which no path explains | Confirmed against `P2_FIRST_WORK_RUN.json` (four differing artefacts) and by inspection of the file | Report corrected to four; determinism now separates identity differences from the timing field |
| "2.31 s" probe latency appears in no receipt | Confirmed: `P5A` records `seconds: 7.2` | Replaced |
| Five cited artefacts were not in the tree (`lane_probe.out`, `lane_verify.out`, the dispatcher backup, the delivered `EXISTING_AFFECTED_TESTS_RAW.txt`, this file) | Confirmed: they existed in the round workspace and were never staged. This file did not exist yet when they looked | `stage_repo.py` now stages all of them; `logs/` and `package/` grew accordingly |
| The staging inventory never listed the five narrative documents | Confirmed — F-09's failure mode was still visible in the inventory built to catch it | Why the second commit exists; staging is subtree-scoped now, not `rmtree` |
| Finding counts disagreed (ten, eleven, eight) across three files | Confirmed | One count: fourteen numbered findings |
| `prepare.py` does not snapshot `fixtures`, so a clean rebuild stays 34/1 even after the import-order fix | **Accepted as reported** — I did not rebuild from scratch to confirm the two `FileNotFoundError`s, so it is recorded with that caveat | **F-13**; the 35/35 claim is now conditional |
| The delivery's 35/0 record shares `elapsed_seconds` with its 34/1 predecessor to sixteen digits | **Confirmed directly**: both files carry `1.0183297000003222`; this round's two runs measured 6.1035 s and 5.4547 s | **F-14**; a defect of the delivered package, not of this round |

## What they got wrong

- **"429 rows unresolved"** was flagged untraced. Correct — and worse than they knew: there is no such
  number. Re-measured from the manifest against the delivered tree: 446 plain `Path.exists()` misses, of
  which **31** are the book-directory rename and **415** resolve with the `\\?\` prefix (the 260-character
  Win32 limit). Every "429" in the findings and the report is gone — it survives only in this
  correction note; **F-02 / F-02b** carry the split.
- One auditor read the Phase 2 argument as an unbuildability proof from compression arithmetic. The archive
  is unbuildable for a different reason — the membership was wrong — and the arithmetic argument was a bad
  inference on top of a real gap. Both withdrawn; `P7` replaces them.
- The same auditor called the writer overrun "more than nine minutes" unsupported. It was eight and a half;
  F-11 now cites the rollout file and the termination time instead of a rounded feeling.

## Score

Nine findings reproduced and acted on, one accepted with a stated caveat, two rejected. The three that
mattered most — a seal that excluded 29 MB, a receipt labelled PASS whose own verdict was FAIL, and a false
"not reconstructible" inference — were mine, and all three were caught by processes with no reason to be
kind. That is what an advisory audit is worth. It is still not the lane that failed closed.
