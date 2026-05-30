import { afterEach, describe, expect, it, vi } from "vitest";

import { askChatBI } from "./chatbiClient";

describe("askChatBI", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("posts the natural-language question to the backend ask endpoint", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        intent_summary: { provider: "mock", model: "mock", summary: "Auto PO by manufacturer." },
        execution_summary: "Executed auto_po_ratio_summary grouped by manufacturer against dummy PO-item data.",
        tool_call: { tool: "auto_po_ratio_summary", arguments: { group_by: "manufacturer" } },
        result: { tool: "auto_po_ratio_summary", groups: [] },
      }),
    });
    vi.stubGlobal("fetch", fetchMock);

    const response = await askChatBI("show auto PO ratio by manufacturer");

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/chatbi/ask",
      expect.objectContaining({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: "show auto PO ratio by manufacturer" }),
      }),
    );
    expect(response.execution_summary).toContain("auto_po_ratio_summary");
  });

  it("throws a structured http error when the backend rejects the question", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 422,
        json: async () => ({ detail: { unsupported_reason: "price trend is outside approved ChatBI scope" } }),
      }),
    );

    await expect(askChatBI("show price trend")).rejects.toMatchObject({
      status: 422,
      detail: { unsupported_reason: "price trend is outside approved ChatBI scope" },
    });
  });
});
