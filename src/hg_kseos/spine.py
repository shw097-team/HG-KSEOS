from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterator

from .errors import InvariantViolation, LeaseConflict, StaleState
from .util import canonical_json, new_id, sha256_text, utc_now


TRANSITIONS: dict[str, dict[str | None, set[str]]] = {
    "requirement": {
        None: {"CANDIDATE"},
        "CANDIDATE": {"FROZEN", "REJECTED"},
        "FROZEN": {"IMPLEMENTED", "REJECTED"},
        "IMPLEMENTED": {"VERIFIED", "ROLLED_BACK"},
        "VERIFIED": {"ACCEPTED", "REPAIR", "ROLLED_BACK"},
        "REPAIR": {"IMPLEMENTED", "REJECTED"},
        "ACCEPTED": {"ROLLED_BACK"},
        "REJECTED": set(),
        "ROLLED_BACK": {"IMPLEMENTED"},
    },
    "taskspec": {
        None: {"DRAFT"},
        "DRAFT": {"ADMITTED", "REJECTED"},
        "ADMITTED": {"RUNNING", "CANCELLED"},
        "RUNNING": {"VERIFIED", "REPAIR", "FAILED", "CANCELLED"},
        "REPAIR": {"RUNNING", "FAILED"},
        "VERIFIED": {"PACKAGED"},
        "PACKAGED": set(),
        "REJECTED": set(),
        "FAILED": set(),
        "CANCELLED": set(),
    },
}


