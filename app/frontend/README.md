# Frontend

The first ChatPUL frontend slice is a local ChatBI workbench.

## Stack

- React
- TypeScript
- Vite
- Ant Design
- TanStack Query

## Boundaries

- The main workflow calls `POST /api/chatbi/ask`.
- `POST /api/chatbi/tools/execute` has client-side types for future debugging, but it is not the default UI path.
- Supplier Knowledge Base is a disabled placeholder only.
- No real company, supplier, pricing, purchasing, project, or internal report data should be used here.
- Source trace and source-column meanings are rendered only from backend metadata.

## Local Setup

Install dependencies once:

```powershell
npm install
```

Start the backend from the repository root:

```powershell
python -m uvicorn app.backend.main:app --host 127.0.0.1 --port 8000
```

Start the frontend from `app/frontend`:

```powershell
npm run dev
```

Open the Vite URL, usually `http://127.0.0.1:5173`.

The Vite dev server proxies `/api` to `http://127.0.0.1:8000`. The default frontend API base URL is `/api`; override with `VITE_API_BASE_URL` only for local experiments.

## Validation

```powershell
npm test
npm run typecheck
npm run build
```

When `CHATBI_LLM_ENABLED=false`, `/api/chatbi/ask` returns the backend disabled state. DeepSeek live testing is optional and must use dummy questions only.
