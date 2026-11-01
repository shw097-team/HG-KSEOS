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

So the fix is not another gate -- gates only refuse after the fact. The fix is to make the compliant path the cheapest
path: one command, three lanes, receipts written where the gate looks for them.

  python scripts/far_round.py --run FAR-20261031-047-EXAMPLE --question "the question, in full"

It dispatches PLAN, then EXECUTE, then VERIFY_SECURITY, each against the previous lane's output, and writes:

  runs/<run>/PLAN_RECEIPT.json
  runs/<run>/EXECUTE_RECEIPT.json
  runs/<run>/VERIFY_RECEIPT.json
  runs/<run>/lane_output/<lane>.md
  runs/<run>/STATE.json

It does not write the synthesis. The synthesis is the author's job -- but it can no longer be produced without the
three receipts sitting next to it, because producing them is now one command.

Exit codes: 0 all three lanes served and receipts written; 3 a lane refused (named); 4 a lane timed out.
"""

from __future__ import annotations

import argparse
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
    ("execute", "EXECUTE", "opencode-go/deepseek-v4.1-flash", 420),
    ("verify", "VERIFY_SECURITY", "openai-codex/gpt-6.1-sol", 420),
]

# Transport is a property of the arm's provider, not a global flag. Measured in hgk-lane-dispatch.py's own notes:
# an opencode-go arm pointed at the chatgpt.com OAuth upstream answers "model is not supported"; the loopback serves it.
TRANSPORT = {
    "openai-codex/gpt-6.1-sol": ["--codex-home", "C:/Users/user/.codex", "--allow-human-home-transport",
                                 "--relay-base", "https://chatgpt.com/backend-api/codex",
                                 "--identity-source", "codex-rollout"],
    "opencode-go/deepseek-v4.1-flash": ["--relay-base", "http://127.0.0.1:10101/v1",
                                        "--identity-source", "codex-rollout"],
}


def run_lane(kind: str, lane: str, arm: str, timeout: int, brief: pathlib.Path, run_dir: pathlib.Path) -> dict:
    nonce = f"FAR-{kind.upper()}-{secrets.token_hex(4).upper()}"
    text = brief.read_text(encoding="utf-8")
    brief.write_text(f"NONCE-ECHO: {nonce}\n\n{text}", encoding="utf-8", newline="")
    out = run_dir / f"_{kind}_dispatch.json"
    cmd = [sys.executable, str(DISPATCH), "--lane", lane, "--require-arm", arm,
           "--prompt", str(brief), "--nonce", nonce, "--timeout", str(timeout // 2),
           "--json-out", str(out)] + TRANSPORT[arm]
    started = time.time()
    subprocess.run(cmd, cwd=str(K), capture_output=True, text=True, timeout=timeout + 60)
    receipt: dict = {"lane": lane, "required_arm": arm, "served_arm": arm, "nonce": nonce,
                     "attempted_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    if not out.exists():
        receipt.update({"ok": False, "code": "NO_DISPATCH_RECEIPT"})
        return receipt
    d = json.loads(out.read_text(encoding="utf-8"))
    a = (d.get("attempts") or [{}])[0]
    receipt.update({
        "ok": bool(d.get("ok")), "code": d.get("code"),
        "model": a.get("model"), "rank": a.get("rank"), "exit": a.get("exit"),
        "nonce_present": bool(a.get("nonce_present")),
        "usage_receipt_ok": bool(d.get("usage_receipt_ok")),
        "seconds": round(time.time() - started, 2),
        "dispatch_receipt": str(out),
    })
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
        (run_dir / "lane_output" / f"{kind}.md").write_text("\n".join(said), encoding="utf-8", newline="")
    except Exception as exc:
        receipt["output_capture_error"] = f"{exc.__class__.__name__}: {exc}"
    return receipt


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run", required=True, help="FAR run id, e.g. FAR-20261031-047-EXAMPLE")
    ap.add_argument("--question", required=True, help="the research question, in full")
    ap.add_argument("--lanes", default="plan,execute,verify")
    args = ap.parse_args(argv)
    wanted = {x.strip().lower() for x in args.lanes.split(",") if x.strip()}

    run_dir = RUNS / args.run
    (run_dir / "lane_output").mkdir(parents=True, exist_ok=True)
    work = run_dir / "lane_output"
    receipts: dict[str, dict] = {}

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
            prev_file = work / f"{'plan' if kind == 'execute' else 'execute'}.md"
            if prev_file.exists():
                prev_text = prev_file.read_text(encoding="utf-8", errors="replace")[:6000]
            brief = work / f"_brief_{kind}.md"
            role = ("Build exactly one work package from the plan. Keep it small enough to finish. Report what you "
                    "changed and why." if kind == "execute" else
                    "Check the work against the question, not against the writer's summary. Decide PASS or FAIL and "
                    "name what you relied on.")
            brief.write_text(f"# {kind.upper()} brief\n\nQuestion:\n{args.question}\n\n"
                             f"PLAN output:\n{prev_text}\n\n{role}\n\n"
                             "Begin your reply with the nonce line exactly as given above, verbatim.\n", encoding="utf-8", newline="")
        r = run_lane(kind, lane, arm, timeout, brief, run_dir)
        receipts[kind] = r
        (run_dir / f"{kind.upper()}_RECEIPT.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
        print(f"{kind:8} ok={r.get('ok')} code={r.get('code')} model={r.get('model')} "
              f"nonce={r.get('nonce_present')} usage={r.get('usage_receipt_ok')} {r.get('seconds')}s")
        if not r.get("ok"):
            state = {"schema": "HGK-FAR-STATE/1", "run": args.run, "publication_status": "UNPUBLISHED",
                     "stopped_at": kind, "receipts": receipts}
            (run_dir / "STATE.json").write_text(json.dumps(state, ensure_ascii=False, indent=1),
                                                encoding="utf-8", newline="")
            return 4 if r.get("exit") == "TIMEOUT" else 3

    state = {"schema": "HGK-FAR-STATE/1", "run": args.run,
             "publication_status": "LANES_SERVED" if len(receipts) == len(wanted) else "UNPUBLISHED",
             "lanes_required": sorted(wanted), "lanes_served": sorted(receipts),
             "receipts": receipts, "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
             "next": "write ResearchSynthesis.md; scripts/far_lane_gate.py decides whether it may be called published"}
    (run_dir / "STATE.json").write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8", newline="")
    print(f"\nSTATE: {state['publication_status']} -> {run_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
