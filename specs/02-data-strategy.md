# Data Strategy

## Direction

The product should be database-backed. SQL Server is the initial target because the company test environment has Microsoft SQL Server 2022 Express and SSMS 20.x installed.

For ChatBI, the planned source path is SAP export data converted into database tables. The database does not exist yet, so initial schema work should be driven by approved ChatBI tools, field dictionary needs, and existing PowerBI/SAP export structure.

ChatBI and Supplier Knowledge Base data must use separate database boundaries. The shared product entry point may orchestrate both capabilities, but the databases should not share mutable business tables.

## Relationship With PowerBI

Existing PowerBI work should not be discarded.

The strategy has two phases:

1. Learn from existing PowerBI data sources to understand available fields, relationships, definitions, and report logic.
2. Move toward a maintained database as the durable data source, while keeping database outputs usable by PowerBI.

For the ChatBI MVP, existing PowerBI data-source logic may inform the PO-item fact model, field dictionary, reporting dimensions, lead-time calculations, and auto PO ratio definitions. This preserves a migration path where current PowerBI logic is documented first and later rebuilt in SQL Server-backed tables, views, or trusted backend query logic.

## ChatBI MVP Data Flow

The MVP should preserve the existing PowerBI-facing workflow as much as possible while introducing SQL Server as the durable ChatBI source.

The approved transitional flow is:

1. SAP export files are produced through the existing approved business process.
2. A future SAP-export processing script converts those exports into a canonical ChatBI Excel workbook whose shape stays close to the current PowerBI data source.
3. A SQL import script loads the canonical ChatBI Excel workbook into SQL Server staging tables.
4. SQL views, stored procedures, or backend-owned query logic expose the stable reporting layer used by ChatBI.
5. Existing or future PowerBI reports may continue to consume the canonical Excel workbook during transition, or later consume approved SQL views.

The SAP-export processing script is a future work item. For now, specs should reserve this step and define the target shape, but no SAP processing code should be written until a later approved implementation plan exists.

The canonical ChatBI Excel workbook is a compatibility layer, not the final source of truth. It exists to preserve current PowerBI review habits, support manual validation, and provide a stable handoff into SQL Server.

The SQL reporting layer is the ChatBI query source. ChatBI should not read directly from ad hoc SAP exports or depend on Excel formula recalculation at answer time.

## ChatBI and Supplier KB Database Isolation

The product has one unified user entry point, but ChatBI and Supplier Knowledge Base should be treated as separate data products:

- ChatBI database: procurement reporting and analytics data derived from approved SAP exports, PowerBI source logic, and future SQL Server reporting models.
- Supplier Knowledge Base database: maintained supplier profiles, represented manufacturer relationships, authorization evidence, capability notes, and approved supplier knowledge records.

The two databases must not directly share tables for suppliers, manufacturers, materials, authorizations, or spend evidence in the MVP.

If both capabilities need to refer to similar business concepts, each database owns its own representation:

- ChatBI supplier and manufacturer dimensions are analytical dimensions used for reporting.
- Supplier KB supplier and manufacturer records are knowledge objects with ownership, verification, and retrieval rules.

Any future cross-capability bridge must be specified before implementation. A bridge spec must define the mapping owner, allowed fields, refresh direction, conflict handling, data sensitivity, and whether the link is read-only.

## Database as Durable Source

The long-term direction is that each capability has a durable database source for its own data boundary. PowerBI can consume approved ChatBI database tables or views for reporting. Supplier KB data should remain in its separate knowledge database unless a later approved spec creates controlled read-only outputs.

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

ChatBI tools should prefer stable ChatBI tables, views, stored procedures, or backend-owned query logic. The LLM must not write SQL directly.

Supplier KB views, if added later, must stay inside the Supplier KB database boundary and must not be treated as ChatBI reporting views unless a later approved bridge spec says so.

## Formula Column Strategy

Existing PowerBI or Excel formula columns should be treated as business-rule documentation and compatibility outputs.

The preferred MVP handling is:

- Preserve raw imported source fields in SQL staging tables.
- Generate canonical ChatBI Excel with formula-column values already calculated by the future processing script, not left for Excel to recalculate.
- Import those calculated compatibility values into SQL staging for reconciliation and troubleshooting.
- Reimplement official ChatBI measures and classifications in SQL views, stored procedures, or backend-owned query logic before they are exposed to ChatBI.
- Track the formula source, business meaning, SQL/backend implementation, and validation status in the field dictionary or a later formula registry.

For MVP workday calculations, `NETWORKDAYS` semantics are sufficient: Monday through Friday working days, without China public holiday or company calendar adjustment. A company calendar table is deferred until a later spec requires it.

