"""Open the R18 candidate PR via the GitHub REST API. Token read from the local PAT file; never printed."""
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

OWNER, REPO = "shw097-team", "HG-KSEOS"
HEAD, BASE = "candidate/r18-openspec-only", "main"
PAT = Path(r"C:\Projects\Agent_Workspace\API KEY\GITHUB-REPO_SHW097-4.txt").read_text(
    encoding="utf-8", errors="ignore")
TOKEN = re.search(r"(github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{30,})", PAT).group(1)

BODY = """## What

Adds the OpenSpec change `fhs-msc-skeleton-spine-revision2` and a publishable round-R18 evidence index.

Candidate-only: no config, no raw receipts, no credentials, no host paths.

## Measured (round R18, isolated copy of the byte-frozen revision2 package)

| Check | Result |
|---|---|
| Source freeze | 82 manifest rows, 83/83 digests, 84 ZIP members byte-identical, 22-node / 36-edge DAG |
| `tools/validate.py` as delivered | 2788 PASS / 1 FAIL (`SOURCE-BYTES-UNCHANGED`) |
| Same validator after repairing 29 stale source pins | 2789 PASS / 0 FAIL |
| 96-cell semantic oracle | 50 PASS_LOCAL_ORACLE / 46 HOLD / 0 FAIL, 679/0 — matches the claim |
| WP-level oracle traceability | 22/22 WPs unbacked (POS and NEG) |

## Defects recorded by the change

- **D-R18-01** — `source_manifest.json` pins 29 inputs in the superseded `_SKELETON_SPINE_DRAFT` tree, so the
  author's own `SOURCE-BYTES-UNCHANGED` check asserts that revision2 never happened. Repaired in the isolated
  copy (data only); the shipped package still carries it.
- **FAR-R18-05** — per-WP oracles in `wp_graph.json` have no backing case/cell/runner binding. Recorded, not
  synthesised.

## Claim ceiling

No native qualification, no independent acceptance, no release. The candidate's own scope string remains
`NOT_NATIVE_QUALIFICATION` with `native_case_pass = 0` and `independent_verdict = NOT_RUN`; this PR does not
raise that ceiling.
"""


def api(path, method="POST", payload=None):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{OWNER}/{REPO}{path}",
        data=json.dumps(payload).encode() if payload else None, method=method,
        headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28", "Content-Type": "application/json",
                 "User-Agent": "hermes-r18"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode()[:400]}


status, out = api("/pulls", payload={
    "title": "openspec: FHS-MSC Skeleton+Spine revision2 change + round R18 evidence index",
    "head": HEAD, "base": BASE, "body": BODY, "draft": False})
print("create:", status, out.get("html_url") or out.get("error"))
if status in (200, 201):
    Path(r"C:\Projects\Agent_Workspace\var\R18-FHS-SKELETON-SPINE-20261029\receipts\PR_HGK_R18.json"
         ).write_text(json.dumps({"status": status, "number": out.get("number"), "url": out.get("html_url"),
                                  "head": HEAD, "base": BASE, "title": out.get("title")},
                                 ensure_ascii=False, indent=1), encoding="utf-8")
