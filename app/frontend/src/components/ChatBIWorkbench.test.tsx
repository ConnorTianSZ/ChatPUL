import { fireEvent, render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import type { ReactElement } from "react";
import { describe, expect, it } from "vitest";

import { ChatBIHttpError } from "../api/chatbiClient";
import { ChatBIWorkbench } from "./ChatBIWorkbench";
import type { ChatBIAskResponse } from "../types/chatbi";

const successfulResponse: ChatBIAskResponse = {
  intent_summary: { provider: "mock", model: "mock", summary: "Auto PO ratio by manufacturer." },
  execution_summary: "Executed auto_po_ratio_summary grouped by manufacturer against dummy PO-item data.",
  tool_call: { tool: "auto_po_ratio_summary", arguments: { group_by: "manufacturer" } },
  result: {
    tool: "auto_po_ratio_summary",
    understood_request: "Executed auto_po_ratio_summary grouped by manufacturer against dummy PO-item data.",
    group_by: "manufacturer",
    source_trace: {
      dataset: { id: "dummy_po_items", version: "seed-20260528-rowcount-300", is_dummy: true },
      tool: "auto_po_ratio_summary",
      group_by: "manufacturer",
      filters_applied: { include_blank_manufacturer: true, wbs_scope: "all" },
      time_range_applied: { date_field: "doc_date" },
      source_columns: [
        {
          field_name: "auto_po_ratio",
          source_header: "PO created by",
          business_label: "Auto PO ratio",
          meaning: "UC4-created PO item count divided by all filtered PO item rows.",
          source_trace_label: "UC4CPIC count over all filtered PO item rows",
        },
      ],
    },
    groups: [{ group_key: "DummyMfr-X", uc4_count: 33, total: 84, ratio: 0.392857 }],
  },
};

describe("ChatBIWorkbench", () => {
  it("submits a dummy question and shows summaries, results, and source trace", async () => {
    renderWorkbench(<ChatBIWorkbench askClient={async () => successfulResponse} />);

    fireEvent.change(screen.getByLabelText("ChatBI question"), {
      target: { value: "show auto PO ratio by manufacturer" },
    });
    fireEvent.click(screen.getByRole("button", { name: /run question/i }));

    expect(await screen.findByText(/Executed auto_po_ratio_summary/)).toBeInTheDocument();
    expect(screen.getByText("DummyMfr-X")).toBeInTheDocument();
    expect(screen.getByText("dummy_po_items / seed-20260528-rowcount-300")).toBeInTheDocument();
    expect(screen.getByText("Auto PO ratio")).toBeInTheDocument();
  });

  it("shows a structured unsupported metric error instead of a fabricated result", async () => {
    renderWorkbench(
      <ChatBIWorkbench
        askClient={async () => {
          throw new ChatBIHttpError(422, { unsupported_reason: "price trend is outside approved ChatBI scope" });
        }}
      />,
    );

    fireEvent.change(screen.getByLabelText("ChatBI question"), {
      target: { value: "show price trend" },
    });
    fireEvent.click(screen.getByRole("button", { name: /run question/i }));

    expect(await screen.findByText(/price trend is outside approved ChatBI scope/i)).toBeInTheDocument();
    expect(screen.queryByText("DummyMfr-X")).not.toBeInTheDocument();
  });
});

function renderWorkbench(node: ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: {
      mutations: { retry: false },
      queries: { retry: false },
    },
  });

  return render(<QueryClientProvider client={queryClient}>{node}</QueryClientProvider>);
}
