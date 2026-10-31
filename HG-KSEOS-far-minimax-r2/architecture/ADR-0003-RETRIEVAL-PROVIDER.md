# ADR-0003: P0 retrieval provider

Status: Accepted for local P0 construction

SQLite FTS5 is the single active P0 retrieval core because it is native, local, reversible, and available through the qualified Python SQLite library. Qdrant, Chroma, pgvector, Milvus, and other same-slot providers remain deferred or standby until a source-defined scale trigger and comparative pilot justify activation.

The FTS index, graph projection, and memory retrieval views are derived. Source withdrawal must remove affected derived records; rebuild must reproduce the same canonical source identities and citation anchors. Unsupported queries must abstain rather than fabricate grounding.

Rollback: drop and rebuild derived tables from immutable source units. Canonical sources and promotion evidence are never deleted by retrieval rollback.
