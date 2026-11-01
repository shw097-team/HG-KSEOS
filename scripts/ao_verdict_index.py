"""Every independent sitting, from the files, newest last — because the shared aggregate got overwritten.

`run_ao_batch.py` wrote one `AO_BATCH.json` per invocation, and three invocations overlapped: the WP-12 re-sit
finished last and replaced the file, taking the WP-11 PASS sitting with it even though that sitting's reply and
receipt were still on disk. An aggregate that any later run can replace is not a record.

This index is built only from the immutable per-sitting artefacts (`AO_REPLY_<nonce>.md`, `AO_RECEIPT_<nonce>.json`)
and is written to a path the dispatch never touches. For each WP it lists every sitting in time order with the
nonce, the served arm, the rank, the usage receipt and the checker's own verdict block, so the transition is
visible: WP-11 FAIL, FAIL, PASS — not "PASS" with the earlier refusals missing.

Usage:
    python scripts/ao_verdict_index.py --json ops/session-20261031/FHS-ALLPASS-20261031/AO_VERDICTS.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import time

SESSION = pathlib.Path(__file__).resolve().parents[1] / "ops" / "session-20261031" / "FHS-ALLPASS-20261031"


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def verdict_block(text: str) -> dict | None:
    blocks, cur, inside = [], [], False
    for line in text.splitlines():
        if line.strip().startswith("```json"):
            inside, cur = True, []
            continue
        if inside and line.strip().startswith("```"):
            inside = False
            blocks.append("\n".join(cur))
            continue
        if inside:
            cur.append(line)
    for b in reversed(blocks):
        try:
            return json.loads(b)
        except ValueError:
            continue
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=str(SESSION / "AO_VERDICTS.json"))
    args = ap.parse_args()

    sittings = []
    for wpdir in sorted(p for p in SESSION.glob("WP-FHS-*") if p.is_dir()):
        for reply in sorted(wpdir.glob("AO_REPLY_AO-*.md")):
            nonce = re.sub(r"^AO_REPLY_|\.md$", "", reply.name)
            rec_path = wpdir / f"AO_RECEIPT_{nonce}.json"
            rec = {}
            if rec_path.is_file():
                try:
                    rec = json.loads(rec_path.read_text(encoding="utf-8"))
                except ValueError:
                    rec = {}
            att = (rec.get("attempts") or [{}])[-1]
            vb = verdict_block(reply.read_text(encoding="utf-8", errors="replace")) or {}
            sittings.append({
                "wp": wpdir.name,
                "nonce": nonce,
                "reply": str(reply),
                "reply_sha256": sha(reply),
                "receipt": str(rec_path) if rec_path.is_file() else None,
                "mtime": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(reply.stat().st_mtime)),
                "dispatch_ok": rec.get("ok"),
                "served_arm": rec.get("served_arm") or (f"{att.get('provider')}/{att.get('model')}"
                                                        if att.get("model") else None),
                "rank": att.get("rank"),
                "nonce_present": att.get("nonce_present"),
                "usage_receipt_ok": rec.get("usage_receipt_ok"),
                "checker_overall": vb.get("overall"),
                "clauses": [{"id": c.get("id"), "verdict": c.get("verdict")} for c in vb.get("clauses", [])],
            })

    by_wp: dict[str, list] = {}
    for s in sorted(sittings, key=lambda x: x["mtime"]):
        by_wp.setdefault(s["wp"], []).append(s)

    summary = {wp: {"sittings": len(v), "sequence": [s["checker_overall"] for s in v],
                    "latest": v[-1]["checker_overall"], "latest_nonce": v[-1]["nonce"],
                    "distinct_principal_from_maker": any(
                        (s.get("served_arm") or "").split("/")[0] not in ("opencode-go",) for s in v)}
               for wp, v in by_wp.items()}

    doc = {"schema": "HGK-AO-VERDICTS/1", "at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
           "rule": ("built only from per-sitting reply and receipt files; a later batch cannot overwrite it because "
                    "no dispatch writes this path. The sequence is kept so a PASS cannot hide the sittings that "
                    "refused before it"),
           "summary": summary, "sittings": [s for v in by_wp.values() for s in v]}
    out = pathlib.Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"json": str(out), "sha256": sha(out), "summary": summary}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
