# RESUME_CHECKPOINT — FHS-MSC / PIPD-LS, 2026-11-01

Paste this file's "opening instruction" into a fresh session to continue without re-deriving anything.

## Opening instruction

> Continue `FHS-MSC_PIPD-LS-PKG`. Start from
> `HG-KSEOS/ops/session-20261031/FHS-ALLPASS-20261031/FINAL_ENGINEERING_REPORT.md` and `EVIDENCE_INDEX.json`.
> The queue stands at 19 PASS / 3 FAIL (WP-12, WP-13, WP-20). Do not re-measure WP-11 — it is closed with an
> independent 5/5 PASS. Take the three FAILs in the order below, one office per brief, and do not settle a WP to
> PASS on your own verdict: the checker that must say PASS is a VERIFY_SECURITY sitting through
> `scripts/run_ao_batch.py`.

## State as of this checkpoint

- **Queue**: 22 WP → 19 PASS / 3 FAIL / 0 pending. Rendered to `C:/wg/queue/TODO.md` and `GOAL.json`.
- **WP-11** PASS — `WP-FHS-11/NINE_CELL_TABLE.json`, 9 measured / 9 PASS / 0 carried; AO nonce
  `AO-WP-FHS-11-74EF001B`, `openai-codex/gpt-6.1-sol`, rank 1, 5/5 clauses.
- **WP-12** FAIL `RECOVERY_ENTRY_UNSTABLE` — the requirement is met (product runtime answers, E33 passes) but the
  *failure* of the recovery entry is not stable enough to claim: exit 1 (empty stdout), then a timeout, then exit 2.
- **WP-13** FAIL `C5_GRANT_NOT_BOUND_AT_EFFECT_TIME` — C1–C4 pass twice; the historical swap's grant postdates it
  and excludes its targets. The repair (`hotswap.py --grant`) is shipped and demonstrated POS and NEG.
- **WP-20** FAIL `CELLS_NOT_MEASURED` — 18 PASS / 12 surface-exists / 48 no-runner / 114 named NOFIT, all 192 named.
- **O-1** — 516 main-only files: 492 ADOPT, 24 RETIRE, 0 undecided.
- **E2E** — E33–E42: 6 PASS, 4 NOT_RUN with the absent object named.
- **TQAEP** — 24 planned tests, 0 executed, `live_acceptance: NOT_RUN`. DEV ECP and OPS ECP not re-measured.
- **Unpushed work**: HG-KSEOS `candidate/r18-fhs-skeleton-spine-20261029`; PIPD
  `candidate/wp13-grant-bound-hotswap`.

## Next three actions, in order

1. **WP-12, one measurement, not a fourth opinion.** Run the recovery entry five times with the same clean
   environment and record every outcome. If it is ≥3/5 a clean non-zero exit with empty stdout and no nonce, the
   clause becomes a statement about a stable defect and can be re-sat. If it stays mixed, the honest close is to
   retire the forwarder from PATH (host-owner action, one command) and re-measure the shim alone.
2. **WP-13 C5.** Re-run the ABI swap on the ABI fixture (`var/FHS-ALLPASS-20261031/wp13/target`, `abi-run/`) under a
   covering grant. `hotswap.py --grant` now refuses non-covering grants before any effect, so this is the first
   round in which that swap can be performed lawfully. Keep the refusal receipt beside the positive one.
3. **WP-20**, 12 cells: install a profile-shaped and a plugin-shaped artefact into
   `…/hermes/profiles/hgk-governed/{profiles,plugins}`, ask the loader, remove, ask again. Then either the owner
   accepts `NOFIT_NAMED` as a cell state for the seven surface-less Kinds or the matrix is scoped down.

## How to reproduce the measurements

```bash
cd C:/Projects/Agent_Workspace/HG-KSEOS
python scripts/wp11_hermes_cells.py                     # 3 Hermes cells (~45 s)
python scripts/wp11_host_cells.py --hosts CODEX,CLAUDE_CODE --profiles LITE,STANDARD,ASSURED   # 6 cells (~4 min)
python scripts/wp11_nine_cell_rollup.py                 # table, fail-closed, non-zero if a receipt is missing
python scripts/wp12_runtime_path_lab.py --json ops/session-20261031/FHS-ALLPASS-20261031/WP-FHS-12/RUNTIME_PATH_LAB.json
python scripts/wp12_maxpath_controlled_repro.py --json ops/session-20261031/FHS-ALLPASS-20261031/WP-FHS-12/MAXPATH_CONTROLLED_REPRO.json
python scripts/wp13_grant_bound_swap.py --json C:/Projects/Agent_Workspace/var/FHS-ALLPASS-20261031/wp13/HOTSWAP_GRANT_BOUND_RECEIPT.json
python scripts/wp20_surface_inventory.py --json ops/session-20261031/FHS-ALLPASS-20261031/WP-FHS-20/SURFACE_INVENTORY.json --tsv ops/session-20261031/FHS-ALLPASS-20261031/WP-FHS-20/SURFACE_INVENTORY.tsv
python scripts/e2e_w18_probe.py --json ops/session-20261031/FHS-ALLPASS-20261031/E2E_W18_E33_E42.json
python scripts/evidence_index.py                        # re-hash every cited artefact
python scripts/run_ao_batch.py --only WP-FHS-12 --timeout 600   # one office per brief, nonce echoed in the prompt
```

## Traps this round paid for — do not re-learn them

- `HERMES_HOME` must be the **profile** directory. Pointing it at the product root silently runs the `default`
  profile, loads no `hgk-governed` skill, and the turn hangs until the timeout.
- An agent markdown file under `~/.claude/agents/` is inert unless the command names it with `--agent`. Without
  that flag the cell measures nothing and the negative can even leak.
- `codex`/`claude` are `.cmd` shims on Windows; `subprocess` needs `shutil.which(name)` or it raises WinError 2,
  which reads like a missing host.
- A `\\?\`-prefixed copy is readable only with the same prefix; Python's importer does not use it. That asymmetry
  is what makes the 259/260 experiment conclusive — do not "fix" it.
- `shutil.rmtree(..., ignore_errors=True)` on a long-path tree silently leaves it behind, and a later
  `if not dst.exists()` then skips the copy and the test measures the wrong package. Remove the guard, copy always.
- A verdict built as `not any(checks.values())` inverts the meaning of every key. One polarity, stated once.
- The FAR brief must name the deliverable path explicitly: `lane_output/<kind>.md` is the transcript capture, and a
  lane that writes its work package there loses it.
