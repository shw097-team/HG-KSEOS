import hashlib
import json
import collections
import pathlib

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
SUB = ROUND / "subject"
CAN = pathlib.Path("C:/Projects/Agent_Workspace/知識庫/實作相關DOC/Fabric vNext/Semantic World OS Fabric/SBL_PIPD/FHS-MSC/"
                   "FHS-MSC_PIPD-LS-PKG/FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE/"
                   "FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2")


def xp(p):
    s = str(p).replace("/", "\\")
    if s.startswith("\\\\?\\"):
        return s
    if s.startswith("\\\\"):
        return "\\\\?\\UNC\\" + s[2:]
    return "\\\\?\\" + s


def entries(root):
    f = pathlib.Path(xp(root)) / "03_TESTS_AND_READBACK" / "artifact_checksums.sha256"
    out = []
    for line in open(f, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        h, p = line.split(None, 1)
        out.append((p.strip().lstrip("*"), h.lower()))
    return out


def digest(root):
    e = sorted(entries(root))
    return hashlib.sha256(("\n".join(p + ":" + h for p, h in e)).encode()).hexdigest(), len(e)


ds, ns = digest(SUB)
dc, nc = digest(CAN)
print("subject   digest %s (%d entries)" % (ds[:16], ns))
print("canonical digest %s (%d entries)" % (dc[:16], nc))
print("checksum-list identical:", ds == dc)
print()

ok = bad = miss = 0
off = []
for p, h in entries(SUB):
    f = pathlib.Path(xp(SUB / p))
    if not f.exists():
        miss += 1
        off.append(("MISSING", p))
        continue
    d = hashlib.sha256(open(f, "rb").read()).hexdigest()
    if d == h:
        ok += 1
    else:
        bad += 1
        off.append(("DRIFT", p))
print("subject per-entry: match=%d drift=%d missing=%d" % (ok, bad, miss))
for k, p in off[:10]:
    print("  ", k, p)
print()

g = json.loads((SUB / "03_TESTS_AND_READBACK" / "wp_graph.json").read_text(encoding="utf-8"))
print("write_set histogram over all 22 WPs:", dict(collections.Counter(str(n.get("write_set")) for n in g["nodes"])))
print()

print("B5 evidence index present?")
for p in ["Fabric/evidence", "SBL/evidence", "HG-KSEOS/evidence"]:
    b = pathlib.Path("C:/Projects/Agent_Workspace") / p
    hits = sorted(x.name for x in b.glob("*R18*")) if b.is_dir() else []
    print("  %-18s exists=%s r18=%s" % (p, b.is_dir(), hits))
