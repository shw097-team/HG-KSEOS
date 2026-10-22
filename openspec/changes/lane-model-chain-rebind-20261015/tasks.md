## Tasks

### 1. Config changeset (candidate)
- [ ] 1.1 Update `config/lane-route-slots.candidate.json`: PLAN ordered_pool -> 1 openai-codex/gpt-6.1-sol (effort medium), 2 opencode-go/glm-5.3-flash, 3 opencode-go/deepseek-v4.1-flash (demote remaining optional arms below); VERIFY ordered_pool same; EXECUTE ordered_pool -> 1 opencode-go/deepseek-v4.1-flash, 2 openai-codex/gpt-6-luna, 3 nvidia/deepseek-ai/deepseek-v4.1-flash; keep role labels DEFAULT/FALLBACK1/FALLBACK2; keep per-arm measured/feasibility text; preserve prior chain as `previous_revision_*` records.
- [ ] 1.2 Update `config/model-lane-assignment.json`: assignment[PLAN].assigned_* -> openai-codex/gpt-6.1-sol (effort medium), assignment[VERIFY_SECURITY].supply_selector.unspecified_default/arms.A -> openai-codex/gpt-6.1-sol medium (arm B -> opencode-go/glm-5.3-flash, arm C -> opencode-go/deepseek-v4.1-flash); lane_chains order update matching 1.1; add authoritative note "rebind per owner order 2026-10-15, round FAR-LANE-ROUTE-REBIND-20261015"; bump registry_epoch -> 18 and revision -> 18.
- [ ] 1.3 Update `config/lane-routing-registry.yaml`: replace round_model_exclusions block with the NEW round scope (HGK-SOLUTION-APPLY-20261012 -> FAR-LANE-ROUTE-REBIND-20261015) and empty/purposeful exclusion set; refresh source_of_routes sha256 + revision 18; epoch 18; append history entry with rollback pointer.
- [ ] 1.4 .bak each touched config before writing; record digests in var/FAR-LANE-ROUTE-REBIND-20261015/sources/.

### 2. Readback + tests
- [ ] 2.1 `lane_policy.load_registry()` returns epoch 18 and projected routes matching 1.1/1.2/1.3; `check_exclusions` admits gpt-6.1-sol for the new round.
- [ ] 2.2 Update `tests/test_lane_policy.py` expected orders/epochs; add one test: resolver order == owner-declared chain (PLAN/VERIFY/EXECUTE).
- [ ] 2.3 Extend `scripts/runtime_role_binding_assert.py` mandate file schema with per-lane `chain` (ordered list); a declared arm must be IN its lane chain; tests OK (new negative case lives in tests/test_far_lane_fix_20261015.py pattern).

### 3. E2E lane turn receipts
- [ ] 3.1 EXECUTE lane turn (default DeepSeek, GO) — receipt ok:true, required==served.
- [ ] 3.2 VERIFY lane turn with a mandate naming fallback1 GLM — receipt ok:true, required==served.
- [ ] 3.3 PLAN not dispatchable via codex lanes; record Hermes session model readback in the round evidence instead (advisory).
- [ ] 3.4 (Blocked, owner-gated) EXECUTE fallback arms: nvidia requires relay-restart window; luna requires backend admission work — record as pre-existing limitation, not a new defect.

### 4. Governance
- [ ] 4.1 Manifest + digests in var/FAR-LANE-ROUTE-REBIND-20261015/.
- [ ] 4.2 Candidate -> owner review; acceptance NOT recorded by agents.
