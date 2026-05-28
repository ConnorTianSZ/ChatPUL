import pytest
from pydantic import ValidationError

from app.backend.chatbi.models import parse_tool_call


def test_accepts_valid_structured_tool_call():
    call = parse_tool_call(
        {
            "tool": "auto_po_ratio_summary",
            "arguments": {
                "group_by": "manufacturer",
                "numerator_rule": "po_created_by_equals_uc4cpic",
            },
        }
    )

    assert call.tool == "auto_po_ratio_summary"
    assert call.arguments.group_by == "manufacturer"


@pytest.mark.parametrize(
    "payload",
    [
        {"tool": "price_trend_summary", "arguments": {"group_by": "supplier"}},
        {"tool": "supplier_dimension_summary", "arguments": {"group_by": "supplier"}, "sql": "select 1"},
        {"tool": "supplier_dimension_summary", "arguments": {"group_by": "supplier", "query": "select 1"}},
        {"tool": "supplier_dimension_summary", "arguments": {"group_by": "quality_risk"}},
        {
            "tool": "auto_po_ratio_summary",
            "arguments": {
                "group_by": "buyer",
                "numerator_rule": "po_created_by_equals_zuser1",
            },
        },
        {
            "tool": "lead_time_summary",
            "arguments": {
                "lead_time_type": "both",
                "group_by": "buyer",
                "filters": {"wbs_scope": "project_only"},
            },
        },
    ],
)
def test_rejects_unapproved_or_sql_shaped_tool_calls(payload):
    with pytest.raises(ValidationError):
        parse_tool_call(payload)

