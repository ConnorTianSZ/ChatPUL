import { describe, expect, it } from "vitest";

import { buildResultTables, describeSourceTrace } from "./resultModel";
import type { ToolExecutionResult } from "../types/chatbi";

const autoPoResult: ToolExecutionResult = {
  tool: "auto_po_ratio_summary",
  understood_request: "Executed auto_po_ratio_summary grouped by manufacturer against dummy PO-item data.",
  group_by: "manufacturer",
  source_trace: {
    dataset: {
      id: "dummy_po_items",
      version: "seed-20260528-rowcount-300",
      is_dummy: true,
      path: "data/dummy/dummy_po_items.csv",
    },
    tool: "auto_po_ratio_summary",
    group_by: "manufacturer",
    filters_applied: { include_blank_manufacturer: true, wbs_scope: "all" },
    time_range_applied: { date_field: "doc_date" },
    source_columns: [
      {
        field_name: "manufacturer_name",
        source_header: "Manufactur",
        business_label: "Manufacturer",
        meaning: "Source manufacturer value used as a ChatBI analytical dimension.",
        source_trace_label: "Manufactur source field",
      },
      {
        field_name: "auto_po_ratio",
        source_header: "PO created by",
        business_label: "Auto PO ratio",
        meaning: "UC4-created PO item count divided by all filtered PO item rows.",
        source_trace_label: "UC4CPIC count over all filtered PO item rows",
      },
    ],
  },
  groups: [
    { group_key: "DummyMfr-X", uc4_count: 33, total: 84, ratio: 0.392857 },
    { group_key: "<BLANK>", uc4_count: 18, total: 50, ratio: 0.36, is_blank_manufacturer: true },
  ],
};

describe("resultModel", () => {
  it("turns auto PO groups into a renderable table without assuming nested result.result", () => {
    const tables = buildResultTables(autoPoResult);

    expect(tables).toHaveLength(1);
    expect(tables[0]).toMatchObject({
      title: "Groups",
      rows: [
        { group_key: "DummyMfr-X", uc4_count: 33, total: 84, ratio: 0.392857 },
        { group_key: "<BLANK>", uc4_count: 18, total: 50, ratio: 0.36 },
      ],
    });
  });

  it("summarizes source trace from backend metadata only", () => {
    const trace = describeSourceTrace(autoPoResult.source_trace);

    expect(trace.datasetLabel).toBe("dummy_po_items / seed-20260528-rowcount-300");
    expect(trace.dummyLabel).toBe("Dummy fixture");
    expect(trace.sourceColumns).toEqual([
      expect.objectContaining({
        fieldName: "manufacturer_name",
        label: "Manufacturer",
        meaning: "Source manufacturer value used as a ChatBI analytical dimension.",
      }),
      expect.objectContaining({
        fieldName: "auto_po_ratio",
        label: "Auto PO ratio",
        meaning: "UC4-created PO item count divided by all filtered PO item rows.",
      }),
    ]);
  });
});
