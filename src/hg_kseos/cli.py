from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .bootstrap import bootstrap, reconcile_tt
from .doctor import doctor
from .errors import HGKError
from .knowledge import KnowledgeFactory
from .providers import qualify_hermes_core
from .recovery import backup_database, restore_database
from .release import EvidenceEnvelope, ReleaseReducer
from .spine import SharedSpine


def project_config(root: Path) -> dict[str, Any]:
    return json.loads((root / "config" / "project.json").read_text(encoding="utf-8"))


def spine_for(root: Path) -> SharedSpine:
    config = project_config(root)
    return SharedSpine(root / config["canonical_database"])


def emit(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hg-kseos")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("bootstrap")
    commands.add_parser("doctor")
    commands.add_parser("migrate")
    commands.add_parser("reconcile-tt")
    commands.add_parser("qualify-hermes-core")
    commands.add_parser("snapshot")

    ingest = commands.add_parser("ingest")
    ingest.add_argument("path", type=Path)
    ingest.add_argument("--rank", required=True)
    ingest.add_argument("--anchor", default="full")

    promote = commands.add_parser("promote")
    promote.add_argument("candidate_id")
    promote.add_argument("--verifier", required=True)
    promote.add_argument("--evidence", required=True)
    promote.add_argument("--title", required=True)

    search = commands.add_parser("search")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=5)

    commands.add_parser("rebuild-knowledge")

    backup = commands.add_parser("backup")
    backup.add_argument("--destination", type=Path)

    restore = commands.add_parser("restore")
    restore.add_argument("backup", type=Path)
    restore.add_argument("--sha256", required=True)
    restore.add_argument("--destination", type=Path, required=True)

    release = commands.add_parser("release-reduce")
    release.add_argument("envelope", type=Path)
    return parser


def run(args: argparse.Namespace) -> Any:
    root = args.root.resolve(strict=True)
    if args.command == "bootstrap":
        return bootstrap(root)
    if args.command == "doctor":
        return doctor(root)
    if args.command == "reconcile-tt":
        return reconcile_tt(root)
    if args.command == "qualify-hermes-core":
        return qualify_hermes_core(root)
    spine = spine_for(root)
    if args.command == "migrate":
        spine.initialize()
        return {"status": "MIGRATION_PASS", "snapshot": spine.snapshot()}
    if args.command == "snapshot":
        return spine.snapshot()
    if args.command == "ingest":
        path = args.path.resolve(strict=True)
        return KnowledgeFactory(spine).ingest_text(
            str(path), path.read_text(encoding="utf-8"), args.rank, args.anchor
        )
    if args.command == "promote":
        doc_id = KnowledgeFactory(spine).promote(
            args.candidate_id, args.verifier, args.evidence, args.title
        )
        return {"doc_id": doc_id, "status": "PROMOTED"}
    if args.command == "search":
        return {"query": args.query, "results": KnowledgeFactory(spine).search(args.query, args.limit)}
    if args.command == "rebuild-knowledge":
        return KnowledgeFactory(spine).rebuild()
    if args.command == "backup":
        config = project_config(root)
        destination = args.destination or (root / config["backup_root"])
        return backup_database(spine.database, destination)
    if args.command == "restore":
        return restore_database(args.backup, args.sha256, args.destination)
    if args.command == "release-reduce":
        envelope = EvidenceEnvelope.from_dict(json.loads(args.envelope.read_text(encoding="utf-8")))
        return ReleaseReducer(spine).reduce(envelope)
    raise AssertionError(args.command)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = run(args)
        emit(result)
    except (HGKError, OSError, ValueError, RuntimeError) as exc:
        emit({"verdict": "FAIL_CLOSED", "error_type": type(exc).__name__, "error": str(exc)})
        return 1
    return 1 if isinstance(result, dict) and result.get("verdict") in {"FAIL", "FAIL_CLOSED"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
