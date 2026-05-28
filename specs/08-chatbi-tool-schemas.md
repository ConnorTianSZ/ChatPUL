# ChatBI BI Tool JSON Schemas

## Purpose

This spec defines the first ChatBI BI tool JSON contracts.

These schemas describe the structured JSON that the LLM may produce when selecting a BI tool. They are not SQL schemas, not report lineage documents, and not backend implementation code.

The backend must validate the selected tool and arguments before execution. The LLM must not write SQL, request raw database rows, or add unapproved fields.

## Current Scope

The first ChatBI tools are:

1. `order_volume_summary`
2. `pr_lead_time_summary`
3. `po_confirmation_summary`
4. `auto_po_ratio_summary`

They are designed around the PO-item fact grain defined in `specs/04-chatbi-domain-spec.md`.

The first ChatBI version must cover these MVP data areas:

| MVP data area | Required BI tool support | Required grouping views |
| --- | --- | --- |
| Supplier dimension data | PO item count by supplier account/code and supplier name from the ChatBI reporting source | supplier; buyer when the question asks buyer-level supplier coverage |
| Manufacturer dimension data | PO item count by `Manufactur`, including explicit `<BLANK>` handling | manufacturer; buyer when the question asks buyer-level manufacturer coverage |
| Lead time data | PR lead time and PO confirmation lead time bucket summaries | buyer and manufacturer |
| Auto PO ratio data | `UC4CPIC / all` at PO-item grain | buyer and manufacturer |

Supplier and manufacturer dimensions in these tools are ChatBI analytical dimensions only. They are not Supplier Knowledge Base supplier profiles, represented-manufacturer records, authorization records, or capability records.

The current dummy fixture in `data/dummy/dummy_po_items.csv` and `data/dummy/dummy_po_items_expected.json` validates the first measurable structures:

- `row_count`;
- `manufacturer_distribution`;
- `wbs_distribution`;
- `pr_lead_time`;
- `oc_lead_time`;
- `auto_po_ratio`.

The current expected JSON directly covers auto PO ratio by buyer and by manufacturer. It directly covers PR and OC lead-time buckets by buyer. Lead-time-by-manufacturer is an MVP tool requirement and should be added to the expected JSON fixture before implementation work uses manufacturer-level lead-time tests.

Real data will come from approved SAP exports, the future canonical ChatBI Excel workbook, and SQL Server staging/reporting objects. Dummy data comes from `tests/fixtures/generate_dummy_po_items.py` and is intentionally synthetic.

## Shared Rules

Every tool call uses this envelope shape:

```json
{
  "tool": "tool_name",
  "arguments": {}
}
```

Shared validation rules:

- `tool` must match one of the approved tool names.
- `arguments` must match the selected tool schema.
- Unknown properties are rejected.
- Raw SQL, database names, table names, row payloads, and free-form formulas are not accepted as tool arguments.
- Date strings use `YYYY-MM-DD`.
- Blank manufacturer handling is explicit. When grouped by manufacturer, blank source values should be returned under the label `<BLANK>` unless the user explicitly filters them out.
- `time_range` defaults to `Doc. Date` / `doc_date` if omitted.
- MVP working-day calculations use Excel `NETWORKDAYS` semantics: Monday through Friday only, no public-holiday or company-calendar adjustment.

## Common Argument Concepts

The schemas below repeat common concepts rather than relying on hidden defaults:

| Concept | Meaning |
| --- | --- |
| `group_by` | The result dimension requested by the user. `none` means an overall summary. |
| `time_range` | Optional inclusive date range filter. |
| `filters` | Optional structured filters over approved PO-item dimensions. |
| `sort` | Optional result ordering for grouped outputs. |
| `limit` | Optional row limit for grouped outputs; ignored for bucket-only summaries. |

Common filter fields:

