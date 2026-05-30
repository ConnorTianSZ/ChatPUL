export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | JsonValue[] | { [key: string]: JsonValue };

export type ToolName =
  | "supplier_dimension_summary"
  | "manufacturer_dimension_summary"
  | "lead_time_summary"
  | "auto_po_ratio_summary";

export type IntentSummary = {
  provider?: string;
  model?: string;
  summary?: string;
  [key: string]: JsonValue | undefined;
};

export type ToolCall = {
  tool?: ToolName | string;
  arguments?: Record<string, JsonValue>;
  [key: string]: JsonValue | undefined;
};

export type SourceColumn = {
  field_name?: string;
  source_header?: string;
  business_label?: string;
  meaning?: string;
  source_trace_label?: string;
  [key: string]: JsonValue | undefined;
};

export type DatasetTrace = {
  id?: string;
  version?: string;
  path?: string;
  is_dummy?: boolean;
  database?: string;
  schema?: string;
  view?: string;
  import_batch_id?: string | number;
  [key: string]: JsonValue | undefined;
};

export type SourceTrace = {
  dataset?: DatasetTrace;
  tool?: string;
  tool_name?: string;
  group_by?: string;
  filters_applied?: Record<string, JsonValue>;
  time_range_applied?: Record<string, JsonValue>;
  source_columns?: SourceColumn[];
  [key: string]: JsonValue | SourceColumn[] | DatasetTrace | undefined;
};

export type ResultRow = Record<string, JsonValue | undefined>;

export type ToolExecutionResult = {
  tool?: string;
  understood_request?: string;
  group_by?: string;
  source_trace?: SourceTrace;
  filters_applied?: Record<string, JsonValue>;
  rows?: ResultRow[];
  groups?: ResultRow[];
  overall?: ResultRow;
  buckets?: Record<string, number>;
  pr_buckets?: Record<string, number>;
  po_confirmation_buckets?: Record<string, number>;
  [key: string]: JsonValue | SourceTrace | ResultRow[] | ResultRow | Record<string, number> | undefined;
};

export type ChatBIAskResponse = {
  intent_summary: IntentSummary;
  execution_summary: string;
  tool_call: ToolCall;
  result: ToolExecutionResult;
};

export type ToolExecuteRequest = {
  tool: ToolName;
  arguments: Record<string, JsonValue>;
};