Formula columns should be classified before schema design:

- Row identity and row-level derived fields, such as `Combine` and reporting month, may be generated in SQL views or backend import logic.
- Classification fields, such as PR and OC lead-time buckets, should be generated from tested SQL/backend rules.
- Aggregate measures, such as auto PO ratio, should be calculated dynamically from filtered PO item rows, not stored as fixed Excel columns.

## Field Dictionary

ChatBI should expose only approved table headers and hard-coded field meanings to the LLM. Field meanings should be maintained in the system as durable metadata, not inferred from raw database rows.

The field dictionary should connect business language to database structure after the schema exists.

## ChatBI MVP Data Preparation Reference

The current ChatBI data-preparation reference is a locally saved, ignored workbook derived from existing PowerBI/SAP-source work:

- path: `data/raw/email-attachments/2026-05-28-newchatbi-data-prep/chatbi data sample.xlsx`;
- sheet: `PO List`;
- role: field and formula interpretation reference, not a committed fixture.

The workbook indicates the first ChatBI fact should be a PO item row and documents candidate fields for supplier, manufacturer, buyer, WBS, material, lead time, order confirmation, plant, and MRP analysis.

Known caveats from the source:

- `Manufactur` may be blank because dummy material numbers or incomplete source records do not carry manufacturer values.
- `WBS element` may be blank because some PO rows are not project-related.
- `PO created by = UC4CPIC` is the current source rule for identifying automatically created PO items.
- Existing PowerBI formulas for lead time and classification should be transcribed into tested SQL/backend logic before production use.

The source workbook must not be committed. Any development fixture derived from it must be synthetic and placed under `data/dummy/` or `database/sqlserver/dummy-data/`.

## Dummy Data Requirement

Development uses dummy data only. Dummy data must preserve useful structure but must not copy real supplier names, prices, project details, internal report values, or confidential identifiers.

For ChatBI flow testing, dummy data may include synthetic supplier names, project numbers, purchase order numbers, and prices. These values must be clearly artificial.

The ChatBI dummy PO-item fixture is a test fixture, not a business source. Its current files are:

- generator: `tests/fixtures/generate_dummy_po_items.py`;
- dataset: `data/dummy/dummy_po_items.csv`;
- expected results: `data/dummy/dummy_po_items_expected.json`;
- rationale: `data/dummy/dummy_po_items_README.md`.

The dummy fixture is intentionally different from real data:

- Source: dummy rows are generated by deterministic local Python code; real rows come from approved SAP exports, existing PowerBI source logic, and later SQL Server imports in the company environment.
- Purpose: dummy data is for automated tests and eval reproducibility; real data is for business analysis after approved ingestion.
- Content: dummy data uses fake suppliers, fake manufacturers, fake material numbers, fake WBS values, fake PO numbers, and synthetic prices; real data may include sensitive supplier, price, purchasing, project, and internal report details.
- Shape: dummy data matches the approved PO-item column shape and deliberately over-represents edge cases; real data may have different distributions, larger volume, source-system quirks, and refresh timing constraints.
- Storage: dummy data belongs in `data/dummy/` or `database/sqlserver/dummy-data/`; real data must not be committed and must remain in approved local or company-controlled storage.
- Expected results: dummy data has a checked-in expected JSON file for independent validation; real data must not have checked-in answer files containing business results.

For Supplier KB representation testing, dummy data may include synthetic supplier numbers, synthetic manufacturer names, fake authorization certificate numbers, artificial validity dates, and artificial authorization scopes. Dummy values must not copy real supplier names, real manufacturer authorization documents, real certificate numbers, or real commercial terms.

For Supplier KB spend-derived evidence testing, dummy data may include synthetic 2025 supplier totals, material descriptions, source-provided manufacturer labels, Pareto ranks, cumulative order-value shares, and AI-translation draft statuses. Dummy values must be clearly artificial and must not copy real 2025 supplier spend, supplier names, manufacturer names, material descriptions, material numbers, or pricing details.

## Current Boundary

No physical schema is approved yet.

The logical database boundary is approved: ChatBI and Supplier Knowledge Base must be separate databases or equivalent isolated schemas with no shared mutable business tables. Schema design begins after the first ChatBI and Supplier Knowledge Base domain details, dummy data, and evaluation cases are specified.

## Open Data Questions

- Which PowerBI reports or datasets should be mapped first?
- Which data fields are already stable and trusted?
- Which fields are sensitive or permission-restricted?
- Which records should be owned by procurement versus imported from other systems?
- Which source should be authoritative for supplier-account-to-manufacturer authorization validity?
