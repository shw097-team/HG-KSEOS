RUN FAR-20261031-046-LANE-ROUTING-COMPLETE

Gate 1 - implementation: replace the bypassable FAR runner with a registry-bound three-lane chain that preserves full dispatcher receipts, binds run/question/subject digests, and stops on missing or invalid evidence.
Gate 2 - deterministic tests: prove complete pass plus missing lane, wrong arm, prompt-only nonce, missing usage, stale, changed subject, provisional, subset, and publication-bypass refusals with no model calls.
Gate 3 - independent check: re-derive the implementation and test evidence independently, then issue an advisory checker verdict. This task does not grant canonical acceptance or publication.
