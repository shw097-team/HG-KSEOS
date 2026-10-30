#!/usr/bin/env python3
"""review_lock — the maker may not move the subject while a checker is reading it.

Why this exists: on 2026-10-30 two independent checker sittings ended with
`ERR_CHECKER_MUTATED_SUBJECT` / `verdict_void_reason: the guarded subject changed during the turn`
because the maker committed into the guarded tree while the checker was running. The guard did its job
(it voided the verdict); the maker simply should not have been able to commit. Three rounds in a row
lost a checker verdict this way.

Mechanism (small on purpose):
  acquire --subject <path> --nonce <N>   record the subject and a live lock
  check --path <p> ...                   exit 1 if a live lock covers any path  (used by pre-commit)
  check --staged                         same, over `git diff --cached --name-only`
  release --nonce <N>                    drop the lock
  list                                   show live locks

A lock is a file under `var/review-locks/`. It dies with its TTL, so a crashed checker cannot wedge the
repository forever -- but a live lock refuses the commit, which is the point.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
LOCKS = ROOT / "var" / "review-locks"


def now() -> datetime:
    return datetime.now(timezone.utc)


def live() -> list[dict]:
    out = []
    if not LOCKS.is_dir():
        return out
    for p in sorted(LOCKS.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 - a corrupt lock must not block silently
            continue
        expires = datetime.fromisoformat(d["expires_at"])
        if expires > now():
            d["_path"] = str(p)
            out.append(d)
    return out


def covers(lock: dict, path: pathlib.Path) -> bool:
    subject = pathlib.Path(lock["subject"]).resolve()
    target = path.resolve()
    return target == subject or subject in target.parents


def cmd_acquire(args) -> int:
    subject = pathlib.Path(args.subject)
    if not subject.is_absolute():
        subject = (pathlib.Path.cwd() / subject).resolve()
    if not subject.exists():
        print(json.dumps({"ok": False, "code": "SUBJECT_MISSING", "subject": str(subject)}))
        return 2
    LOCKS.mkdir(parents=True, exist_ok=True)
    record = {
        "nonce": args.nonce,
        "pid": os.getpid(),
        "subject": str(subject),
        "reason": args.reason,
        "created_at": now().isoformat(timespec="seconds"),
        "expires_at": (now() + timedelta(minutes=args.ttl_min)).isoformat(timespec="seconds"),
    }
    (LOCKS / f"{args.nonce}.json").write_text(json.dumps(record, indent=1), encoding="utf-8")
    print(json.dumps({"ok": True, "lock": record}))
    return 0


def cmd_release(args) -> int:
    p = LOCKS / f"{args.nonce}.json"
    if p.exists():
        p.unlink()
        print(json.dumps({"ok": True, "released": args.nonce}))
        return 0
    print(json.dumps({"ok": True, "released": None, "note": "no such lock"}))
    return 0


def staged_paths() -> list[pathlib.Path]:
    r = subprocess.run(["git", "-C", str(ROOT), "diff", "--cached", "--name-only"],
                       capture_output=True, text=True)
    return [ROOT / line.strip() for line in r.stdout.splitlines() if line.strip()]


def cmd_check(args) -> int:
    paths = staged_paths() if args.staged else [pathlib.Path(p) for p in (args.path or [])]
    if not paths:
        return 0
    blocking = []
    for lock in live():
        hit = [str(p) for p in paths if covers(lock, p)]
        if hit:
            blocking.append({"nonce": lock["nonce"], "subject": lock["subject"],
                             "expires_at": lock["expires_at"], "paths": hit[:5]})
    if blocking:
        print(json.dumps({"ok": False, "code": "SUBJECT_UNDER_REVIEW", "locks": blocking},
                         ensure_ascii=False))
        for b in blocking:
            print(f"review_lock: {b['subject']} is being checked under {b['nonce']} until "
                  f"{b['expires_at']}; committing into it would void that checker's verdict", file=sys.stderr)
        return 1
    return 0


def _holder_alive(lock: dict) -> bool | None:
    """Is the PID that took this lock still running? Checked by PID, never by "is python running" --
    the reaper itself runs in python, so the coarse check would keep every lock forever."""
    pid = lock.get("pid")
    if not isinstance(pid, int):
        return None
    try:
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                             capture_output=True, text=True, timeout=20).stdout
        return str(pid) in out
    except Exception:  # noqa: BLE001
        return None


def cmd_reap(_args) -> int:
    """Remove locks whose holder is gone. A killed dispatcher used to leave a lock behind, and the
    pre-commit hook then refused legitimate commits -- the cure must not become the next outage."""
    reaped, kept = [], []
    for lock in live():
        alive = _holder_alive(lock)
        if alive is False:
            pathlib.Path(lock["_path"]).unlink(missing_ok=True)
            reaped.append(lock["nonce"])
        else:
            kept.append({"nonce": lock["nonce"], "holder_alive": alive})
    print(json.dumps({"reaped": reaped, "kept": kept}, ensure_ascii=False))
    return 0


def cmd_list(_args) -> int:
    print(json.dumps({"locks": live()}, ensure_ascii=False, indent=1))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="refuse maker commits into a subject under review")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("acquire"); a.add_argument("--subject", required=True)
    a.add_argument("--nonce", required=True); a.add_argument("--reason", default="checker reading the subject")
    a.add_argument("--ttl-min", type=int, default=120); a.set_defaults(fn=cmd_acquire)
    r = sub.add_parser("release"); r.add_argument("--nonce", required=True); r.set_defaults(fn=cmd_release)
    c = sub.add_parser("check"); c.add_argument("--path", action="append")
    c.add_argument("--staged", action="store_true"); c.set_defaults(fn=cmd_check)
    rp = sub.add_parser("reap"); rp.set_defaults(fn=cmd_reap)
    l = sub.add_parser("list"); l.set_defaults(fn=cmd_list)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
