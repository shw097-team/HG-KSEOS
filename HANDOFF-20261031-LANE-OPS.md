# HANDOFF — 2026-10-31 (session 20261030_134733_756c82) → next session

Read this first. It states what is真, what is broken, and the exact next command.

## 1. Where the work stands

| Item | State |
|---|---|
| Registry (work_queue) | **16 PASS / 3 FAIL / 3 NOT_RUN** of 22 |
| FAIL | WP-FHS-10, WP-FHS-12, WP-FHS-13 |
| NOT_RUN | WP-FHS-11, WP-FHS-17, WP-FHS-20 |
| ALL PASS | **not reached** — do not report otherwise |
| HG-KSEOS HEAD | `dcba557` → this handoff commit (branch `candidate/r18-fhs-skeleton-spine-20261029`, **not** main) |

WP-20 evidence is the strongest of the three open units: 192/192 cells RAW
(`probe-all {"RAW":192}`, per host Hermes 48 · Codex 48 · Claude Code 48 · DeepSeek 48, `verify ALL_CELLS_EVIDENCED`),
raws in `C:\wg\queue\WP-FHS-20\output\cell-raws\` with `CELL_RAWS_PROVENANCE.md`. What it still lacks is the officer's
own **Reader ACK** and a production evidence verifier — that is what the 02:09 VOID named.

## 2. What this session actually fixed (each with the measurement that proves it)

1. **Console windows — three separate sources, all now measured at 0**
   - The guard `import winproc; winproc.install()` had been inserted *above* the module docstring in 7 files
     (`hgk-lane-dispatch.py`, `ops_status.py`, `stall_monitor.py`, `review_lock.py`, …). Text in a docstring never runs,
     so `install()` never executed. `scripts/console_guard_gate.py` now parses each entry point with `ast` and refuses
     `CONSOLE_GUARD_NOT_EXECUTED` (31/31 clean).
   - `DETACHED_PROCESS` is a window factory: a parent with no console hands a NEW console to every child. It was still
     live in `relay_daemon.py` and the retired `lane_watchdog.py`. The gate now refuses `DETACHED_PROCESS` anywhere in
     `scripts/` (`DETACHED_PROCESS_IS_A_WINDOW_FACTORY`).
   - The grandchildren: `CREATE_NO_WINDOW` leaves the child with **no** console, so the `git` that codex/node start each
     allocate one (measured 14 `git.EXE` windows in one tick, none started by us). `hgk-lane-dispatch.py` now starts the
     codex tree with `CREATE_NEW_CONSOLE` + `STARTUPINFO.wShowWindow=SW_HIDE`: one hidden console, inherited.
   - **Measured after**: 3 dispatches live for 10 minutes → **0 console-window events** (recorder `scripts/window_watch.py`
     alive, `var/console-window-events.jsonl`).
   - Boot-time `opencodex proxy … 10101` window: the Startup-folder `ocx-relay-start.cmd` is archived under
     `var/autostart-archive/`; the only launcher is `scripts/relay_daemon.py` (CREATE_NO_WINDOW). A `.cmd` in Startup is
     a visible console by construction.

2. **A timeout that could not end.** `subprocess.run(timeout=…)` kills only `codex.cmd` and then blocks forever on pipes
   held by `node`/`codex.exe`; a dispatch with `--timeout 180` was still alive at 300 s with no receipt.
   Now: `Popen` + `taskkill /T /F`, then drain → measured `exit: TIMEOUT` at 60 s, no orphans.

3. **A budget spent on refusals.** Gate refusals (`ERR_DURABLE_GATE_NO_GO`, "refused before spawn") were counted as maker
   rounds, so all three open units halted at `rounds: 6` without the maker ever running. Only a receipt that carries a
   spawn is a round now. Void guard counts only voids against the *current* subject.

4. **A loop that amplified itself.** One command produced ten live dispatches (each unit's `chain_next` started another
   tick) — the owner sees exactly that as "windows popping in a loop". `var/driver.lock` (pid + liveness) caps it at one
   tick; `chain_next` hands the lock over.

5. **Ghost locks.** `review_lock` matched its own PowerShell query (the nonce is in the command line of the process doing
   the asking), so 40 dead locks read ALIVE for ever and blocked every commit. Fixed by excluding the asker/shells and
   treating the nonce as the evidence, not the pid. `review_lock.py reap` clears the remainder.

6. **IR-4 had no subject to check.** `C:\wg\queue` was in **no git repository**, so every dispatch refused with
   `NO_REPO`. The queue is now a git worktree; the volatile status surface (`STATUS.json/.md`, `TODO.md`, `GOAL.json`,
   logs) is untracked so the tree can be clean, and receipts/verdicts are committed.

## 3. What is broken — read before dispatching anything

**The relay cannot serve the EXECUTE arm.** Through `127.0.0.1:10101`:

| Model | Result |
|---|---|
| `gpt-6.1-sol` (PLAN / VERIFY) | **works** — `chat completions` answered in 3.5 s (2026-10-31 09:49) |
| `opencode-go/deepseek-v4.1-flash` (EXECUTE) | **fails** — upstream 400 `MissingSessionID`: "Request is missing x-opencode-session" |

Why: the `openai` provider was `disabled: true` in `C:\Users\user\.opencodex\config.json` — that is why PLAN/VERIFY
could never serve; it is now `false` (config backup: `config.backup-20261031093326.json`). The `opencode-go` route fails
because ocx **2.11.0** does not send the session header the upstream now requires, and that header does not appear
anywhere in the 2.11.0 bundle.

Upgrading to **2.94.0 was tried and rolled back**: after the upgrade the proxy stayed in
`OpenCodex local native-main profile maintenance is active; retry this request` and even `gpt-6.1-sol` stopped answering.
It is back on 2.11.0, health 200, `gpt-6.1-sol` verified working again.

So: **EXECUTE dispatches will time out with `Connection failed: error sending request`** until the deepseek transport is
decided. Do not read that as a maker failure.

## 4. Exact resume steps

```bash
cd C:/Projects/Agent_Workspace/HG-KSEOS
python scripts/relay_daemon.py status          # expect RELAY_OK, health 200
python scripts/console_guard_gate.py --all     # expect 31/31, exit 0
python -c "import sys;sys.path.insert(0,'scripts');import continuation_driver as d;print('rounds', d.execute_rounds(__import__('pathlib').Path(r'C:/wg/queue/WP-FHS-17')))"
python scripts/review_lock.py reap             # clear any ghost lock before committing
python scripts/continuation_driver.py --once --parallel 3 --auto-record   # one tick, three units, at most one tick at a time
```

VERIFY the transport before blaming the loop:

```bash
curl -sS -m 30 -X POST http://127.0.0.1:10101/v1/chat/completions -H 'Content-Type: application/json' \
  -d '{"model":"gpt-6.1-sol","messages":[{"role":"user","content":"say ok"}],"max_tokens":8}'
