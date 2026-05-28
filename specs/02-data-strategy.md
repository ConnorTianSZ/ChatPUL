# Data Strategy

## Direction

The product should be database-backed. SQL Server is the initial target because the company test environment has Microsoft SQL Server 2022 Express and SSMS 20.x installed.

For ChatBI, the planned source path is SAP export data converted into database tables. The database does not exist yet, so initial schema work should be driven by approved ChatBI tools, field dictionary needs, and existing PowerBI/SAP export structure.

## Relationship With PowerBI

Existing PowerBI work should not be discarded.

The strategy has two phases:

1. Learn from existing PowerBI data sources to understand available fields, relationships, definitions, and report logic.
2. Move toward a maintained database as the durable data source, while keeping database outputs usable by PowerBI.

## Database as Durable Source

The long-term direction is that the database stores maintained procurement and supplier data. PowerBI can then consume database tables or views instead of depending on scattered original sources.

Supplier KB data must distinguish procurement-facing supplier accounts from represented manufacturers:

- A supplier account is the internal supplier number or procurement-facing supplier record.
- A manufacturer is the original manufacturer, brand owner, or capability owner.
- A supplier-account-to-manufacturer representation links one supplier account to one represented manufacturer.
- Authorization certificates belong to the supplier-account-to-manufacturer representation, not only to the supplier account.
- Manufacturer-specific material coverage, product strengths, and application scenarios should not be collapsed into the supplier account's own capability fields unless a maintainer explicitly confirms that the supplier itself owns that capability.

Supplier KB may also store supplier spend-derived evidence, starting with a proposed 2025 dataset:

- supplier-level annual order value for 2025;
- selected material descriptions covering the first 80% of each supplier's 2025 order value;
- source-provided or human-reviewed manufacturer mapping when available;
- AI-assisted Chinese translation drafts for English material descriptions, when allowed by data safety rules.

This data is commercial procurement evidence. It must remain separate from confirmed supplier capability fields so that historical spend does not become an unreviewed capability claim.
It also must remain separate from authorization evidence so that purchase history does not become an unreviewed claim that the supplier is currently authorized for a manufacturer.

Existing PowerBI sources may help identify the available fields and definitions for the 2025 detail source. The database should preserve a future path where validated database tables or views can serve PowerBI, but early Supplier KB imports should not discard source traceability.

## SQL Views

`database/sqlserver/views/` is reserved for views that expose stable, analysis-friendly shapes for the app and PowerBI.

Potential view categories:

- ChatBI reporting views.
- Supplier summary views.
- Supplier-manufacturer representation views.
- Authorization certificate status views.
- Supplier spend-derived evidence views with sensitive commercial fields excluded by default.
- PowerBI compatibility views.
- Data quality inspection views.

ChatBI tools should prefer stable tables, views, stored procedures, or backend-owned query logic. The LLM must not write SQL directly.

## Field Dictionary

ChatBI should expose only approved table headers and hard-coded field meanings to the LLM. Field meanings should be maintained in the system as durable metadata, not inferred from raw database rows.

The field dictionary should connect business language to database structure after the schema exists.

## Dummy Data Requirement

Development uses dummy data only. Dummy data must preserve useful structure but must not copy real supplier names, prices, project details, internal report values, or confidential identifiers.

For ChatBI flow testing, dummy data may include synthetic supplier names, project numbers, purchase order numbers, and prices. These values must be clearly artificial.

For Supplier KB representation testing, dummy data may include synthetic supplier numbers, synthetic manufacturer names, fake authorization certificate numbers, artificial validity dates, and artificial authorization scopes. Dummy values must not copy real supplier names, real manufacturer authorization documents, real certificate numbers, or real commercial terms.

For Supplier KB spend-derived evidence testing, dummy data may include synthetic 2025 supplier totals, material descriptions, source-provided manufacturer labels, Pareto ranks, cumulative order-value shares, and AI-translation draft statuses. Dummy values must be clearly artificial and must not copy real 2025 supplier spend, supplier names, manufacturer names, material descriptions, material numbers, or pricing details.

## Current Boundary

No schema is approved yet. Schema design begins after the first ChatBI and Supplier Knowledge Base domain details are specified.

## Open Data Questions

- Which PowerBI reports or datasets should be mapped first?
- Which data fields are already stable and trusted?
- Which fields are sensitive or permission-restricted?
- Which records should be owned by procurement versus imported from other systems?
- Which source should be authoritative for supplier-account-to-manufacturer authorization validity?
