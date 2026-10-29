# VERIFY brief — R20 closure round, second attempt (A1..A8, owner authorization, subset replay)

You are the independent VERIFY lane. You did not write any of this. Falsify it.

**You are in a READ-ONLY sandbox.** Do not attempt to create, write, or delete files — the write will be
refused, and that refusal is not a finding about the code. Deliver your JSON in your final message instead.

Windows long paths are OFF on this host: never `cd` into the package tree, never use `pathlib.rglob` there.

Repo under test (a git worktree, not the main checkout):

```
C:\Projects\Agent_Workspace\wt-r19-delivery   branch candidate/r19-fhs-implementation @ 96f0daa
C:\Projects\Agent_Workspace\wt-r20-subset     branch the subset branch @ 2d0b9f5 (PR #6, base main)
```

Run commands from the worktree root with `PYTHONPATH=src`. Anything needing a temporary directory or a
credential is HOLD for you — measure what reads and pure computation allow, and say plainly what you could
not execute.

## C1 — the two previously-uncollectable modules now import

Read `tests/test_native_boundaries.py` and `tests/test_r6_artifact_scope.py`. Both used
`import test_native_admission as fixture`; `tests/` is a package (it has `__init__.py`), so that import could
not resolve. The fix is a relative import with a direct-execution fallback.

Round 2 finding you raised: the `except ImportError: import test_native_admission` fallback could load a
DIFFERENT top-level module and mask a real failure. It is gone — the import is relative-only, so a broken
import fails loudly. Claim: no bare-name fallback remains anywhere in those two files (grep for it), and the
relative import is the only path. A `pytest --collect-only` you cannot run is HOLD, not PASS.

## C2 — receipts name their producer, and uncomparable receipts are refused

```bash
python tools/compare_lane_receipts.py \
  C:/Projects/Agent_Workspace/var/R20-FHS-20261029/receipts/VERIFY_LANE_R20_PASS2.json \
  C:/Projects/Agent_Workspace/var/R20-FHS-20261029/lane/far_verify2_stdout.json
```

Expect exit **4** with `ERR_PRODUCER_UNKNOWN`: both receipts predate the producer field. Then read the
dispatcher's `producer_identity()` and confirm a current receipt carries `producer.script_sha256` +
`producer.git_head`, and that `nonce_present_anywhere` / `nonce_in_agent_message` are separate fields with the
strict carrier still deciding `ok`.

## C3 — assignment drift is data, never a rewritten evidence file

```bash
python tools/config_drift.py --repo config/model-lane-assignment.json \
  --host C:/Projects/Agent_Workspace/HG-KSEOS/config/model-lane-assignment.json
```

The correct reading of its output (the previous attempt failed this claim because the brief named a key that
does not exist — the tool was right, the brief was wrong):

- `affects_issued_evidence` is `false`, and `lanes_with_identity_change` is `[]`;
- the drift **does** include `supply_selector`, `additional_routes` and `reasoning_effort` beyond
  `transport_model` — those are drift fields, not identity changes;
- `assigned_provider` / `assigned_model` / `authority` are identical on both sides.

Falsify the last point yourself with `python -c` and a direct comparison of the two JSON files.

## C4 — a declared fallback chain is representable and never merged into the primary

Round 3 finding you raised -- accepted in full: my test was a TAUTOLOGY. It passed identically for the
composed code and for a contaminating mutant, so it pinned nothing. `primary` is composed from the assigned
pair plus the declared transport model, and the invariant is now CHECKED AT RUNTIME: a role row that declares
the same arm as both primary and fallback is refused with `ERR_ASSIGNMENT_PRIMARY_FALLBACK_OVERLAP`. That is
the only shape in which the two lists can collide, and exactly the shape a contaminating implementation would
silently union into one list.

Round 4 finding you raised, accepted: the overlap check compared EXACT strings, so a case variant
(`OpenAI-Codex/GPT-6.1-SOL` vs `openai-codex/gpt-6.1-sol`) and a DECLARED ALIAS
(`desktop_router/gpt-6.1-sol` vs `openai-codex/gpt-6.1-sol`) both slipped through with `ok=true`. Overlap is
now decided with `arm_served_equivalent()`, the same equivalence the verdict uses, and both shapes are pinned
by tests. Claim: read `lane_assigned_arms()` and the four tests, and try to construct a row where the two
lists hold the same arm WITHOUT the refusal firing. Expect 10 tests in that file. Execution is HOLD.

## C5 — the 8 owner packets cover every residue exactly once

```bash
python tools/render_owner_requests.py \
  --archive "C:/Projects/Agent_Workspace/var/R20-FHS-20261029/build/FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision3.zip" \
  --check
```

Expect `packets=8 ids_across_packets=75 cells=46 stages=18 holds=11` and exit 0. Do the arithmetic yourself:
41 cells in OR-4..OR-7 plus 5 PERFORMANCE cells folded into OR-5 = 46; 18 stages in OR-1..OR-3; 11 holds in OR-8.

## C6 — the document's numbers are the receipts' numbers

```bash
python tools/evidence_reconcile.py --receipts C:/Projects/Agent_Workspace/var/R20-FHS-20261029/receipts \
  --doc evidence/R20-FHS-20261029/EVIDENCE_INDEX.md \
  --archive "C:/Projects/Agent_Workspace/var/R20-FHS-20261029/build/FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision3.zip"
```

