import { Table, Typography } from "antd";
import type { ColumnsType } from "antd/es/table";

import { buildResultTables, formatCell } from "../lib/resultModel";
import type { JsonValue, ToolExecutionResult } from "../types/chatbi";

const { Text } = Typography;

export function ResultTables({ result }: { result: ToolExecutionResult | undefined }) {
  const tables = buildResultTables(result);

  if (tables.length === 0) {
    return null;
  }

  return (
    <section className="result-section" aria-label="ChatBI result">
      <Text className="section-kicker">Result</Text>
      <div className="table-stack">
        {tables.map((table) => (
          <div key={table.title} className="result-table-block">
            <Text strong>{table.title}</Text>
            <Table
              size="small"
              rowKey="__rowKey"
              columns={columnsForRows(table.rows)}
              dataSource={withRowKeys(table.title, table.rows)}
              pagination={table.rows.length > 10 ? { pageSize: 10, size: "small" } : false}
              scroll={{ x: "max-content" }}
            />
          </div>
        ))}
      </div>
    </section>
  );
}

function columnsForRows(rows: Record<string, JsonValue | undefined>[]): ColumnsType<Record<string, JsonValue | undefined>> {
  const keys = Array.from(new Set(rows.flatMap((row) => Object.keys(row))));
  return keys.map((key) => ({
    title: humanize(key),
    dataIndex: key,
    key,
    render: (value: JsonValue | undefined) => formatCell(value),
  }));
}

function withRowKeys(
  title: string,
  rows: Record<string, JsonValue | undefined>[],
): (Record<string, JsonValue | undefined> & { __rowKey: string })[] {
  return rows.map((row, index) => ({ ...row, __rowKey: `${title}-${index}` }));
}

function humanize(key: string): string {
  return key
    .replaceAll("_", " ")
    .replaceAll(".", " / ")
    .replace(/\b\w/g, (value) => value.toUpperCase());
}
