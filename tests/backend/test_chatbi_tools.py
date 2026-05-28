import json
from pathlib import Path

from app.backend.chatbi.executor import execute_tool_call
from app.backend.chatbi.models import parse_tool_call
from app.backend.chatbi.repository import DummyPoItemRepository


ROOT = Path(__file__).resolve().parents[2]
EXPECTED = json.loads((ROOT / "data" / "dummy" / "dummy_po_items_expected.json").read_text(encoding="utf-8"))


def execute(payload):
    repository = DummyPoItemRepository(ROOT / "data" / "dummy" / "dummy_po_items.csv")
    return execute_tool_call(parse_tool_call(payload), repository)


def rows_by_key(result):
    return {row["group_key"]: row for row in result["rows"]}


def groups_by_key(result):
    return {row["group_key"]: row for row in result["groups"]}


def test_supplier_dimension_summary_matches_supplier_ground_truth():
    result = execute({"tool": "supplier_dimension_summary", "arguments": {"group_by": "supplier"}})

    rows = rows_by_key(result)
    assert result["understood_request"] == "Executed supplier_dimension_summary grouped by supplier against dummy PO-item data."
    assert result["total"] == EXPECTED["row_count"]
    assert result["source_trace"]["dataset"]["is_dummy"] is True
    assert set(rows) == set(EXPECTED["supplier_distribution"])

    for supplier_code, expected_entry in EXPECTED["supplier_distribution"].items():
        assert rows[supplier_code]["supplier_name"] == expected_entry["supplier_name"]
        assert rows[supplier_code]["po_item_count"] == expected_entry["po_item_count"]


def test_manufacturer_dimension_summary_keeps_blank_bucket_explicit():
    result = execute({"tool": "manufacturer_dimension_summary", "arguments": {"group_by": "manufacturer"}})

    rows = rows_by_key(result)
    assert rows["<BLANK>"]["is_blank_manufacturer"] is True
    for manufacturer, count in EXPECTED["manufacturer_distribution"].items():
        assert rows[manufacturer]["po_item_count"] == count


def test_wbs_scope_filter_keeps_blank_wbs_queryable():
    result = execute(
        {
            "tool": "supplier_dimension_summary",
            "arguments": {"group_by": "wbs_status", "filters": {"wbs_scope": "blank_wbs"}},
        }
    )

    rows = rows_by_key(result)
    assert result["total"] == EXPECTED["wbs_distribution"]["blank_wbs"]
    assert rows == {"blank_wbs": {"group_key": "blank_wbs", "po_item_count": EXPECTED["wbs_distribution"]["blank_wbs"]}}


def test_auto_po_ratio_summary_matches_manufacturer_ground_truth():
    result = execute(
        {
            "tool": "auto_po_ratio_summary",
            "arguments": {
                "group_by": "manufacturer",
                "numerator_rule": "po_created_by_equals_uc4cpic",
            },
        }
    )

    groups = groups_by_key(result)
    for manufacturer, expected_entry in EXPECTED["auto_po_ratio"]["by_manufacturer"].items():
        assert groups[manufacturer]["uc4_count"] == expected_entry["uc4_count"]
        assert groups[manufacturer]["total"] == expected_entry["total"]
        assert groups[manufacturer]["ratio"] == expected_entry["ratio"]


def test_lead_time_summary_matches_buyer_and_manufacturer_ground_truth():
    by_buyer = execute(
        {"tool": "lead_time_summary", "arguments": {"lead_time_type": "both", "group_by": "buyer"}}
    )
    buyer_groups = groups_by_key(by_buyer)

    for buyer, expected_buckets in EXPECTED["pr_lead_time"]["by_buyer"].items():
        assert buyer_groups[buyer]["pr_buckets"] == expected_buckets
    for buyer, expected_buckets in EXPECTED["oc_lead_time"]["by_buyer"].items():
        assert buyer_groups[buyer]["po_confirmation_buckets"] == expected_buckets

    by_manufacturer = execute(
        {"tool": "lead_time_summary", "arguments": {"lead_time_type": "both", "group_by": "manufacturer"}}
    )
    manufacturer_groups = groups_by_key(by_manufacturer)

    for manufacturer, expected_buckets in EXPECTED["pr_lead_time"]["by_manufacturer"].items():
        assert manufacturer_groups[manufacturer]["pr_buckets"] == expected_buckets
    for manufacturer, expected_buckets in EXPECTED["oc_lead_time"]["by_manufacturer"].items():
        assert manufacturer_groups[manufacturer]["po_confirmation_buckets"] == expected_buckets


def test_source_trace_is_structured_and_does_not_expose_raw_rows():
    result = execute(
        {
            "tool": "supplier_dimension_summary",
            "arguments": {
                "group_by": "buyer",
                "filters": {"buyer_keys": ["MFA"], "include_blank_manufacturer": False},
            },
        }
    )

    assert "raw_rows" not in result
    assert result["source_trace"]["tool"] == "supplier_dimension_summary"
    assert result["source_trace"]["filters_applied"]["buyer_keys"] == ["MFA"]
    assert result["source_trace"]["filters_applied"]["include_blank_manufacturer"] is False
    assert {"field_name", "source_header", "business_label", "meaning"} <= set(
        result["source_trace"]["source_columns"][0]
    )


def test_source_trace_includes_active_filter_source_columns():
    result = execute(
        {
            "tool": "supplier_dimension_summary",
            "arguments": {"group_by": "supplier", "filters": {"plants": ["P001"]}},
        }
    )

    source_field_names = {entry["field_name"] for entry in result["source_trace"]["source_columns"]}
    assert "plant" in source_field_names
