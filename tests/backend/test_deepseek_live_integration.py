import os

import pytest

from app.backend.chatbi.intent import DeepSeekIntentProvider


pytestmark = pytest.mark.skipif(
    os.getenv("CHATBI_LLM_ENABLED", "false").lower() != "true" or not os.getenv("DEEPSEEK_API_KEY"),
    reason="DeepSeek live tests require CHATBI_LLM_ENABLED=true and DEEPSEEK_API_KEY",
)


def test_deepseek_live_parses_dummy_auto_po_question_without_rows():
    provider = DeepSeekIntentProvider()

    result = provider.parse("Using dummy data, show auto PO ratio by buyer.")

    assert result.tool_call.tool == "auto_po_ratio_summary"
    assert result.tool_call.arguments.group_by == "buyer"
    assert result.intent_summary["provider"] == "deepseek"
    assert result.intent_summary["model"] == os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")

