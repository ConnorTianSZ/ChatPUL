from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MIGRATION = ROOT / "database" / "sqlserver" / "migrations" / "001_create_chatbi_dummy_reporting.sql"
RECONCILIATION = ROOT / "database" / "sqlserver" / "scripts" / "reconcile_chatbi_dummy_reporting.sql"
LOADER = ROOT / "database" / "sqlserver" / "dummy-data" / "load_dummy_po_items.py"


def test_sqlserver_migration_defines_isolated_chatbi_reporting_objects():
    sql = MIGRATION.read_text(encoding="utf-8")

    assert "CREATE SCHEMA chatbi" in sql
    assert "CREATE TABLE chatbi.import_batch" in sql
    assert "CREATE TABLE chatbi.po_item_staging" in sql
    assert "CREATE OR ALTER VIEW chatbi.vw_po_item_reporting" in sql
    assert "supplier_kb" not in sql.lower()
    assert "JOIN supplier" not in sql


def test_sqlserver_reconciliation_script_uses_reporting_view_only():
    sql = RECONCILIATION.read_text(encoding="utf-8")

    assert "chatbi.vw_po_item_reporting" in sql
    assert "COUNT_BIG(*)" in sql
    assert "UC4CPIC" in sql
    assert "supplier_kb" not in sql.lower()


def test_dummy_loader_uses_dummy_csv_and_environment_configuration_only():
    text = LOADER.read_text(encoding="utf-8")

    assert "data/dummy/dummy_po_items.csv" in text
    assert "data/raw" not in text
    assert "SQLSERVER_DATABASE" in text
    assert "DEEPSEEK_API_KEY" not in text

