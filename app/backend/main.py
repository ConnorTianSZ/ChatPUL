from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError

from app.backend.chatbi.executor import execute_tool_call
from app.backend.chatbi.models import parse_tool_call
from app.backend.chatbi.repository import get_po_item_repository


app = FastAPI(title="ChatPUL Backend")


@app.post("/api/chatbi/tools/execute")
def execute_chatbi_tool(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        tool_call = parse_tool_call(payload)
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    repository = get_po_item_repository()
    return execute_tool_call(tool_call, repository)
