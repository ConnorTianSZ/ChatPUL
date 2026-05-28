from fastapi.testclient import TestClient

from app.backend.main import app


client = TestClient(app)


def test_execute_tool_endpoint_returns_result_with_source_trace():
    response = client.post(
        "/api/chatbi/tools/execute",
        json={
            "tool": "auto_po_ratio_summary",
            "arguments": {
                "group_by": "none",
                "numerator_rule": "po_created_by_equals_uc4cpic",
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["tool"] == "auto_po_ratio_summary"
    assert body["understood_request"] == "Executed auto_po_ratio_summary grouped by none against dummy PO-item data."
    assert body["overall"] == {"uc4_count": 104, "total": 300, "ratio": 0.346667}
    assert body["source_trace"]["dataset"]["id"] == "dummy_po_items"
    assert body["source_trace"]["dataset"]["is_dummy"] is True


def test_execute_tool_endpoint_rejects_invalid_shape_before_execution():
    response = client.post(
        "/api/chatbi/tools/execute",
        json={
            "tool": "supplier_dimension_summary",
            "arguments": {"group_by": "supplier", "formula": "sum(Net Price)"},
        },
    )

    assert response.status_code == 422
    body = response.json()
    assert body["detail"][0]["type"] == "extra_forbidden"

