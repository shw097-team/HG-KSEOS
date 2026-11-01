"""P5 repo readback: prove that what GitHub holds for the PR head equals the
bounded WriteSet that was staged locally.

Read-only. Never prints the token. Writes a receipt JSON.

Checks
  R1  PR exists, is open, head sha == the commit under test, base branch declared
  R2  the remote ref for the head branch resolves to the same commit
  R3  GitHub's recursive tree for that commit lists exactly the expected paths
      (no extra files, nothing missing)
  R4  every blob sha in GitHub's tree equals the local git blob sha (git object
      identity: proves the stored bytes are the committed bytes)
  R5  full content readback: each blob is downloaded from the API, decoded, and
      its sha256 compared with the local file's sha256
  R6  the compare main...head is additive-only (no modified / deleted / renamed)
"""
import base64
import hashlib
import json
import subprocess
import sys
import urllib.error
import urllib.request

TOKEN_FILE = r"C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt"
API = "https://api.github.com"
OWNER = "shw097-team"
REPO = "HG-KSEOS"
BRANCH = "fhs-msc-handoff-patch-v1-exec-20261030"
LOCAL_REPO = r"C:/wg/repo"
SCOPES = ["fhs_msc_handoff_20261030", "openspec/changes/fhs-msc-handoff-patch-v1-exec"]
OUT = sys.argv[1] if len(sys.argv) > 1 else "p5d_receipt.json"


def token():
    with open(TOKEN_FILE, "r", encoding="utf-8") as fh:
        return fh.read().strip()


def api(path):
    url = path if path.startswith("http") else API + path
    req = urllib.request.Request(url, method="GET")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("Authorization", "Bearer " + token())
    req.add_header("User-Agent", "hgk-p5-readback")
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())


def git(*args, binary=False):
    out = subprocess.run(["git", "-C", LOCAL_REPO, *args], capture_output=True, check=True)
    return out.stdout if binary else out.stdout.decode("utf-8", "replace")


