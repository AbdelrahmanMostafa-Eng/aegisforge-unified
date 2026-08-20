from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .catalog import discover_skills
from .policy import assess
from .skilllib.registry import discover, write_registry
from .skilllib.router import route, search
from .validator import validate_repo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aegisforge",
        description="Risk-aware workflow assessment and searchable skill operations for software agents.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    assess_parser = subparsers.add_parser("assess", help="classify a task and select a workflow")
    assess_parser.add_argument("--text", required=True, help="natural-language task description")
    assess_parser.add_argument("--pretty", action="store_true", help="pretty-print JSON output")

    validate_parser = subparsers.add_parser("validate", help="validate an AegisForge repository")
    validate_parser.add_argument("path", nargs="?", default=".", help="repository path")

    skills_parser = subparsers.add_parser("skills", help="list discoverable skills")
    skills_parser.add_argument("path", nargs="?", default=".", help="repository path")
    skills_parser.add_argument("--status", help="filter by lifecycle status")
    skills_parser.add_argument("--domain", help="filter by domain")
    skills_parser.add_argument("--pretty", action="store_true", help="pretty-print JSON output")

    for command, help_text in (("search", "search skills by intent or keywords"), ("route", "route a task to the smallest likely skill set")):
        command_parser = subparsers.add_parser(command, help=help_text)
        command_parser.add_argument("query")
        command_parser.add_argument("--root", default=".", help="repository root")
        command_parser.add_argument("--limit", type=int, default=10 if command == "search" else 5)

    index_parser = subparsers.add_parser("index", help="write generated registry indexes")
    index_parser.add_argument("path", nargs="?", default=".", help="repository path")

    return parser


def _json_print(value: object, pretty: bool = False) -> None:
    print(json.dumps(value, indent=2 if pretty else None, sort_keys=True))


def _run_assess(args: argparse.Namespace) -> int:
    _json_print(assess(args.text).to_dict(), args.pretty)
    return 0


def _run_validate(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    findings = validate_repo(root)
    if not findings:
        print(f"valid: {root}")
        return 0
    for finding in findings:
        print(f"{finding.severity}: {finding.path}: {finding.message}")
    return 1 if any(finding.severity == "error" for finding in findings) else 0


def _run_skills(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    records, issues = discover(root)
    if issues:
        print(f"discovery_issues={len(issues)}", file=sys.stderr)
    payload = []
    for record in records:
        if args.status and record.status != args.status:
            continue
        if args.domain and args.domain not in record.domains:
            continue
        payload.append({
            "id": record.id,
            "name": record.name,
            "status": record.status,
            "risk": record.risk_level,
            "summary": record.summary,
            "path": record.path,
        })
    _json_print(payload, args.pretty)
    return 0


def _run_search_or_route(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    records, issues = discover(root)
    if issues:
        print(f"discovery_issues={len(issues)}", file=sys.stderr)
    matches = search(records, args.query, args.limit) if args.command == "search" else route(records, args.query, args.limit)
    _json_print([
        {
            "id": match.record.id,
            "name": match.record.name,
            "score": round(match.score, 3),
            "risk": match.record.risk_level,
            "status": match.record.status,
            "path": match.record.path,
            "reasons": list(match.reasons),
        }
        for match in matches
    ], True)
    return 0


def _run_index(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    records, issues = discover(root)
    if any(issue.severity == "error" for issue in issues):
        print("cannot index repository with validation errors", file=sys.stderr)
        return 1
    output = write_registry(root, records)
    print(f"Wrote {len(records)} skills to {output}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "assess":
        return _run_assess(args)
    if args.command == "validate":
        return _run_validate(args)
    if args.command == "skills":
        return _run_skills(args)
    if args.command in {"search", "route"}:
        return _run_search_or_route(args)
    if args.command == "index":
        return _run_index(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
