import pytest

from app.backend.chatbi.intent import (
    DeepSeekIntentProvider,
    IntentParseResult,
    UnsupportedIntentError,
    build_intent_messages,
    parse_llm_content,
)


def test_intent_prompt_contains_allowed_metadata_without_rows_or_credentials():
    messages = build_intent_messages("auto PO ratio by buyer")
    prompt_text = "\n".join(message["content"] for message in messages)

    assert "auto_po_ratio_summary" in prompt_text
    assert "supplier_dimension_summary" in prompt_text
    assert "Buyer key" in prompt_text
    assert "90000001" not in prompt_text
    assert "Dummy Supplier A" not in prompt_text
    assert "DEEPSEEK_API_KEY" not in prompt_text
    assert "chatbi.vw_po_item_reporting" not in prompt_text


def test_parse_llm_content_accepts_valid_tool_call_wrapper():
    result = parse_llm_content(
        """
        {
          "intent_summary": "User asks for auto PO ratio by buyer.",
          "tool_call": {
            "tool": "auto_po_ratio_summary",
            "arguments": {
              "group_by": "buyer",
              "numerator_rule": "po_created_by_equals_uc4cpic"
            }
          }
        }
        """,
        provider="deepseek",
        model="deepseek-v4-flash",
    )

    assert result.intent_summary["summary"] == "User asks for auto PO ratio by buyer."
    assert result.tool_call.tool == "auto_po_ratio_summary"
    assert result.tool_call.arguments.group_by == "buyer"


def test_parse_llm_content_rejects_unsupported_metric():
    with pytest.raises(UnsupportedIntentError) as exc:
        parse_llm_content(
            """
            {
              "intent_summary": "User asks for price trend.",
              "unsupported_reason": "Price trend is outside approved ChatBI MVP tools.",
              "tool_call": null
            }
            """,
            provider="deepseek",
            model="deepseek-v4-flash",
        )

    assert "Price trend" in str(exc.value)


def test_parse_llm_content_rejects_sql_shaped_tool_call():
    with pytest.raises(ValueError):
        parse_llm_content(
            """
            {
              "intent_summary": "Unsafe request.",
              "tool_call": {
                "tool": "supplier_dimension_summary",
                "arguments": {"group_by": "supplier", "sql": "select * from chatbi.vw_po_item_reporting"}
              }
            }
            """,
            provider="deepseek",
            model="deepseek-v4-flash",
        )


class FakeHttpResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeHttpClient:
    def __init__(self):
        self.payload = None

    def post(self, url, headers, json):
        self.url = url
        self.headers = headers
        self.payload = json
        return FakeHttpResponse(
            {
                "choices": [
                    {
                        "message": {
                            "content": '{"intent_summary":"Supplier count by supplier.","tool_call":{"tool":"supplier_dimension_summary","arguments":{"group_by":"supplier"}}}'
                        }
                    }
                ]
            }
        )


def test_deepseek_provider_posts_openai_compatible_chat_completion_payload():
    client = FakeHttpClient()
    provider = DeepSeekIntentProvider(api_key="test-key", http_client=client)

    result = provider.parse("supplier count by supplier")

    assert isinstance(result, IntentParseResult)
    assert client.url == "https://api.deepseek.com/chat/completions"
    assert client.headers["Authorization"] == "Bearer test-key"
    assert client.payload["model"] == "deepseek-v4-flash"
    assert client.payload["response_format"] == {"type": "json_object"}
    assert result.tool_call.tool == "supplier_dimension_summary"

