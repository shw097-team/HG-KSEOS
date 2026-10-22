## Why

The host carries `credential.helper = manager` in the **system-scope** git configuration
(`C:/Program Files/Git/etc/gitconfig`), installed as a Git for Windows default. Git consults
configured credential helpers before falling back to `GIT_ASKPASS`, so every git invocation that
needs authentication reaches Git Credential Manager (GCM 2.7.0). GCM's `credential.interactive`
**defaults to "permit interaction"**, so when the credential store cannot answer, GCM presents a
GUI account-selection window. Under an unattended long-running session nobody answers it, and the
git call blocks indefinitely.

The failure is not a one-off. Three measured properties make it recurrent:

1. **GCM's Windows credential cache masks it for hours.** Every push looks healthy until the first
   call that genuinely needs interaction. The defect therefore presents as a delayed, intermittent
   hang rather than a reproducible fault. A prior governed round recorded the mechanism verbatim:
   *"it is easy to miss because GCM answers from its cache for a while and every push looks fine
   until it does not."*
2. **Every existing remedy is an invocation-level opt-in.** A prior round lost
   `-c credential.helper=` while reconstructing a push by hand, "which opened the host's
   credential-manager Account chooser over an unattended lane". An in-tree `GIT_ASKPASS` shim was
   separately found not to work under native git (MSYS `.sh` path), so it is a dead remedy that a
   trusting session still relies on.
3. **There are four partial remedies on this host and zero defaults.** What is missing is not a
   mechanism; it is a default.

A second interactive surface was measured in this round: after a credential helper fails, git
falls back to its **own** prompt path (it attempts the askpass program and then the controlling
terminal). Neutralising GCM alone therefore leaves a prompt path open.

## What Changes

- **L1 (the only new artefact) — make the non-interactive posture the DEFAULT at user scope.**
  Add to `~/.gitconfig`:
  ```gitconfig
  [credential]
      helper =                    # empty value resets the accumulated helper list
      helper = manager --no-ui    # cached credentials still answer silently; no GUI
      interactive = false         # GCM must fail rather than wait for a non-existent user
  ```
  Measured and documented bases: git's own `gitcredentials(7)` states that an empty
  `credential.helper` "resets the helper list to empty (so you may override a helper set by a
  lower-priority config file)", and GCM's own documentation defines `credential.interactive` as
  *"Permit or disable GCM from interacting with the user (showing GUI or TTY prompts). If
  interaction is required but has been disabled, an error is returned … helpful when using GCM in
  headless and unattended environments … preferable to fail than to hang indefinitely waiting for
  a non-existent user."*
  The system-scope `manager` entry is **left untouched** (no admin action, and the human's
  interactive path is preserved), because the higher-priority reset already displaces it.
- **L2 — activate the already-admitted credential broker for the governed write lane.** The
  standing broker at `scripts/cred/` (admission `REQ-HGK-CREDBROKER-001`) already runs git with
  `GIT_CONFIG_NOSYSTEM=1`, a helper reset and `GIT_TERMINAL_PROMPT=0`, so its child process cannot
  reach GCM by construction. `INSTALL.md`/`ADMISSION_RECEIPT.md` state that activation is a
  separate, later, separately-admitted change; this change admits and wires that activation, and
  reports `NOT_ACTIVATED` rather than claiming it if the wiring cannot be shown.
- **L3 — ship the consumer, and close the second prompt surface.** A fail-closed preflight asserts
  the EFFECTIVE `credential.helper` resolution (not the candidate file's contents) and exits
  non-zero when the invariant is unsatisfied; the lane environment gains `GIT_TERMINAL_PROMPT=0`.
  Per the standing rule that a control is only a control if something consumes it, the caller is
  proven by a grep outside this change's own worktree, and a consumer with no caller is reported
  `DETECTION_ONLY`, never PASS.

## Impact

Affected: the user-scope git configuration on this host; new tooling under
`HG-KSEOS/scripts/gcm-containment/`; the round's evidence tree; the governed write lane's
invocation contract.
Not affected: the system-scope git configuration; the GCM installation or its version; provider or
model bindings; the sealed EXECUTE lane; the Shared Spine schema; any credential value (no secret
is read, printed, hashed or copied by this change); any repository remote.

Claim ceiling: `CANDIDATE_ONLY`. Local measurement is not independent acceptance, and applying a
host configuration is not a release. Residual, to be stated wherever L1 is claimed: L1 is
user-scope (it does not constrain other Windows users on a shared machine), and any explicit
override (`-c credential.helper=manager`, `GIT_CONFIG_SYSTEM`, `GIT_CONFIG_GLOBAL`,
`GIT_CONFIG_NOSYSTEM`) escapes it — which is precisely why L2 and L3 exist.
