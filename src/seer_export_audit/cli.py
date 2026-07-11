"""Command-line entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from .audit import audit_export
from .report import write_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seer-export-audit",
        description="Structural quality control for delimited registry exports.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    audit = subparsers.add_parser("audit", help="Audit one export and optional companion dictionary.")
    audit.add_argument("--data", required=True, type=Path, help="UTF-8 delimited export file.")
    audit.add_argument("--dictionary", type=Path, help="Optional simple delimited dictionary with `variable` header.")
    audit.add_argument("--output", required=True, type=Path, help="Directory for JSON and Markdown reports.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "audit":
        report = audit_export(args.data, args.dictionary)
        json_path, markdown_path = write_reports(report, args.output)
        print(f"Audit status: {report['summary']}")
        print(f"JSON report: {json_path}")
        print(f"Markdown report: {markdown_path}")
        return 0
    return 2
