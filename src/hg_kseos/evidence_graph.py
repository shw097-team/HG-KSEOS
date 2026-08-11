"""EVO-005 — Canonical Evidence Graph / Attestation Manifest.

Single machine truth source for evidence (no second Evidence authority).
Nodes: Subject / Requirement / Execution / Artifact / Verification.
Artifact full digest stored once; proof capsules reference ids only.
"""
from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS subjects (
    subject_id TEXT PRIMARY KEY, digest TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS requirements (
    requirement_id TEXT PRIMARY KEY, claim_scope TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS executions (
    execution_id TEXT PRIMARY KEY, requirement_id TEXT NOT NULL,
    runner TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS artifacts (
    artifact_id TEXT PRIMARY KEY, path TEXT NOT NULL, bytes INTEGER NOT NULL,
    sha256 TEXT NOT NULL, media_type TEXT, producer TEXT NOT NULL,
    subject_digest TEXT, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS verifications (
    verification_id TEXT PRIMARY KEY, requirement_id TEXT NOT NULL,
    checker TEXT NOT NULL, verdict TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS edges (
    edge_id TEXT PRIMARY KEY, kind TEXT NOT NULL,
    src TEXT NOT NULL, dst TEXT NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS runner_summaries (
    summary_id TEXT PRIMARY KEY, runner TEXT NOT NULL, note TEXT, created_at TEXT NOT NULL
);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str, seed: str = "") -> str:
    """Deterministic id: seed-based when provided (reproducible graph),
    otherwise time-based."""
    if seed:
        return f"{prefix}-{hashlib.sha256(f'{prefix}:{seed}'.encode()).hexdigest()[:16]}"
    return f"{prefix}-{hashlib.sha256(f'{prefix}:{utc_now()}'.encode()).hexdigest()[:16]}"


class EvidenceGraph:
    def __init__(self, db_path: Path) -> None:
        self.db = db_path
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    # ---- nodes ----
    def register_subject(self, subject_id: str, digest: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO subjects(subject_id,digest,created_at) VALUES(?,?,?)",
                (subject_id, digest, utc_now()))

    def register_requirement(self, requirement_id: str, scope: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO requirements(requirement_id,claim_scope,created_at) VALUES(?,?,?)",
                (requirement_id, scope, utc_now()))

    def register_execution(self, execution_id: str, requirement_id: str,
                           runner: str, status: str = "RUN") -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO executions(execution_id,requirement_id,runner,status,created_at) VALUES(?,?,?,?,?)",
                (execution_id, requirement_id, runner, status, utc_now()))

    def register_artifact(self, path: str, producer: str,
                          media_type: str | None = None,
                          subject_digest: str | None = None) -> dict[str, Any]:
        p = Path(path)
        b = p.read_bytes()
        sha = hashlib.sha256(b).hexdigest()
        # deterministic artifact id: seed = path + sha (reproducible graph)
        artifact_id = new_id("ART", seed=f"{p}:{sha}")
        with self.conn:
            self.conn.execute(
                "INSERT INTO artifacts(artifact_id,path,bytes,sha256,media_type,producer,subject_digest,created_at) VALUES(?,?,?,?,?,?,?,?)",
                (artifact_id, str(p), len(b), sha, media_type, producer, subject_digest, utc_now()))
        return {"artifact_id": artifact_id, "path": str(p), "bytes": len(b),
                "sha256": sha, "media_type": media_type, "producer": producer}

    def register_verification(self, verification_id: str, requirement_id: str,
                              checker: str, verdict: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO verifications(verification_id,requirement_id,checker,verdict,created_at) VALUES(?,?,?,?,?)",
                (verification_id, requirement_id, checker, verdict, utc_now()))

    # ---- edges ----
    def _edge(self, kind: str, src: str, dst: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO edges(edge_id,kind,src,dst,created_at) VALUES(?,?,?,?,?)",
                (new_id("EDGE", seed=f"{kind}:{src}:{dst}"), kind, src, dst, utc_now()))

    def link_execution_produced(self, execution_id: str, artifact_id: str) -> None:
        self._edge("execution_produced", execution_id, artifact_id)

    def link_artifact_about(self, artifact_id: str, subject_id: str) -> None:
        self._edge("artifact_about", artifact_id, subject_id)

    def link_verification_checks(self, verification_id: str, artifact_id: str) -> None:
        self._edge("verification_checks", verification_id, artifact_id)

    def link_requirement_supported(self, requirement_id: str, verification_id: str) -> None:
        self._edge("requirement_supported_by", requirement_id, verification_id)

    # ---- queries ----
    def requirement_supported_by(self, requirement_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """SELECT v.verification_id, v.checker, v.verdict, v.requirement_id
               FROM verifications v
               WHERE v.requirement_id = ? ORDER BY v.created_at""",
            (requirement_id,)).fetchall()
        return [dict(r) for r in rows]

    def verification_records(self) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT * FROM verifications").fetchall()
        return [dict(r) for r in rows]

    def artifact_record(self, artifact_id: str) -> dict[str, Any] | None:
        row = self.conn.execute("SELECT * FROM artifacts WHERE artifact_id=?", (artifact_id,)).fetchone()
        return dict(row) if row else None

    def graph_root_digest(self) -> str:
        """Deterministic digest of the whole canonical graph (nodes+edges).
        Timestamps excluded so the digest is reproducible across re-builds
        of the same registered artifacts."""
        parts = []
        tables = {
            "subjects": ["subject_id", "digest"],
            "requirements": ["requirement_id", "claim_scope"],
            "executions": ["execution_id", "requirement_id", "runner", "status"],
            "artifacts": ["artifact_id", "path", "bytes", "sha256", "media_type",
                          "producer", "subject_digest"],
            "verifications": ["verification_id", "requirement_id", "checker", "verdict"],
            "edges": ["edge_id", "kind", "src", "dst"],
            "runner_summaries": ["summary_id", "runner", "note"],
        }
        for table, cols in tables.items():
            rows = self.conn.execute(
                f"SELECT {','.join(cols)} FROM {table} ORDER BY rowid").fetchall()
            parts.append(table + ":" + repr([tuple(r) for r in rows]))
        return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()

    # ---- runner summary (NOT authority) ----
    def register_runner_summary(self, runner: str, note: str) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO runner_summaries(summary_id,runner,note,created_at) VALUES(?,?,?,?)",
                (new_id("SUM"), runner, note, utc_now()))

    # ---- capsule (references ids only) ----
    def proof_capsule(self, requirement_id: str, verification_id: str,
                      artifact_id: str) -> dict[str, str]:
        return {"requirement_id": requirement_id, "verification_id": verification_id,
                "artifact_id": artifact_id}

    def validate_capsule(self, capsule: dict[str, Any]) -> dict[str, Any]:
        """Capsule must reference ids only — no duplicated digest/candidate/count."""
        bad = [k for k in ("sha256", "bytes", "candidate", "count", "verdict")
               if k in capsule]
        if bad:
            return {"valid": False, "reason": f"duplicate truth fields: {bad}"}
        missing = [k for k in ("requirement_id", "verification_id", "artifact_id")
                   if k not in capsule]
        if missing:
            return {"valid": False, "reason": f"missing: {missing}"}
        return {"valid": True, "reason": "ok"}
