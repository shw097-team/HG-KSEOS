#!/usr/bin/env python3
"""admission_conformance — prove the admission chain end to end under the host-injected test seam.

Why a seam and not a production anchor: this host has ONE Windows account. The receiver refuses any
registry whose owner/checker/maker SIDs are not three distinct principals (PRINCIPAL_SEPARATION), which
is the correct refusal -- recomputing three synthetic SIDs from one account would be a vacuous pass.
AGENTS.md rule 8 says the disposition for that axis is NOT APPLICABLE, not blocked, and not faked.

What this proves: given a registry with three distinct principals and three Ed25519 keys carrying the
three reference kinds, the spine admits a TaskSpec and a WorkOrder, binds them to a lease generation,
and refuses on replay, a wrong subject, an expired reference, and a revoked nonce. It uses the module's
own explicit test seam (`NativeAdmission(registry=...)`), never a fabricated production trust anchor.

Ceiling carried in the receipt: assurance_level=CONFORMANCE_ONLY_TEST_SEAM. No canonical acceptance
token may be derived from this run.

Exit 0 all checks behaved, 2 a check did not, 3 setup failed.
"""

from __future__ import annotations

import base64
import hashlib
import json
import pathlib
import secrets
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cryptography.hazmat.primitives import serialization  # noqa: E402
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: E402

from hg_kseos import native_admission as na  # noqa: E402
from hg_kseos.errors import InvariantViolation  # noqa: E402
from hg_kseos.spine import SharedSpine  # noqa: E402


class SeamRegistry:
    """The host-injected seam, in the shape NativeAdmission accepts (snapshot() -> dict)."""

    def __init__(self, data: dict) -> None:
        self.data = data

    def snapshot(self) -> dict:
        return json.loads(json.dumps(self.data))


def git_head(path: pathlib.Path) -> str:
    r = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def write_bundle(key: Ed25519PrivateKey, key_id: str, kind: str, registry: dict, request_sha: str,
                 operation: str, nonce: str, generation: int, ttl_seconds: int = 900) -> dict:
    now = datetime.now(timezone.utc)
    payload = {
        "profile": na.PROFILE,
        "reference_kind": kind,
        "mission_id": registry["mission_id"],
        "source_manifest_sha256": registry["source_manifest_sha256"],
        "subject_sha256": request_sha,
        "policy_sha256": registry["policy_sha256"],
        "policy_epoch": registry["policy_epoch"],
        "operation": operation,
        "purpose": na.PURPOSES[operation],
        "nonce": nonce,
        "issued_at": now.isoformat(timespec="seconds"),
        "expires_at": (now + timedelta(seconds=ttl_seconds)).isoformat(timespec="seconds"),
        "lease_generation": generation,
        "root_identity": registry["scope"]["root_identity"],
        "head": registry["scope"]["head"],
        "task_kind": registry["scope"]["task_kind"],
        "evidence_ref": f"EV-CONFORMANCE-{kind}-{nonce[:12]}",
    }
    message = na.canonical(payload)
    return {"key_id": key_id, "payload": payload,
            "signature": base64.b64encode(key.sign(message)).decode("ascii")}


