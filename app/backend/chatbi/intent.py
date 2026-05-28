import json
import os
from dataclasses import dataclass
from typing import Any, Protocol

import httpx
from pydantic import ValidationError

from app.backend.chatbi.field_dictionary import FIELD_DICTIONARY
from app.backend.chatbi.models import ToolCall, parse_tool_call


APPROVED_TOOL_NAMES = (
    "supplier_dimension_summary",
    "manufacturer_dimension_summary",
    "lead_time_summary",
    "auto_po_ratio_summary",
)


@dataclass(frozen=True)
class IntentParseResult:
    intent_summary: dict[str, str]
    tool_call: ToolCall


class IntentProvider(Protocol):
    def parse(self, question: str) -> IntentParseResult:
        ...


class UnsupportedIntentError(Exception):
    pass


def field_dictionary_prompt_summary() -> list[dict[str, object]]:
    return [
        {
            "field_name": entry.field_name,
            "business_label": entry.business_label,
            "meaning": entry.meaning,
            "allowed_usages": list(entry.allowed_usages),
            "caveats": list(entry.caveats),
        }
        for entry in FIELD_DICTIONARY.values()
    ]


def approved_tool_contract_summary() -> dict[str, object]:
    return {
        "approved_tools": list(APPROVED_TOOL_NAMES),
        "tool_selection": {
            "supplier_dimension_summary": (
                "Supplier list, supplier PO item count, supplier coverage, supplier split by buyer or manufacturer."
            ),
            "manufacturer_dimension_summary": (
                "Manufacturer list, manufacturer PO item count, blank manufacturer bucket, manufacturer split by buyer."
            ),
            "lead_time_summary": (
                "PR lead time, PO confirmation lead time, missing OC, delivered without OC."
            ),
            "auto_po_ratio_summary": "Auto PO ratio, UC4 share, automation rate.",
        },
        "required_response_shape": {
            "intent_summary": "short deterministic sentence in the same language as the user when possible",
            "tool_call": {"tool": "one approved tool name", "arguments": "arguments matching the approved schema"},
            "unsupported_reason": "string only when the request is outside approved tool scope",
        },
        "scope_limits": [
            "No price trend, value-weighted automation ratio, quality risk, or delivery risk metrics.",
            "Do not write SQL.",
            "Do not request raw rows.",
            "Do not add table names, database names, formulas, or unapproved argument fields.",
        ],
    }


def build_intent_messages(question: str) -> list[dict[str, str]]:
    system_payload = {
        "role": "ChatBI intent parser",
        "instructions": [
            "Return JSON only.",
            "Select exactly one approved ChatBI tool when the request is supported.",
            "Return unsupported_reason and null tool_call when the user asks for an unsupported metric.",
            "Never write SQL or include SQL/table/database names in the tool call.",
            "Never ask for or include raw database rows, query results, credentials, or source data records.",
        ],
        "tool_contract": approved_tool_contract_summary(),
        "field_dictionary": field_dictionary_prompt_summary(),
    }
    return [
        {"role": "system", "content": json.dumps(system_payload, ensure_ascii=False)},
        {"role": "user", "content": question},
    ]


def parse_llm_content(content: str, provider: str, model: str) -> IntentParseResult:
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM response was not valid JSON") from exc

    if not isinstance(parsed, dict):
        raise ValueError("LLM response must be a JSON object")

    unsupported_reason = parsed.get("unsupported_reason")
    if unsupported_reason:
        raise UnsupportedIntentError(str(unsupported_reason))

    raw_tool_call = parsed.get("tool_call")
    if raw_tool_call is None and "tool" in parsed and "arguments" in parsed:
        raw_tool_call = parsed
    if raw_tool_call is None:
        raise ValueError("LLM response did not include tool_call")

    try:
        tool_call = parse_tool_call(raw_tool_call)
    except ValidationError as exc:
        raise ValueError("LLM tool_call failed backend validation") from exc

    return IntentParseResult(
        intent_summary={
            "provider": provider,
            "model": model,
            "summary": str(parsed.get("intent_summary", "LLM selected an approved ChatBI tool.")),
        },
        tool_call=tool_call,
    )


class DeepSeekIntentProvider:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        http_client: Any | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise RuntimeError("DEEPSEEK_API_KEY is required when CHATBI_LLM_ENABLED=true")
        self.base_url = (base_url or os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")).rstrip("/")
        self.model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")
        self.http_client = http_client or httpx.Client(timeout=30)

    def parse(self, question: str) -> IntentParseResult:
        response = self.http_client.post(
            self.base_url + "/chat/completions",
            headers={
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": build_intent_messages(question),
                "response_format": {"type": "json_object"},
                "stream": False,
            },
        )
        response.raise_for_status()
        payload = response.json()
        content = payload["choices"][0]["message"]["content"]
        return parse_llm_content(content, provider="deepseek", model=self.model)


def llm_enabled() -> bool:
    return os.getenv("CHATBI_LLM_ENABLED", "false").lower() == "true"


def get_intent_provider() -> IntentProvider:
    return DeepSeekIntentProvider()
