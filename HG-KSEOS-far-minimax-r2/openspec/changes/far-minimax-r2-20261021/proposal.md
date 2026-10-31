# Rebind the three lanes to the re-issued owner order (MiniMax M3.1 Flash / DeepSeek V4.1 Flash)

## Why

The owner re-issued the model order for the three governed lanes on 2026-10-21:

| Lane | Target | Engine |
|---|---|---|
| PLAN | `opencode-go/minimax-m3.1-flash-free` (MiniMax M3.1 Flash, OPENCODE GO) | Hermes (internal orchestration plane) |
| EXECUTE | `opencode-go/deepseek-v4.1-flash` (DeepSeek V4.1 Flash, OPENCODE GO) | Codex CLI (bounded writer) |
| VERIFY_SECURITY | `opencode-go/minimax-m3.1-flash-free` (MiniMax M3.1 Flash, OPENCODE GO) | Codex CLI (Independent Acceptance Officer) |

This SUPERSEDES the 2026-10-21 order that put `openai-codex/gpt-6.1-sol` on PLAN and
VERIFY_SECURITY. The EXECUTE lane keeps DeepSeek V4.1 Flash, now by explicit order rather than
by omission.

## What changes

The order is written into four surfaces in one change set, and the pool remains the single
selection authority:

1. `config/lane-route-slots.candidate.json` - the dispatch-time pool. The target arm becomes
   rank 1 and the automatic selection; the demoted arm is RETAINED as a reachable fallback, so a
   future re-order is a rank reorder rather than a rebuild.
2. `config/lane-routing-registry.yaml` - the declaration (epoch 26 -> 27). Every route row is
   re-derived from the pool, including `arms[]`, `fallbacks[]`, `canonical_identity`,
   `selected_arm`, `selected_arm_identity`, `admission_status` and the route-level
   `auth`/`oauth`/`reasoning_effort` posture.
3. `config/model-lane-assignment.json` - the registry's `source_of_routes` and the SoD
   declarations, derived from the pool.
4. `AGENTS.md` - the owner chain.

Every prose field that names a rank-1 is updated in the same change: the pool's `declared_by`,
each lane's `selection_note`, `placement_rationale` and `change_log`, and the AGENTS.md owner
chain. An artifact whose prose contradicts its own data is a defect, not a style issue - the
previous pool shipped with every `selection_note` still naming the wrong rank-1.

## Separation of duties

The maker/checker pair is (EXECUTE, VERIFY_SECURITY): the writer runs DeepSeek V4.1 Flash and
the checker runs MiniMax M3.1 Flash, so that pair is model-distinct. The pair (PLAN,
VERIFY_SECURITY) is on ONE model, so that pair is NOT model-distinct. Both facts are declared;
neither is hidden behind a single global flag.

## What this change does NOT do

It does not accept anything, merge anything, release anything, or claim external acceptance.
Local green is not an acceptance.
