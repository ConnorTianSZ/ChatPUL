from app.backend.chatbi.repository import (
    DummyPoItemRepository,
    SqlServerPoItemRepository,
    get_po_item_repository,
)


SQL_VIEW_ROW = {
    "wbs_element": "",
    "buyer_key": "MFA",
    "supplier_code": "80000001",
    "supplier_name": "Dummy Supplier A",
    "po_document_number": "90000001",
    "po_item_number": "00010",
    "material_number": "DUMMY-MAT-001",
    "material_short_text": "Dummy bracket assembly",
    "manufacturer_part_number": "DUMMY-MPN-0001",
    "manufacturer_name": None,
    "quantity": "5",
    "net_price": "20",
    "net_value_domestic_currency": "100",
    "currency": "CNY",
    "doc_date": "2026-01-07",
    "pr_date": "2026-01-05",
    "order_confirmation_date": "2026-01-09",
    "goods_receipt_posting_date": None,
    "statistical_delivery_date": "2026-01-16",
    "po_created_by": "UC4CPIC",
    "plant": "P001",
    "mrp_type": "ND",
    "import_batch_id": 1,
    "source_dataset_id": "dummy_po_items",
    "source_dataset_version": "seed-20260528-rowcount-300",
}


class FakeCursor:
    def __init__(self, rows):
        self.description = [(column,) for column in rows[0].keys()]
        self._rows = rows

    def execute(self, query):
        self.query = query
        return self

    def fetchall(self):
        return [tuple(row.values()) for row in self._rows]


class FakeConnection:
    def __init__(self, rows):
        self.rows = rows
        self.closed = False

    def cursor(self):
        return FakeCursor(self.rows)

    def close(self):
        self.closed = True


def test_sqlserver_repository_maps_reporting_view_rows_to_po_item_shape():
    connection = FakeConnection([SQL_VIEW_ROW])
    repository = SqlServerPoItemRepository(connection_factory=lambda: connection)

    rows = repository.list_rows()

    assert rows == [
        {
            "WBS element": "",
            "PGr": "MFA",
            "Vendor": "80000001",
            "Name 1": "Dummy Supplier A",
            "Doc. No.": "90000001",
            "Item": "00010",
            "Material": "DUMMY-MAT-001",
            "Short Text": "Dummy bracket assembly",
            "MPN": "DUMMY-MPN-0001",
            "Manufactur": "",
            "Quantity": "5",
            "Net Price": "20",
            "Net Value Domestic Currency": "100",
            "Crcy": "CNY",
            "Doc. Date": "2026-01-07",
            "PR Date": "2026-01-05",
            "order confirmatioin date": "2026-01-09",
            "GR-D.o.Post": "",
            "S.Del.Dat": "2026-01-16",
            "PO created by": "UC4CPIC",
            "Plant": "P001",
            "MRP Type": "ND",
        }
    ]
    assert connection.closed is True


def test_sqlserver_repository_metadata_identifies_sql_reporting_view():
    repository = SqlServerPoItemRepository(connection_factory=lambda: FakeConnection([SQL_VIEW_ROW]))

    metadata = repository.metadata

    assert metadata["id"] == "chatbi_sqlserver_po_items"
    assert metadata["is_dummy"] is True
    assert metadata["schema"] == "chatbi"
    assert metadata["view"] == "vw_po_item_reporting"


def test_get_po_item_repository_defaults_to_dummy_csv(monkeypatch):
    monkeypatch.delenv("DATA_MODE", raising=False)

    assert isinstance(get_po_item_repository(), DummyPoItemRepository)


def test_get_po_item_repository_selects_sqlserver(monkeypatch):
    monkeypatch.setenv("DATA_MODE", "sqlserver")

    assert isinstance(get_po_item_repository(), SqlServerPoItemRepository)

