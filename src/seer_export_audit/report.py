"""Writers for machine-readable and reviewer-friendly audit output."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_reports(report: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "audit_report.json"
    markdown_path = output_dir / "audit_report.md"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# Export structural audit",
        "",
        f"**Status:** `{report['summary']}`",
        "",
        "## Export",
        "",
        f"- File: `{report['data_file']}`",
        f"- Rows: {report['row_count']}",
        f"- Columns: {report['column_count']}",
        f"- Detected delimiter: `{report['data_delimiter']}`",
        f"- Blank header positions: {report['blank_header_positions'] or 'none'}",
        f"- Duplicate headers: {', '.join(report['duplicate_headers']) or 'none'}",
        f"- Irregular rows: {report['irregular_row_count']}",
        "",
        "## Missingness",
        "",
        "| Variable | Missing cells | Missing % |",
        "| --- | ---: | ---: |",
    ]
    for variable, values in report["missing_by_column"].items():
        lines.append(f"| {variable} | {values['missing_cells']} | {values['missing_percent']} |")

    dictionary = report.get("dictionary")
    if dictionary:
        lines.extend([
            "",
            "## Dictionary alignment",
            "",
            f"- Dictionary: `{dictionary['file']}` ({dictionary['variable_count']} variables)",
            "- Export variables missing from dictionary: "
            + (", ".join(dictionary["undocumented_export_variables"]) or "none"),
            "- Dictionary variables absent from export: "
            + (", ".join(dictionary["dictionary_variables_absent_from_export"]) or "none"),
        ])

    lines.extend([
        "",
        "## Interpretation",
        "",
        "This is a structural audit only. Review variable definitions, data-use restrictions, and study-specific coding decisions separately.",
    ])
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, markdown_path
