"""O-1: classify the 516 files that exist on `origin/main` and nowhere in the r18 tree.

The handover called this a graft problem. It is not: `git merge-base origin/main HEAD` exits 1, so the two
trees share no history at all, and `--allow-unrelated-histories` would import 83 commits of a different
lineage rather than adopt 516 files. The decision therefore has to be per file, on content.

Rules, in order, each of which names the measurement that decided it (no file gets a verdict by category
alone):

  DUPLICATE_CONTENT   the same bytes exist at another path in HEAD  -> RETIRE (nothing to bring in)
  SAME_PATH_DIFFERS   the path exists in HEAD with different bytes  -> cannot happen for this set; recorded
  REFERENCED_BY_R18   the path (or its basename) is named by a text file in HEAD -> ADOPT
  TEST_OF_ABSENT_SUBJECT  under tests/ and its subject module is not in HEAD -> RETIRE
  HISTORY_ONLY        under evidence/ or a handoff body directory -> RETAIN (belongs to main's own record)
  OWNER_DECISION      none of the above -> the owner decides, with the file's own last author named

Usage:
    python scripts/o1_main_only_classify.py [--json out.json] [--tsv out.tsv]
"""
from __future__ import annotations

try:  # every child of this process must be consoleless; see scripts/winproc.py
    import winproc as _winproc  # noqa: E402
    _winproc.install()
except Exception:
    pass

import argparse
import hashlib
import json
import pathlib
import re
import subprocess
import sys
from collections import Counter, defaultdict

REPO = pathlib.Path(__file__).resolve().parents[1]
BASE = "origin/main"
HEAD = "HEAD"


def git(*args: str) -> str:
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True,
                       errors="replace", encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(f"GIT_FAILED {' '.join(args)}: {r.stderr.strip()[:300]}")
    return r.stdout


def blob_shas(rev: str) -> dict[str, str]:
    out = {}
    for line in git("ls-tree", "-r", rev).splitlines():
        meta, _, path = line.partition("\t")
        parts = meta.split()
        if len(parts) == 3 and parts[1] == "blob":
            out[path] = parts[2]
    return out


def last_author(path: str) -> str:
    try:
        line = git("log", "-1", "--format=%an|%ad|%h", BASE, "--", path).strip()
        return line
    except SystemExit:
        return ""


def text_index() -> str:
    """All text bytes reachable in HEAD, for the reference test. Binary files are skipped by extension."""
    out = subprocess.run(["git", "-C", str(REPO), "grep", "-I", "-h", "-e", "", HEAD],
                         capture_output=True, text=True, errors="replace", encoding="utf-8")
    return out.stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=str(REPO / "ops" / "session-20261031" / "FHS-ALLPASS-20261031"
                                          / "O1" / "MAIN_ONLY_CLASSIFICATION.json"))
    ap.add_argument("--tsv", default=str(REPO / "ops" / "session-20261031" / "FHS-ALLPASS-20261031"
                                         / "O1" / "MAIN_ONLY_CLASSIFICATION.tsv"))
    args = ap.parse_args()

    main_blobs = blob_shas(BASE)
    head_blobs = blob_shas(HEAD)
    head_sha_to_paths = defaultdict(list)
    for p, s in head_blobs.items():
        head_sha_to_paths[s].append(p)
    head_paths = set(head_blobs)
    main_only = sorted(set(main_blobs) - head_paths)
    common = sorted(set(main_blobs) & head_paths)

    corpus = text_index()
    rows = []
    for path in main_only:
        sha = main_blobs[path]
        name = path.rsplit("/", 1)[-1]
        stem = name.rsplit(".", 1)[0]
        row = {"path": path, "blob": sha, "bytes": None, "verdict": None, "why": None,
               "last_author": last_author(path)}
        if sha in head_sha_to_paths:
            row["verdict"] = "RETIRE"
            row["why"] = f"DUPLICATE_CONTENT: identical bytes at {head_sha_to_paths[sha][0]} in HEAD"
        elif path in corpus:
            row["verdict"] = "ADOPT"
            row["why"] = "REFERENCED_BY_R18: the exact path is named by a tracked text file in HEAD"
        elif len(stem) >= 8 and stem in corpus:
            row["verdict"] = "ADOPT"
            row["why"] = "REFERENCED_BY_R18: the basename stem is named by a tracked text file in HEAD"
        elif path.startswith("tests/"):
            subject = re.sub(r"^tests/", "", path)
            subject = re.sub(r"^test_", "", subject)
            row["verdict"] = "RETIRE"
            row["why"] = (f"TEST_OF_ABSENT_SUBJECT: no module matching {subject!r} is in HEAD, "
                          "so the test has no subject to check in this tree")
        elif path.startswith("evidence/") or path.startswith("fhs_msc_handoff_20261030/"):
            row["verdict"] = "RETAIN"
            row["why"] = ("HISTORY_ONLY: evidence/handoff body of main's own lineage; adopting it would "
                          "import another tree's record as if it were this tree's")
        else:
            row["verdict"] = "OWNER_DECISION"
            row["why"] = "no mechanical signal: not duplicated, not referenced, not a test, not evidence"
        rows.append(row)

    counts = Counter(r["verdict"] for r in rows)
    by_area = Counter(r["path"].split("/")[0] if "/" in r["path"] else "<root>" for r in rows)
    adoption_groups = Counter((r["path"].split("/")[0] if "/" in r["path"] else "<root>")
                              for r in rows if r["verdict"] == "ADOPT")

    doc = {
        "schema": "HGK-O1-MAIN-ONLY-CLASSIFICATION/1",
        "measured_from": {"base": BASE, "head": HEAD,
                          "base_files": len(main_blobs), "head_files": len(head_blobs),
                          "common_paths": len(common), "main_only": len(main_only),
                          "head_only": len(set(head_paths) - set(main_blobs)),
                          "merge_base": "NONE (unrelated histories: git merge-base exits 1)"},
        "rule": ("content first: identical bytes -> RETIRE; referenced by HEAD -> ADOPT; test of an absent "
                 "subject -> RETIRE; evidence/handoff body -> RETAIN; otherwise the owner decides"),
        "counts": dict(counts),
        "adopt_by_area": dict(adoption_groups),
        "files": rows,
    }
    out = pathlib.Path(args.json)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")

    tsv = pathlib.Path(args.tsv)
    with tsv.open("w", encoding="utf-8") as fh:
        fh.write("verdict\tpath\tblob\tlast_author\twhy\n")
        for r in rows:
            fh.write(f"{r['verdict']}\t{r['path']}\t{r['blob']}\t{r['last_author']}\t{r['why']}\n")

    print(json.dumps({"json": str(out), "tsv": str(tsv),
                      "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
                      "counts": dict(counts),
                      "adopt_by_area": dict(adoption_groups),
                      "denominator": len(rows)}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
