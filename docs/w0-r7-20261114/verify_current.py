"""Verify the W0 current set is intact. Run from FHS_NEXT/:
    python deliverables/FHS_vNEXT_PLP_W0/verify_current.py
Exit 0 = current unchanged; exit 1 = drift (prints which).
"""
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
CUR = json.loads((HERE / "CURRENT.json").read_text(encoding="utf-8"))
bad = []


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


for d in CUR["documents"]:
    p = HERE / d["name"]
    if not p.is_file():
        bad.append(f"MISSING {d['name']}")
        continue
    got = sha(p)
    if got != d["sha256"]:
        bad.append(f"DRIFT {d['name']} {got[:16]} != {d['sha256'][:16]}")

r9 = HERE / CUR["current_document"]["name"]
b = r9.read_bytes()
s = b.find(b"<!-- BEGIN R8-RETAINED-BYTES")
s = b.find(b"\n", s) + 1
e = b.find(b"<!-- END R8-RETAINED-BYTES")
r8 = (pathlib.Path(__file__).resolve().parents[2] / CUR["base_document"]["path"]).read_bytes()
if b[s:e] != r8:
    bad.append("EMBEDDED_R8_MISMATCH")
if hashlib.sha256(r8).hexdigest() != CUR["base_document"]["sha256"]:
    bad.append("BASE_R8_CHANGED")

print(json.dumps({
    "current": CUR["delivery_revision"],
    "state": CUR["state"],
    "documents": len(CUR["documents"]),
    "r9_sha256": sha(r9),
    "r8_embedded_identical": b[s:e] == r8,
    "delta_count": b.count(b"### DELTA-"),
    "drift": bad,
    "verdict": "PASS" if not bad else "FAIL",
}, ensure_ascii=False, indent=1))
sys.exit(0 if not bad else 1)
