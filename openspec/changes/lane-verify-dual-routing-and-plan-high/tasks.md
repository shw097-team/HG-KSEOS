## 1. Admission (done before any write)

- [x] 1.1 Freeze `REQ-FAR-LANE-SOD-006` in the Shared Spine with one TaskSpec + WorkOrder per lane (`writer=codex` for EXECUTE)
- [x] 1.2 Create board `far-lane-sod-006` with the gate DAG ADMISSION→PLAN→EXECUTE→SWARM(A,B)→GATE→EVIDENCE and GSTACK/OPENSPEC + ACCEPTANCE
- [x] 1.3 Pin per-card `reasoning_effort` on the VERIFY/ACCEPTANCE cards (the compensating control for the PLAN HIGH default)

## 2. PLAN - FAR research

- [ ] 2.1 Q1: how `-HIGH` is expressed as a default, which surface makes it a default, and every declaration site it must reach
- [ ] 2.2 Q1: the per-model-vs-per-lane conflict and the only per-dispatch effort surface
- [ ] 2.3 Q3: the SoD verdict on the instruction as written (coherent clause vs conflicting clause)
- [ ] 2.4 Q2: the selection surface, the co-equal dual-arm encoding, the default-arm before/after, lane-shaped liveness of both arms
- [ ] 2.5 Q2: the maker/checker collision matrix and which pairs a pre-dispatch gate must refuse

## 3. EXECUTE - the tracked amendment (writer=codex, sealed lane)

- [ ] 3.1 `config/model-lane-assignment.json` → revision 10 (PLAN effort, VERIFY dual selector, `sod_conflicts`, effective wiring)
- [ ] 3.2 `config/lane-routing-registry.yaml` → epoch 10 (PLAN effort, VERIFY arms, projection bindings, declared conflict) with every comment preserved
- [ ] 3.3 Amendment receipt naming every byte changed, before/after sha256, and the raw check output

## 4. Live Hermes wiring

- [x] 4.1 `agent.reasoning_overrides = {"gpt-6.1-sol": "high"}` with a YAML-type read-back and a `resolve_reasoning_config` proof
- [x] 4.2 `delegation.provider/model = openai-codex/gpt-6.1-sol` (the unspecified default arm) with read-back
- [ ] 4.3 Record pre-image, post-image and the byte-exact rollback

## 5. SWARM - independent verification on BOTH arms

- [ ] 5.1 SWARM-A on `opencode-go/glm-5.3-flash` (medium): per-claim verdict on the PLAN findings and the amendment
- [ ] 5.2 SWARM-B on `openai-codex/gpt-6.1-sol` (medium): independent verdict on the same subjects, simultaneously proving the dual route is real
- [ ] 5.3 Record for each arm the served model/provider from the runtime log, not from the dispatch banner

## 6. GATE - automated detection and repair

- [ ] 6.1 Run the registry drift gate; zero `severity=error` findings is the exit condition
- [ ] 6.2 On any finding, repair the declaration (never the expectation) and re-run until clean
- [ ] 6.3 Record the raw gate output, the epoch, the checked-site count and the source digest

## 7. OPENSPEC / GSTACK route evidence

- [ ] 7.1 `openspec validate lane-verify-dual-routing-and-plan-high --strict`
- [ ] 7.2 GSTACK named-method route check: registry ACTIVE_SELECTED + route(flow) evidence for this round
- [ ] 7.3 Record, per surface, whether it was SELECTED or `NOT_SELECTED_WITH_REASON` (silent fallback prohibited)

## 8. Evidence freeze

- [ ] 8.1 Enumerate and hash every round artifact
- [ ] 8.2 Write the evidence manifest
- [ ] 8.3 Generate the single evidence MD LAST so it binds every digest
- [ ] 8.4 Mirror to the further roots and assert byte equality by re-hashing
- [ ] 8.5 `claim_ceiling: CANDIDATE_ONLY`; no acceptance, no promotion, no self-signature
