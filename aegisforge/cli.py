from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from dataclasses import asdict
import io
import json
from pathlib import Path
import platform
import sys
from typing import Any

from . import __version__
from .catalog import discover_skills
from .evaluation import evaluate_all, load_scenarios
from .evidence import EvidenceLedger
from .policy import assess
from .schema import load_schema, validate_schema_document
from .skilllib.frontmatter import read_skill_file
from .skilllib.registry import discover, load_registry, registry_is_fresh, write_registry
from .skilllib.router import explain_route, search
from .validator import validate_repo


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aegisforge",
        description="Risk-aware workflow assessment and searchable skill operations for software agents.",
    )
    parser.add_argument("--version", action="version", version=f"aegisforge {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    assess_parser = subparsers.add_parser("assess", help="classify a task and select a workflow")
    assess_parser.add_argument("text", nargs="?", help="natural-language task description")
    assess_parser.add_argument("--text", dest="text_option", help="natural-language task description")
    assess_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON (default)")
    assess_parser.add_argument("--human", action="store_true", help="emit readable human-oriented output")
    assess_parser.add_argument("--pretty", action="store_true", help="compatibility alias for JSON output")

    validate_parser = subparsers.add_parser("validate", help="validate a repository and its skill contracts")
    validate_parser.add_argument("path", nargs="?", default=".", help="repository path")
    validate_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    skills_parser = subparsers.add_parser("skills", help="list discoverable skills")
    skills_parser.add_argument("path", nargs="?", default=".", help="repository path")
    skills_parser.add_argument("--status", help="filter by lifecycle status")
    skills_parser.add_argument("--domain", help="filter by domain")
    skills_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON (default)")
    skills_parser.add_argument("--human", action="store_true", help="emit readable human-oriented output")
    skills_parser.add_argument("--pretty", action="store_true", help="compatibility alias for JSON output")

    for command, help_text in (("search", "search skills by intent or keywords"), ("route", "route a task to the smallest likely skill set")):
        command_parser = subparsers.add_parser(command, help=help_text)
        command_parser.add_argument("query")
        command_parser.add_argument("--root", default=".", help="repository root")
        command_parser.add_argument("--limit", type=int, default=10 if command == "search" else 5)
        command_parser.add_argument("--harness", help="require compatibility with a harness")
        command_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON (default)")
        command_parser.add_argument("--human", action="store_true", help="emit readable human-oriented output")

    inspect_parser = subparsers.add_parser("inspect", help="inspect one skill by ID or path")
    inspect_parser.add_argument("skill")
    inspect_parser.add_argument("--root", default=".", help="repository root")
    inspect_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    evaluate_parser = subparsers.add_parser("evaluate", help="run deterministic agent-scenario benchmarks")
    evaluate_parser.add_argument("path", nargs="?", default="evaluation/scenarios.json", help="scenario JSON file")
    evaluate_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    doctor_parser = subparsers.add_parser("doctor", help="diagnose installation, registry, schema, and test readiness")
    doctor_parser.add_argument("path", nargs="?", default=".", help="repository path")
    doctor_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    index_parser = subparsers.add_parser("index", help="write generated registry indexes")
    index_parser.add_argument("path", nargs="?", default=".", help="repository path")

    evidence_parser = subparsers.add_parser("evidence", help="validate a structured evidence ledger")
    evidence_parser.add_argument("path", help="evidence JSON file")
    evidence_parser.add_argument("--require-approval", action="store_true")
    evidence_parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    return parser


def _json_print(value: object) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def _root(value: str) -> Path:
    return Path(value).resolve()


def _load_records(root: Path):
    if registry_is_fresh(root):
        try:
            return load_registry(root), []
        except (OSError, ValueError, KeyError, json.JSONDecodeError):
            pass
    return discover(root)


def _run_assess(args: argparse.Namespace) -> int:
    text = args.text_option or args.text
    if not text:
        raise SystemExit("assess requires a task description")
    result = assess(text).to_dict()
    if args.json or not getattr(args, "human", False):
        _json_print(result)
    else:
        print(f"Risk: {result['risk_level'].upper()}")
        print(f"Workflow: {result['workflow']}")
        print(f"Task type: {result['task_type']}")
        print(f"Confirmation required: {'yes' if result['requires_confirmation'] else 'no'}")
        print("Reasons:")
        for reason in result["reasons"]:
            print(f"  - {reason}")
        print("Required controls:")
        for control in result["required_controls"]:
            print(f"  - {control}")
    return 0


def _run_validate(args: argparse.Namespace) -> int:
    root = _root(args.path)
    findings = validate_repo(root)
    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warning"]
    if args.json:
        _json_print({"valid": not errors, "errors": len(errors), "warnings": len(warnings), "findings": [asdict(finding) for finding in findings]})
    else:
        for finding in findings:
            print(f"{finding.severity}: {finding.path}: {finding.message}")
        print(f"Validated {root}: {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


def _run_skills(args: argparse.Namespace) -> int:
    root = _root(args.path)
    records, issues = _load_records(root)
    payload = []
    for record in records:
        if args.status and record.status != args.status:
            continue
        if args.domain and args.domain not in record.domains:
            continue
        payload.append({"id": record.id, "name": record.name, "status": record.status, "risk": record.risk_level, "summary": record.summary, "path": record.path})
    if args.json or not getattr(args, "human", False):
        _json_print(payload)
    else:
        for record in payload:
            print(f"{record['id']}\t{record['status']}\t{record['risk']}\t{record['summary']}")
        if issues:
            print(f"Discovery reported {len(issues)} issue(s)", file=sys.stderr)
    return 0


def _match_payload(match: Any) -> dict[str, Any]:
    return {"id": match.record.id, "name": match.record.name, "score": round(match.score, 3), "risk": match.record.risk_level, "status": match.record.status, "path": match.record.path, "reasons": list(match.reasons)}


def _run_search(args: argparse.Namespace) -> int:
    root = _root(args.root)
    records, issues = _load_records(root)
    matches = search(records, args.query, args.limit, harness=args.harness)
    payload = [_match_payload(match) for match in matches]
    if args.json or not getattr(args, "human", False):
        _json_print(payload)
    else:
        if not payload:
            print("No matching skills found.")
        for index, match in enumerate(payload, 1):
            print(f"{index}. {match['id']} [{match['status']}, {match['risk']}] score={match['score']}")
            print(f"   why: {', '.join(match['reasons'])}")
        if issues:
            print(f"Discovery reported {len(issues)} issue(s)", file=sys.stderr)
    return 0


def _run_route(args: argparse.Namespace) -> int:
    root = _root(args.root)
    records, issues = _load_records(root)
    explanation = explain_route(records, args.query, args.limit, harness=args.harness)
    payload = {"query": explanation.query, "harness": explanation.harness, "selected": [_match_payload(match) for match in explanation.selected], "rejected": [_match_payload(match) for match in explanation.rejected]}
    if args.json or not getattr(args, "human", False):
        _json_print(payload)
    else:
        print(f"Selected skills for: {args.query}")
        for match in payload["selected"]:
            print(f"  - {match['id']} [{match['status']}, {match['risk']}] score={match['score']}")
            print(f"    why: {', '.join(match['reasons'])}")
        if payload["rejected"]:
            print("Rejected alternatives:")
            for match in payload["rejected"][:5]:
                print(f"  - {match['id']} score={match['score']}")
    return 0


def _run_inspect(args: argparse.Namespace) -> int:
    root = _root(args.root)
    records, issues = discover(root)
    record = next((item for item in records if item.id == args.skill or item.path == args.skill or item.path.rstrip("/") == args.skill.rstrip("/")), None)
    if record is None:
        print(f"skill not found: {args.skill}", file=sys.stderr)
        return 1
    path = root / record.path
    metadata, body = read_skill_file(path)
    payload = {"record": _match_payload(type("Match", (), {"record": record, "score": 0.0, "reasons": ()})()), "metadata": metadata, "body": body}
    if args.json:
        _json_print(payload)
    else:
        print(f"{record.name} ({record.id})")
        print(f"Status: {record.status} | Risk: {record.risk_level} | Confirmation: {record.confirmation}")
        print(f"Path: {record.path}")
        print("\n" + body)
    return 0


def _run_evaluate(args: argparse.Namespace) -> int:
    report = evaluate_all(load_scenarios(args.path))
    payload = report.to_dict()
    if args.json:
        _json_print(payload)
    else:
        print(f"Evaluation: {report.passed}/{report.total} passed ({report.pass_rate:.1%})")
        for result in report.results:
            marker = "PASS" if result.passed else "FAIL"
            print(f"{marker} {result.scenario_id}: {result.actual_risk}/{result.actual_workflow}")
            for failure in result.failures:
                print(f"  - {failure}")
    return 0 if report.failed == 0 else 1


def _run_doctor(args: argparse.Namespace) -> int:
    root = _root(args.path)
    checks: list[dict[str, Any]] = []
    checks.append({"name": "python", "ok": sys.version_info >= (3, 11), "detail": platform.python_version()})
    checks.append({"name": "package-import", "ok": True, "detail": "aegisforge import succeeded"})
    findings = validate_repo(root)
    errors = [finding for finding in findings if finding.severity == "error"]
    warnings = [finding for finding in findings if finding.severity == "warning"]
    checks.append({"name": "repository-validation", "ok": not errors, "detail": f"{len(errors)} errors, {len(warnings)} warnings"})
    checks.append({"name": "registry", "ok": registry_is_fresh(root), "detail": "fresh" if registry_is_fresh(root) else "missing or stale; run aegisforge index"})
    for schema_file in sorted((root / "schemas").glob("*.json")):
        try:
            schema = load_schema(schema_file)
            schema_findings = validate_schema_document(schema)
            checks.append({"name": f"schema:{schema_file.name}", "ok": not schema_findings, "detail": "; ".join(schema_findings) or "valid"})
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            checks.append({"name": f"schema:{schema_file.name}", "ok": False, "detail": str(exc)})
    payload = {"ok": all(check["ok"] for check in checks), "checks": checks}
    if args.json:
        _json_print(payload)
    else:
        for check in checks:
            print(f"{'PASS' if check['ok'] else 'FAIL'} {check['name']}: {check['detail']}")
    return 0 if payload["ok"] else 1


def _run_index(args: argparse.Namespace) -> int:
    root = _root(args.path)
    records, issues = discover(root)
    if any(issue.severity == "error" for issue in issues):
        print("cannot index repository with validation errors", file=sys.stderr)
        return 1
    output = write_registry(root, records)
    print(f"Wrote {len(records)} skills to {output}")
    return 0


def _run_evidence(args: argparse.Namespace) -> int:
    ledger = EvidenceLedger.load(args.path)
    findings = ledger.validate(require_approval=args.require_approval)
    payload = {"valid": not findings, "passed": ledger.passed, "findings": findings, "ledger": ledger.to_dict()}
    if args.json:
        _json_print(payload)
    else:
        print(f"Evidence ledger: {'valid' if not findings else 'invalid'}")
        for finding in findings:
            print(f"  - {finding}")
    return 0 if not findings else 1


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "assess":
        return _run_assess(args)
    if args.command == "validate":
        return _run_validate(args)
    if args.command == "skills":
        return _run_skills(args)
    if args.command == "search":
        return _run_search(args)
    if args.command == "route":
        return _run_route(args)
    if args.command == "inspect":
        return _run_inspect(args)
    if args.command == "evaluate":
        return _run_evaluate(args)
    if args.command == "doctor":
        return _run_doctor(args)
    if args.command == "index":
        return _run_index(args)
    if args.command == "evidence":
        return _run_evidence(args)
    return 2


if __name__ == "__main__":
    sys.exit(main())
