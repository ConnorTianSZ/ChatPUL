import csv
import os
from decimal import Decimal
from pathlib import Path
from typing import Callable, Protocol


class PoItemRepository(Protocol):
    @property
    def metadata(self) -> dict[str, object]:
        ...

    def list_rows(self) -> list[dict[str, str]]:
        ...


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


SQL_TO_SOURCE_HEADERS = {
    "wbs_element": "WBS element",
    "buyer_key": "PGr",
    "supplier_code": "Vendor",
    "supplier_name": "Name 1",
    "po_document_number": "Doc. No.",
    "po_item_number": "Item",
    "material_number": "Material",
    "material_short_text": "Short Text",
    "manufacturer_part_number": "MPN",
    "manufacturer_name": "Manufactur",
    "quantity": "Quantity",
    "net_price": "Net Price",
    "net_value_domestic_currency": "Net Value Domestic Currency",
    "currency": "Crcy",
    "doc_date": "Doc. Date",
    "pr_date": "PR Date",
    "order_confirmation_date": "order confirmatioin date",
    "goods_receipt_posting_date": "GR-D.o.Post",
    "statistical_delivery_date": "S.Del.Dat",
    "po_created_by": "PO created by",
    "plant": "Plant",
    "mrp_type": "MRP Type",
}


class SqlServerPoItemRepository:
    def __init__(self, connection_factory: Callable[[], object] | None = None) -> None:
        self.connection_factory = connection_factory or sqlserver_connection

    @property
    def metadata(self) -> dict[str, object]:
        return {
            "id": "chatbi_sqlserver_po_items",
            "version": "sqlserver-dummy-reporting-v1",
            "is_dummy": True,
            "database": os.getenv("SQLSERVER_DATABASE", "ChatPUL_Dev"),
            "schema": "chatbi",
            "view": "vw_po_item_reporting",
        }

    def list_rows(self) -> list[dict[str, str]]:
        connection = self.connection_factory()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    wbs_element, buyer_key, supplier_code, supplier_name,
                    po_document_number, po_item_number, material_number, material_short_text,
                    manufacturer_part_number, manufacturer_name, quantity, net_price,
                    net_value_domestic_currency, currency, doc_date, pr_date,
                    order_confirmation_date, goods_receipt_posting_date, statistical_delivery_date,
                    po_created_by, plant, mrp_type, import_batch_id,
                    source_dataset_id, source_dataset_version
                FROM chatbi.vw_po_item_reporting
                """
            )
            column_names = [description[0] for description in cursor.description]
            rows = []
            for record in cursor.fetchall():
                sql_row = dict(zip(column_names, record))
                rows.append(sql_row_to_po_item(sql_row))
            return rows
        finally:
            connection.close()


def sql_row_to_po_item(sql_row: dict[str, object]) -> dict[str, str]:
    return {
        source_header: normalize_sql_value(sql_row.get(sql_field))
        for sql_field, source_header in SQL_TO_SOURCE_HEADERS.items()
    }


def normalize_sql_value(value: object) -> str:
    if value is None:
        return ""
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, Decimal):
        normalized = value.normalize()
        if normalized == normalized.to_integral():
            return str(int(normalized))
        return format(normalized, "f")
    return str(value)


def sqlserver_connection_string() -> str:
    driver = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 17 for SQL Server")
    host = os.getenv("SQLSERVER_HOST", "localhost")
    instance = os.getenv("SQLSERVER_INSTANCE", "SQLEXPRESS")
    database = os.getenv("SQLSERVER_DATABASE", "ChatPUL_Dev")
    trusted = os.getenv("SQLSERVER_TRUSTED_CONNECTION", "true").lower() == "true"
    trust_cert = os.getenv("SQLSERVER_TRUST_SERVER_CERTIFICATE", "true").lower() == "true"
    server = host if instance == "" else host + "\\" + instance
    authentication = "Trusted_Connection=yes;" if trusted else ""
    certificate = "TrustServerCertificate=yes;" if trust_cert else ""
    return f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};{authentication}{certificate}"


def sqlserver_connection():
    try:
        import pyodbc
    except ImportError as exc:
        raise RuntimeError("pyodbc is required when DATA_MODE=sqlserver") from exc
    return pyodbc.connect(sqlserver_connection_string())


def get_po_item_repository() -> PoItemRepository:
    data_mode = os.getenv("DATA_MODE", "dummy_csv")
    if data_mode == "dummy_csv":
        return DummyPoItemRepository()
    if data_mode == "sqlserver":
        return SqlServerPoItemRepository()
    raise ValueError(f"Unsupported DATA_MODE: {data_mode}")
