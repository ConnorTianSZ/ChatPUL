# Backend

Backend application code lives here.

The first implemented slice is the ChatBI backend tool executor:

- FastAPI endpoint: `POST /api/chatbi/tools/execute`
- FastAPI endpoint: `POST /api/chatbi/ask`
- Structured ChatBI tool-call validation with Pydantic.
- Dummy PO-item CSV repository for local development.
- Backend-owned calculations for the four approved ChatBI MVP tools.
- Minimal field dictionary metadata for result labels and source traceability.
- Optional DeepSeek V4 Flash intent parsing for dummy-data local testing.

Current boundaries:

- The endpoint accepts structured tool JSON directly.
- Natural-language LLM parsing is disabled by default with `CHATBI_LLM_ENABLED=false`.
- SQL Server dummy reporting is available through `DATA_MODE=sqlserver` after local SQL setup.
- No real company data should be used on the development machine.

## Local Run

From the repository root:

```powershell
python -m uvicorn app.backend.main:app --host 127.0.0.1 --port 8000
```

The frontend Vite dev server proxies `/api` to this backend during local workbench testing.