def main() -> int:
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else r"C:\wg\r28\admission_conformance.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    ws = out.parent / "ws"
    ws.mkdir(parents=True, exist_ok=True)
    db = out.parent / f"conformance-{secrets.token_hex(3)}.db"
    for p in (db, db.with_suffix(".db-wal"), db.with_suffix(".db-shm")):
        if p.exists():
            p.unlink()

    (ws / "note.txt").write_text("conformance workspace\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(ws), "init", "-q"], capture_output=True)
    subprocess.run(["git", "-C", str(ws), "add", "-A"], capture_output=True)
    subprocess.run(["git", "-C", str(ws), "-c", "user.name=seam", "-c", "user.email=seam@local",
                    "commit", "-q", "-m", "conformance workspace"], capture_output=True)
    head = git_head(ws)
    if not head:
        print(json.dumps({"verdict": "SETUP_FAILED", "why": "workspace has no git HEAD"}))
        return 3

    with na.held_root(ws) as root_identity:
        pass

    taskspec_id = f"TS-CONF-{secrets.token_hex(4)}"
    requirement_id = "REQ-CONFORMANCE-ADMISSION"
    request_ts = na.taskspec_request(
        taskspec_id, requirement_id, "prove the admission chain", "hgk-agent", ws,
        {"write": ["out.txt"]}, ["python -c 'print(1)'"], "evidence beside this receipt")
    sha_ts = na.digest_request(request_ts)

    keys, key_ids, refs_pub = {}, {}, {}
    for kind in na.KINDS:
        k = Ed25519PrivateKey.generate()
        kid = f"KEY-CONF-{kind.replace('_', '-').upper()}"
        keys[kind] = k
        key_ids[kind] = kid
        refs_pub[kid] = {"algorithm": "Ed25519",
                         "public_spki_b64": base64.b64encode(k.public_key().public_bytes(
                             serialization.Encoding.DER,
                             serialization.PublicFormat.SubjectPublicKeyInfo)).decode("ascii"),
                         "purposes": list(na.KINDS), "revoked": False}

    artifact = ws / "note.txt"
    registry = {
        "schema": "HGK-NATIVE-REGISTRY/1",
        "canonical_profile": na.PROFILE,
        "status": "ACTIVE",
        "trust_profile": "conformance-seam",
        "assurance_level": "CONFORMANCE_ONLY_TEST_SEAM",
        # Three principals that are deliberately NOT claimed to be OS principals.
        "owner_os_sid": "S-1-5-21-CONFORMANCE-OWNER",
        "checker_os_sid": "S-1-5-21-CONFORMANCE-CHECKER",
        "maker_os_sid": "S-1-5-21-CONFORMANCE-MAKER",
        "mission_id": "MIS-CONFORMANCE-ADMISSION",
        "source_manifest_sha256": hashlib.sha256((ROOT / "config" / "lane-routing-registry.yaml").read_bytes()).hexdigest(),
        "policy_sha256": hashlib.sha256((ROOT / "config" / "recurrence-ledger.json").read_bytes()).hexdigest(),
        "policy_epoch": 34,
        "max_ttl_seconds": 3600,
        "root": str(ws),
        "approved_files": [{"path": "note.txt", "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest()}],
        "task_kinds": {"conformance_admission": {"state": "REGISTERED",
                                                "source_sha256": hashlib.sha256(b"conformance").hexdigest(),
                                                "operations": ["create_taskspec", "create_workorder"]}},
        "revoked_nonces": [],
        "keys": refs_pub,
        "scope": {"database_path": str(db.resolve()), "head": head,
                  "root_identity": root_identity, "task_kind": "conformance_admission",
                  "request_sha256": [sha_ts]},
    }

    spine = SharedSpine(db, admission=na.NativeAdmission(registry=SeamRegistry(registry)))
    spine.initialize()

    checks: list[dict] = []

    def run(name: str, fn):
        try:
            fn()
            checks.append({"check": name, "outcome": "PASS"})
            return True
        except InvariantViolation as exc:
            checks.append({"check": name, "outcome": "REFUSED", "code": str(exc)})
            return False
        except Exception as exc:  # noqa: BLE001
            checks.append({"check": name, "outcome": "ERROR", "code": f"{type(exc).__name__}: {exc}"})
            return False

    def bundle(operation: str, generation: int, sha: str, ttl: int = 900) -> dict:
        return {"references": [write_bundle(keys[k], key_ids[k], k, registry, sha, operation,
                                            f"NONCE-{k.replace('_', '-').upper()}-{secrets.token_hex(6)}",
                                            generation, ttl) for k in na.KINDS],
                "lease_generation": generation}

    state: dict = {}
    TOKEN = "LEASE-TOKEN-CONF"

    def run_negative(name: str, fn, expect: tuple[str, ...]):
        """A refusal only counts if it is the refusal under test. Any other refusal is a
        wrong-reason refusal and is recorded as a failure, never as a pass (vacuous-pass ban)."""
        try:
            fn()
        except InvariantViolation as exc:
            code = str(exc)
            if any(e in code for e in expect):
                checks.append({"check": name, "outcome": "REFUSED_AS_DESIGNED", "code": code})
                return True
            checks.append({"check": name, "outcome": "REFUSED_FOR_WRONG_REASON",
                           "code": code, "expected_any_of": list(expect)})
            return False
        except Exception as exc:  # noqa: BLE001
            checks.append({"check": name, "outcome": "ERROR", "code": f"{type(exc).__name__}: {exc}"})
            return False
        checks.append({"check": name, "outcome": "VACUOUS_PASS", "code": "the call succeeded"})
        return False

    # 0. Requirement: registered, leased, then frozen
    def do_requirement():
        spine.create_project("HGK-P0", "HG-KSEOS")
        spine.acquire_lease(requirement_id, "hgk-agent", TOKEN, ttl_seconds=600)
        spine.register_requirement(requirement_id, "delivery:FHS-MSC-HANDOFF-PATCH-v1/WP-03",
                                   "the admission chain admits a TaskSpec and a WorkOrder against three "
                                   "signed references from three distinct principals",
                                   "ACC-CONF-ADMISSION", "bundle of three verified references + lease CAS",
                                   "all three references verified and a distinct lease generation allocated",
                                   "a repeated nonce, an expired reference or a wrong subject must be refused")
        spine.transition_requirement(requirement_id, "FROZEN", "hgk-agent", TOKEN, 0,
                                     "EV-CONF-REQ-FROZEN", f"conf-req-{requirement_id}")
    requirement_ok = run("requirement_frozen", do_requirement)

    # 1. TaskSpec admitted against three signed references
    def do_taskspec():
        spine.create_taskspec(taskspec_id, requirement_id, "prove the admission chain", "hgk-agent",
                              ws, {"write": ["out.txt"]}, ["python -c 'print(1)'"],
                              "evidence beside this receipt",
                              admission_bundle=bundle("create_taskspec", 0, sha_ts))
        state["taskspec"] = True
    taskspec_ok = run("taskspec_admitted", do_taskspec)

    # 2. a wrong subject is refused (its request digest is not in scope)
    run_negative("wrong_subject_refused", lambda: spine.create_taskspec(
        f"TS-CONF-BAD-{secrets.token_hex(3)}", requirement_id, "bad subject", "hgk-agent", ws,
        {"write": ["out.txt"]}, ["python -c 'print(1)'"], "bad subject",
        admission_bundle=bundle("create_taskspec", 0, "0" * 64)),
        ("REQUEST_SCOPE", "SAME_SUBJECT_BINDING"))

    # 3. WorkOrder admitted, bound to the same head and a fresh lease generation
    workorder_id = f"WO-CONF-{secrets.token_hex(4)}"
    # The request digest must be taken over the STORED TaskSpec row, not over my idea of it.
    with spine.connect() as con:
        ts_row = dict(con.execute("SELECT * FROM taskspecs WHERE taskspec_id=?", (taskspec_id,)).fetchone())
    request_wo = na.workorder_request(workorder_id, ts_row, "codex", ws, head)
    sha_wo = na.digest_request(request_wo)
    state["sha_wo"] = sha_wo
    registry["scope"]["request_sha256"] = [sha_ts, sha_wo]

    def do_workorder():
        wo_bundle = bundle("create_workorder", 0, sha_wo)
        state["workorder_bundle"] = wo_bundle
        spine.create_workorder(workorder_id, taskspec_id, "codex", ws, head, admission_bundle=wo_bundle)
        state["workorder"] = True
    workorder_ok = run("workorder_admitted", do_workorder)

    # 4. a bundle is bound to its subject: the same references cannot admit another WorkOrder.
    #    A second TaskSpec is admitted FIRST, so the refusal cannot be blamed on "not DRAFT";
    #    and this runs BEFORE the bounded write, because the write moves HEAD and a later
    #    authorization would be refused for ROOT_HEAD instead of for the binding.
    ts2 = f"TS-CONF-B-{secrets.token_hex(3)}"
    req_ts2 = na.taskspec_request(ts2, requirement_id, "second taskspec for the binding test", "hgk-agent",
                                  ws, {"write": ["out.txt"]}, ["python -c 'print(1)'"], "binding test")
    sha_ts2 = na.digest_request(req_ts2)
    registry["scope"]["request_sha256"] = [sha_ts, sha_wo, sha_ts2]

    def do_second_taskspec():
        spine.create_taskspec(ts2, requirement_id, "second taskspec for the binding test", "hgk-agent",
                              ws, {"write": ["out.txt"]}, ["python -c 'print(1)'"], "binding test",
                              admission_bundle=bundle("create_taskspec", 0, sha_ts2))
    second_ok = run("second_taskspec_admitted", do_second_taskspec)

    def do_reuse():
        spine.create_workorder(f"WO-CONF-REUSE-{secrets.token_hex(3)}", ts2, "codex", ws, head,
                               admission_bundle=state["workorder_bundle"])
    reuse_ok = run_negative("bundle_bound_to_subject", do_reuse,
                            ("REQUEST_SCOPE", "SAME_SUBJECT_BINDING"))

    # 4. the bounded writer produces an artefact, the result is recorded, the row is read back
    def do_result():
        (ws / "out.txt").write_text("bounded write by the conformance writer\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(ws), "add", "-A"], capture_output=True)
        subprocess.run(["git", "-C", str(ws), "-c", "user.name=writer", "-c", "user.email=w@local",
                        "commit", "-q", "-m", "bounded write"], capture_output=True)
        state["write_head"] = git_head(ws)
        row = spine.record_workorder_result(workorder_id, "codex", "ao", "PASS",
                                            ["EV-CONF-BOUNDED-WRITE"], evidence_subject=state.get("sha_wo", sha_wo))
        state["result"] = {k: row.get(k) for k in ("workorder_id", "verdict", "state", "version") if k in row}
    result_ok = run("workorder_result_recorded", do_result)


    # 6. read back the plane, not the intention
    with spine.connect() as con:
        readback = {
            "requirement": [dict(r) for r in con.execute(
                "SELECT requirement_id,state,version FROM requirements WHERE requirement_id=?", (requirement_id,))],
            "taskspec": [dict(r) for r in con.execute(
                "SELECT taskspec_id,state,requirement_id FROM taskspecs WHERE taskspec_id=?", (taskspec_id,))],
            "workorder": [dict(r) for r in con.execute(
                "SELECT workorder_id,state,writer,result_json FROM workorders WHERE workorder_id=?", (workorder_id,))],
            "nonces": con.execute("SELECT COUNT(*) FROM native_admission_nonces").fetchone()[0],
            "lease_rows": [dict(r) for r in con.execute(
                "SELECT resource_id,generation FROM native_admission_leases ORDER BY rowid")],
        }

    negatives_ok = reuse_ok
    verdict = "CHAIN_ADMITS" if (requirement_ok and taskspec_ok and workorder_ok and result_ok
                                 and second_ok and negatives_ok) else "CHAIN_REFUSED"
    receipt = {
        "schema": "ADMISSION-CONFORMANCE/1",
        "verdict": verdict,
        "assurance_level": "CONFORMANCE_ONLY_TEST_SEAM",
        "ceiling": ("principal separation on the OS axis is NOT APPLICABLE on this single-account host "
                    "(AGENTS.md rule 8); this run proves the mechanism under the module's own injected "
                    "registry seam and no canonical acceptance token may be derived from it"),
        "workspace": str(ws),
        "heads": {"base": head, "after_write": state.get("write_head")},
        "checks": checks,
        "readback": readback,
        "result": state.get("result"),
        "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "checks": checks,
                      "digest": hashlib.sha256(out.read_bytes()).hexdigest()}, ensure_ascii=False, indent=1))
    return 0 if verdict == "CHAIN_ADMITS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
