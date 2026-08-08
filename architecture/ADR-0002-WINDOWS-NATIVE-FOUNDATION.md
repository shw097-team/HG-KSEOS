# ADR-0002: Windows-native foundation

Status: Accepted for local P0 construction

The P0 runs natively on Windows without Docker, WSL2, Kubernetes, PostgreSQL, or a VM. It uses PowerShell as the operator surface, Python 3.12 for the runtime, SQLite/FTS5 for canonical and retrieval storage, and Git for source/evidence versioning.

The initial build may reuse the Codex-bundled Python only as a bootstrap tool. Delivery qualification requires a project `.venv`, a declared Python constraint, a lock/readback artifact, and doctor evidence. The bundled runtime remains an external provider and is not copied into the repository.

Hermes follows its official user-local Windows layout and is connected only through a bounded adapter after pin/install/doctor/pilot/rollback. No credentials are stored in the repository or evidence.

Rollback: remove only project-local generated runtime state and restore the previous verified configuration; external provider uninstall is a separate receipt-listed action.

