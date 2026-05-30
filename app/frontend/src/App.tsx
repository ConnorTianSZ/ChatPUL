import { useState } from "react";
import { Layout, Menu, Space, Tag, Typography } from "antd";
import type { MenuProps } from "antd";
import { BookOpen, Database, MessageSquareText } from "lucide-react";

import { ChatBIWorkbench } from "./components/ChatBIWorkbench";
import { SupplierKbPlaceholder } from "./components/SupplierKbPlaceholder";

const { Content, Header, Sider } = Layout;
const { Text } = Typography;

type PageKey = "chatbi" | "supplier-kb";

const menuItems: MenuProps["items"] = [
  { key: "chatbi", icon: <MessageSquareText size={17} aria-hidden="true" />, label: "ChatBI" },
  { key: "supplier-kb", icon: <BookOpen size={17} aria-hidden="true" />, label: "Supplier KB" },
];

export function App() {
  const [page, setPage] = useState<PageKey>("chatbi");

  return (
    <Layout className="app-shell">
      <Sider className="app-sider" width={232} breakpoint="lg" collapsedWidth={0}>
        <div className="brand-lockup">
          <div className="brand-mark">CP</div>
          <div>
            <Text className="brand-name">ChatPUL</Text>
            <Text className="brand-subtitle">Procurement workbench</Text>
          </div>
        </div>
        <Menu
          mode="inline"
          selectedKeys={[page]}
          items={menuItems}
          onClick={(event) => setPage(event.key as PageKey)}
          className="app-menu"
        />
      </Sider>
      <Layout>
        <Header className="app-header">
          <Space size={10} wrap>
            <Tag icon={<Database size={14} aria-hidden="true" />} color="green">
              dummy source
            </Tag>
            <Tag color="blue">FastAPI /api</Tag>
            <Tag color="default">no real data</Tag>
          </Space>
        </Header>
        <Content className="app-content">{page === "chatbi" ? <ChatBIWorkbench /> : <SupplierKbPlaceholder />}</Content>
      </Layout>
    </Layout>
  );
}
