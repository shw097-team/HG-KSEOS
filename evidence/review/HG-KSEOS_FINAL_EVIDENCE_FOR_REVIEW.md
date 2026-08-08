# HG-KSEOS task-2 evidence for review

Status: `RESUMED_AFTER_AUTHORIZED_PATH_REBIND`  
Captured at: `2026-08-08T10:13:00+08:00`  
Claim ceiling: `IN_PROGRESS_NOT_A_DELIVERY_VERDICT`  
Production: `NOT_AUTHORIZED`

This is the single rolling evidence document required by `HG-KSEOS_CODEX_任務執行指令-2`. It is not yet a final delivery report and does not yet claim `HG-KSEOS_LOCAL_DELIVERY_PASS`.

Authorization received: the user explicitly authorized rebinding TaskSpec/project `maker_root` and `writable_roots` to the exact canonical root and closing `TT-HGK-WRITE-BINDING`. The four reviewed governance changes were applied; no broader authority was inferred.

## Frozen task and predecessor identity

- Task-2 file: `C:\Projects\Agent_Workspace\HG-KSEOS\任務執行指令\HG-KSEOS_CODEX_任務執行指令-2.md`
- Task-2 SHA-256: `95EF4750A92520321B8B66AF63D64F8A0AC9F739F810B216E721DA3CFC86930F`
- Reused predecessor candidate: `C:\Users\user\OneDrive\Documents\HLPE\work\HGK-CONSTRUCTION-AUTONOMOUS-BOOTSTRAP-001`
- Predecessor HEAD: `27396f7b306b485ad138ee624c5b7e231f99cb92`
- Predecessor status before materialization: clean

## Completed evidence

### G0 canonical filesystem binding

The exact root `C:\Projects\Agent_Workspace\HG-KSEOS` passed create, read, edit, rename, nested-write, readback, and delete operations with a uniquely named temporary canary. The canary directory was removed after verification. The root path resolved exactly and the scan found no reparse point in the target tree. Existing nested engineering repositories were inspected read-only and their dirty state was preserved.

Result: `G0_FILESYSTEM_PASS`.

### G1 control corpus and predecessor payload qualification

- Package index SHA-256: `A187C845915CC802ACC0DF34DFD3F6A647E20FA6F1BD6F51A63B61D7C9555E14`
- Group-07 SHA-256: `8A30CB146A3BE4ADE7D5BEE3BF17174D4C1B50452F3E23E5638D7568AC9F16E2`
- Materialized control manifest SHA-256: `6929efb2efd17f8534ef2f2c019a372a371c56023e0932138d84267b4164a52b`
- Control files checked: 60
- Source/candidate control mismatches: 0
- Control counts: 18 skills, 10 agents, 12 prompts, 8 workflows, 6 state machines

Result: `G1_CONTROL_BINDING_PASS`.

### G2 Codex execution surfaces

- Windows package: `OpenAI.Codex_26.803.5235.0_x64__2p2nqsd0c76g0`
- Bundled CLI version: `codex-cli 0.147.0-alpha.6.5`
- Bundled `codex.exe` SHA-256: `FB5C760E14CF8FE86E12E49E8A3E7F237AF06082D6B9FE1E411E463B7229C916`
- Authenticode: valid, signer `OpenAI OpCo, LLC`
- Authentication: `Logged in using ChatGPT`; doctor reported stored mode `chatgpt`, no stored API key
- Provider connectivity: WebSocket handshake `HTTP 101`; fixed-nonce provider smoke returned `HGK_CODEX_PROVIDER_SMOKE_PASS nonce=95EF4750`
- App-server schema smoke: 285 files, 2,921,262 bytes
- `codex-code-mode-host.exe` SHA-256: `E1DD9FA70FEE2BAD00671EB9EF0089CF86CD1A9765CB9A4160082514D7399B95`
- `codex-command-runner.exe` SHA-256: `5BFA04502BC8E2D0CB218A841AD91694AEC7AA52F0EBB446A80D8536360E3ED8`
- `codex-windows-sandbox-setup.exe` SHA-256: `59A71FCDF5DCDA0D3E277162439119FAC4B2A4A9DA9C5205B8DAB683C0A8FB7F`
- The same-version relay copies matched their source hashes and retained valid signatures.
- Canonical workspace-write smoke completed create, exact byte readback (`48474B5F434F4445585F574F524B53504143455F57524954455F504153530A`), delete, and final absence, returning `HGK_CODEX_WORKSPACE_WRITE_PASS`.
- Required compatibility condition: exclude the inaccessible `Microsoft\WindowsApps\pwsh.exe` alias from the CLI child process PATH so the sandbox uses system `powershell.exe`.
- Doctor had one non-runtime failure: `TERM=dumb` in the non-interactive evidence pipeline. It is not recorded as a full doctor PASS.

Official interpretation used for this evidence: the ChatGPT desktop app and Codex CLI are distinct local clients with their own sign-in surfaces; app-server is an experimental integration protocol, not the CLI itself. References: `https://learn.chatgpt.com/docs/auth`, `https://learn.chatgpt.com/docs/app-server`, and `https://learn.chatgpt.com/docs/developer-commands?surface=cli`.

### G4 predecessor materialization checkpoint

- Prior payload manifest SHA-256: `D6F190F7111346E58E8D2F01C52168BA11C80A1156831423A02963E4B6D0CB1F`
- Manifest rows: 352
- Source hash failures before copy: 0
- Target collisions before copy: 0
- Files copied create-new-only: 352
- Canonical readback mismatches: 0
- Frozen authority directories and nested engineering repositories were not modified or reset.
- `.gitignore` was extended to keep frozen top-level authority inputs and nested engineering repositories outside the future canonical implementation repository.

Result: `G4_MATERIALIZATION_PARTIAL`. Path governance has not been rebound and TST-092 is not closed.

## Resolved HITL checkpoint

The safety reviewer initially rejected the persistent governance patch that would:

1. change `plans/TASKSPEC-HGK-MASTER.yaml` from the HLPE companion maker root to `C:\Projects\Agent_Workspace\HG-KSEOS`;
2. change its writable root to the exact canonical root;
3. change `config/project.json` maker root to the exact canonical root; and
4. close `TT-HGK-WRITE-BINDING` using the passed G0 canary evidence.

The required explicit, informed user approval was subsequently received. The TaskSpec, project config, and TT ledger now bind only the exact canonical root. The prior rejected combined patch had not been partially applied.

## Work not completed

- Canonical TaskSpec/project path rebind and TT closure
- Canonical implementation Git initialization, branch, baseline commit, and isolated worktree
- G3 Hermes + Codex real provider loop and failure-path evidence
- G5 disposable real uninstall and 78 protected-provider final dispositions
- G6 case-specific 92/92 maker acceptance and independent checker acceptance
- TST-054 and TST-092 closure
- deterministic `scripts\hgk-final-gate.ps1`
- package regeneration, exact-set readback, final independent seal, clean final HEAD, and final delivery verdict

## Exact restart point

After authorization, apply only the reviewed canonical path-governance patch, verify the four changed records, then initialize the implementation repository while ignoring all frozen authority and nested engineering roots. Resume at G3 from that exact clean commit.

## User action status

Completed. The authorization did not permit broader writes to `C:\Projects`, source mutation, nested-repo reset, remote push, deployment, or production release.
