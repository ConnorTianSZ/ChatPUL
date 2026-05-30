IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = N'chatbi')
BEGIN
    EXEC(N'CREATE SCHEMA chatbi');
END;
GO

IF OBJECT_ID(N'chatbi.vw_po_item_reporting', N'V') IS NOT NULL
BEGIN
    DROP VIEW chatbi.vw_po_item_reporting;
END;
GO

IF OBJECT_ID(N'chatbi.po_item_staging', N'U') IS NOT NULL
BEGIN
    DROP TABLE chatbi.po_item_staging;
END;
GO

IF OBJECT_ID(N'chatbi.import_batch', N'U') IS NOT NULL
BEGIN
    DROP TABLE chatbi.import_batch;
END;
GO

CREATE TABLE chatbi.import_batch (
    import_batch_id int IDENTITY(1,1) NOT NULL CONSTRAINT pk_chatbi_import_batch PRIMARY KEY,
    source_dataset_id nvarchar(100) NOT NULL,
    source_dataset_version nvarchar(100) NOT NULL,
    source_file_name nvarchar(260) NOT NULL,
    loaded_at datetime2(0) NOT NULL CONSTRAINT df_chatbi_import_batch_loaded_at DEFAULT SYSUTCDATETIME(),
    row_count int NOT NULL
);
GO

CREATE TABLE chatbi.po_item_staging (
    po_item_staging_id int IDENTITY(1,1) NOT NULL CONSTRAINT pk_chatbi_po_item_staging PRIMARY KEY,
    import_batch_id int NOT NULL,
    wbs_element nvarchar(100) NULL,
    buyer_key nvarchar(20) NOT NULL,
    supplier_code nvarchar(50) NOT NULL,
    supplier_name nvarchar(200) NOT NULL,
    po_document_number nvarchar(50) NOT NULL,
    po_item_number nvarchar(20) NOT NULL,
    material_number nvarchar(100) NULL,
    material_short_text nvarchar(500) NULL,
    manufacturer_part_number nvarchar(200) NULL,
    manufacturer_name nvarchar(200) NULL,
    quantity decimal(18, 4) NULL,
    net_price decimal(18, 4) NULL,
    net_value_domestic_currency decimal(18, 4) NULL,
    currency nvarchar(10) NULL,
    doc_date date NOT NULL,
    pr_date date NULL,
    order_confirmation_date date NULL,
    goods_receipt_posting_date date NULL,
    statistical_delivery_date date NULL,
    po_created_by nvarchar(100) NULL,
    plant nvarchar(20) NULL,
    mrp_type nvarchar(20) NULL,
    CONSTRAINT fk_chatbi_po_item_staging_import_batch
        FOREIGN KEY (import_batch_id) REFERENCES chatbi.import_batch(import_batch_id)
);
GO

CREATE UNIQUE INDEX ux_chatbi_po_item_staging_batch_doc_item
ON chatbi.po_item_staging(import_batch_id, po_document_number, po_item_number);
GO

CREATE OR ALTER VIEW chatbi.vw_po_item_reporting AS
SELECT
    s.wbs_element,
    s.buyer_key,
    s.supplier_code,
    s.supplier_name,
    s.po_document_number,
    s.po_item_number,
    s.material_number,
    s.material_short_text,
    s.manufacturer_part_number,
    s.manufacturer_name,
    s.quantity,
    s.net_price,
    s.net_value_domestic_currency,
    s.currency,
    CONVERT(char(10), s.doc_date, 23) AS doc_date,
    CONVERT(char(10), s.pr_date, 23) AS pr_date,
    CONVERT(char(10), s.order_confirmation_date, 23) AS order_confirmation_date,
    CONVERT(char(10), s.goods_receipt_posting_date, 23) AS goods_receipt_posting_date,
    CONVERT(char(10), s.statistical_delivery_date, 23) AS statistical_delivery_date,
    s.po_created_by,
    s.plant,
    s.mrp_type,
    s.import_batch_id,
    b.source_dataset_id,
    b.source_dataset_version,
    b.loaded_at
FROM chatbi.po_item_staging AS s
INNER JOIN chatbi.import_batch AS b
    ON b.import_batch_id = s.import_batch_id;
GO
