## 1. Admission and research

- [x] 1.1 Admit the round through the typed Shared Spine API: `REQ-STRICT-DECLARATION-014` FROZEN v1, oracle fixed before the check, `ACC-STRICT-DECLARATION-014` = NOT_RUN, 2 TS/WO pairs (EXEC writer=codex, VERIFY writer=verifier)
- [x] 1.2 Record the write-set amendment as the **owner's grant** in the admission source locator (AGENTS.md's no-self-broadening rule preserved)
- [x] 1.3 FAR research `FAR-RUN-STRICT-DECLARATION-014` on the real harness (Q1 OQ11 adjudication, Q2 type discipline, Q3 carrier discipline, Q4 sweep), terminal `RESEARCH_PARTIAL`
- [x] 1.4 GSTACK named-method route check receipt
- [x] 1.5 KANBAN board `far-strict-declaration-20261011` + SWARM DAG (root + 4 workers + verifier + synthesizer)

## 2. Candidate pack (writer = codex, via the sealed EXECUTE lane)

- [ ] 2.1 S1: the resolver refuses a wrongly-typed declaration with a typed error instead of coercing rank/provider/model
- [ ] 2.2 S2: the dispatcher's raw-pool read applies the same exact typing (no `int()` coercion)
- [ ] 2.3 S3: a carrier counts only when it is a complete LF/CRLF-terminated, strictly UTF-8-decodable JSON object
- [ ] 2.4 S4: no regression of the previous frozen classification, the declared-capability skip/override, the lane-home isolation refusal
- [ ] 2.5 Scope: the writer touched only the four admitted files

## 3. Tests and probes

- [ ] 3.1 S1 positive/negative/boundary: well-typed pool loads; `1.9` / `"1"` / `true` / `null` rank and integer/boolean/null provider or model each raise the typed refusal
- [ ] 3.2 S2: a non-integer raw-pool rank is a typed refusal, not a coerced match
- [ ] 3.3 S3: unterminated / invalid-UTF-8 / U+2028-terminated carriers each fail to produce a success; a CRLF and an LF carrier both succeed
- [ ] 3.4 Permanent probes extended (P24-P28) so each false-green class cannot return unnoticed
- [ ] 3.5 The whole suite passes

## 4. Verification and closure

- [ ] 4.1 Maker-side gates: pytest + the declaration probes
- [ ] 4.2 Independent checker lane (VERIFY/SECURITY, `openai-codex/gpt-6.1-sol`) re-derives S1-S4 from the raw bytes; verdict + explicit UNVERIFIED items
- [ ] 4.3 Iterate: every new finding is FAR-researched and repaired, then re-checked
- [ ] 4.4 Freeze the round; evidence + claim ceiling recorded

## 5. Semi-closure definition (what "done except external acceptance" means here)

- [ ] 5.1 All actionable items, gaps and decisions closed locally
- [ ] 5.2 External acceptance explicitly NOT claimed: `ACC-STRICT-DECLARATION-014` stays NOT_RUN
- [ ] 5.3 Nothing promoted, no route change, no service restart, no credential operation
