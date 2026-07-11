"""Dependency-free structural checks for delimited exports."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Any


SUPPORTED_DELIMITERS = ",\t|;"


def detect_dialect(path: Path) -> csv.Dialect:
    """Detect a common delimited-text dialect from a small UTF-8 sample."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(8192)
    if not sample.strip():
        raise ValueError(f"Input file is empty: {path}")
    try:
        return csv.Sniffer().sniff(sample, delimiters=SUPPORTED_DELIMITERS)
    except csv.Error:
        class PipeDialect(csv.excel):
            delimiter = "|"

        return PipeDialect()


def read_table(path: Path) -> tuple[list[str], list[list[str]], str]:
    """Read a UTF-8 delimited table without retaining any more than needed."""
    dialect = detect_dialect(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle, dialect))
    if not rows:
        raise ValueError(f"Input file is empty: {path}")
    headers = [cell.strip() for cell in rows[0]]
    return headers, rows[1:], dialect.delimiter


def read_dictionary(path: Path) -> tuple[set[str], str]:
    """Read the required `variable` column from a simple companion dictionary."""
    headers, rows, delimiter = read_table(path)
    normalized = {name.casefold(): index for index, name in enumerate(headers)}
    if "variable" not in normalized:
        raise ValueError("Dictionary must contain a `variable` header.")
    index = normalized["variable"]
    variables = {
        row[index].strip()
        for row in rows
        if len(row) > index and row[index].strip()
    }
    return variables, delimiter


def audit_export(data_path: Path, dictionary_path: Path | None = None) -> dict[str, Any]:
    """Create a structural audit report without interpreting clinical content."""
    headers, rows, delimiter = read_table(data_path)
    header_counts = Counter(headers)
    duplicate_headers = sorted(name for name, count in header_counts.items() if name and count > 1)
    blank_header_positions = [index + 1 for index, name in enumerate(headers) if not name]
    expected_width = len(headers)
    irregular_rows = [index + 2 for index, row in enumerate(rows) if len(row) != expected_width]

    missing_by_column: dict[str, dict[str, float | int]] = {}
    for index, name in enumerate(headers):
        blank_cells = sum(1 for row in rows if index >= len(row) or not row[index].strip())
        missing_by_column[name or f"column_{index + 1}"] = {
            "missing_cells": blank_cells,
            "missing_percent": round((blank_cells / len(rows) * 100) if rows else 0.0, 2),
        }

    report: dict[str, Any] = {
        "tool_version": "0.1.1",
        "data_file": data_path.name,
        "data_delimiter": delimiter,
        "row_count": len(rows),
        "column_count": expected_width,
        "blank_header_positions": blank_header_positions,
        "duplicate_headers": duplicate_headers,
        "irregular_row_count": len(irregular_rows),
        "irregular_row_numbers": irregular_rows,
        "missing_by_column": missing_by_column,
        "dictionary": None,
        "summary": "pass",
    }

    if blank_header_positions or duplicate_headers or irregular_rows:
        report["summary"] = "review_required"

    if dictionary_path:
        variables, dictionary_delimiter = read_dictionary(dictionary_path)
        export_variables = {name for name in headers if name}
        undocumented = sorted(export_variables - variables)
        unused = sorted(variables - export_variables)
        report["dictionary"] = {
            "file": dictionary_path.name,
            "delimiter": dictionary_delimiter,
            "variable_count": len(variables),
            "undocumented_export_variables": undocumented,
            "dictionary_variables_absent_from_export": unused,
        }
        if undocumented:
            report["summary"] = "review_required"

    return report
