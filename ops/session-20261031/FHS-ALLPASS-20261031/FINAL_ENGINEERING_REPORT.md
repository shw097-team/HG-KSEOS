# FHS-MSC_PIPD-LS-PKG — final engineering report, round 2026-11-01

Scope: the remaining construction of `FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1`, executed from the single
thin prompt of 2026-11-01. Every claim below names an artefact in `EVIDENCE_INDEX.json` (20 items, all present,
each with its sha256). Where a claim could not be established, the item is `FAIL` with a named blocker and a
precise unblock — not a redefined success criterion.

## 1. Headline

| | before this round | after |
|---|---|---|
| work queue (22 WP) | 18 PASS / 4 FAIL | **19 PASS / 3 FAIL / 0 pending** |
| WP-11 nine cells | 6 PASS + 3 `LOADER_PASS_MODEL_HALF_UNMEASURED` | **9 measured this round, 9 PASS**, 0 carried |
| WP-12 runtime path | `RUNTIME_PATH_UNRESOLVED` | entry found and measured; blocker narrowed to the broken dependency install |
| WP-13 C1–C4 | unproven | **PASS in two independent sittings** |
| WP-13 C5 | unproven | FAIL (recorded), repair shipped and demonstrated |
| WP-20 | 18 PASS + 168 anonymous `NO_HOST_SURFACE` | 18 PASS + 12 surface-exists + 48 no-runner + **114 named NOFIT** |
| W18 E2E | not run | **6 PASS, 4 refused by name** |
| FAR three-lane | not run | 3 studies run through `far_round.py` → gate; 3 defects found and fixed |

The three FAILs are honest and each has a one-line unblock (§6). Nothing here is a 100% claim.

## 2. What the independent checkers did to this round

The round's most useful output is the list of things three separate VERIFY_SECURITY sittings refused. Each
refusal was a real defect in my own artefacts, and each was fixed rather than argued with:

| sitting | finding | fix |
|---|---|---|
| WP-11 #1 clause 3 | the receipt read `completed`/`api_calls` and then dropped them | receipt carries both, plus the usage path |
| WP-11 #1 clause 4 | the roll-up counted six carried rows as PASS without opening their receipts, and still said 9/9 with those receipts removed | three states, carried counted apart, **non-zero exit when a receipt it needs is missing** |
| WP-11 #2 clause 4 | four of the six carried `archive_prefix` values no longer match today's `PIPD/dist/prof-*/export_manifest.json` | all six re-measured this round; **no carried rows remain** |
| WP-12 #1 clause 2 | the negative's error line was scraped from a shared log and **predated the run by three minutes** | bound to the run's own streams, or not claimed |
| WP-12 #1 arithmetic | 222 characters reported for a 260-character target | `pkg.parents[2]`, not four `.parent` hops |
| WP-12 #2 clause 2 | the recorded command is not the entry `hermes` resolves to; equivalence not established | three arms in one clean environment |
| WP-13 #1 C5 | the grant was issued **100 s after** the swap and its writeset excluded the swap targets | see §4 |

FAR had its own two: the EXECUTE lane's work package was overwritten by the transcript capture (9,678 → 1,879
bytes, `execute.md` naming collision), and the repaired round produced a specification that deferred the decision
to a future executor. Both are brief-shape defects, both fixed in `far_round.py`; the third round produced a
decision document and its VERIFY lane failed the document on scope, which is a finding about the document, not
the harness.

## 3. WP-11 — nine cells, measured

`WP-FHS-11/NINE_CELL_TABLE.json` (sha256 in the index): denominator 9, **9 measured this round, 9 PASS, 0
carried, 0 unmeasured**. Per cell: install a probe carrying a fresh token and the profile's archive digest into
the host's own skill surface → ask the host for both in a clean cwd → remove the probe → ask again. A cell is PASS
only when the positive answer carries both facts and the negative carries neither.

- Hermes 3/3 (`hermes-cells/HERMES_CELL_*.json`), model `deepseek-v4.1-flash` / `opencode-go`, `completed: true`.
- Codex 3/3 (`host-cells/CODEX_CELL_*.json`), `codex exec`, current manifests.
- Claude Code 3/3 (`host-cells/CLAUDE_CODE_CELL_*.json`). These only pass once the agent file is loaded with
  `--agent`, which is also why the previous round's generic receipts never measured a profile: an agent markdown
  file is inert unless it is named.

Independent acceptance: AO sitting 3, nonce `AO-WP-FHS-11-74EF001B`, served `openai-codex/gpt-6.1-sol` (rank 1,
usage receipt ok), **5/5 clauses PASS**.

## 4. WP-13 — the swap that could not have been authorised

C1–C4 PASS in two independent sittings: the ABI consumer resolves per call, CONTROL shows v1 before, POS shows v2
after through the consumer, NEG shows the old identity no longer served.

C5 FAIL, and the reason is structural rather than clerical: **`hotswap.py` had no way to accept a grant**, so
every swap it performed was unauthorised by construction, and the only grant in the tree was issued 100 s after
the effect with a writeset that named `abi.py` and `hotswap.py` — neither of them the target.

Repair (`PIPD/tools/hotswap.py`, branch `candidate/wp13-grant-bound-hotswap`):
- `--grant` binds **before any effect**; the signature is decided by the issuer's own verifier (no second opinion
  about what a valid signature is), and the consumer adds the half the issuer cannot know: does this grant name
  the file we are about to overwrite and the artefact we are about to install, and does it predate the effect.