```

## 5. Open decisions (need the owner, not the loop)

1. **How EXECUTE reaches `deepseek-v4.1-flash`.** Options: (a) upgrade ocx and wait out its profile maintenance,
   (b) keep a tiny local shim that adds `x-opencode-session` in front of `opencode.ai/zen/go`, (c) run EXECUTE on the
   `gpt-6.1-sol` arm as a declared exception. (a) and (b) keep the mandate; (c) does not. **Not decided by me.**
2. **WP-20's officer.** 192/192 cells are RAW; the VOID named Reader ACK and a production verifier. Someone has to sit
   as Reader and sign, or the unit cannot go PASS.
3. **The FAT FAR run** `FAR-HANDOFF-V1-LANE-OBLIGATION-AND-WINDOWS-20261031` currently reads `INVALID_RESEARCH` by its own
   gate (`scripts/far_lane_gate.py`) because its PLAN/VERIFY receipts do not exist yet — PLAN now has a working transport,
   so this is the cheapest next PASS in the whole set.

## 6. Artefacts of record

- `scripts/`: `console_guard_gate.py`, `far_lane_gate.py`, `window_watch.py`, `detach.py`, `relay_daemon.py`,
  `continuation_driver.py`, `hgk-lane-dispatch.py`, `review_lock.py`, `host_matrix.py`.
- Evidence: `var/console-window-events.jsonl` (window events, 20 ms `EnumWindows`), `C:\wg\queue\**\*.json` (receipts),
  `C:\wg\queue\WP-FHS-20\output\cell-raws\` (192 raws), `var/far/<run>/PLAN_RECEIPT.json` (refusals for the FAR PLAN).
- FAR synthesis: `Fabric/FABRIC/fabric-autonomous-research/runs/FAR-HANDOFF-V1-LANE-OBLIGATION-AND-WINDOWS-20261031/ResearchSynthesis.md`
  (explicitly marked `INVALID_RESEARCH` until its receipts land — that is the gate working, not a claim of completion).

## 7. Commits

```
dcba557 the locks outlived their holders, and the window source was a grandchild
ffb93d8 a timeout that cannot end, a budget spent on refusals, a void guard that counted history
de953d5 the console guard was text inside a docstring, so it never ran
b5dde8c four ways the loop judged the wrong thing
c016235 the frozen snapshot is created before it is copied into
```

## 8. Durability note for the next session

`var/shared-spine/hg-kseos.db` is **git-ignored**, so the TT rows written this session (two closed, two opened) exist
only on this disk. The authoritative copy of that reasoning is `HANDOFF-20261031-LANE-OPS.md` §3 and §5 — if the database
is ever rebuilt, re-insert from here rather than trusting the schema.
