# Implementation index and discardable-layer audit — 2026-10-31

Purpose: answer one question honestly — **is any implementation living only somewhere that can be deleted
without anyone noticing?** Measured, not asserted.

## 1. Where each piece now lives

| piece | canonical (durable) copy | working copy | verdict |
|---|---|---|---|
| `sign_r21_amendment.py` | `ops/session-20261031/tools/` | `var/R18-…/tools/` (gitignored) | durable |
| `owner_window.py` with `close --force` | `ops/session-20261031/tools/` | `var/B1-PIPD-PKG-20261027/` (gitignored) | durable |
| R21 delegation + signature + receipt | `ops/session-20261031/receipts/` | `var/R18-…/governance/` | durable |
| R18 delegation receipt (`f5ebdd5f`) | `ops/session-20261031/receipts/` | `var/R18-…/receipts/` | durable |
| window force-close receipt | `ops/session-20261031/receipts/` | `~/.hgk-owner/artifacts/` | durable |
| R18 round receipts / governance / tools (117 files, 2.8 MB) | `ops/session-20261031/r18-durable/` | `var/R18-…/` (1.0 GB round) | durable subset |
| subject body manifest (83 files + digests) | `ops/session-20261031/r18-durable/artifact_checksums.sha256` | `var/R18-…/subject/` | digest-bound, see §2 |
| WP-FHS-17 officer / builder / reproduce fixes | `ops/session-20261031/queue-patches/` **and** queue repo commit `3fca7b9` | `/c/wg/queue` | durable (two copies) |
| FAR-028 / 029 / 030 | Fabric repo, pushed (`2527b81`, `31a97ed`, `325e4fe`) | — | durable |
| F3 console-window gate + delta wiring | HG-KSEOS commit `440cb34` | — | durable |

## 2. Things that are still outside version control, and why that is survivable

| location | size | what it is | why it is not in git | binding |
|---|---|---|---|---|
| `知識庫/…/FHS-MSC_PIPD-LS-PKG_2026-10-30_HANDOFF-PATCH-v1` | 228 MB / 917 files | the **frozen subject** (the spec body the packages are judged against) | too large; it is an input, not an artefact | its digest `subject_digest_sha256 = 5a06d8dd…` is inside every signed delegation, and `artifact_checksums.sha256` (83 entries) is now copied into `r18-durable/` |
| `var/R18-FHS-SKELETON-SPINE-20261029` | 1.0 GB | round working tree: subject copies, build outputs, receipts | gitignored by design (`var/`) | receipts + governance + tools copied (2.8 MB); subject digest ties the rest |
| `var/B1-PIPD-PKG-20261027` | 759 MB | earlier round, holds the owner-window tool | gitignored by design | the tool itself is copied; the rest is historical |
| `/c/wg/queue` | 81 MB (+2.6 MB bundle) | the 22-package queue and every lane receipt | **has no git remote** | committed locally at `3fca7b9` (0 uncommitted) **and** bundled to `C:\wg\queue-20261031.bundle`, sha256 `a3f2c03bf413…` |

**The honest answer to "was anything dumped into a discardable layer":** yes, three things were, and all
three are now mirrored into a tracked path or digest-bound:

1. the two signing tools lived only in `var/` → copied to `ops/session-20261031/tools/`;
2. the R21/R18 delegations and the force-close receipt lived only in `var/` and `~/.hgk-owner/` → copied to
   `ops/session-20261031/receipts/`;
3. the WP-FHS-17 repairs lived only in `/c/wg/queue`, which has **no remote** → copied to
   `ops/session-20261031/queue-patches/` *and* committed in the queue repo, *and* bundled.

What is **not** claimed: the 228 MB subject and the 1 GB `var/` rounds are not backed up. They are inputs and
build output. If that disk dies, the spec body is gone unless the owner has another copy — that is a finding,
not something a commit can fix.

## 3. One defect found while doing this audit

`WP-FHS-11/build/nul.txt` — `nul` is a reserved DOS device name, so `git add` fails on it with
`open(...): No such file or directory` and **the entire queue commit is rejected**. That is why 279 files sat
uncommitted. Removed with the `\\?\` prefix; the queue now commits clean. Any future package that writes a
file literally named `nul`/`con`/`aux` will reproduce this.

## 4. Verification commands (re-runnable by a new session)

```bash
cd /c/Projects/Agent_Workspace/HG-KSEOS && git log --oneline -5 && git status --porcelain
cd /c/wg/queue && git log --oneline -1 && git status --porcelain | wc -l    # expect 3fca7b9, 0
cd /c/Projects/Agent_Workspace/Fabric && git log --oneline -1               # expect d3a13b1
python -c "import json;d=json.load(open(r'C:/Projects/Agent_Workspace/HG-KSEOS/ops/session-20261031/receipts/R21_signing_receipt.json',encoding='utf-8'));print(d['signature_verifies'], d['wp_allowlist'])"
sha256sum /c/wg/queue-20261031.bundle | cut -c1-16                        # expect a3f2c03bf413
```

## 5. Close-out stamp

| repo | head | tree | pushed |
|---|---|---|---|
| HG-KSEOS (`candidate/r18-fhs-skeleton-spine-20261029`) | **`287c8df`** | clean (0 changes) | branch + tag **`candidate-r21-20261031`** |
| Fabric (`pub/far-minimax-mandate-20261021`) | **`d3a13b1`** | 6 entries left, all deliberate (below) | yes |
| `/c/wg/queue` (`master`) | **`3fca7b9`** | clean (0 changes) | **no remote** — bundled instead |

Deliberately left dirty in Fabric, each with a reason rather than a shrug:

| entry | size | why not in this close-out |
|---|---|---|
| `fabric-autonomous-research/methods/` | 62 MB | not this session's work; committing 62 MB of methods without reviewing them would be a bulk dump, not a record |
| `stage/` | 95 MB | staging tree, not evidence |
| `Fabric-rebind-publish/` | 70 MB | build output of an earlier round |
| `_far_commit_msg.txt` | 1.3 KB | temp message file from an earlier commit |
| `W3-SWOF-R153-01.owner-attested.json`, `Fabric使用說明文檔.md` | 9 / 702 lines changed | another session's pending edits; not mine to commit |

The three large trees are the only substantial unversioned material left on this host besides the 228 MB frozen
subject and the 1 GB `var/` rounds. That is stated, not hidden.
