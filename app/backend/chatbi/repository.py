import csv
from pathlib import Path


class DummyPoItemRepository:
    def __init__(self, csv_path: Path | None = None) -> None:
        root = Path(__file__).resolve().parents[3]
        self.csv_path = csv_path or root / "data" / "dummy" / "dummy_po_items.csv"

    @property
    def metadata(self) -> dict[str, object]:
        return {
            "id": "dummy_po_items",
            "version": "seed-20260528-rowcount-300",
            "path": "data/dummy/dummy_po_items.csv",
            "is_dummy": True,
            "fixture_generator": "tests/fixtures/generate_dummy_po_items.py",
        }

    def list_rows(self) -> list[dict[str, str]]:
        with self.csv_path.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
