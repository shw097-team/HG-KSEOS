#!/usr/bin/env python3
"""Run one FAR round through all three lanes, in order, and write the receipts.

Why this exists. Nine FAR runs (036-044) were published with nothing but a ResearchSynthesis.md, and `--lane PLAN`
appeared zero times across the engagement. Two explanations were tested and both were wrong:

  * "the lanes are not available" -- FALSE. Measured this round: PLAN `openai-codex/gpt-6.1-sol` served in 12 s,
    EXECUTE `opencode-go/deepseek-v4.1-flash` served in 14.46 s, VERIFY_SECURITY `openai-codex/gpt-6.1-sol` served
    twice. All three work.
  * "the rule is not written down" -- FALSE. AGENTS.md has carried "Session plane != lane plane" since 2026-10-30,
    and names this exact failure.

The real cause is an incentive gradient: writing the synthesis by hand is ONE step, dispatching three lanes is
THREE commands with flags that each have a failure mode (sealed home + OAuth relay, provider-qualified vs bare model
id, one work package per brief). Under any time pressure the cheap path wins, and the cheap path leaves prose that
looks identical to the routed path.

The lifecycle makes the compliant path the cheapest path: one command dispatches all three lanes and writes typed
indexes over the raw dispatcher receipts. Closure is decided later by the gate, which resolves every index back to
the unchanged raw receipt, so successful dispatch alone cannot claim a publishable study.

  python scripts/far_round.py --run FAR-20261031-047-EXAMPLE --question "the question, in full"

It dispatches PLAN, then EXECUTE, then VERIFY_SECURITY, each against the previous lane's output, and writes:

  runs/<run>/PLAN_RECEIPT.json
  runs/<run>/EXECUTE_RECEIPT.json
  runs/<run>/VERIFY_RECEIPT.json
  runs/<run>/lane_output/<lane>.md
  runs/<run>/STATE.json

It does not write the synthesis. The synthesis is the author's job, but ``scripts/far_lane_gate.py`` will not accept
it unless all three indexed raw receipts still prove their lane claims.

Exit codes: 0 all three lanes served and receipts written; 3 a lane refused (named); 4 a lane timed out.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import secrets
import subprocess
import sys
import time

K = pathlib.Path(__file__).resolve().parent.parent
DISPATCH = K / "scripts" / "hgk-lane-dispatch.py"
RUNS = pathlib.Path(r"C:\Projects\Agent_Workspace\Fabric\fabric-autonomous-research\runs")

LANES = [
    # (kind, lane flag, require-arm, timeout seconds)
    ("plan", "PLAN", "openai-codex/gpt-6.1-sol", 300),
    ("execute", "EXECUTE", "opencode-go/deepseek-v4.1-flash", 600),
    ("verify", "VERIFY_SECURITY", "openai-codex/gpt-6.1-sol", 600),
]

REQUIRED_KINDS = {"plan", "execute", "verify"}
LANE_IDS = {"PLAN", "EXECUTE", "VERIFY_SECURITY"}

# Transport is a property of the arm's provider, not a global flag. Measured in hgk-lane-dispatch.py's own notes:
# an opencode-go arm pointed at the chatgpt.com OAuth upstream answers "model is not supported"; the loopback serves it.
TRANSPORT = {
    "openai-codex/gpt-6.1-sol": ["--codex-home", "C:/Users/user/.codex", "--allow-human-home-transport",
                                 "--relay-base", "https://chatgpt.com/backend-api/codex",
                                 "--identity-source", "codex-rollout"],
    "opencode-go/deepseek-v4.1-flash": ["--relay-base", "http://127.0.0.1:10101/v1",
                                        "--identity-source", "codex-rollout"],
}


def sha256_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_question(question: str) -> str:
    return hashlib.sha256(question.encode("utf-8")).hexdigest()


def valid_run_id(value: str) -> bool:
    """Accept one FAR directory name, never a path expression."""
    return (
        value.startswith("FAR-")
        and pathlib.PurePath(value).name == value
        and all(char.isalnum() or char in "-_." for char in value)
    )


def summarize_dispatch(
    run_id: str,
    lane: str,
    arm: str,
    nonce: str,
    question_digest: str,
    raw_path: pathlib.Path,
    run_dir: pathlib.Path,
    dispatch: dict | None = None,
) -> dict:
    """Bind one lane summary to its immutable raw dispatcher receipt.

    The raw file remains authoritative. This summary is only a typed index into it, and records
    the raw bytes' digest so a later gate can reject post-hoc replacement.
    """
    summary = {
        "schema": "HGK-FAR-LANE-SUMMARY/2",
        "run": run_id,
        "lane": lane,
        "nonce": nonce,
        "required_arm": arm,
        "question_sha256": question_digest,
        "dispatch_receipt": raw_path.relative_to(run_dir).as_posix(),
    }
    if not raw_path.is_file():
        summary.update({"ok": False, "code": "NO_DISPATCH_RECEIPT", "served_arm": None})
        return summary

    summary["dispatch_receipt_sha256"] = sha256_file(raw_path)
    try:
        d = dispatch if dispatch is not None else json.loads(raw_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        summary.update({
            "ok": False,
            "code": "UNREADABLE_DISPATCH_RECEIPT",
            "served_arm": None,
            "detail": f"{exc.__class__.__name__}: {exc}",
        })
        return summary

    if not isinstance(d, dict):
        summary.update({
            "ok": False,
            "code": "INVALID_DISPATCH_RECEIPT",
            "served_arm": None,
            "detail": "JSON root is not an object",
        })
        return summary

    attempts = d.get("attempts") if isinstance(d.get("attempts"), list) else []
    attempt = attempts[-1] if attempts and isinstance(attempts[-1], dict) else {}
    provider = attempt.get("provider")
    model = attempt.get("model")
    served_arm = f"{provider}/{model}" if provider and model else model
    summary.update({
        "ok": bool(d.get("ok")),
        "code": d.get("code"),
        "served_arm": served_arm,
        "rank": attempt.get("rank"),
        "exit": attempt.get("exit"),
        "usage_receipt_ok": bool(d.get("usage_receipt_ok")),
    })
    return summary


def run_lane(
    kind: str,
    lane: str,
    arm: str,
    timeout: int,
    brief: pathlib.Path,
    run_dir: pathlib.Path,
    run_id: str,
    question_digest: str,
) -> dict:
    nonce = f"FAR-{kind.upper()}-{secrets.token_hex(4).upper()}"
    text = brief.read_text(encoding="utf-8")
    brief.write_text(f"NONCE-ECHO: {nonce}\n\n{text}", encoding="utf-8", newline="")
    out = run_dir / f"_{kind}_dispatch.json"
    cmd = [sys.executable, str(DISPATCH), "--lane", lane, "--require-arm", arm,
           "--prompt", str(brief), "--nonce", nonce, "--timeout", str(timeout),
           "--json-out", str(out)] + TRANSPORT[arm]
    started = time.time()
    subprocess.run(cmd, cwd=str(K), capture_output=True, text=True, timeout=timeout + 60)
    receipt = summarize_dispatch(run_id, lane, arm, nonce, question_digest, out, run_dir)
    receipt["attempted_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    receipt["seconds"] = round(time.time() - started, 2)
    if receipt.get("code") in {"NO_DISPATCH_RECEIPT", "UNREADABLE_DISPATCH_RECEIPT",
                               "INVALID_DISPATCH_RECEIPT"}:
        return receipt
    try:
        d = json.loads(out.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        receipt.update({
            "ok": False,
            "code": "UNREADABLE_DISPATCH_RECEIPT",
            "detail": f"{exc.__class__.__name__}: {exc}",
        })
        return receipt
    a = (d.get("attempts") or [{}])[-1]
    # the lane's own words, kept as an artefact so the synthesis can be checked against it
    try:
        p = pathlib.Path(a["stdout_path"])
        said = []
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                o = json.loads(line)
            except Exception:
                continue
            it = o.get("item") or {}
            if it.get("type") == "agent_message":
                said.append(it.get("text") or "")
        (run_dir / "lane_output").mkdir(exist_ok=True)
        # Never write the transcript where the lane may have put its deliverable: FAR-054 lost a 9.7 kB work
        # package that way (the EXECUTE lane wrote lane_output/execute.md, this capture overwrote it with a
        # 1.9 kB transcript, and the VERIFY lane convicted the resulting artifact -- correctly).
        (run_dir / "lane_output" / f"{kind}_reply.md").write_text("\n".join(said), encoding="utf-8", newline="")
    except Exception as exc:
        receipt["output_capture_error"] = f"{exc.__class__.__name__}: {exc}"
    deliverable = run_dir / "lane_output" / "WORKPACKAGE.md"
    if deliverable.is_file():
        receipt["deliverable"] = deliverable.relative_to(run_dir).as_posix()
        receipt["deliverable_sha256"] = sha256_file(deliverable)
        receipt["deliverable_bytes"] = deliverable.stat().st_size
    return receipt


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", required=True, help="FAR run id, e.g. FAR-20261031-047-EXAMPLE")
    ap.add_argument("--question", required=True, help="the research question, in full")
    ap.add_argument("--lanes", default="plan,execute,verify")
    ap.add_argument("--no-repo-read", action="store_true",
                    help="default on for EXECUTE: forbid repository reading in the brief")
    ap.add_argument("--carry-chars", type=int, default=400,
                    help="how much of the previous lane output to carry forward; measured: 6000 chars made "
                         "EXECUTE fail usage reconciliation at 212s, 2000 keeps the turn short")
    args = ap.parse_args(argv)
    wanted = {x.strip().lower() for x in args.lanes.split(",") if x.strip()}
    if wanted != REQUIRED_KINDS:
        ap.error("the authoritative FAR round requires exactly PLAN, EXECUTE, and VERIFY")
    if not args.question.strip():
        ap.error("--question must not be empty")
    if not valid_run_id(args.run):
        ap.error("--run must be one safe FAR directory name")

    run_dir = RUNS / args.run
    (run_dir / "lane_output").mkdir(parents=True, exist_ok=True)
    work = run_dir / "lane_output"
    receipts: dict[str, dict] = {}
    question_digest = sha256_question(args.question)

    brief = work / "_brief_plan.md"
    brief.write_text(f"# PLAN brief\n\n{args.question}\n\n"
                     "Answer as the planning lane: structure the problem, name what would have to be true, and say what "
                     "the EXECUTE lane should build. Do not write code.\n\n"
                     "Begin your reply with the nonce line exactly as given above, verbatim.\n", encoding="utf-8", newline="")

    for kind, lane, arm, timeout in LANES:
        if kind not in wanted:
            continue
        if kind != "plan":
            prev = receipts.get("plan" if kind == "execute" else "execute", {})
            prev_text = ""
            prev_kind = "plan" if kind == "execute" else "execute"
            prev_file = work / f"{prev_kind}_reply.md"
            if not prev_file.exists():
                prev_file = work / f"{prev_kind}.md"
            if prev_file.exists():
                prev_text = prev_file.read_text(encoding="utf-8", errors="replace")[:2000]
            brief = work / f"_brief_{kind}.md"
            role = (f"Answer the question as the executing lane and WRITE THE ANSWER TO THIS EXACT FILE: "
                    f"{work / 'WORKPACKAGE.md'}. Make the decision the question asks for, compare the candidates "
                    "against the evidence stated in the brief, and name what would falsify your choice. A document "
                    "that tells a future executor to decide, or that lists criteria without applying them, does not "
                    "answer the question and will be failed by the checker. Do NOT read the repository: everything "
                    "you need is in this brief (measured: a build brief that sends the arm into the repo stalls past "
                    "600s; the same brief kept self-contained finishes in under a minute). Then report what you "
                    "produced and that file's sha256." if kind == "execute" else
                    "Check the work against the question, not against the writer's summary. Decide PASS or FAIL and "
                    "name what you relied on.")
            brief.write_text(f"# {kind.upper()} brief\n\nQuestion:\n{args.question}\n\n"
                             f"PLAN output:\n{prev_text}\n\n{role}\n\n"
                             "Begin your reply with the nonce line exactly as given above, verbatim.\n", encoding="utf-8", newline="")
        r = run_lane(kind, lane, arm, timeout, brief, run_dir, args.run, question_digest)
        receipts[kind] = r
        (run_dir / f"{kind.upper()}_RECEIPT.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
        print(f"{kind:8} ok={r.get('ok')} lane={r.get('lane')} code={r.get('code')} "
              f"served={r.get('served_arm')} usage={r.get('usage_receipt_ok')} "
              f"{r.get('seconds')}s")
        if not r.get("ok"):
            state = {"schema": "HGK-FAR-STATE/2", "run": args.run,
                     "question_sha256": question_digest, "publication_status": "UNPUBLISHED",
                     "stopped_at": kind, "receipts": receipts}
            (run_dir / "STATE.json").write_text(json.dumps(state, ensure_ascii=False, indent=1),
                                                encoding="utf-8", newline="")
            return 4 if r.get("exit") == "TIMEOUT" else 3

    state = {"schema": "HGK-FAR-STATE/2", "run": args.run,
             "question_sha256": question_digest,
             "publication_status": "LANE_DISPATCH_COMPLETE",
             "lanes_required": sorted(wanted), "lanes_served": sorted(receipts),
             "receipts": receipts, "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
             "next": "write ResearchSynthesis.md with a Lane evidence line; scripts/far_lane_gate.py "
                     "decides whether the run is publishable"}
    (run_dir / "STATE.json").write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    print(f"\nSTATE: {state['publication_status']} -> {run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