class SharedSpine:
    def __init__(self, database: Path, schema: Path | None = None) -> None:
        self.database = database.resolve()
        self.schema = schema or Path(__file__).with_name("schema.sql")

    def _open(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database, timeout=15)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA busy_timeout = 15000")
        return connection

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = self._open()
        try:
            yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        self.database.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as connection:
            connection.executescript(self.schema.read_text(encoding="utf-8"))
            connection.execute(
                "INSERT OR REPLACE INTO schema_meta(key,value) VALUES('schema_digest',?)",
                (sha256_text(self.schema.read_text(encoding="utf-8")),),
            )

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        connection = self._open()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def create_project(self, project_id: str = "HGK-P0", name: str = "HG-KSEOS") -> None:
        now = utc_now()
        with self.transaction() as connection:
            connection.execute(
                """INSERT OR IGNORE INTO projects
                   (project_id,name,product_root,state,version,created_at,updated_at)
                   VALUES(?,?, 'HG-KSEOS','ACTIVE',0,?,?)""",
                (project_id, name, now, now),
            )

    def bind_workspace(self, workspace_id: str, project_id: str, path: Path, mode: str) -> None:
        digest = sha256_text(str(path.resolve()).casefold())
        with self.transaction() as connection:
            connection.execute(
                """INSERT INTO workspaces(workspace_id,project_id,path,mode,identity_digest,created_at)
                   VALUES(?,?,?,?,?,?)
                   ON CONFLICT(workspace_id) DO UPDATE SET
                     path=excluded.path, mode=excluded.mode, identity_digest=excluded.identity_digest""",
                (workspace_id, project_id, str(path.resolve()), mode, digest, utc_now()),
            )

    def acquire_lease(self, resource_id: str, holder: str, token: str, ttl_seconds: int = 300) -> None:
        now = datetime.now(UTC)
        expires = now + timedelta(seconds=ttl_seconds)
        token_hash = sha256_text(token)
        with self.transaction() as connection:
            existing = connection.execute(
                "SELECT holder,expires_at FROM leases WHERE resource_id=?", (resource_id,)
            ).fetchone()
            if existing and datetime.fromisoformat(existing["expires_at"].replace("Z", "+00:00")) > now:
                if existing["holder"] != holder:
                    raise LeaseConflict(f"ERR_DUAL_WRITER:{resource_id}:{existing['holder']}")
            connection.execute(
                """INSERT INTO leases(resource_id,holder,token_hash,expires_at,created_at)
                   VALUES(?,?,?,?,?)
                   ON CONFLICT(resource_id) DO UPDATE SET holder=excluded.holder,
                     token_hash=excluded.token_hash,expires_at=excluded.expires_at,
                     created_at=excluded.created_at""",
                (resource_id, holder, token_hash, expires.isoformat().replace("+00:00", "Z"), utc_now()),
            )

    def release_lease(self, resource_id: str, holder: str, token: str) -> None:
        with self.transaction() as connection:
            row = connection.execute(
                "SELECT holder,token_hash FROM leases WHERE resource_id=?", (resource_id,)
            ).fetchone()
            if not row or row["holder"] != holder or row["token_hash"] != sha256_text(token):
                raise LeaseConflict(f"ERR_LEASE_RELEASE_AUTH:{resource_id}")
            connection.execute("DELETE FROM leases WHERE resource_id=?", (resource_id,))

    def _assert_lease(self, connection: sqlite3.Connection, resource_id: str, holder: str, token: str) -> None:
        row = connection.execute(
            "SELECT holder,token_hash,expires_at FROM leases WHERE resource_id=?", (resource_id,)
        ).fetchone()
        if not row or row["holder"] != holder or row["token_hash"] != sha256_text(token):
            raise LeaseConflict(f"ERR_LEASE_REQUIRED:{resource_id}")
        expiry = datetime.fromisoformat(row["expires_at"].replace("Z", "+00:00"))
        if expiry <= datetime.now(UTC):
            raise LeaseConflict(f"ERR_LEASE_EXPIRED:{resource_id}")

    def register_requirement(
        self,
        requirement_id: str,
        source_locator: str,
        wording: str,
        acceptance_id: str,
        oracle: str,
        threshold: str,
        negative_fixture: str,
        priority: str = "P0",
        project_id: str = "HGK-P0",
    ) -> None:
        if not all((requirement_id, source_locator, wording, acceptance_id, oracle, negative_fixture)):
            raise InvariantViolation("ERR_REQUIREMENT_CRITICAL_FIELD_MISSING")
        now = utc_now()
        with self.transaction() as connection:
            connection.execute(
                """INSERT INTO requirements
                   (requirement_id,project_id,source_locator,wording,priority,state,version,
                    acceptance_id,rollback_pointer,created_at,updated_at)
                   VALUES(?,?,?,?,?,'CANDIDATE',0,?,?,?,?)""",
                (
                    requirement_id,
                    project_id,
                    source_locator,
                    wording,
                    priority,
                    acceptance_id,
                    f"RB-{requirement_id}",
                    now,
                    now,
                ),
            )
            connection.execute(
                """INSERT INTO acceptances
                   (acceptance_id,requirement_id,oracle,threshold,negative_fixture,verdict,updated_at)
                   VALUES(?,?,?,?,?,'NOT_RUN',?)""",
                (acceptance_id, requirement_id, oracle, threshold or "EXPLICIT_ORACLE_PASS", negative_fixture, now),
            )

    def transition_requirement(
        self,
        requirement_id: str,
        to_state: str,
        actor: str,
        token: str,
        expected_version: int,
        evidence_ref: str,
        idempotency_key: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        with self.transaction() as connection:
            prior = connection.execute(
                "SELECT state,version,rollback_pointer FROM requirements WHERE requirement_id=?",
                (requirement_id,),
            ).fetchone()
            if not prior:
                raise InvariantViolation(f"ERR_REQUIREMENT_UNKNOWN:{requirement_id}")
            duplicate = connection.execute(
                "SELECT event_id,resulting_version,to_state FROM canonical_events WHERE idempotency_key=?",
                (idempotency_key,),
            ).fetchone()
            if duplicate:
                return dict(duplicate) | {"idempotent_replay": True}
            self._assert_lease(connection, requirement_id, actor, token)
            if prior["version"] != expected_version:
                raise StaleState(
                    f"ERR_STALE_VERSION:{requirement_id}:expected={expected_version}:actual={prior['version']}"
                )
            allowed = TRANSITIONS["requirement"].get(prior["state"], set())
            if to_state not in allowed:
                raise InvariantViolation(f"ERR_ILLEGAL_TRANSITION:{prior['state']}->{to_state}")
            resulting_version = expected_version + 1
            now = utc_now()
            updated = connection.execute(
                """UPDATE requirements SET state=?,version=?,updated_at=?
                   WHERE requirement_id=? AND version=?""",
                (to_state, resulting_version, now, requirement_id, expected_version),
            )
            if updated.rowcount != 1:
                raise StaleState(f"ERR_CONCURRENT_UPDATE:{requirement_id}")
            event_id = new_id("EVT")
            connection.execute(
                """INSERT INTO canonical_events
                   (event_id,idempotency_key,entity_type,entity_id,from_state,to_state,actor,
                    expected_version,resulting_version,payload_json,evidence_ref,rollback_pointer,created_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    event_id,
                    idempotency_key,
                    "requirement",
                    requirement_id,
                    prior["state"],
                    to_state,
                    actor,
                    expected_version,
                    resulting_version,
                    canonical_json(payload or {}),
                    evidence_ref,
                    prior["rollback_pointer"],
                    now,
                ),
            )
            return {"event_id": event_id, "resulting_version": resulting_version, "to_state": to_state}

    def create_taskspec(
        self,
        taskspec_id: str,
        requirement_id: str,
        objective: str,
        owner: str,
        writable_root: Path,
        permissions: dict[str, Any],
        tests: list[str],
        evidence_plan: str,
    ) -> None:
        if not objective or not tests or not evidence_plan:
            raise InvariantViolation("ERR_TASKSPEC_CRITICAL_FIELD_MISSING")
        now = utc_now()
        with self.transaction() as connection:
            requirement = connection.execute(
                "SELECT state FROM requirements WHERE requirement_id=?", (requirement_id,)
            ).fetchone()
            if not requirement or requirement["state"] != "FROZEN":
                raise InvariantViolation("ERR_TASKSPEC_REQUIRES_FROZEN_REQUIREMENT")
            connection.execute(
                """INSERT INTO taskspecs
                   (taskspec_id,requirement_id,objective,owner,writable_root,permissions_json,
                    tests_json,rollback_pointer,evidence_plan,state,version,created_at,updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?,'DRAFT',0,?,?)""",
                (
                    taskspec_id,
                    requirement_id,
                    objective,
                    owner,
                    str(writable_root.resolve()),
                    canonical_json(permissions),
                    canonical_json(tests),
                    f"RB-{taskspec_id}",
                    evidence_plan,
                    now,
                    now,
                ),
            )

    def create_workorder(
        self,
        workorder_id: str,
        taskspec_id: str,
        writer: str,
        worktree: Path,
        base_head: str,
    ) -> None:
        if not writer or not base_head:
            raise InvariantViolation("ERR_WORKORDER_CRITICAL_FIELD_MISSING")
        now = utc_now()
        with self.transaction() as connection:
            taskspec = connection.execute(
                "SELECT state FROM taskspecs WHERE taskspec_id=?", (taskspec_id,)
            ).fetchone()
            if not taskspec or taskspec["state"] != "DRAFT":
                raise InvariantViolation("ERR_WORKORDER_REQUIRES_DRAFT_TASKSPEC")
            connection.execute(
                "UPDATE taskspecs SET state='ADMITTED',version=version+1,updated_at=? WHERE taskspec_id=?",
                (now, taskspec_id),
            )
            connection.execute(
                """INSERT INTO workorders
                   (workorder_id,taskspec_id,writer,worktree,base_head,state,rollback_pointer,created_at,updated_at)
                   VALUES(?,?,?,?,?,'CREATED',?,?,?)""",
                (workorder_id, taskspec_id, writer, str(worktree.resolve()), base_head, f"RB-{workorder_id}", now, now),
            )

    def record_workorder_result(
        self,
        workorder_id: str,
        writer: str,
        checker: str,
        verdict: str,
        evidence_refs: list[str],
    ) -> None:
        if writer == checker:
            raise InvariantViolation("ERR_WORKORDER_SELF_REVIEW")
        if verdict not in {"PASS", "FAIL"} or not evidence_refs:
            raise InvariantViolation("ERR_WORKORDER_RESULT_INCOMPLETE")
        with self.transaction() as connection:
            row = connection.execute(
                "SELECT writer,state FROM workorders WHERE workorder_id=?", (workorder_id,)
            ).fetchone()
            if not row or row["writer"] != writer or row["state"] != "CREATED":
                raise InvariantViolation("ERR_WORKORDER_RESULT_STATE")
            result = {"verdict": verdict, "checker": checker, "evidence_refs": evidence_refs}
            connection.execute(
                "UPDATE workorders SET state=?,result_json=?,updated_at=? WHERE workorder_id=?",
                ("VERIFIED" if verdict == "PASS" else "FAILED", canonical_json(result), utc_now(), workorder_id),
            )

    def rollback_workorder(self, workorder_id: str, evidence_ref: str) -> None:
        with self.transaction() as connection:
            row = connection.execute(
                "SELECT state,rollback_pointer FROM workorders WHERE workorder_id=?", (workorder_id,)
            ).fetchone()
            if not row or row["state"] != "VERIFIED":
                raise InvariantViolation("ERR_WORKORDER_NOT_ROLLBACKABLE")
            now = utc_now()
            connection.execute(
                "UPDATE workorders SET state='ROLLED_BACK',updated_at=? WHERE workorder_id=?",
                (now, workorder_id),
            )
            connection.execute(
                """INSERT INTO rollback_records
                   (rollback_id,target_type,target_id,pre_state_digest,post_state_digest,status,evidence_ref,created_at,updated_at)
                   VALUES(?,?,?,?,?,'PASS',?,?,?)""",
                (
                    row["rollback_pointer"],
                    "WORKORDER",
                    workorder_id,
                    sha256_text("VERIFIED"),
                    sha256_text("ROLLED_BACK"),
                    evidence_ref,
                    now,
                    now,
                ),
            )

    def register_evidence(
        self, evidence_id: str, kind: str, locator: str, sha256: str, producer: str, checker: str | None = None
    ) -> None:
        if len(sha256) != 64:
            raise InvariantViolation("ERR_EVIDENCE_SHA256")
        with self.transaction() as connection:
            connection.execute(
                """INSERT INTO evidence_refs(evidence_id,kind,locator,sha256,producer,checker,created_at)
                   VALUES(?,?,?,?,?,?,?)""",
                (evidence_id, kind, locator, sha256.lower(), producer, checker, utc_now()),
            )

    def open_tt(self, tt_id: str, subject: str, owner: str, blocking: bool, close_criteria: str) -> None:
        now = utc_now()
        with self.transaction() as connection:
            connection.execute(
                """INSERT INTO tt_records
                   (tt_id,subject,owner,blocking,close_criteria,status,created_at,updated_at)
                   VALUES(?,?,?,?,?,'OPEN',?,?)
                   ON CONFLICT(tt_id) DO UPDATE SET subject=excluded.subject,owner=excluded.owner,
                     blocking=excluded.blocking,close_criteria=excluded.close_criteria,updated_at=excluded.updated_at""",
                (tt_id, subject, owner, int(blocking), close_criteria, now, now),
            )

    def close_tt(self, tt_id: str, evidence_ref: str) -> None:
        with self.transaction() as connection:
            updated = connection.execute(
                """UPDATE tt_records SET status='CLOSED',evidence_ref=?,updated_at=?
                   WHERE tt_id=? AND status='OPEN'""",
                (evidence_ref, utc_now(), tt_id),
            )
            if updated.rowcount != 1:
                raise InvariantViolation(f"ERR_TT_NOT_OPEN:{tt_id}")

    def snapshot(self) -> dict[str, Any]:
        tables = (
            "requirements",
            "acceptances",
            "taskspecs",
            "workorders",
            "canonical_events",
            "evidence_refs",
            "tt_records",
            "sources",
            "source_units",
            "knowledge_docs",
            "kg_edges",
            "kg_assertions",
            "memory_records",
            "provider_bindings",
            "project_lifecycles",
            "project_transitions",
            "evolution_signals",
            "improvement_candidates",
        )
        with self.connect() as connection:
            counts = {table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for table in tables}
            blocking = connection.execute(
                "SELECT COUNT(*) FROM tt_records WHERE blocking=1 AND status!='CLOSED'"
            ).fetchone()[0]
            schema_version = connection.execute(
                "SELECT value FROM schema_meta WHERE key='schema_version'"
            ).fetchone()[0]
        return {"schema_version": schema_version, "counts": counts, "open_blocking_tt": blocking}
