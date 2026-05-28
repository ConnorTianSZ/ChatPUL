# Backend

Backend application code lives here.

The first implemented slice is the ChatBI backend tool executor:

- FastAPI endpoint: `POST /api/chatbi/tools/execute`
- Structured ChatBI tool-call validation with Pydantic.
- Dummy PO-item CSV repository for local development.
- Backend-owned calculations for the four approved ChatBI MVP tools.
- Minimal field dictionary metadata for result labels and source traceability.

Current boundaries:

- The endpoint accepts structured tool JSON directly.
- No natural-language LLM parsing is implemented in this slice.
- No SQL Server schema, migration, import, or reporting view is implemented in this slice.
- No real company data should be used on the development machine.