- Refusal is demonstrated: the old grant produces `ERR_GRANT_NOT_BOUND` with three named problems
  (`GRANT_EXPIRED`, `GRANT_WRITESET_EXCLUDES_TARGET`, `GRANT_WRITESET_EXCLUDES_CANDIDATE`) and **nothing moves**
  (`HOTSWAP_REFUSED_NONCOVERING_GRANT.json`).
- The positive: a fresh fixture swapped under a covering grant, ten checks true, POS/NEG parity held
  (`HOTSWAP_GRANT_BOUND_RECEIPT.json`, nonce `WP13-BOUND-1793505697`).

A different fixture still cannot retro-authorise the earlier swap, and the third checker said so. WP-13 stays FAIL
with that sentence as its blocker.

## 5. WP-20 — 192 cells, no anonymous bucket

`WP-FHS-20/SURFACE_INVENTORY.json`: 192 cells, four states, every cell carrying a reason.

| state | n | meaning |
|---|---|---|
| `MEASURED_PASS` | 18 | AGENT_SKILL × {Hermes, Codex, Claude} × 3 modes × 2 providers, each with a removal negative |
| `SURFACE_EXISTS_NOT_RUN` | 12 | Hermes PROFILE and PLUGIN dirs exist; the Kind-shaped artefact was not installed this round |
| `NOT_RUN_NO_RUNNER` | 48 | DeepSeek Harness: no local runner on this machine |
| `NOFIT_NAMED` | 114 | no install surface for that Kind on that host, **with the absent object named** |

The previous 168-cell `NO_HOST_SURFACE` bucket is gone. No cell was promoted.

## 6. The three FAILs, with their unblocks

- **WP-FHS-12 `RECOVERY_ENTRY_UNSTABLE`** — the W18 requirement is met and measured (product runtime answered a
  nonce turn with pid, model and a completed usage file; the fresh-PID ordinary goal E33 passed; the PATH shim
  also answers clean). What cannot be established is the *failure* of `D:\Hermes-Recovery\live22\bin\hermes`:
  three samples gave exit 1 with empty stdout, then a timeout, then exit 2. Unblock: retire the forwarder from
  PATH (host owner) or repair the dependency install — 10 `openai` modules sit at or past 260 characters and 10
  extension modules are built for cp314 in a 3.11 runtime.
- **WP-FHS-13 `C5_GRANT_NOT_BOUND_AT_EFFECT_TIME`** — re-run the ABI swap on the ABI fixture under a covering
  grant (now possible), or have the owner record the earlier effect as unauthorised-but-superseded.
- **WP-FHS-20 `CELLS_NOT_MEASURED`** — exercise the 12 existing-surface cells; accept or scope the 7 Kinds that
  have no install surface on any host here.

## 7. O-1 — the 516 main-only files

`O1_MAIN_ONLY_CLASSIFICATION.json`: `origin/main` and `HEAD` have no merge base (unrelated histories), 746 vs 2160
files, 230 common paths, **516 main-only**. Content-first classification: **492 ADOPT, 24 RETIRE, 0 undecided**,
with per-file reasons. No graft, no force push, no unauthorised main push.

## 8. Completion by item group — measured, not estimated

The previous round's `86.4% / 64% / 69% / 53% / 44%` were estimates. This round did not spend its budget on
re-measuring DEV ECP and OPS ECP, so those two are reported as **not re-measured**, and the old percentages are
**withheld rather than restated**.

| group | denominator | measured this round | note |
|---|---|---|---|
| DEV ECP | per PD-06 write set | not re-measured | the round's engineering change is the `hotswap.py` grant binding, shipped with its own POS/NEG |
| OPS ECP | 32 sub-contracts | not re-measured | requires a live Host/Issuer round; nothing here was signed on its behalf |
| TQAEP | 24 planned tests in `PlannedTQAEP.json` (the delivery's larger 120+124+38 inventory is a different denominator) | **0 of 24 executed** — every test carries `oracle_ref` and both POS/NEG fixtures, none carries a runner, and the package's own state is `PLANNED` / `DESIGN_CANDIDATE` / `live_acceptance: NOT_RUN` | a `TQAEP_DESIGNED` declaration is not an acceptance, and this report does not treat it as one |

## 9. Native E2E, W18 E33–E42

`E2E_W18_E33_E42.json`: **6 PASS, 4 NOT_RUN**, each NOT_RUN naming the absent object rather than a category.

- E33 PASS — fresh PID, ordinary 162-character goal, no B1 prompt, no lane chosen by hand.
- E34 PASS — PLAN lane served `openai-codex/gpt-6.1-sol` where required, rank 1, nonce present.
- E36 PASS — VERIFY_SECURITY served a different principal from the maker (`opencode-go/deepseek-v4.1-flash`).
- E37 PASS — every model used was enabled in the live config at the time of use.
- E41 PASS — no owner question was asked in an unattended turn; the KnownAnswer ledger is absent on this host,
  which is recorded rather than papered over.
- E42 PASS — 19 queue rows PASS while 3 stay blocked: unrelated READY work did advance beside the HOLDs.
- E35, E38, E39, E40 NOT_RUN — no HGK WorkID bound to the EXECUTE brief; no journal intent for a crash/restart;
  no SourceFreeze to drift; no world effect returning `UNKNOWN_EFFECT`.

## 10. Availability of FHS-MSC

Portable host dogfood (WP-11) is available on three hosts with nine measured cells and an independent PASS. The
W18 normal mode (WP-12) is available through the product runtime and the PATH shim, with a hole in the recovery
entry that this round measured three different ways and did not smooth over. CAP-on-demand with hot swap (WP-13)
is available **only** under a covering grant from today: the tool that performs the swap can now refuse, which is
the property that was missing. The Kind matrix (WP-20) is available for agent skills on three hosts and for
nothing else, and now says so cell by cell.
