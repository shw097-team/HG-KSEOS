# HGI Lane Enforcement Kit — adoption guide (CANDIDATE)

Round: **FAR-LANE-SOD-003**. Writer: Codex EXECUTE lane, model pin `opencode-go / deepseek-v4.1-flash`.
Round dir: `C:\projects\Agent_Workspace\HG-KSEOS\var\far-lane-sod-003`.

> **Boundary statement.** Nothing in the live Hermes install, `%LOCALAPPDATA%\HG-KSEOS\**`,
> `C:\Users\user\.codex\**`, the Shared Spine database, any acceptance receipt, or the canonical
> policy `config/model-lane-assignment.json` has been changed. Every artifact below is written
> **inside HG-KSEOS only** and is **CANDIDATE**. No credential value is written, echoed, or logged;
> credentials are referenced by environment-variable name only. There is no network call carrying
> credentials, no publishing, and no remote mutation. `claim_ceiling: CANDIDATE_ONLY`.

Interpreter used for every Python command: `C:\projects\Agent_Workspace\HG-KSEOS\.venv\Scripts\python.exe`
(Python 3.12.14). PowerShell component targets `pwsh` 7.6.5.

---

## 1. Component map

| # | Artifact | Role | Applied vs staged |
|---|---|---|---|
| 1 | `config/lane-routing-registry.yaml` | Single source of truth for routes, SoD, projections | Applied (candidate file); not read by any live process |
| 2 | `src/hg_kseos/lane_policy.py` | load / `project_policy` / `check_drift` / `check_sod` / `render_receipt` | Applied (candidate library) |
| 3 | `scripts/hgk-lane-policy.py` | CLI: `validate` / `generate` / `diff-live` / `epoch` | Applied (candidate CLI) |
| 4 | `scripts/hgk-lane-guard.py` | Pre-dispatch SoD/epoch/admission gate | Applied (candidate CLI); **not yet wired** into the dispatcher |
| 5 | `src/hg_kseos/lane_admission.py` | Admission record model + receipt writer | Applied (candidate library) |
| 6 | `scripts/probe-hgk-lane.py` | Lane-shaped admission probe (`--dry-run` offline) | Applied; live exercise **staged** |
| 7 | `scripts/hgk-artifact-gate.py` | Repaired gate checker (self-scan excluded) | Applied (candidate CLI) |
| 8 | `scripts/supervise-hgk-opencodex.ps1` | Relay supervisor (healthz + /v1/models, bounded restart) | Applied; scheduled task **staged** |
| 9 | `tests/test_lane_policy.py` | Conformance regression (3 methods, 42 subcases) | Applied (test) |
| 10 | `openspec/changes/lane-sod-enforcement/` | Brownfield change from D1–D25 | Applied (change doc) |

---

## 2. Exact commands

```powershell
$HGK = 'C:\projects\Agent_Workspace\HG-KSEOS'
$PY  = "$HGK\.venv\Scripts\python.exe"
Set-Location $HGK

# 1/2/3 — registry, library, policy CLI
& $PY scripts\hgk-lane-policy.py epoch
& $PY scripts\hgk-lane-policy.py validate          # exit 1 on fatal drift; 0 with debt-only warnings
& $PY scripts\hgk-lane-policy.py diff-live
& $PY scripts\hgk-lane-policy.py generate          # writes var\far-lane-sod-003\evidence\lane-policy-projected.json

# 4 — pre-dispatch guard (exit 0 admit / 2 SoD / 3 not admitted / 4 stale epoch)
& $PY scripts\hgk-lane-guard.py --lane VERIFY_SECURITY `
    --maker-engine codex-cli --maker-model deepseek-v4.1-flash `
    --target-engine hermes --target-model glm-5.3-flash --target-provider opencode-go `
    --admission var\far-lane-sod-003\evidence\lane-admission\VERIFY_SECURITY__opencode-go__glm-5.3-flash__hermes\receipt.json `
    --receipt var\far-lane-sod-003\evidence\guard.json

# 5/6 — lane-shaped admission probe (offline dry-run; never ADMITTED from a direct completion)
& $PY scripts\probe-hgk-lane.py --lane VERIFY_SECURITY --provider opencode-go `
    --model glm-5.3-flash --engine hermes --dry-run

