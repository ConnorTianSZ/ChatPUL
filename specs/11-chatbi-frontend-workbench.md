# ChatBI Frontend Workbench Milestone

## Purpose

This milestone adds the first frontend foundation for ChatBI after the backend dummy tool and intent parser contracts are stable.

The goal is a local demo workbench where a user can enter a dummy ChatBI question, call the existing `/api/chatbi/ask` endpoint, and inspect:

- LLM intent summary when LLM parsing is enabled;
- deterministic backend execution summary;
- result tables for the four approved ChatBI result shapes;
- structured `source_trace`;
- dummy/source status;
- a disabled Supplier Knowledge Base placeholder inside the unified entry point.

## Scope

This milestone may add:

- a React + TypeScript + Vite frontend under `app/frontend/`;
- Ant Design for workbench controls and layout;
- TanStack Query for API state management;
- a Vite dev proxy from `/api` to the local FastAPI backend;
- an API client for `POST /api/chatbi/ask`;
- typed client shapes for future `POST /api/chatbi/tools/execute` debugging;
- frontend rendering for existing backend result and source trace structures;
- frontend typecheck, build, and smoke/component acceptance checks;
- local README instructions for backend-first and frontend-second startup.

This milestone must not add:

- real company, supplier, price, purchasing, project, or internal report data;
- production authentication or authorization;
- complex charting;
- Supplier Knowledge Base upload, cleaning, search, or normalization;
- frontend-invented field meanings;
- SQL, raw database rows, credentials, or raw LLM prompt payload display.

## Pre-Acceptance Gate

Before frontend implementation starts, the current backend must be checked locally:

- run `python -m pytest -q`;
- start FastAPI locally;
- verify `POST /api/chatbi/tools/execute` with a dummy structured tool call;
- verify `POST /api/chatbi/ask` returns the disabled state when `CHATBI_LLM_ENABLED=false`;
- run DeepSeek live validation only when `DEEPSEEK_API_KEY` is configured, using dummy questions only;
- run SQL Server live validation only when the local SQL connection is configured and available.

DeepSeek and SQL Server live checks are optional gates. Missing local credentials or connection values must be recorded but must not block the frontend foundation.

Initial implementation pre-acceptance result on 2026-05-28:

- default backend suite: `44 passed, 2 skipped`;
- `/api/chatbi/tools/execute`: returned dummy `auto_po_ratio_summary` with structured source trace;
- `/api/chatbi/ask` with LLM disabled: returned HTTP 503 and disabled detail;
- `DEEPSEEK_API_KEY`: not configured in the shell;
- SQL Server connection env: not configured in the shell.

## Frontend Architecture

The frontend is a local single-page workbench.

Core modules:

- app shell: navigation, product name, and environment/source indicators;
- ChatBI page: question input, example prompts, submit action, loading state, errors, disabled LLM state, result inspection;
- Supplier KB placeholder: visible but explicitly disabled/coming-soon;
- API client: backend request/response types and fetch wrapper;
- result renderer: shape-tolerant display for approved ChatBI tool outputs;
- source trace renderer: structured metadata display from backend-provided fields.

The first screen must be the actual workbench, not a marketing page.

## Backend Interface

The frontend primary path uses:

- `POST /api/chatbi/ask`

The request shape is:

```json
{
  "question": "show auto PO ratio by manufacturer"
}
```

The response contains:

- `intent_summary`;
- `execution_summary`;
- `tool_call`;
- `result`.

The frontend may include type definitions for the existing structured execution endpoint:

- `POST /api/chatbi/tools/execute`

The UI must not expose this endpoint as the default user workflow in this milestone.

## Result Rendering Rules

The renderer must tolerate these existing backend shapes:

- dimension result rows, such as supplier or manufacturer summaries;
- auto PO ratio `overall` and `groups`;
- lead-time `buckets` and grouped buckets;
- structured errors from backend validation or disabled LLM state.

The renderer must not assume a single nested `result.result` object. Backend tool responses currently place result fields at the top level under the `/tools/execute` response, while `/ask` wraps the executed tool response under `result`.

## Source Trace Rules

`source_trace` must be displayed as structured metadata, not as free text.

At minimum, the frontend must show:

- dataset id;
- dataset version or refresh marker;
- dummy fixture marker;
- tool name;
- group-by value;
- applied filters;
- applied time range;
- source columns used.

For source columns, the frontend must display only backend-provided metadata such as:

- field name;
- source header;
- business label;
- meaning;
- source trace label.

The frontend must not invent tooltip text or business field meanings. Tooltip-ready source column display must come from backend metadata.

## UX Boundary

The visual direction is a quiet enterprise workbench:

- dense enough for repeated procurement analysis;
- restrained color use;
- clear navigation between ChatBI and the disabled Supplier KB area;
- explicit dummy/source status;
- error states that state what is unsupported without fabricating substitute metrics.

No hero page, decorative dashboard background, or marketing layout is allowed in this milestone.

## Frontend Environment

The default frontend API base URL is same-origin `/api`, so local Vite can proxy API calls to FastAPI.

Supported environment variable:

- `VITE_API_BASE_URL=/api`

The frontend README must document local startup order:

1. start backend;
2. start frontend;
3. open the Vite URL.

## Acceptance

The milestone is accepted when:

- backend `python -m pytest -q` passes;
- frontend dependency installation succeeds;
- frontend `npm run typecheck` passes;
- frontend `npm run build` passes;
- browser smoke opens the ChatBI page;
- dummy question `show auto PO ratio by manufacturer` can display a result, execution summary, and source trace when LLM parsing is enabled or mocked by test;
- unsupported metric `show price trend` displays a structured unsupported/error state instead of fabricated results;
- Supplier KB placeholder is visible and does not imply upload/search is implemented.

## Commit Boundaries

Commit A:

- adds this spec and records pre-acceptance;
- does not add frontend functionality.

Commit B:

- scaffolds React + TypeScript + Vite + Ant Design + TanStack Query;
- adds the app shell, ChatBI page, API client, result renderer, source trace renderer, and Supplier KB placeholder;
- updates README instructions.

Commit C:

- adds frontend acceptance checks and smoke/component tests;
- records post-acceptance results through testable scripts.
