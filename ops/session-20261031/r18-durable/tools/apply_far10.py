"""FAR_R18-10 D1/D3/D4: canonical-owner gate, toolchain stamping, cross-session lock.

D1  the gate now refuses any delegation whose owner key is not the canonical owner identity
    (~/.hgk-owner, fingerprint prefix 412b3519). My R18 envelope is a second key: it stays on disk as
    evidence of the drill, but it can no longer authorise anything. --allow-noncanonical-owner exists
    only so the drill's own positive controls remain runnable, and it prints the refusal reason loudly.
D3  every claim that depends on the lane toolchain gets git HEAD + dirty recorded, because
    scripts/hgk-lane-dispatch.py is currently modified by another session and cannot be re-derived
    from a commit.
D4  a 30-line lock so two sessions cannot silently overwrite the same shared file.
"""
import json
import pathlib
import subprocess

ROUND = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029")
WS = pathlib.Path(r"C:\Projects\Agent_Workspace")
CANON_PREFIX = "412b3519"

# ---------------------------------------------------------------- D1: gate
g = ROUND / "tools" / "delegation_gate.py"
s = g.read_text(encoding="utf-8")
if "REFUSED_NONCANONICAL_OWNER" not in s:
    s = s.replace('''    ap.add_argument("--reason", default="")''',
                  '''    ap.add_argument("--reason", default="")
    ap.add_argument("--allow-noncanonical-owner", action="store_true",
                    help="drill only: run the gate with a non-canonical owner key so its own positive "
                         "controls stay exercisable. Never use this to claim authority.")''')
    s = s.replace('''    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(env["public_key_hex"]))''',
'''    canonical = str(env.get("fingerprint", "")).startswith(CANON_PREFIX)
    if not canonical and not a.allow_noncanonical_owner:
        out = {"schema": "R18.DELEGATION_GATE/1",
               "at_utc": datetime.now(timezone.utc).isoformat(),
               "wp": a.wp, "effect_class": a.cls, "target": a.target,
               "owner_fingerprint": env.get("fingerprint"),
               "canonical_owner_prefix": CANON_PREFIX,
               "decision": "REFUSED_NONCANONICAL_OWNER",
               "detail": ("this delegation is signed by a second owner key. The canonical owner identity is "
                          "~/.hgk-owner/owner.key.enc (fingerprint prefix %s). Re-sign under that key via the "
                          "existing owner window, or pass --allow-noncanonical-owner for a drill only." % CANON_PREFIX),
               "recorded": False}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 9
    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(env["public_key_hex"]))''')
    s = s.replace('''HARD_DENY = {''', '''CANON_PREFIX = "412b3519"

HARD_DENY = {''')
    g.write_text(s, encoding="utf-8")
    print("D1 gate patched: REFUSED_NONCANONICAL_OWNER")

# ---------------------------------------------------------------- D3: stamp
def git(repo, *args):
    try:
        p = subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True, text=True, timeout=60)
        return p.stdout.strip()
    except Exception as e:
        return "ERR:%s" % type(e).__name__

stamp = {"schema": "R18.CONCURRENCY_STAMP/1", "repos": {}}
for name, repo in [("HG-KSEOS", WS / "HG-KSEOS"), ("PIPD", WS / "PIPD"), ("Fabric", WS / "Fabric"),
                   ("SBL", WS / "SBL"), ("workspace", WS)]:
    if not (repo / ".git").exists() and not (repo / ".git").is_file():
        continue
    stamp["repos"][name] = {
        "head": git(repo, "rev-parse", "HEAD"),
        "branch": git(repo, "rev-parse", "--abbrev-ref", "HEAD"),
        "dirty_files": len([x for x in git(repo, "status", "--porcelain").splitlines() if x.strip()]),
        "lane_dispatcher_modified": bool(git(repo, "status", "--porcelain", "--", "scripts/hgk-lane-dispatch.py")),
    }
stamp["note"] = ("lane receipts produced while scripts/hgk-lane-dispatch.py is dirty are reproducible only "
                 "against this working tree, not against any commit")
(ROUND / "receipts" / "CONCURRENCY_STAMP.json").write_text(json.dumps(stamp, ensure_ascii=False, indent=1),
                                                           encoding="utf-8")
print("D3 stamp:", {k: (v["head"][:8], v["dirty_files"], v["lane_dispatcher_modified"])
                    for k, v in stamp["repos"].items()})

# ---------------------------------------------------------------- D4: lock tool
lock = ROUND / "tools" / "session_lock.py"
lock.write_text('''"""Cross-session lock: var/_locks/<area>.lock holds {session, purpose, ttl, created}.

Two sessions writing the same shared file silently is the failure this prevents. It is deliberately
dumb: a json file, a ttl, no daemon. acquire refuses if a live lock owned by someone else exists;
release deletes yours; status lists.
"""
import json, pathlib, sys, time

LOCKS = pathlib.Path(r"C:\\Projects\\Agent_Workspace\\var\\_locks")
SELF = "R18-20261029"


def _p(area):
    return LOCKS / (area.replace("/", "_") + ".lock")


def acquire(area, purpose, ttl_minutes=60):
    LOCKS.mkdir(parents=True, exist_ok=True)
    p = _p(area)
    if p.is_file():
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            d = {}
        live = d.get("expires_at", 0) > time.time()
        if live and d.get("session") != SELF:
            print(json.dumps({"acquired": False, "holder": d}, ensure_ascii=False))
            return 1
    d = {"session": SELF, "area": area, "purpose": purpose, "created": time.time(),
         "expires_at": time.time() + ttl_minutes * 60, "ttl_minutes": ttl_minutes}
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"acquired": True, "lock": str(p), "expires_in_minutes": ttl_minutes}, ensure_ascii=False))
    return 0


def release(area):
    p = _p(area)
    if p.is_file():
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            d = {}
        if d.get("session") == SELF:
            p.unlink()
            print(json.dumps({"released": area}))
            return 0
        print(json.dumps({"released": False, "held_by": d.get("session")}))
        return 1
    print(json.dumps({"released": False, "reason": "no lock"}))
    return 1


def status():
    out = []
    for p in sorted(LOCKS.glob("*.lock")) if LOCKS.is_dir() else []:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            d = {"unreadable": p.name}
        d["live"] = d.get("expires_at", 0) > time.time()
        out.append(d)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: session_lock.py acquire <area> <purpose> [ttl_min] | release <area> | status")
    cmd = sys.argv[1]
    if cmd == "acquire":
        sys.exit(acquire(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "-",
                         int(sys.argv[4]) if len(sys.argv) > 4 else 60))
    if cmd == "release":
        sys.exit(release(sys.argv[2]))
    sys.exit(status())
''', encoding="utf-8")
print("D4 lock tool written")
