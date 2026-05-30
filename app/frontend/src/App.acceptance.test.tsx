import { act, fireEvent, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { App } from "./App";
import { renderWithClient } from "./test/renderWithClient";

describe("App acceptance", () => {
  it("opens on the ChatBI workbench with local dummy-source status", async () => {
    await renderApp();

    expect(screen.getByText("ChatPUL")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "ChatBI" })).toBeInTheDocument();
    expect(screen.getByLabelText("ChatBI question")).toHaveValue("show auto PO ratio by manufacturer");
    expect(screen.getByText("dummy source")).toBeInTheDocument();
    expect(screen.getByText("no real data")).toBeInTheDocument();
  });

  it("keeps Supplier KB visible but explicitly disabled", async () => {
    await renderApp();

    await act(async () => {
      fireEvent.click(screen.getByText("Supplier KB"));
    });

    expect(screen.getByRole("heading", { name: "Supplier Knowledge Base" })).toBeInTheDocument();
    expect(screen.getByText("Coming soon")).toBeInTheDocument();
    expect(screen.getByText(/Upload, search, cleaning, normalization/)).toBeInTheDocument();
  });
});

async function renderApp() {
  await act(async () => {
    renderWithClient(<App />);
    await Promise.resolve();
  });
}
