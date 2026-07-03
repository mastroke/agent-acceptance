"""agent-acceptance CLI: run both legs -> one combined JSON + markdown report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .orchestrator import build_report
from .report import render_report

_DEFAULT_SCENARIOS = Path(__file__).resolve().parents[2] / "examples" / "scenarios.yaml"


def _cmd_run(args: argparse.Namespace) -> int:
    scenarios = Path(args.scenarios)
    if not scenarios.exists():
        print(f"scenarios file not found: {scenarios}", file=sys.stderr)
        return 2
    report = build_report(
        scenarios,
        project=args.project,
        memory_domain=args.memory_domain,
        memory_data_dir=args.memory_data_dir,
        memory_download=args.memory_download,
        max_episodes=args.max_episodes,
        memory_threshold=args.memory_threshold,
    )
    out_json = Path(args.output) if args.output else scenarios.with_suffix(".acceptance.json")
    out_json.write_text(json.dumps(report.as_dict(), indent=2) + "\n")
    out_md = Path(args.report) if args.report else scenarios.with_suffix(".acceptance.md")
    out_md.write_text(render_report(report))
    print(f"Wrote {out_json} + {out_md} — verdict {report.verdict.value}")
    # exit code: 0 PASS, 1 FAIL, 2 CONDITIONAL/behavioral-only (still a signal)
    v = report.verdict.value
    if v == "PASS":
        return 0
    if v == "FAIL":
        return 1
    return 2


def _cmd_report(args: argparse.Namespace) -> int:
    data = json.loads(Path(args.results).read_text())
    from .models import BehavioralBlock, CombinedReport, MemoryBlock
    report = CombinedReport(
        project=data.get("project", ""),
        behavioral=BehavioralBlock(**data.get("behavioral", {"ran": False, "project": "", "verdict": ""})),
        memory=MemoryBlock(**data.get("memory", {"ran": False})),
        memory_threshold=data.get("memory_threshold", 0.5),
    )
    out_md = Path(args.output) if args.output else Path(args.results).with_suffix(".md")
    out_md.write_text(render_report(report))
    print(f"Wrote {out_md}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-acceptance",
        description="One acceptance report for agentic AI: behavioral sign-off + memory-governance gate.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="Run both legs and write a combined report")
    run_p.add_argument("scenarios", nargs="?", default=str(_DEFAULT_SCENARIOS),
                       help="Path to agent-handoff scenarios YAML (default: bundled examples/scenarios.yaml)")
    run_p.add_argument("--project", help="Override project name in the report")
    run_p.add_argument("--memory-domain", help="GateMem domain to score (e.g. medical, office). Omit to skip memory governance.")
    run_p.add_argument("--memory-data-dir", help="Local GateMem bench tree (Ray368 JSONL shards)")
    run_p.add_argument("--memory-download", action="store_true", help="Allow the harness to download public GateMem data")
    run_p.add_argument("--max-episodes", type=int, default=1, help="Cap episodes scored (default 1)")
    run_p.add_argument("--memory-threshold", type=float, default=0.5, help="MGS threshold for the governance gate (default 0.5)")
    run_p.add_argument("-o", "--output", help="Output combined JSON path")
    run_p.add_argument("--report", help="Output markdown report path")
    run_p.set_defaults(func=_cmd_run)

    rep_p = sub.add_parser("report", help="Render markdown from a saved combined JSON")
    rep_p.add_argument("results", help="Path to combined acceptance JSON")
    rep_p.add_argument("-o", "--output", help="Output markdown path")
    rep_p.set_defaults(func=_cmd_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
