import hashlib
import os
import shutil
import sys

BS = chr(92)


def xp(p):
    p = p.replace("/", BS)
    return p if p.startswith(BS * 2 + "?") else BS * 2 + "?" + BS + p


root = sys.argv[1]
dst_root = sys.argv[2]
rel = sys.argv[3]
src = os.path.join(root, rel.replace("/", BS))
dst = os.path.join(dst_root, rel.replace("/", BS))
shutil.copyfile(xp(src), dst)
h = hashlib.sha256()
with open(dst, "rb") as f:
    for c in iter(lambda: f.read(1 << 20), b""):
        h.update(c)
print("copied", os.path.getsize(dst), h.hexdigest())
