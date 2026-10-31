"""Cross-session lock: var/_locks/<area>.lock holds {session, purpose, ttl, created}.

Two sessions writing the same shared file silently is the failure this prevents. It is deliberately
dumb: a json file, a ttl, no daemon. acquire refuses if a live lock owned by someone else exists;
release deletes yours; status lists.
"""
import json, pathlib, sys, time

LOCKS = pathlib.Path(r"C:\Projects\Agent_Workspace\var\_locks")
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
