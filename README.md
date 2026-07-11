# seer-export-audit

Privacy-conscious quality control for delimited registry exports and their
data dictionaries.

`seer-export-audit` is a small, dependency-free command-line tool that checks
whether an exported table is structurally ready for reproducible analysis. It
detects duplicate or blank headers, irregular rows, missingness, and mismatches
between an export and a companion data dictionary. It then writes a JSON report
for pipelines and a readable Markdown report for methods review.

It is designed for SEER*Stat-style workflows, but intentionally operates on
generic delimited exports. It does not read SEER databases, send data anywhere,
or replace registry documentation.

> **Data rule:** Never commit registry exports, patient-level data, or study
> files. This repository includes synthetic fixtures only; see [NOTICE.md](NOTICE.md).

## Why this exists

Population-based studies often begin with a manually exported table. Before
modelling, analysts need a stable audit trail showing which variables were
exported, whether rows are well formed, and whether the supplied dictionary
actually documents the fields in use. This tool makes that handoff reviewable
without exposing source data.

## Quick start

Requires Python 3.10+ and has no third-party dependencies.

```bash
python -m pip install -e .
seer-export-audit audit \
  --data examples/synthetic_export.txt \
  --dictionary examples/synthetic_dictionary.dic \
  --output reports/example
```

The command writes:

```text
reports/example/
  audit_report.json
  audit_report.md
```

Alternatively, run directly from a clone:

```bash
python -m seer_export_audit audit --data examples/synthetic_export.txt --output reports/example
```

## Companion dictionary format

The dictionary is a UTF-8 delimited text file with a header row. Only
`variable` is required. `label`, `type`, and `allowed_values` are optional.

### Important: native `.dic` files

This tool does **not** directly parse every native or vendor-specific
SEER*Stat `.dic` file. Before auditing, export or convert the relevant field
definitions into the simple delimited format described below. The conversion
file must have a `variable` header; it may use comma, tab, pipe, or semicolon
as its delimiter. This limitation is intentional and keeps the audit contract
transparent and reviewable.

```text
variable|label|type|allowed_values
diagnosis_year|Year of diagnosis|integer|2000-2026
sex|Sex at diagnosis|string|1,2
```

The delimiter is detected automatically for comma, tab, pipe, and semicolon
files. This deliberately simple interchange format makes the audit layer easy
to review and does not claim to parse every vendor-specific dictionary format.

## What is checked

- file encoding and delimiter detection;
- blank and duplicate column headers;
- data rows with the wrong number of cells;
- total rows and per-column missingness;
- fields in the export but absent from the dictionary;
- fields in the dictionary but absent from the export.

## Development

```bash
python -m unittest discover -s tests -v
```

Contributions, bug reports, and requests for additional export formats are
welcome. Please use synthetic, aggregate, or schema-only examples in issues.

## Scope and non-goals

- This project is not affiliated with NCI, SEER, or SEER*Stat.
- It does not validate study design, coding decisions, or registry eligibility.
- It does not upload, retain, or transmit input data.
- Users remain responsible for data-use agreements and disclosure controls.

## License

[MIT](LICENSE)