| Filter | Source meaning |
| --- | --- |
| `buyer_keys` | `PGr` values. |
| `supplier_codes` | `Vendor` values. |
| `supplier_names` | `Name 1` values. |
| `manufacturer_names` | `Manufactur` values, excluding blank unless `<BLANK>` is explicitly requested. |
| `include_blank_manufacturer` | Whether blank `Manufactur` rows are included. Defaults to true. |
| `wbs_scope` | `all`, `with_wbs`, or `blank_wbs`. |
| `plants` | `Plant` values. |
| `mrp_types` | `MRP Type` values. |
| `po_created_by` | `PO created by` values. This is a filter only; it must not redefine the auto PO ratio numerator. |

## Tool 1: `order_volume_summary`

### Intent

Summarize PO-item volume from the approved ChatBI PO-item reporting source.

This tool covers supplier, manufacturer, buyer, WBS, plant, MRP, and month-level count questions. In the MVP, the stable measure is PO item count. Order value output is deferred until permission and display rules are approved.

### Dummy Expected JSON Coverage

This tool can validate against:

- `row_count` when `group_by = "none"`;
- `manufacturer_distribution` when `group_by = "manufacturer"`;
- `wbs_distribution` when `group_by = "wbs_status"`.

The current expected JSON does not yet include supplier-level or plant-level distributions. Supplier-level grouping remains an MVP tool requirement because supplier dimension data is required for the first ChatBI version.

### Input JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "order_volume_summary tool call",
  "type": "object",
  "required": ["tool", "arguments"],
  "additionalProperties": false,
  "properties": {
    "tool": { "const": "order_volume_summary" },
    "arguments": {
      "type": "object",
      "required": ["group_by"],
      "additionalProperties": false,
      "properties": {
        "group_by": {
          "type": "string",
          "enum": ["none", "buyer", "supplier", "manufacturer", "wbs_status", "plant", "mrp_type", "month"]
        },
        "time_range": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "date_field": {
              "type": "string",
              "enum": ["doc_date", "pr_date", "order_confirmation_date", "goods_receipt_posting_date", "statistical_delivery_date"],
              "default": "doc_date"
            },
            "from": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" },
            "to": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" }
          }
        },
        "filters": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "buyer_keys": { "type": "array", "items": { "type": "string" } },
            "supplier_codes": { "type": "array", "items": { "type": "string" } },
            "supplier_names": { "type": "array", "items": { "type": "string" } },
            "manufacturer_names": { "type": "array", "items": { "type": "string" } },
            "include_blank_manufacturer": { "type": "boolean", "default": true },
            "wbs_scope": { "type": "string", "enum": ["all", "with_wbs", "blank_wbs"], "default": "all" },
            "plants": { "type": "array", "items": { "type": "string" } },
            "mrp_types": { "type": "array", "items": { "type": "string" } },
            "po_created_by": { "type": "array", "items": { "type": "string" } }
          }
        },
        "sort": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "by": { "type": "string", "enum": ["po_item_count", "group_key"] },
            "direction": { "type": "string", "enum": ["asc", "desc"], "default": "desc" }
          }
        },
        "limit": { "type": "integer", "minimum": 1, "maximum": 100 }
      }
    }
  }
}
```

### Result Contract

Expected result fields:

- `tool`: `order_volume_summary`;
- `understood_request`: one sentence;
- `group_by`;
- `filters_applied`;
- `rows`: grouped result rows with `group_key`, `po_item_count`, and optional `blank_bucket`;
- `total`: total PO item count after filters;
- `source_trace`: data source, date field, refresh/import batch when available.

## Tool 2: `pr_lead_time_summary`

### Intent

Summarize PR lead time from PR creation date to PO document date.

Formula:

`NETWORKDAYS(PR Date, Doc. Date) - 1`

Rows with missing or invalid `PR Date` are classified as `not statistic`.

### Dummy Expected JSON Coverage

This tool can validate against:

- `pr_lead_time.buckets` when `group_by = "none"`;
- `pr_lead_time.by_buyer` when `group_by = "buyer"`.

`group_by = "manufacturer"` is also required for the first ChatBI version. The dummy expected JSON should be extended with `pr_lead_time.by_manufacturer` before SQL/backend implementation uses this scenario as an automated acceptance check.

### Input JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "pr_lead_time_summary tool call",
  "type": "object",
  "required": ["tool", "arguments"],
  "additionalProperties": false,
  "properties": {
    "tool": { "const": "pr_lead_time_summary" },
    "arguments": {
      "type": "object",
      "required": ["group_by"],
      "additionalProperties": false,
      "properties": {
        "group_by": {
          "type": "string",
          "enum": ["none", "buyer", "supplier", "manufacturer", "month"]
        },
        "bucket_set": {
          "type": "string",
          "const": "spec_default_pr_lead_time"
        },
        "time_range": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "date_field": {
              "type": "string",
              "enum": ["doc_date", "pr_date"],
              "default": "doc_date"
            },
            "from": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" },
            "to": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" }
          }
        },
        "filters": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "buyer_keys": { "type": "array", "items": { "type": "string" } },
            "supplier_codes": { "type": "array", "items": { "type": "string" } },
            "supplier_names": { "type": "array", "items": { "type": "string" } },
            "manufacturer_names": { "type": "array", "items": { "type": "string" } },
            "include_blank_manufacturer": { "type": "boolean", "default": true },
            "wbs_scope": { "type": "string", "enum": ["all", "with_wbs", "blank_wbs"], "default": "all" },
            "plants": { "type": "array", "items": { "type": "string" } },
            "mrp_types": { "type": "array", "items": { "type": "string" } }
          }
        }
      }
    }
  }
}
```

