import csv
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tests" / "fixtures" / "generate_dummy_po_items.py"
CSV_PATH = ROOT / "data" / "dummy" / "dummy_po_items.csv"
JSON_PATH = ROOT / "data" / "dummy" / "dummy_po_items_expected.json"
README_PATH = ROOT / "data" / "dummy" / "dummy_po_items_README.md"

EXPECTED_HEADER = [
    "WBS element",
    "PGr",
    "Vendor",
    "Name 1",
    "Doc. No.",
    "Item",
    "Material",
    "Short Text",
    "MPN",
    "Manufactur",
    "Quantity",
    "Net Price",
    "Net Value Domestic Currency",
    "Crcy",
    "Doc. Date",
    "PR Date",
    "order confirmatioin date",
    "GR-D.o.Post",
    "S.Del.Dat",
    "PO created by",
    "Plant",
    "MRP Type",
]


class DummyPoItemGeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        cls.stdout = result.stdout
        cls.stderr = result.stderr
        cls.returncode = result.returncode

    def test_script_runs_and_writes_required_files(self):
        self.assertEqual(self.returncode, 0, self.stderr)
        self.assertIn("PASS exactly 300 rows written", self.stdout)
        self.assertTrue(CSV_PATH.exists())
        self.assertTrue(JSON_PATH.exists())
        self.assertTrue(README_PATH.exists())

    def test_csv_schema_and_required_coverage(self):
        self.assertEqual(self.returncode, 0, self.stderr)
        with CSV_PATH.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.assertEqual(reader.fieldnames, EXPECTED_HEADER)
            rows = list(reader)

        self.assertEqual(len(rows), 300)
        self.assertEqual(len({(row["Doc. No."], row["Item"]) for row in rows}), 300)

        for row in rows:
            for field in ["Doc. No.", "Item", "PGr", "Vendor", "Doc. Date"]:
                self.assertNotEqual(row[field], "")
            self.assertEqual(row["Crcy"], "CNY")
            self.assertRegex(row["Name 1"], r"^Dummy Supplier [A-J]$")
            self.assertIn(row["Manufactur"], ["", "DummyMfr-X", "DummyMfr-Y", "DummyMfr-Z"])
            self.assertTrue(row["Doc. Date"].startswith("2026-"))

        blank_mfr = sum(1 for row in rows if row["Manufactur"] == "")
        blank_wbs = sum(1 for row in rows if row["WBS element"] == "")
        uc4_count = sum(1 for row in rows if row["PO created by"] == "UC4CPIC")

        self.assertGreaterEqual(blank_mfr, 10)
        self.assertGreaterEqual(blank_wbs, 20)
        self.assertGreaterEqual(uc4_count, 1)
        self.assertLess(uc4_count, 300)

    def test_expected_json_shape_and_totals(self):
        self.assertEqual(self.returncode, 0, self.stderr)
        expected = json.loads(JSON_PATH.read_text(encoding="utf-8"))

        self.assertEqual(expected["row_count"], 300)
        self.assertEqual(expected["seed"], 20260528)
        self.assertEqual(expected["auto_po_ratio"]["overall"]["total"], 300)
        self.assertEqual(sum(expected["manufacturer_distribution"].values()), 300)
        self.assertEqual(
            expected["wbs_distribution"]["with_wbs"] + expected["wbs_distribution"]["blank_wbs"],
            300,
        )
        self.assertEqual(sum(expected["pr_lead_time"]["buckets"].values()), 300)
        self.assertEqual(sum(expected["oc_lead_time"]["buckets"].values()), 300)

        for bucket_count in expected["pr_lead_time"]["buckets"].values():
            self.assertGreaterEqual(bucket_count, 1)
        for bucket_count in expected["oc_lead_time"]["buckets"].values():
            self.assertGreaterEqual(bucket_count, 1)

        self.assertIn("<BLANK>", expected["manufacturer_distribution"])
        self.assertIn("<BLANK>", expected["auto_po_ratio"]["by_manufacturer"])

    def test_readme_mentions_each_eval_and_synthetic_data_rule(self):
        self.assertEqual(self.returncode, 0, self.stderr)
        readme = README_PATH.read_text(encoding="utf-8")
        self.assertIn("Synthetic data only", readme)
        for eval_id in ["EVAL-017", "EVAL-018", "EVAL-019", "EVAL-020"]:
            self.assertIn(eval_id, readme)

    def test_script_is_deterministic(self):
        self.assertEqual(self.returncode, 0, self.stderr)

        first_hashes = {
            path: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in [CSV_PATH, JSON_PATH, README_PATH]
        }
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        second_hashes = {
            path: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in [CSV_PATH, JSON_PATH, README_PATH]
        }
        self.assertEqual(first_hashes, second_hashes)


if __name__ == "__main__":
    unittest.main()