Expect `checked=17 mismatches=0`. Without `--archive` the same command checks 13 (the four archive
measurements have no source) — that is why the flag is in the command this time. Then falsify the checker:
mutate one number in an in-memory copy of the doc and confirm it reports one mismatch and exits 3.

## C7 — `--require-arm` constrains the SELECTION, not just the verdict

Measured defects: a run naming `openai-codex/gpt-6.1-sol` without a rank override spent **350.27 s** on rank-1
`opencode-go/deepseek-v4.1-flash` and only then returned `ERR_REQUIRED_ARM_NOT_SERVED`; a later run that
selected and served the right arm through an alias was refused after **210.09 s** (TT-R20-17).

Read `selection_filter` in a current receipt and in the dispatcher source. Claim: `candidates_after` is exactly
the required arm (alias-equivalent), the filter runs before any spawn, and a required arm matching nothing
refuses with a typed code **pre-spawn**. Execution HOLD is acceptable; a claim that cannot be read out of the
source is FAIL.

## C8 — the owner authorization is a real owner act

Read `wt-r19-delivery/evidence/R20-FHS-20261029/owner_receipts/OWNER_AUTHORIZATION_R20.summary.json`.
Round 3 finding you raised: you could not read `~/.hgk-owner/window.json`, so C8 was a correct HOLD -- an
authorization nobody else can check is decorative. The this file now carries `body_json` verbatim AND
`owner_public_hex`, so it verifies from this committed file alone, with no key file. Check:

1. `payload_sha256` == sha256 of `body_json` (compute it).
2. `signature_hex` verifies under `owner_public_hex` over those same bytes (Ed25519) -- both are in
   this file, so the check is executable without any permission or key file.
3. `window_id` / `task_id` (`R20-FHS-CLOSURE`) / `owner_fingerprint` are consistent between the projection
   and `window_at_sign`, and `ops_used_at_signing` is 1.
4. `does_not_authorise` still lists OR-6 separation of duties and OR-8 external acceptance.

A signature that does not bind to the bytes it claims is decorative: FAIL it, naming which check broke.

## C9 — the full suite carries no failure introduced by this round

Author-side measurement to check, not to trust, at `ddaa679` with a clean tree:

```
74 failed / 732 passed / 0 errors
```

against `6086908` in `C:\Projects\Agent_Workspace\wt-r20-baseline`:

```
88 failed / 686 passed / 2 collection errors (22 tests could not even be collected there)
```

The 74 are a strict SUBSET of the 88 (set difference computed in code: 0 new ids, 14 previously-failing ones
now pass). An earlier brief of mine said 88/712 at the previous commit — that number was measured with a DIRTY
tree, which the `test_c2_case_run` allowlist reacts to. Treat the pair above as the claim.

Your job: read the commits' diffs for anything that could turn a green test red without appearing in the
failed-id set (a test that stops being collected counts), and say whether "subset" was measured or asserted.
Execution is HOLD for you.

## C10 — the subset replay is what it claims to be

Do not take a number from me: derive it.

```bash
python -c "import json;d=json.load(open('C:/Projects/Agent_Workspace/wt-r20-subset/SUBSET_MANIFEST.json',encoding='utf-8'));print(d['schema'],d['file_count'],d['files_listed'],d['synced_from_candidate'],len(d['deleted_not_applied']))"
cd C:/Projects/Agent_Workspace/wt-r20-subset && git -c core.quotepath=false diff --name-only origin/main HEAD | wc -l
```

For the blob ids, hash the WORKING TREE file (`git hash-object -- <path>`), not `HEAD:<path>` — an earlier
generation of this manifest hashed HEAD and recorded pre-sync blobs for the three files the same commit was
changing. `blob_source` inside the file states which one is now used.

Claim: `file_count` equals the measured diff count; `files_listed` equals `file_count - 1` with
`SUBSET_MANIFEST.json` as the only unlisted path; every listed blob id matches `HEAD:<path>`; both
`deleted_not_applied` documents still exist on the branch. Any inequality is a FAIL, whichever direction it
points — three earlier generations of this manifest were wrong in three different directions (last-sync count,
then self-exclusion), and each time the mismatch was the finding.

## C11 — the alias verdict cannot be widened by a model-name match

Round 2 finding you raised: `arm_equivalent('unlisted-provider/gpt-6.1-sol','gpt-6.1-sol')` is true through
the bare-model rule, so a BARE `--require-arm` could accept an undeclared provider. Selection keeps that
leniency (its pool entry already carries a provider); the VERDICT now uses `arm_served_equivalent()`, where
only an exact match or an owner-declared alias pair counts. Claim: `arm_served_equivalent` returns False for
the unlisted-provider/bare pair and True for the declared alias pair; the two tests in
`test_lane_assignment_fallbacks.py` pin both. Try to find a served label this would still accept without a
declaration — that is a FAIL.

## Output — in your FINAL MESSAGE only (no files)

```json
{"schema": "R20.CLOSURE_CHALLENGE/1", "nonce": "<the nonce you were given>",
 "claims": [{"id": "C1", "verdict": "PASS|HOLD|FAIL", "measured": "...", "what_you_did": "..."}],
 "overall": "PASS|HOLD|FAIL",
 "what_i_could_not_test": ["..."]}
```

No claim is PASS without something you actually ran or read in this session, and `measured` must quote a number
or a line from it. HOLD beats PASS when a claim is only true by construction.