### Result Contract

Expected result fields:

- `tool`: `pr_lead_time_summary`;
- `understood_request`: one sentence;
- `group_by`;
- `buckets`: counts for `0<=X<=3`, `3<X<=7`, `>7days`, and `not statistic`;
- `groups`: optional grouped bucket counts;
- `calculation_note`: states `NETWORKDAYS(PR Date, Doc. Date) - 1`;
- `source_trace`.

## Tool 3: `po_confirmation_summary`

### Intent

Summarize PO order confirmation lead time and order-confirmation status.

Formula:

`NETWORKDAYS(Doc. Date, order confirmatioin date) - 1`

Rows with blank order confirmation dates are classified as:

- `Delivered without OC` when `GR-D.o.Post` is populated;
- `no order confirmation` otherwise.

### Dummy Expected JSON Coverage

This tool can validate against:

- `oc_lead_time.buckets` when `group_by = "none"`;
- `oc_lead_time.by_buyer` when `group_by = "buyer"`.

`group_by = "manufacturer"` is also required for the first ChatBI version. The dummy expected JSON should be extended with `oc_lead_time.by_manufacturer` before SQL/backend implementation uses this scenario as an automated acceptance check.

### Input JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "po_confirmation_summary tool call",
  "type": "object",
  "required": ["tool", "arguments"],
  "additionalProperties": false,
  "properties": {
    "tool": { "const": "po_confirmation_summary" },
    "arguments": {
      "type": "object",
      "required": ["group_by"],
      "additionalProperties": false,
      "properties": {
        "group_by": {
          "type": "string",
          "enum": ["none", "buyer", "supplier", "manufacturer", "month"]
        },
        "bucket_set": {
          "type": "string",
          "const": "spec_default_po_confirmation"
        },
        "time_range": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "date_field": {
              "type": "string",
              "enum": ["doc_date", "order_confirmation_date", "goods_receipt_posting_date"],
              "default": "doc_date"
            },
            "from": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" },
            "to": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" }
          }
        },
        "filters": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "buyer_keys": { "type": "array", "items": { "type": "string" } },
            "supplier_codes": { "type": "array", "items": { "type": "string" } },
            "supplier_names": { "type": "array", "items": { "type": "string" } },
            "manufacturer_names": { "type": "array", "items": { "type": "string" } },
            "include_blank_manufacturer": { "type": "boolean", "default": true },
            "wbs_scope": { "type": "string", "enum": ["all", "with_wbs", "blank_wbs"], "default": "all" },
            "plants": { "type": "array", "items": { "type": "string" } },
            "mrp_types": { "type": "array", "items": { "type": "string" } }
          }
        }
      }
    }
  }
}
```

### Result Contract

Expected result fields:

- `tool`: `po_confirmation_summary`;
- `understood_request`: one sentence;
- `group_by`;
- `buckets`: counts for `<=3`, `3<X<=7`, `>7`, `no order confirmation`, and `Delivered without OC`;
- `groups`: optional grouped bucket counts;
- `calculation_note`: states `NETWORKDAYS(Doc. Date, order confirmatioin date) - 1` and blank-confirmation classification rules;
- `source_trace`.

## Tool 4: `auto_po_ratio_summary`

### Intent

Calculate automatic PO ratio from PO item rows.

Definition:

`count(PO created by = UC4CPIC) / count(all PO item rows in the same filter context)`

The numerator rule is fixed for the MVP. Tool arguments may filter the dataset, but they must not redefine the numerator creator.

### Dummy Expected JSON Coverage

This tool can validate against:

- `auto_po_ratio.overall` when `group_by = "none"`;
- `auto_po_ratio.by_buyer` when `group_by = "buyer"`;
- `auto_po_ratio.by_manufacturer` when `group_by = "manufacturer"`.

### Input JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "auto_po_ratio_summary tool call",
  "type": "object",
  "required": ["tool", "arguments"],
  "additionalProperties": false,
  "properties": {
    "tool": { "const": "auto_po_ratio_summary" },
    "arguments": {
      "type": "object",
      "required": ["group_by"],
      "additionalProperties": false,
      "properties": {
        "group_by": {
          "type": "string",
          "enum": ["none", "buyer", "supplier", "manufacturer", "month"]
        },
        "numerator_rule": {
          "type": "string",
          "const": "po_created_by_equals_uc4cpic"
        },
        "time_range": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "date_field": {
              "type": "string",
              "enum": ["doc_date", "pr_date", "order_confirmation_date", "goods_receipt_posting_date", "statistical_delivery_date"],
              "default": "doc_date"
            },
            "from": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" },
            "to": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" }
          }
        },
        "filters": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "buyer_keys": { "type": "array", "items": { "type": "string" } },
            "supplier_codes": { "type": "array", "items": { "type": "string" } },
            "supplier_names": { "type": "array", "items": { "type": "string" } },
            "manufacturer_names": { "type": "array", "items": { "type": "string" } },
            "include_blank_manufacturer": { "type": "boolean", "default": true },
            "wbs_scope": { "type": "string", "enum": ["all", "with_wbs", "blank_wbs"], "default": "all" },
            "plants": { "type": "array", "items": { "type": "string" } },
            "mrp_types": { "type": "array", "items": { "type": "string" } }
          }
        },
        "sort": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "by": { "type": "string", "enum": ["ratio", "uc4_count", "total", "group_key"] },
            "direction": { "type": "string", "enum": ["asc", "desc"], "default": "desc" }
          }
        },
        "limit": { "type": "integer", "minimum": 1, "maximum": 100 }
      }
    }
  }
}
```

### Result Contract

Expected result fields:

- `tool`: `auto_po_ratio_summary`;
- `understood_request`: one sentence;
- `group_by`;
- `numerator_rule`: `PO created by = UC4CPIC`;
- `overall` or `groups`, each with `uc4_count`, `total`, and `ratio`;
- `source_trace`.

## Tool Selection Guidance

The LLM should select tools by business intent:

| User intent | Tool |
| --- | --- |
| How many PO items, by supplier, manufacturer, buyer, WBS status, plant, MRP, or month | `order_volume_summary` |
| PR-to-PO creation speed, PR lead time, PR bucket distribution | `pr_lead_time_summary` |
| Order confirmation speed, missing OC, delivered without OC | `po_confirmation_summary` |
| Auto PO ratio, UC4 share, automation rate | `auto_po_ratio_summary` |

If a user asks for unsupported metrics such as price trend, value-weighted automation ratio, quality risk, or delivery risk, the backend should reject the tool call or ask for clarification until a later approved schema exists.

## Open Questions

- Should `order_volume_summary` expose net order value after permission and display rules are approved?
- Should supplier-level expected JSON be added to the dummy fixture for future validation?
- Which response shape should the frontend prefer for grouped bucket results: nested table rows or chart-ready series?
