# ChatBI Backend Tool Slice

## Purpose

This spec approves the first ChatBI implementation slice: backend-owned BI tool execution against the synthetic PO-item fixture.

The slice exists to prove the tool contracts, deterministic calculations, strict validation, minimal field semantics, and source traceability before SQL Server, frontend rendering, or LLM intent parsing are added.

## Approved Scope

The first backend slice supports only these approved tools from `specs/08-chatbi-tool-schemas.md`:

- `supplier_dimension_summary`
- `manufacturer_dimension_summary`
- `lead_time_summary`
- `auto_po_ratio_summary`

The only data source for development execution is `data/dummy/dummy_po_items.csv`. Expected values are derived from `data/dummy/dummy_po_items_expected.json`.

The API accepts structured tool JSON directly. It does not parse natural language and does not call an LLM.

## Explicit Non-Scope

This slice does not implement:

- SQL Server staging tables, migrations, views, stored procedures, or import scripts.
- Frontend UI, charting, or tooltip rendering.
- Natural-language to tool-call parsing.
- Supplier Knowledge Base features.
- Cross-feature supplier or manufacturer mapping.
- Real company data ingestion or validation.

## Validation Boundary

The backend must reject unsupported requests before data access.

Validation is structural:

- Tool names are limited to the four approved tool names.
- Tool arguments are typed models.
- Unknown properties are forbidden at the tool-call and argument levels.
- Unsupported enum values are rejected.
- Raw SQL, table names, query text, formula text, and unsupported metric instructions are not accepted as request fields.

The backend must not silently drop unknown request properties or coerce unsupported metric requests into a different metric.

## Minimal Field Dictionary

The backend must include a minimal ChatBI field dictionary for all exposed dummy PO-item source fields used by v1 tools.

Each dictionary entry must include:

- application field name;
- source header;
- business label;
- data type;
- business meaning suitable for a future tooltip;
- allowed usages such as filter, group, result, calculation, or source trace;
- source trace label;
- caveats when relevant.

The dictionary is used in this slice for result labels, validation support, and `source_trace`. Frontend tooltip rendering is deferred, but tooltip-ready field meanings must exist now so the backend is not semantically hollow.

## Result Semantics

`understood_request` in this slice is a deterministic backend execution summary. It is not an LLM interpretation and must not claim that an AI understood the user.

Every successful tool result must include `source_trace` generated from backend metadata and the field dictionary. At minimum it includes:

- dataset identifier;
- dataset version or refresh marker;
- dummy fixture marker;
- tool name;
- group-by value;
- filters applied;
- time range applied;
- source columns used.

When manufacturer values are grouped, blank source `Manufactur` values are represented as `<BLANK>` unless the request explicitly excludes blank manufacturers.

Lead-time calculations use Monday-through-Friday `NETWORKDAYS` semantics with no public-holiday or company-calendar adjustment.

Auto PO ratio is count-based at PO-item grain:

`count(PO created by = UC4CPIC) / count(all filtered PO item rows)`

## Acceptance Tests

Implementation is acceptable when automated tests prove:

- dummy fixture generation remains deterministic and synthetic;
- each field used by the tools has dictionary metadata;
- invalid tool calls from EVAL-024 are rejected before data access;
- unsupported metric-shaped requests are rejected by structure;
- each approved tool matches expected dummy fixture results;
- blank manufacturer, blank WBS, PR/OC lead-time buckets, and UC4CPIC ratio rules match `specs/07-eval-cases.md`;
- API responses contain deterministic `understood_request` values and structured `source_trace`;
- no LLM call, raw SQL, credentials, real data, or raw database rows are involved.

## Current Boundary

After this slice is stable, the next implementation slice may introduce SQL Server dummy staging/import/reporting objects. That later slice must preserve the public tool contracts unless a new approved spec changes them.
