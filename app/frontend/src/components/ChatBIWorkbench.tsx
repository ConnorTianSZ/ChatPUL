import { useMemo, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Alert, Button, Input, Space, Tag, Typography } from "antd";
import { Play, RotateCcw } from "lucide-react";

import { ChatBIHttpError, askChatBI, formatErrorDetail } from "../api/chatbiClient";
import type { ChatBIAskResponse } from "../types/chatbi";
import { ResultTables } from "./ResultTables";
import { SourceTracePanel } from "./SourceTracePanel";

const { Text, Title } = Typography;
const { TextArea } = Input;

const EXAMPLES = [
  "show auto PO ratio by manufacturer",
  "show supplier summary by buyer",
  "show pr lead time by manufacturer",
  "show price trend",
];

export type ChatBIWorkbenchProps = {
  askClient?: (question: string) => Promise<ChatBIAskResponse>;
};

export function ChatBIWorkbench({ askClient = askChatBI }: ChatBIWorkbenchProps) {
  const [question, setQuestion] = useState(EXAMPLES[0]);

  const mutation = useMutation({
    mutationFn: async (value: string) => askClient(value),
  });

  const errorMessage = useMemo(() => {
    if (!mutation.error) {
      return null;
    }
    if (mutation.error instanceof ChatBIHttpError) {
      return {
        status: mutation.error.status,
        message: formatErrorDetail(mutation.error.detail),
      };
    }
    return {
      status: undefined,
      message: mutation.error instanceof Error ? mutation.error.message : "ChatBI request failed.",
    };
  }, [mutation.error]);

  const submit = () => {
    const trimmed = question.trim();
    if (trimmed.length === 0) {
      return;
    }
    mutation.mutate(trimmed);
  };

  return (
    <section className="chatbi-workbench" aria-labelledby="chatbi-title">
      <div className="workbench-heading">
        <div>
          <Title id="chatbi-title" level={2}>
            ChatBI
          </Title>
          <Text type="secondary">Dummy PO-item analytics through the approved backend contract.</Text>
        </div>
        <Space size={8} wrap>
          <Tag color="blue">local workbench</Tag>
          <Tag color="green">dummy data only</Tag>
          <Tag color="default">LLM gated by backend</Tag>
        </Space>
      </div>

      <div className="question-panel">
        <label className="question-label" htmlFor="chatbi-question">
          ChatBI question
        </label>
        <TextArea
          id="chatbi-question"
          aria-label="ChatBI question"
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          rows={3}
          placeholder="Ask an approved dummy ChatBI question"
        />
        <div className="question-actions">
          <Space wrap>
            <Button type="primary" icon={<Play size={16} aria-hidden="true" />} loading={mutation.isPending} onClick={submit}>
              Run question
            </Button>
            <Button icon={<RotateCcw size={16} aria-hidden="true" />} onClick={() => mutation.reset()}>
              Clear result
            </Button>
          </Space>
          <Space size={6} wrap>
            {EXAMPLES.map((example) => (
              <Button key={example} size="small" type="text" onClick={() => setQuestion(example)}>
                {example}
              </Button>
            ))}
          </Space>
        </div>
      </div>

      {errorMessage ? (
        <Alert
          type={errorMessage.status === 503 ? "warning" : "error"}
          showIcon
          message={errorMessage.status === 503 ? "ChatBI intent parser disabled" : "ChatBI request rejected"}
          description={errorMessage.message}
        />
      ) : null}

      {mutation.data ? (
        <div className="result-stack">
          <section className="summary-strip" aria-label="Execution summaries">
            <div>
              <Text className="section-kicker">Intent summary</Text>
              <p>{mutation.data.intent_summary.summary ?? "Intent parser returned an approved tool call."}</p>
              <Text type="secondary">
                {mutation.data.intent_summary.provider ?? "provider unknown"} / {mutation.data.intent_summary.model ?? "model unknown"}
              </Text>
            </div>
            <div>
              <Text className="section-kicker">Execution summary</Text>
              <p>{mutation.data.execution_summary}</p>
              <Text type="secondary">{mutation.data.tool_call.tool ?? "tool unknown"}</Text>
            </div>
          </section>

          <ResultTables result={mutation.data.result} />
          <SourceTracePanel trace={mutation.data.result.source_trace} />
        </div>
      ) : null}
    </section>
  );
}
