# SQL Server

SQL Server-specific database assets live here.

## Directories

- `migrations/`: schema migration scripts after schema approval.
- `views/`: stable SQL views for application and PowerBI consumption.
- `scripts/`: operational, inspection, or maintenance SQL scripts.
- `seeds/`: non-sensitive seed data.
- `dummy-data/`: dummy data for development and testing.

## Current Implemented Slice

The first ChatBI SQL Server dummy reporting slice uses:

- schema: `chatbi`;
- staging table: `chatbi.po_item_staging`;
- import metadata table: `chatbi.import_batch`;
- reporting view: `chatbi.vw_po_item_reporting`.

This slice is dummy-data only. It does not create Supplier Knowledge Base tables and does not load real company data.
