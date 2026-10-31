# ADR-0001: Canonical Shared Spine

Status: Accepted for local P0 construction

HG-KSEOS is the only Product Root. The local P0 uses a project-local SQLite database as the durable representation of the Canonical Shared Spine and Typed Project Graph. SQLite is the storage engine, not an independent authority: all writes must enter through validated domain transitions that emit immutable canonical events and evidence references.

Provider databases, Hermes state, Codex sessions, memory, FTS indexes, and knowledge graphs are candidate or derived views. They may be deleted and rebuilt from canonical source records. None can approve its own promotion or release.

The P0 must enforce single-writer leases, optimistic version checks, idempotency keys, legal transition tables, provenance, rollback pointers, and deterministic release reduction. The database remains project-local and is backed up before migrations.

Rollback: restore the last verified SQLite backup and replay accepted events only. A restore mismatch opens a blocking TT.

