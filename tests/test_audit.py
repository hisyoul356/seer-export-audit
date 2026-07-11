import json
import tempfile
import unittest
from pathlib import Path

from seer_export_audit.audit import audit_export
from seer_export_audit.cli import main


ROOT = Path(__file__).resolve().parents[1]


class AuditTests(unittest.TestCase):
    def test_synthetic_fixture_passes(self) -> None:
        report = audit_export(
            ROOT / "examples" / "synthetic_export.txt",
            ROOT / "examples" / "synthetic_dictionary.dic",
        )
        self.assertEqual(report["summary"], "pass")
        self.assertEqual(report["row_count"], 3)
        self.assertEqual(report["missing_by_column"]["stage_group"]["missing_cells"], 1)

    def test_irregular_rows_require_review(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            data = Path(temp_dir) / "bad.txt"
            data.write_text("a|b\n1|2\n3\n", encoding="utf-8")
            report = audit_export(data)
        self.assertEqual(report["summary"], "review_required")
        self.assertEqual(report["irregular_row_numbers"], [3])

    def test_cli_writes_both_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "reports"
            result = main([
                "audit",
                "--data", str(ROOT / "examples" / "synthetic_export.txt"),
                "--dictionary", str(ROOT / "examples" / "synthetic_dictionary.dic"),
                "--output", str(output),
            ])
            self.assertEqual(result, 0)
            self.assertTrue((output / "audit_report.md").exists())
            self.assertEqual(json.loads((output / "audit_report.json").read_text(encoding="utf-8"))["summary"], "pass")


if __name__ == "__main__":
    unittest.main()
