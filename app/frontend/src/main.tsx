import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ConfigProvider } from "antd";
import "antd/dist/reset.css";

import { App } from "./App";
import "./styles.css";

const queryClient = new QueryClient({
  defaultOptions: {
    mutations: {
      retry: false,
    },
    queries: {
      retry: false,
      staleTime: 30_000,
    },
  },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: "#1f6f78",
          colorInfo: "#1f6f78",
          colorSuccess: "#3f7d4f",
          colorWarning: "#b77724",
          borderRadius: 6,
          fontFamily: "Aptos, Segoe UI, sans-serif",
        },
        components: {
          Button: { borderRadius: 6 },
          Card: { borderRadiusLG: 6 },
          Layout: { bodyBg: "#f4f6f7", headerBg: "#ffffff", siderBg: "#172326" },
        },
      }}
    >
      <QueryClientProvider client={queryClient}>
        <App />
      </QueryClientProvider>
    </ConfigProvider>
  </React.StrictMode>,
);
