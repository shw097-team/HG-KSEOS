"""Probe the local Issuer path on a COPY of the spine DB.

FAR_R18-12 Q6 concluded that the 12 HOST_OP/RELEASE rows are not blocked on a second human: the Issuer is
local software and `authorize()` needs only {references, lease_generation}. This probe establishes what a
PERMIT actually requires, by trying the smallest legal path on a throwaway copy of the spine and recording
either a PERMIT or the exact typed refusal. It never touches the canonical DB.
"""
import json
import pathlib
import shutil
import sqlite3
import sys
import time
import traceback

HGK = pathlib.Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
SRC_DB = HGK / "var" / "shared-spine" / "hg-kseos.db"
COPY = ROUND / "scratch_spine_probe.db"
sys.path.insert(0, str(HGK / "src"))

out = {"kind": "R18.ISSUER_PATH_PROBE/1", "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
shutil.copyfile(SRC_DB, COPY)
out["db_copy"] = str(COPY)

conn = sqlite3.connect(COPY)
conn.row_factory = sqlite3.Row
tables = [r[0] for r in conn.execute("select name from sqlite_master where type='table'")]
out["tables"] = tables
for t in tables:
    if any(k in t for k in ("lease", "permit", "admission", "requirement", "nonce")):
        cols = [r[1] for r in conn.execute("pragma table_info(%s)" % t)]
        n = conn.execute("select count(*) from %s" % t).fetchone()[0]
        out.setdefault("tables_schema", {})[t] = {"columns": cols, "rows": n}

try:
    from hg_kseos import native_admission as na
    out["import"] = "ok"
    out["authorize_signature"] = str(__import__("inspect").signature(na.authorize))
except Exception:
    out["import"] = "failed"
    out["import_trace"] = traceback.format_exc()[-600:]

# smallest legal bundle: references must resolve, so probe with an empty reference set to learn the order of
# the refusals rather than to obtain a permit by accident.
try:
    from hg_kseos.spine import SharedSpine
    sp = SharedSpine(str(COPY))
    out["spine"] = "opened"
    for name in ("acquire_lease", "register_requirement", "transition_requirement"):
        out.setdefault("spine_api", {})[name] = str(__import__("inspect").signature(getattr(sp, name)))
    lease = sp.acquire_lease("FHS-MSC-R18-20261029", "ISSUER_PATH_PROBE", 60)
    out["lease"] = lease if isinstance(lease, (str, int, dict)) else str(lease)
except Exception:
    out["lease_error"] = traceback.format_exc().strip().splitlines()[-1][:300]

try:
    probe_conn = sqlite3.connect(COPY)
    from hg_kseos import native_admission as na
    na.authorize(probe_conn, "PROBE_HOST_OP", {"wp": "WP-FHS-02", "subject": "5a06d8dd"},
                 {"references": [], "lease_generation": 0})
    out["authorize_result"] = "PERMIT_OR_UNEXPECTED_SUCCESS"
except Exception as e:
    out["authorize_result"] = "TYPED_REFUSAL"
    out["authorize_error"] = "%s: %s" % (type(e).__name__, str(e)[:300])

conn.close()
(REC := ROUND / "receipts" / "ISSUER_PATH_PROBE.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                                                 encoding="utf-8")
print(json.dumps({k: out[k] for k in ("kind", "tables", "authorize_result", "authorize_error", "lease_error")
                  if k in out}, ensure_ascii=False)[:800])
