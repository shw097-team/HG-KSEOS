"""WP-FHS-05: drive the ORIGINAL PIPD compiler (pipd_ls_sp 0.1.1a4) to emit PI/PD/ECP/TQAEP
candidates into an isolated output root, then record exact commands, exit codes and artifact
digests. No hand-written artefact: every file below is written from the compiler's own stdout.

Negative controls (WP-FHS-05 negative: "sidecar塞strict payload或expected當Raw"):
  N1  a card whose strict payload carries an `expected` field must be refused or must not leak
      that value into the PI's strict payload
  N2  a PI carrying a sidecar key must not have the sidecar promoted into the strict package
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

SRC = pathlib.Path(r"C:\Projects\Agent_Workspace\PIPD_closure_20261029\src")
OUT = pathlib.Path(r"C:\Projects\Agent_Workspace\var\R19-FHS-20261029\pipd_out")
PKG = pathlib.Path(r"C:\Projects\Agent_Workspace\知識庫\實作相關DOC\Fabric vNext\Semantic World OS Fabric\SBL_PIPD\FHS-MSC\FHS-MSC_PIPD-LS-PKG\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE\FHS-MSC_PIPD-LS-PKG_SKELETON_SPINE_REPAIRED_2026-10-29_r2-revision2")


def run(argv: list[str], cwd: pathlib.Path) -> dict:
    env = dict(os.environ, PYTHONPATH=str(SRC), PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-B", "-m", "pipd_ls_sp.cli", "--root", str(OUT)] + argv,
                       cwd=str(cwd), capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    try:
        payload = json.loads(p.stdout[p.stdout.index("{"):])
    except Exception:
        payload = None
    return {"argv": ["pipd"] + argv, "rc": p.returncode, "json": payload,
            "stdout_tail": p.stdout[-400:], "stderr_tail": p.stderr[-400:]}


def dump(name: str, obj) -> pathlib.Path:
    p = OUT / name
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    steps: list[dict] = []

    r = run(["init"], OUT); steps.append({**r, "step": "init"})

    sources = [str(PKG / "01_BODY"), str(PKG / "02_EVIDENCE_APPENDICES"), str(PKG / "03_TESTS_AND_READBACK" / "wp_graph.json")]
    argv = ["intake", "--goal", "FHS-MSC Skeleton+Spine r2-revision2 實作與檢驗（WP-FHS-00..21 typed DAG）"]
    for s in sources:
        argv += ["--source", s]
    argv += ["--constraint", "sources are read-only; candidate-only writes inside the isolated output root",
             "--non-goal", "no release, no promotion, no main-merge"]
    r = run(argv, OUT); steps.append({**r, "step": "intake"})
    if not r["json"]:
        print("intake produced no JSON; abort", r["stdout_tail"], r["stderr_tail"]); return 1
    card = dump("intent_card.json", r["json"])

    r = run(["profile", "--profile", "LITE"], OUT); steps.append({**r, "step": "profile"})

    r = run(["compile-pi", "--intent", str(card), "--profile", "LITE", "--replay", "--explain"], OUT)
    steps.append({**r, "step": "compile-pi"})
    if not r["json"]:
        print("compile-pi failed", r["stdout_tail"], r["stderr_tail"]); return 2
    pi = dump("pi.json", r["json"])

    r = run(["bind-pd", "--pi", str(pi), "--repo-root", r"C:\Projects\Agent_Workspace\PIPD_closure_20261029"], OUT)
    steps.append({**r, "step": "bind-pd"})
    if not r["json"]:
        print("bind-pd failed", r["stdout_tail"], r["stderr_tail"]); return 3
    pd = dump("pd.json", r["json"])

    r = run(["compile-ecp", "--pd", str(pd), "--pi", str(pi), "--explain"], OUT)
    steps.append({**r, "step": "compile-ecp"})
    ecp = dump("ecp.json", r["json"]) if r["json"] else None

    # negative controls ------------------------------------------------------
    neg = []
    # N1: strict payload carrying an `expected` value
    bad = json.loads(card.read_text(encoding="utf-8"))
    bad_strict = dict(bad)
    bad_strict["expected"] = {"verdict": "PASS", "tests": "all"}
    bad_strict["goal"] = bad.get("goal")
    p_bad = dump("intent_card_with_expected.json", bad_strict)
    r = run(["compile-pi", "--intent", str(p_bad), "--profile", "LITE"], OUT)
    leaked = None
    if r["json"]:
        strict = {k: v for k, v in r["json"].items() if k != "sidecar"}
        leaked = "expected" in json.dumps(strict)
    neg.append({"case": "N1_expected_in_strict_input", "rc": r["rc"],
                "expected_value_leaked_into_pi_strict": leaked,
                "refused_or_quarantined": bool(leaked is False or r["rc"] != 0),
                "detail": (r["json"] or {}).get("verdict") if r["json"] else r["stderr_tail"][-200:]})

    # N2: sidecar key inside the PI input must not be promoted to strict
    pi_obj = json.loads(pi.read_text(encoding="utf-8"))
    pi_obj["sidecar"] = {"claim": "PASS", "injected": True}
    p_side = dump("pi_with_sidecar.json", pi_obj)
    r = run(["compile-ecp", "--pd", str(pd), "--pi", str(p_side)], OUT)
    promoted = None
    if r["json"]:
        promoted = "injected" in json.dumps({k: v for k, v in r["json"].items() if k != "sidecar"})
    neg.append({"case": "N2_sidecar_promoted_to_strict", "rc": r["rc"],
                "sidecar_value_promoted": promoted,
                "refused_or_quarantined": bool(promoted is False or r["rc"] != 0),
                "verdict": (r["json"] or {}).get("verdict") if r["json"] else r["stderr_tail"][-200:]})

    arts = {}
    for p in (card, pi, pd, ecp):
        if p is not None and p.is_file():
            arts[p.name] = {"sha256": sha(p), "bytes": p.stat().st_size}

    pi_obj_clean = json.loads(pi.read_text(encoding="utf-8"))
    receipt = {
        "schema": "R19.WP05_PIPD_WRITER_RECEIPT/1",
        "at": datetime.now(timezone.utc).isoformat(),
        "writer": {"package": "pipd_ls_sp", "version": "0.1.1a4",
                   "entry": "python -m pipd_ls_sp.cli", "source_root": str(SRC),
                   "writer_is_original_product": True},
        "output_root_isolated": str(OUT),
        "intent_subject_id": (json.loads(card.read_text(encoding='utf-8')) or {}).get("subject_id"),
        "pi_subject_id": pi_obj_clean.get("subject_id"),
        "pi_replay": pi_obj_clean.get("replay"),
        "artifacts": arts,
        "steps": steps,
        "negative_controls": neg,
        "ack_basis": ("the artefacts above are the compiler's own output; the receipt binds command, "
                      "exit code and sha256. This is a WRITER PRODUCTION ACK, not a promotion ACK and "
                      "not an independent acceptance."),
        "claim_ceiling": "CANDIDATE_ONLY: PI/PD/ECP produced by the original writer into an isolated "
                         "output root; no native effect, no promotion, no independent PASS",
    }
    pathlib.Path(r"C:\Projects\Agent_Workspace\var\R19-FHS-20261029\receipts").mkdir(parents=True, exist_ok=True)
    (OUT / "writer_receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    (pathlib.Path(r"C:\Projects\Agent_Workspace\var\R19-FHS-20261029\receipts") / "WP05_PIPD_WRITER_RECEIPT.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"artifacts": arts, "pi_replay": receipt["pi_replay"],
                      "negatives": [{k: n[k] for k in ("case", "rc", "refused_or_quarantined")} for n in neg]},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
