import csv
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CSV_PATH = ROOT / "data" / "dummy" / "dummy_po_items.csv"
MIGRATION_PATH = ROOT / "database" / "sqlserver" / "migrations" / "001_create_chatbi_dummy_reporting.sql"


def connection_string() -> str:
    driver = os.getenv("SQLSERVER_DRIVER", "ODBC Driver 17 for SQL Server")
    host = os.getenv("SQLSERVER_HOST", "localhost")
    instance = os.getenv("SQLSERVER_INSTANCE", "SQLEXPRESS")
    database = os.getenv("SQLSERVER_DATABASE", "ChatPUL_Dev")
    trusted = os.getenv("SQLSERVER_TRUSTED_CONNECTION", "true").lower() == "true"
    trust_cert = os.getenv("SQLSERVER_TRUST_SERVER_CERTIFICATE", "true").lower() == "true"
    server = host if instance == "" else host + "\\" + instance
    auth = "Trusted_Connection=yes;" if trusted else ""
    certificate = "TrustServerCertificate=yes;" if trust_cert else ""
    return f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};{auth}{certificate}"


def require_pyodbc():
    try:
        import pyodbc
    except ImportError as exc:
        raise SystemExit("pyodbc is required for SQL Server dummy loading. Install requirements.txt first.") from exc
    return pyodbc


def apply_migration(cursor) -> None:
    sql = MIGRATION_PATH.read_text(encoding="utf-8")
    for batch in sql.split("\nGO"):
        statement = batch.strip()
        if statement:
            cursor.execute(statement)


def none_if_blank(value: str) -> str | None:
    if value == "":
        return None
    return value


def load_rows(csv_path: Path = DEFAULT_CSV_PATH) -> int:
    pyodbc = require_pyodbc()
    connection = pyodbc.connect(connection_string())
    try:
        cursor = connection.cursor()
        apply_migration(cursor)
        with csv_path.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        cursor.execute(
            """
            INSERT INTO chatbi.import_batch
                (source_dataset_id, source_dataset_version, source_file_name, row_count)
            OUTPUT INSERTED.import_batch_id
            VALUES (?, ?, ?, ?)
            """,
            "dummy_po_items",
            "seed-20260528-rowcount-300",
            "data/dummy/dummy_po_items.csv",
            len(rows),
        )
        import_batch_id = cursor.fetchone()[0]

        insert_sql = """
            INSERT INTO chatbi.po_item_staging (
                import_batch_id, wbs_element, buyer_key, supplier_code, supplier_name,
                po_document_number, po_item_number, material_number, material_short_text,
                manufacturer_part_number, manufacturer_name, quantity, net_price,
                net_value_domestic_currency, currency, doc_date, pr_date,
                order_confirmation_date, goods_receipt_posting_date, statistical_delivery_date,
                po_created_by, plant, mrp_type
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        for row in rows:
            cursor.execute(
                insert_sql,
                import_batch_id,
                none_if_blank(row["WBS element"]),
                row["PGr"],
                row["Vendor"],
                row["Name 1"],
                row["Doc. No."],
                row["Item"],
                none_if_blank(row["Material"]),
                none_if_blank(row["Short Text"]),
                none_if_blank(row["MPN"]),
                none_if_blank(row["Manufactur"]),
                row["Quantity"],
                row["Net Price"],
                row["Net Value Domestic Currency"],
                none_if_blank(row["Crcy"]),
                row["Doc. Date"],
                none_if_blank(row["PR Date"]),
                none_if_blank(row["order confirmatioin date"]),
                none_if_blank(row["GR-D.o.Post"]),
                none_if_blank(row["S.Del.Dat"]),
                none_if_blank(row["PO created by"]),
                none_if_blank(row["Plant"]),
                none_if_blank(row["MRP Type"]),
            )
        connection.commit()
        return len(rows)
    finally:
        connection.close()


if __name__ == "__main__":
    count = load_rows()
    print(f"Loaded {count} dummy PO item rows into SQL Server.")
