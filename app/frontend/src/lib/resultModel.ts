import type { JsonValue, SourceTrace, ToolExecutionResult } from "../types/chatbi";

export type ResultTable = {
  title: string;
  rows: Record<string, JsonValue | undefined>[];
};

export type SourceTraceSummary = {
  datasetLabel: string;
  dummyLabel: string;
  toolLabel: string;
  groupByLabel: string;
  filters: Record<string, JsonValue>;
  timeRange: Record<string, JsonValue>;
  sourceColumns: {
    fieldName: string;
    label: string;
    sourceHeader: string;
    meaning: string;
    traceLabel: string;
  }[];
};

export function buildResultTables(result: ToolExecutionResult | undefined): ResultTable[] {
  if (!result) {
    return [];
  }

  const tables: ResultTable[] = [];

  if (result.overall && isRecord(result.overall)) {
    tables.push({ title: "Overall", rows: [flattenRow(result.overall)] });
  }
  if (result.rows?.length) {
    tables.push({ title: "Rows", rows: result.rows.map(flattenRow) });
  }
  if (result.groups?.length) {
    tables.push({ title: "Groups", rows: result.groups.map(flattenRow) });
  }
  addBucketTable(tables, "Buckets", result.buckets);
  addBucketTable(tables, "PR Buckets", result.pr_buckets);
  addBucketTable(tables, "PO Confirmation Buckets", result.po_confirmation_buckets);

  return tables;
}

export function describeSourceTrace(trace: SourceTrace | undefined): SourceTraceSummary {
  const dataset = trace?.dataset ?? {};
  const datasetId = asText(dataset.id, "Unknown dataset");
  const datasetVersion = asText(dataset.version, "unversioned");

  return {
    datasetLabel: `${datasetId} / ${datasetVersion}`,
    dummyLabel: dataset.is_dummy === true ? "Dummy fixture" : "Non-dummy source",
    toolLabel: asText(trace?.tool ?? trace?.tool_name, "Unknown tool"),
    groupByLabel: asText(trace?.group_by, "none"),
    filters: toRecord(trace?.filters_applied),
    timeRange: toRecord(trace?.time_range_applied),
    sourceColumns: (trace?.source_columns ?? []).map((column) => ({
      fieldName: asText(column.field_name, "unknown_field"),
      label: asText(column.business_label, asText(column.field_name, "Unknown field")),
      sourceHeader: asText(column.source_header, "unknown source header"),
      meaning: asText(column.meaning, ""),
      traceLabel: asText(column.source_trace_label, ""),
    })),
  };
}

export function formatCell(value: JsonValue | undefined): string {
  if (value === undefined || value === null) {
    return "";
  }
  if (typeof value === "boolean") {
    return value ? "true" : "false";
  }
  if (typeof value === "number") {
    return Number.isInteger(value) ? String(value) : value.toLocaleString(undefined, { maximumFractionDigits: 6 });
  }
  if (typeof value === "string") {
    return value;
  }
  return JSON.stringify(value);
}

function addBucketTable(tables: ResultTable[], title: string, buckets: Record<string, number> | undefined): void {
  if (!buckets) {
    return;
  }
  tables.push({
    title,
    rows: Object.entries(buckets).map(([bucket, count]) => ({ bucket, count })),
  });
}

function flattenRow(row: Record<string, JsonValue | undefined>): Record<string, JsonValue | undefined> {
  const flattened: Record<string, JsonValue | undefined> = {};
  for (const [key, value] of Object.entries(row)) {
    if (isRecord(value)) {
      for (const [childKey, childValue] of Object.entries(value)) {
        flattened[`${key}.${childKey}`] = childValue as JsonValue;
      }
    } else {
      flattened[key] = value;
    }
  }
  return flattened;
}

function asText(value: unknown, fallback: string): string {
  return typeof value === "string" && value.length > 0 ? value : fallback;
}

function toRecord(value: unknown): Record<string, JsonValue> {
  if (!isRecord(value)) {
    return {};
  }
  return value as Record<string, JsonValue>;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
