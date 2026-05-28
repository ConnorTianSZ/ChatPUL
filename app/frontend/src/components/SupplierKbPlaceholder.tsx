import { Alert, Typography } from "antd";
import { Lock } from "lucide-react";

const { Text, Title } = Typography;

export function SupplierKbPlaceholder() {
  return (
    <section className="supplier-placeholder" aria-labelledby="supplier-kb-title">
      <div>
        <Title id="supplier-kb-title" level={2}>
          Supplier Knowledge Base
        </Title>
        <Text type="secondary">Unified entry point placeholder. Business workflows are not implemented in this milestone.</Text>
      </div>
      <Alert
        type="info"
        showIcon
        icon={<Lock size={18} aria-hidden="true" />}
        message="Coming soon"
        description="Upload, search, cleaning, normalization, and contact-data display are intentionally disabled for this slice."
      />
    </section>
  );
}
