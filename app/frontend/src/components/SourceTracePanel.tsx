import { Descriptions, Empty, Space, Tag, Tooltip, Typography } from "antd";
import { Info } from "lucide-react";

import { describeSourceTrace } from "../lib/resultModel";
import type { SourceTrace } from "../types/chatbi";

const { Text } = Typography;

export function SourceTracePanel({ trace }: { trace: SourceTrace | undefined }) {
  if (!trace) {
    return <Empty description="No source trace returned" />;
  }

  const summary = describeSourceTrace(trace);

  return (
    <section className="source-trace" aria-label="Source trace">
      <div className="section-row">
        <Text className="section-kicker">Source trace</Text>
        <Tag color={summary.dummyLabel === "Dummy fixture" ? "green" : "orange"}>{summary.dummyLabel}</Tag>
      </div>
      <Descriptions size="small" bordered column={{ xs: 1, sm: 1, md: 2 }} items={[
        { key: "dataset", label: "Dataset", children: summary.datasetLabel },
        { key: "tool", label: "Tool", children: summary.toolLabel },
        { key: "group", label: "Grouping", children: summary.groupByLabel },
        { key: "filters", label: "Filters", children: <code>{JSON.stringify(summary.filters)}</code> },
        { key: "time", label: "Time range", children: <code>{JSON.stringify(summary.timeRange)}</code> },
      ]} />

      <div className="source-columns">
        <Text strong>Source columns</Text>
        <Space size={8} wrap>
          {summary.sourceColumns.map((column) => (
            <Tooltip
              key={`${column.fieldName}-${column.sourceHeader}`}
              title={
                <span>
                  {column.meaning}
                  {column.traceLabel ? ` ${column.traceLabel}.` : ""}
                </span>
              }
            >
              <Tag className="source-column-tag" icon={<Info size={13} aria-hidden="true" />}>
                {column.label}
              </Tag>
            </Tooltip>
          ))}
        </Space>
      </div>
    </section>
  );
}