# 7 — repaired artifact gate (requires --out and an input digest)
& $PY scripts\hgk-artifact-gate.py --workspace $HGK `
    --manifest var\far-lane-sod-003\evidence\gate_fixture\MANIFEST.json `
    --input-digest <digest-from-manifest> --out var\far-lane-sod-003\evidence\gate_check.json

# 8 — relay supervisor (pwsh 7 only)
pwsh -NoProfile -File scripts\supervise-hgk-opencodex.ps1 -Action Verify
pwsh -NoProfile -File scripts\supervise-hgk-opencodex.ps1 -Action Run -MaxRestarts 3 -WindowSeconds 300

# 9 — conformance regression
& $PY -m unittest tests.test_lane_policy -v
& $PY tests\test_lane_policy.py --self-test      # runs from a copied policy root under the scratch dir

# 10 — OpenSpec validation
openspec validate lane-sod-enforcement --strict
```

---

## 3. Integration points in the live systems

Each row names the live file, symbol, line reference at the time of this round, and the **minimal
diff intent**. None of these edits is performed by this kit; they are staged for an admitted
engineering-base change.

### 3.1 Per-lane dispatch override (closes D2, D5, D6)

- File: `C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent\hermes_cli\kanban_db_dispatch.py`
- Symbol: `_worker_argv` (line 2676); the model/provider override is applied at lines 2694–2699
  (`if task.model_override: cmd.extend(["-m", task.model_override])`, `if task.provider_override: cmd.extend(["--provider", task.provider_override])`).
- Minimal diff intent: before extending `cmd`, call the guard — resolve the task's lane role from
  its WorkOrder/TaskSpec metadata, then `hgk-lane-guard.py` with the resolved target arm and the
  task's admission. On a non-zero exit, do not spawn; record the guard verdict on the card. Also
  make the override mandatory for a lane card so a card cannot fall through to the profile default.
- This is the surface that makes routing survive restart instead of relying on a global pin.

### 3.2 Sealed launcher (EXECUTE) (closes D8)

- File: `C:\projects\Agent_Workspace\HG-KSEOS\scripts\start-hgk-hermes.ps1`
- Symbol: the `Write` action branch (sealed Codex CLI chain). It already pins `-ModelChain` and
  asserts `write_model_used`.
- Minimal diff intent: at the top of the `Write` branch, resolve the registry EXECUTE route and
  refuse if `$ModelChain` is not exactly the single sanctioned model; refuse if the guard verdict
  for `lane=EXECUTE` is not ADMIT. Do not add any out-of-lane fallback arm.

### 3.3 Global fallback + aux fallback (closes D3, D4)

- File: `agent\auxiliary_client.py`
- Symbols: `_plan_fallback_candidate` (line 3977) and the fallback-label selection at line 4434
  (`label = f"fallback_providers[{i}]({fb_provider})"`); module doc note at line 4412 states
  `fallback_providers` keeps the main agent's order.
- Minimal diff intent: gate the fallback path so a governed call may only fall back within the
  registry's declared arms for its own lane (all empty in this candidate). A checker lane must
  never fall back onto an executor model.

### 3.4 Delegation children / PLAN lane (closes D2)

- File: `tools\delegate_tool.py`
- Symbols: `_build_children` (line 365), `delegate_task` (line 440).
- Minimal diff intent: when building children, require the lane role to come from the trusted
  ExecutionBinding/TaskSpec, not a prompt keyword; refuse an unknown role and refuse a child whose
  resolved route is not the registry route for its lane. A VERIFY child must carry the checker arm
  explicitly, never inherit the maker's override.

### 3.5 Codex app-server runtime (closes D19, F8)

- File: `hermes_cli\runtime_provider.py`
- Symbols: `_maybe_apply_codex_app_server_runtime` (line 277), gate at line 284
  (`model_cfg.get("openai_runtime") ... != "codex_app_server"`), and the provider set at lines 95–96.
- Minimal diff intent: none required for correctness today — the binding already leaves
  `model.openai_runtime` unset, which is correct for `provider=opencode-go`. Keep it unset; do not
  reintroduce it. This integration point is documented so a future change does not silently switch
  the runtime and break SoD.

### 3.6 Live runtime config (observation only) (closes D9, D13)

- File: `C:\Users\user\AppData\Local\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\config.yaml`
- Lines: `delegation:` 162, `provider: openai-codex` 164, `model: gpt-6.1-sol` 165,
  `fallback_providers:` 219.
- Minimal diff intent: **none.** This is a shared application settings file consumed by
  non-governed workstreams. The registry records it as a non-authoritative observation, never a
  required match. The guarded dispatch path must not depend on it.

### 3.7 Canonical binding debt (closes D19)

- File: `config\hermes.json`
- Pointers: `/install_root`, `/canonical_hermes_home`, `/provider_route/model`.
- Minimal diff intent: an authorized generation should repoint these to the MSIX install
  (`...\Packages\OpenAI.Codex_2p2nqsd0c76g0\LocalCache\Local\hermes\hermes-agent`) and to
  `deepseek-v4.1-flash`. Until then they are recorded as `PROJECTION_DEBT` (warn), never a PASS.

### 3.8 Live dispatch config binding (RB-1/RB-4)

- File: `config\model-lane-assignment.json` — **read-only** for this round. The registry adopts its
  `sod` block and pins its revision-8 bytes (`sha256 e9480d1eb8cc10bf…`). No edit.

---

## 4. Rollback per component

- **Registry + libraries + CLIs + test + OpenSpec change:** delete the new candidate files. Nothing
  in the live runtime imports them, so removal restores the pre-change tree with no compensating
  write. (Exact paths are listed in §1 and in the receipt.)
- **Guard wiring (staged):** if ever applied to `kanban_db_dispatch.py:2676`, revert by restoring the
  recorded preimage of that single file; dispatch then behaves as before.
- **Launcher edit (staged):** restore the recorded preimage of `start-hgk-hermes.ps1`.
- **Fallback gate (staged):** restore the recorded preimage of `agent\auxiliary_client.py`.
- **Supervisor (staged scheduled task):** remove the task `HGK-OpenCodex-Sealed-10101`; the
  supervisor only ever starts `scripts\start-hgk-hermes.ps1 -Action StartOpenCodex`, so no other
  process tree is affected.
- No rollback entry in the Shared Spine is required because no canonical mutation was performed.

---

## 5. Residual risks

1. **Model attribution is runtime provenance, not weight attestation (U7).** The probe reads the
   runtime log line; it does not cryptographically attest provider-internal weights.
2. **Windows checker containment is unqualified (U2).** A durable process-tree write-deny primitive
   for the checker is not proven here; containment claims stay BLOCKED until measured.
3. **Live lane-shaped admission is staged, not run.** A non-dry `probe-hgk-lane.py` would dispatch
   through the sealed lane; it therefore fails closed (UNPROVEN/REFUSED) without an admitted binding.
4. **Relay child-model enforcement is unproven (U3).** The relay `selectedModels` list is not an
   allowlist gate; the chain pin is the compensating control and a request-boundary guard is still
   required for full enforcement.
5. **Provider separation does not hold and is not claimed.** EXECUTE and VERIFY share
   `opencode-go`; only the model axis separates them.
6. **`config/hermes.json` debt (D19)** remains until an authorized generation migrates it.
7. **Contract denominator (D24) and named adapters (D25)** are only partially closed by this kit;
   this change documents the denominator it does check (42 sites) and ships the OpenSpec adapter.

---

## 6. What is applied vs only staged

**Applied (candidate, inside HG-KSEOS only):** the registry, both libraries, all five scripts, the
test, and the OpenSpec change — each verified by running it this round (raw output in
`var/far-lane-sod-003/evidence/EXECUTE_RECEIPT.json`).

**Only staged (documented, not written anywhere live):** every integration point in §3 — the
dispatcher guard call, the launcher refusal, the fallback gate, the delegation-role enforcement,
the `config/hermes.json` repoint, and the `HGK-OpenCodex-Sealed-10101` scheduled task.
