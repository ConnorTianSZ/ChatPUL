import type { ChatBIAskResponse, ToolExecuteRequest, ToolExecutionResult } from "../types/chatbi";

const DEFAULT_API_BASE_URL = "/api";

function apiBaseUrl(): string {
  const configured = import.meta.env.VITE_API_BASE_URL?.trim();
  return configured && configured.length > 0 ? configured.replace(/\/$/, "") : DEFAULT_API_BASE_URL;
}

function endpoint(path: string): string {
  return `${apiBaseUrl()}${path.startsWith("/") ? path : `/${path}`}`;
}

export class ChatBIHttpError extends Error {
  readonly status: number;
  readonly detail: unknown;

  constructor(status: number, detail: unknown) {
    super(formatErrorDetail(detail));
    this.name = "ChatBIHttpError";
    this.status = status;
    this.detail = detail;
  }
}

export async function askChatBI(question: string): Promise<ChatBIAskResponse> {
  const response = await fetch(endpoint("/chatbi/ask"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  return parseJsonResponse<ChatBIAskResponse>(response);
}

export async function executeChatBITool(request: ToolExecuteRequest): Promise<ToolExecutionResult> {
  const response = await fetch(endpoint("/chatbi/tools/execute"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  return parseJsonResponse<ToolExecutionResult>(response);
}

async function parseJsonResponse<T>(response: Response): Promise<T> {
  const payload = await readJson(response);
  if (!response.ok) {
    throw new ChatBIHttpError(response.status, normalizeErrorDetail(payload));
  }
  return payload as T;
}

async function readJson(response: Response): Promise<unknown> {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

function normalizeErrorDetail(payload: unknown): unknown {
  if (isRecord(payload) && "detail" in payload) {
    return payload.detail;
  }
  return payload;
}

export function formatErrorDetail(detail: unknown): string {
  if (typeof detail === "string") {
    return detail;
  }
  if (isRecord(detail)) {
    if (typeof detail.unsupported_reason === "string") {
      return detail.unsupported_reason;
    }
    if (Array.isArray(detail)) {
      return detail.map((item) => formatErrorDetail(item)).join("; ");
    }
  }
  if (Array.isArray(detail)) {
    return detail.map((item) => formatErrorDetail(item)).join("; ");
  }
  return "ChatBI request failed.";
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}
