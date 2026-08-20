"""Command-line interface for the SKILL.md skill library."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .registry import discover, write_registry
from .router import route, search


def _root(value: str | None) -> Path:
    return Path(value or ".").resolve()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="skill", description="Search and validate the SKILL.md universal skill library.")
    parser.add_argument("--root", default=".", help="repository root (default: current directory)")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="list discovered skills")
    list_parser.add_argument("--domain", help="filter by domain")
    list_parser.add_argument("--status", help="filter by status")

    search_parser = sub.add_parser("search", help="search skills by intent or keywords")
    search_parser.add_argument("query")
    search_parser.add_argument("--limit", type=int, default=10)

    route_parser = sub.add_parser("route", help="route a task to the smallest likely skill set")
    route_parser.add_argument("query")
    route_parser.add_argument("--limit", type=int, default=5)

    sub.add_parser("validate", help="validate all discovered skills")
    sub.add_parser("index", help="write registry/skills.json")
    return parser


def _load(root: Path):
    records, issues = discover(root)
    return records, issues


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = _root(args.root)
    records, issues = _load(root)

    if args.command == "list":
        for record in records:
            if args.domain and args.domain not in record.domains:
                continue
            if args.status and args.status != record.status:
                continue
            print(f"{record.id}\t{record.status}\t{record.summary}")
        return 0

    if args.command in {"search", "route"}:
        matches = search(records, args.query, args.limit) if args.command == "search" else route(records, args.query, args.limit)
        payload = [
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
        ]
        print(json.dumps(payload, indent=2))
        return 0

    if args.command == "validate":
        errors = [issue for issue in issues if issue.severity == "error"]
        warnings = [issue for issue in issues if issue.severity == "warning"]
        for issue in issues:
            print(f"{issue.severity.upper()}: {issue.path}: {issue.message}")
        print(f"Validated {len(records)} skills: {len(errors)} errors, {len(warnings)} warnings")
        return 1 if errors else 0

    if args.command == "index":
        output = write_registry(root, records)
        print(f"Wrote {len(records)} skills to {output}")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
