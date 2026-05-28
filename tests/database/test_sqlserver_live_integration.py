import json
import os
from pathlib import Path

import pytest

from app.backend.chatbi.executor import execute_tool_call
from app.backend.chatbi.models import parse_tool_call
from app.backend.chatbi.repository import SqlServerPoItemRepository


ROOT = Path(__file__).resolve().parents[2]
EXPECTED = json.loads((ROOT / "data" / "dummy" / "dummy_po_items_expected.json").read_text(encoding="utf-8"))


pytestmark = pytest.mark.skipif(
    os.getenv("CHATBI_SQLSERVER_TESTS_ENABLED", "false").lower() != "true",
    reason="SQL Server live tests require CHATBI_SQLSERVER_TESTS_ENABLED=true",
)


def test_sqlserver_repository_executes_auto_po_ratio_against_dummy_reporting_view():
    repository = SqlServerPoItemRepository()
    result = execute_tool_call(
        parse_tool_call(
            {
                "tool": "auto_po_ratio_summary",
                "arguments": {
                    "group_by": "none",
                    "numerator_rule": "po_created_by_equals_uc4cpic",
                },
            }
        ),
        repository,
    )

    assert result["overall"] == EXPECTED["auto_po_ratio"]["overall"]
    assert result["source_trace"]["dataset"]["schema"] == "chatbi"
    assert result["source_trace"]["dataset"]["view"] == "vw_po_item_reporting"

