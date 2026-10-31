#!/usr/bin/env python
"""R18 WP-FHS-00: source currentness + manifest integrity + DAG structure.

Read-only. Sources are addressed through the Win32 extended-length prefix
(\\\\?\\) because the canonical package root is 217 chars and the deepest
payload path is 289 chars, which exceeds MAX_PATH for plain opens.
The canonical root string is recorded verbatim; the prefix is transport only.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

PKG = sys.argv[1]
OUT = sys.argv[2]


def xp(p):
    """Extended-length path for native opens. Transport only."""
    p = p.replace("/", "\\")
    if p.startswith("\\\\?\\"):
        return p
    if p.startswith("\\\\"):
        return "\\\\?\\UNC" + p[1:]
    return "\\\\?\\" + p


def sha256_file(p):
    h = hashlib.sha256()
    with open(xp(p), "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def nbytes(p):
    return os.stat(xp(p)).st_size


manifest_rows = {}
with open(xp(os.path.join(PKG, "MANIFEST.md")), encoding="utf-8") as f:
    for line in f:
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([0-9a-f]{64})\s*\|\s*$", line)
        if m:
            manifest_rows[m.group(1)] = {"bytes": int(m.group(2)), "sha256": m.group(3)}

checksum_rows = {}
cs_path = os.path.join(PKG, "03_TESTS_AND_READBACK", "artifact_checksums.sha256")
with open(xp(cs_path), encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            checksum_rows[parts[1].strip()] = parts[0]

actual = {}
for root, dirs, files in os.walk(xp(PKG)):
    for fn in files:
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, xp(PKG)).replace("\\", "/")
        actual[rel] = nbytes(full)


def classify(rel):
    if rel.endswith(".zip"):
        return "OUTER_ARCHIVE"
    if rel in ("MANIFEST.md", "INDEX.md", "README.md", "COVERAGE_REPORT.md",
               "REPAIR_CLOSURE_REPORT.md"):
        return "DERIVED_OR_PROSE"
    # README: "checksum清單排除自身和封裝檔以避免自指" -- the checksum file cannot list
    # itself; the compensating control is the ZIP readback below, which must cover it.
    if rel == "03_TESTS_AND_READBACK/artifact_checksums.sha256":
        return "DERIVED_CHECKSUM_SELF_EXCLUDED"
    return "PAYLOAD"


manifest_mismatch, manifest_missing = [], []
for rel, rec in manifest_rows.items():
    full = os.path.join(PKG, rel)
    if not os.path.exists(xp(full)):
        manifest_missing.append(rel)
        continue
    got_bytes, got_sha = nbytes(full), sha256_file(full)
    if got_bytes != rec["bytes"] or got_sha != rec["sha256"]:
        manifest_mismatch.append({
            "path": rel, "declared_bytes": rec["bytes"], "actual_bytes": got_bytes,
            "declared_sha256": rec["sha256"], "actual_sha256": got_sha,
            "bytes_ok": got_bytes == rec["bytes"], "sha_ok": got_sha == rec["sha256"],
        })

checksum_mismatch, checksum_missing = [], []
for rel, want in checksum_rows.items():
    full = os.path.join(PKG, rel)
    if not os.path.exists(xp(full)):
        checksum_missing.append(rel)
        continue
    got = sha256_file(full)
    if got != want:
        checksum_mismatch.append({"path": rel, "declared": want, "actual": got})

in_manifest, in_checksum = set(manifest_rows), set(checksum_rows)
unlisted_payload = [r for r in sorted(actual)
                    if classify(r) == "PAYLOAD" and r not in in_manifest and r not in in_checksum]

dag = json.loads(open(xp(os.path.join(PKG, "03_TESTS_AND_READBACK", "wp_graph.json")),
                      encoding="utf-8").read())
nodes = {n["id"]: n for n in dag["nodes"]}
edges = dag["typed_edges"]
edge_pairs = {(e["from"], e["to"]) for e in edges}
dep_pairs = {(d, nid) for nid, n in nodes.items() for d in n.get("depends_on", [])}
dag_findings = []
if len(nodes) != 22:
    dag_findings.append("NODE_COUNT=%d expected 22" % len(nodes))
for p in sorted(edge_pairs - dep_pairs):
    dag_findings.append("EDGE_WITHOUT_DEPENDENCY %s" % (p,))
for p in sorted(dep_pairs - edge_pairs):
    dag_findings.append("DEPENDENCY_WITHOUT_EDGE %s" % (p,))
for p in edge_pairs | dep_pairs:
    for ref in p:
        if ref not in nodes:
            dag_findings.append("UNKNOWN_NODE_REF %s" % ref)
edge_type_vals = sorted({e["type"] for e in edges})
for e in edges:
    if e.get("type") not in ("DATA_OR_ADMISSION", "CAPABILITY"):
        dag_findings.append("UNEXPECTED_EDGE_TYPE %s->%s:%s" % (e["from"], e["to"], e.get("type")))
for nid, n in nodes.items():
    for field in ("tier", "effect_class", "output", "permission_basis", "native_status",
                  "positive", "negative", "first_fail", "phase"):
        if field not in n:
            dag_findings.append("NODE_FIELD_MISSING %s.%s" % (nid, field))

indeg = {n: 0 for n in nodes}
adj = {n: [] for n in nodes}
for d, n in dep_pairs:
    if d in nodes and n in nodes:
        indeg[n] += 1
        adj[d].append(n)
q = sorted(n for n in nodes if indeg[n] == 0)
seen = []
while q:
    cur = q.pop(0)
    seen.append(cur)
    for nxt in sorted(adj[cur]):
        indeg[nxt] -= 1
        if indeg[nxt] == 0:
            q.append(nxt)
cycle_nodes = sorted(set(nodes) - set(seen))
if cycle_nodes:
    dag_findings.append("CYCLE_OR_UNREACHABLE %s" % cycle_nodes)

level = {n: 0 for n in nodes}
for _ in range(len(nodes) + 1):
    changed = False
    for n in nodes:
        for d in nodes[n].get("depends_on", []):
            if level[n] < level[d] + 1:
                level[n] = level[d] + 1
                changed = True
    if not changed:
        break
waves = {}
for n, lv in level.items():
    waves.setdefault(lv, []).append(n)
waves = {k: sorted(v) for k, v in sorted(waves.items())}

repos = {}
for name, path in [
    ("HG-KSEOS", r"C:\Projects\Agent_Workspace\HG-KSEOS"),
    ("Fabric", r"C:\Projects\Agent_Workspace\Fabric"),
    ("PIPD", r"C:\Projects\Agent_Workspace\PIPD"),
    ("SBL", r"C:\Projects\Agent_Workspace\SBL"),
]:
    def g(*args):
        try:
            r = subprocess.run(["git", "-C", path] + list(args), capture_output=True,
                               text=True, timeout=120)
            return r.stdout.strip()
        except Exception as exc:  # noqa: BLE001
            return "ERR:%s" % exc
    head = g("rev-parse", "HEAD")
    branch = g("rev-parse", "--abbrev-ref", "HEAD")
    porcelain = g("status", "--porcelain")
    dirty = [l for l in porcelain.splitlines() if l.strip()]
    repos[name] = {"root": path, "is_git": bool(head), "head": head, "branch": branch,
                   "dirty_count": len(dirty), "dirty_sample": dirty[:15]}

zip_path = os.path.join(PKG, "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2.zip")

# --- outer ZIP readback: every entry must be byte-identical to the on-disk member,
# and every on-disk member must be present in the archive (covers the self-excluded checksum file).
import zipfile
zip_findings = []
zip_entries = []
with zipfile.ZipFile(xp(zip_path)) as z:
    for info in z.infolist():
        if info.is_dir():
            continue
        name = info.filename.replace("\\", "/")
        # archives placed one level down carry the package dir as prefix
        rel = name.split("/", 1)[1] if name.split("/", 1)[0].endswith("revision2") else name
        zip_entries.append(rel)
        disk = os.path.join(PKG, rel)
        if not os.path.exists(xp(disk)):
            zip_findings.append("ZIP_ENTRY_NOT_ON_DISK %s" % rel)
            continue
        if nbytes(disk) != info.file_size:
            zip_findings.append("ZIP_SIZE_DIFF %s disk=%d zip=%d" % (rel, nbytes(disk), info.file_size))
            continue
        if sha256_file(disk) != hashlib.sha256(z.read(info)).hexdigest():
            zip_findings.append("ZIP_BYTES_DIFF %s" % rel)
disk_members = {r for r in actual if r != os.path.basename(zip_path)}
not_in_zip = sorted(disk_members - set(zip_entries))
for rel in not_in_zip:
    zip_findings.append("DISK_MEMBER_NOT_IN_ZIP %s" % rel)

receipt = {
    "schema": "R18.FHS.WP00.SOURCE_CURRENTNESS/1",
    "wp": "WP-FHS-00",
    "collected_utc": datetime.now(timezone.utc).isoformat(),
    "canonical_package_root": PKG,
    "canonical_root_len": len(PKG),
    "max_payload_path_len": max(len(os.path.join(PKG, r.replace("/", "\\"))) for r in actual),
    "path_transport": "win32 extended-length prefix \\\\?\\ (transport only; root string recorded verbatim)",
    "outer_zip_sha256": sha256_file(zip_path),
    "outer_zip_bytes": nbytes(zip_path),
    "counts": {"files_on_disk": len(actual),
               "payload_files": sum(1 for r in actual if classify(r) == "PAYLOAD"),
               "manifest_rows": len(manifest_rows),
               "checksum_rows": len(checksum_rows)},
    "manifest": {"verified_rows": len(manifest_rows) - len(manifest_missing) - len(manifest_mismatch),
                 "missing": manifest_missing, "mismatch": manifest_mismatch},
    "checksums": {"verified_rows": len(checksum_rows) - len(checksum_missing) - len(checksum_mismatch),
                  "missing": checksum_missing, "mismatch": checksum_mismatch},
    "unlisted_payload_files": unlisted_payload,
    "outer_zip_readback": {"entries": len(zip_entries), "findings": zip_findings,
                           "covers_self_excluded_checksum":
                           "03_TESTS_AND_READBACK/artifact_checksums.sha256" in zip_entries},
    "probe_defects_and_corrections": [
        {"defect": "v1 classifier counted 03_TESTS_AND_READBACK/artifact_checksums.sha256 as an "
                   "unlisted PAYLOAD file",
         "why_wrong": "the checksum list is a derived register that by construction cannot list "
                      "itself; README states the exclusion and the ZIP as the compensating readback",
         "correction": "classified as DERIVED_CHECKSUM_SELF_EXCLUDED and the outer-ZIP readback "
                       "was added so the file is still digest-verified against the archive member",
         "recorded": "this receipt"},
    ],
    "dag": {"schema": dag.get("schema"), "native_authority": dag.get("native_authority"),
            "node_count": len(nodes), "edge_count": len(edges), "edge_types": edge_type_vals,
            "findings": dag_findings, "waves": waves,
            "tier_by_wp": {n: nodes[n]["tier"] for n in sorted(nodes)},
            "effect_by_wp": {n: nodes[n]["effect_class"] for n in sorted(nodes)},
            "native_status_by_wp": {n: nodes[n]["native_status"] for n in sorted(nodes)}},
    "repos": repos,
}
receipt["verdict"] = "PASS" if (not manifest_missing and not manifest_mismatch
                                and not checksum_missing and not checksum_mismatch
                                and not dag_findings and not unlisted_payload
                                and not zip_findings) else "FAIL"
with open(xp(OUT), "w", encoding="utf-8") as f:
    json.dump(receipt, f, ensure_ascii=False, indent=1)
print(json.dumps({"verdict": receipt["verdict"], "counts": receipt["counts"],
                  "manifest": receipt["manifest"], "checksums_verified": receipt["checksums"]["verified_rows"],
                  "checksums_missing": receipt["checksums"]["missing"],
                  "checksums_mismatch": receipt["checksums"]["mismatch"],
                  "unlisted": receipt["unlisted_payload_files"],
                  "zip": receipt["outer_zip_sha256"], "dag_findings": dag_findings,
                  "nodes": len(nodes), "edges": len(edges),
                  "zip_entries": len(zip_entries), "zip_findings": zip_findings}, ensure_ascii=False))
print("WAVES", json.dumps(waves, ensure_ascii=False))
for k, v in repos.items():
    print(k, v["head"][:12], v["branch"], "dirty=%d" % v["dirty_count"])
