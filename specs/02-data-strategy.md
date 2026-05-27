# Data Strategy

## Direction

The product should be database-backed. SQL Server is the initial target because the company test environment has Microsoft SQL Server 2022 Express and SSMS 20.x installed.

## Relationship With PowerBI

Existing PowerBI work should not be discarded.

The strategy has two phases:

1. Learn from existing PowerBI data sources to understand available fields, relationships, definitions, and report logic.
2. Move toward a maintained database as the durable data source, while keeping database outputs usable by PowerBI.

## Database as Durable Source

The long-term direction is that the database stores maintained procurement and supplier data. PowerBI can then consume database tables or views instead of depending on scattered original sources.

## SQL Views

`database/sqlserver/views/` is reserved for views that expose stable, analysis-friendly shapes for the app and PowerBI.

Potential view categories:

- ChatBI reporting views.
- Supplier summary views.
- PowerBI compatibility views.
- Data quality inspection views.

## Dummy Data Requirement

Development uses dummy data only. Dummy data must preserve useful structure but must not copy real supplier names, prices, project details, internal report values, or confidential identifiers.

## Current Boundary

No schema is approved yet. Schema design begins after the first ChatBI and Supplier Knowledge Base domain details are specified.

## Open Data Questions

- Which PowerBI reports or datasets should be mapped first?
- Which data fields are already stable and trusted?
- Which fields are sensitive or permission-restricted?
- Which records should be owned by procurement versus imported from other systems?
