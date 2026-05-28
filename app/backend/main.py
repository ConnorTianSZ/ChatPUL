from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from app.backend.chatbi.executor import execute_tool_call
from app.backend.chatbi.intent import (
    UnsupportedIntentError,
    get_intent_provider,
    llm_enabled,
)
from app.backend.chatbi.models import ChatBIAskRequest, parse_tool_call
from app.backend.chatbi.repository import get_po_item_repository


app = FastAPI(title="ChatPUL Backend")


def validation_detail(exc: Exception) -> Any:
    if hasattr(exc, "errors"):
        return exc.errors()
    return str(exc)


@app.post("/api/chatbi/tools/execute")
def execute_chatbi_tool(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        tool_call = parse_tool_call(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    repository = get_po_item_repository()
    return execute_tool_call(tool_call, repository)


@app.post("/api/chatbi/ask")
def ask_chatbi(payload: ChatBIAskRequest) -> dict[str, Any]:
    question = payload.question.strip()
    if not llm_enabled():
        raise HTTPException(status_code=503, detail="ChatBI LLM intent parsing is disabled.")

    try:
        intent = get_intent_provider().parse(question)
        result = execute_tool_call(intent.tool_call, get_po_item_repository())
    except UnsupportedIntentError as exc:
        raise HTTPException(status_code=422, detail={"unsupported_reason": str(exc)}) from exc
    except (ValidationError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=validation_detail(exc)) from exc

    return {
        "intent_summary": intent.intent_summary,
        "execution_summary": result["understood_request"],
        "tool_call": intent.tool_call.model_dump(),
        "result": result,
    }