def main():
    head = git("rev-parse", "HEAD").strip()
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    receipt = {
        "schema": "FHS-MSC-HANDOFF-EXEC-REPO-READBACK/1",
        "round": "FHS-MSC-HANDOFF-PATCH-v1-EXEC-20261030",
        "repo": f"{OWNER}/{REPO}",
        "local_repo": LOCAL_REPO,
        "local_branch": branch,
        "commit_read": head,
        "claim_ceiling": "author-side static; this receipt proves storage fidelity, not acceptance",
    }
    fails = []

    # R1 / R2 -----------------------------------------------------------------
    prs = api(f"/repos/{OWNER}/{REPO}/pulls?state=all&head={OWNER}:{BRANCH}")
    pr = next((p for p in prs if p["head"]["sha"] == head), None)
    remote_ref = [l.split()[0] for l in git("ls-remote", "--heads", "origin", BRANCH).splitlines()]
    r1 = {
        "pr_number": pr["number"] if pr else None,
        "pr_state": pr["state"] if pr else None,
        "pr_url": pr["html_url"] if pr else None,
        "pr_head_sha": pr["head"]["sha"] if pr else None,
        "pr_base_ref": pr["base"]["ref"] if pr else None,
        "pr_base_sha": pr["base"]["sha"] if pr else None,
        "pr_draft": pr["draft"] if pr else None,
        "pr_merged": bool(pr["merged_at"]) if pr else None,
        "pr_head_sha_equals_local_head": bool(pr) and pr["head"]["sha"] == head,
        "remote_ref_sha": remote_ref[0] if remote_ref else None,
        "remote_ref_equals_local_head": bool(remote_ref) and remote_ref[0] == head,
        "verdict": "PASS" if (pr and pr["state"] == "open" and pr["head"]["sha"] == head
                              and remote_ref and remote_ref[0] == head) else "FAIL",
    }
    if r1["verdict"] != "PASS":
        fails.append("R1")
    receipt["R1_pr_and_ref"] = r1

    # R3 ----------------------------------------------------------------------
    local_paths = sorted(
        p for p in git("ls-tree", "-r", "--name-only", head).splitlines() if p
    )
    scoped_local = [p for p in local_paths if any(p == s or p.startswith(s + "/") for s in SCOPES)]
    tree = api(f"/repos/{OWNER}/{REPO}/git/trees/{head}?recursive=1")
    if tree.get("truncated"):
        fails.append("R3")
    scoped_remote = {
        e["path"]: e for e in tree["tree"]
        if e["type"] == "blob" and any(e["path"] == s or e["path"].startswith(s + "/") for s in SCOPES)
    }
    missing = [p for p in scoped_local if p not in scoped_remote]
    extra = sorted(p for p in scoped_remote if p not in set(scoped_local))
    r3 = {
        "scopes": SCOPES,
        "local_paths_in_scope": len(scoped_local),
        "remote_blobs_in_scope": len(scoped_remote),
        "total_blobs_in_commit": sum(1 for e in tree["tree"] if e["type"] == "blob"),
        "local_paths_in_whole_commit": len(local_paths),
        "missing_remote": missing,
        "extra_remote": extra,
        "verdict": "PASS" if not missing and not extra else "FAIL",
    }
    if r3["verdict"] != "PASS":
        fails.append("R3")
    receipt["R3_tree_shape"] = r3

    # R4 ----------------------------------------------------------------------
    local_blob = {}
    for line in git("ls-tree", "-r", head).splitlines():
        meta, path = line.split("\t", 1)
        mode, otype, sha = meta.split()
        local_blob[path] = sha
    r4_mismatch = []
    for path in scoped_local:
        remote_sha = scoped_remote.get(path, {}).get("sha")
        if local_blob[path] != remote_sha:
            r4_mismatch.append({"path": path, "local": local_blob[path], "remote": remote_sha})
    r4 = {
        "compared": len(scoped_local),
        "mismatch": r4_mismatch,
        "verdict": "PASS" if not r4_mismatch and len(scoped_local) == len(scoped_remote) else "FAIL",
    }
    if r4["verdict"] != "PASS":
        fails.append("R4")
    receipt["R4_git_blob_identity"] = r4

    # R5 ----------------------------------------------------------------------
    readback = []
    r5_bad = []
    for path in scoped_local:
        blob = api(f"/repos/{OWNER}/{REPO}/git/blobs/{scoped_remote[path]['sha']}")
        raw = base64.b64decode(blob["content"])
        with open(f"{LOCAL_REPO}/{path}", "rb") as fh:
            local = fh.read()
        remote_sha256 = hashlib.sha256(raw).hexdigest()
        local_sha256 = hashlib.sha256(local).hexdigest()
        # git blob identity recomputed from the downloaded bytes
        git_obj = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
        row = {
            "path": path,
            "bytes": len(raw),
            "sha256_remote": remote_sha256,
            "sha256_local": local_sha256,
            "git_blob_recomputed": git_obj,
            "git_blob_expected": local_blob[path],
        }
        row["ok"] = (
            remote_sha256 == local_sha256 and git_obj == local_blob[path] and len(raw) == len(local)
        )
        if not row["ok"]:
            r5_bad.append(path)
        readback.append(row)
    r5 = {
        "blobs_downloaded": len(readback),
        "bytes_total": sum(r["bytes"] for r in readback),
        "sha256_matched": sum(1 for r in readback if r["ok"]),
        "mismatch": r5_bad,
        "verdict": "PASS" if not r5_bad and len(readback) == len(scoped_local) else "FAIL",
    }
    if r5["verdict"] != "PASS":
        fails.append("R5")
    receipt["R5_content_readback"] = r5
    receipt["R5_blobs"] = readback

    # R6 ----------------------------------------------------------------------
    cmp = api(f"/repos/{OWNER}/{REPO}/compare/main...{head}")
    statuses = {}
    for f in cmp["files"]:
        statuses[f["status"]] = statuses.get(f["status"], 0) + 1
    non_additive = [f["filename"] for f in cmp["files"] if f["status"] != "added"]
    r6 = {
        "base": "main",
        "ahead_by": cmp["ahead_by"],
        "behind_by": cmp["behind_by"],
        "files_changed": len(cmp["files"]),
        "statuses": statuses,
        "non_additive": non_additive,
        "merge_base_sha": cmp["merge_base_commit"]["sha"],
        "commits": [
            {"sha": c["sha"], "message": c["commit"]["message"].splitlines()[0],
             "author": c["commit"]["author"]["name"], "date": c["commit"]["author"]["date"]}
            for c in cmp["commits"]
        ],
        "verdict": "PASS" if not non_additive and statuses.get("added") == len(cmp["files"]) else "FAIL",
    }
    if r6["verdict"] != "PASS":
        fails.append("R6")
    receipt["R6_additive_only"] = r6

    receipt["overall"] = "PASS" if not fails else "FAIL"
    receipt["failed_checks"] = fails
    receipt["next_owner_action"] = (
        "review PR and merge by owner; merge, tag and release remain owner-only"
    )
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(json.dumps({
        "overall": receipt["overall"],
        "failed": fails,
        "pr": [r1["pr_number"], r1["pr_state"], r1["pr_url"]],
        "commit": head,
        "paths": r3["local_paths_in_scope"],
        "blobs_read_back": r5["blobs_downloaded"],
        "bytes_read_back": r5["bytes_total"],
        "additive_files": r6["files_changed"],
        "out": OUT,
    }, indent=1))
    return 0 if receipt["overall"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
