# ChatPUL

Spec-first repository for a procurement-oriented internal tool that combines ChatBI and a Supplier Knowledge Base under one entry point.

## Current Status

This repository is in the SDD bootstrap phase. It contains specs, project rules, and directory placeholders only. No application code or database schema has been committed yet.

## Product Direction

The product is intended for procurement colleagues, initially leaders and team leads, in Bosch China Suzhou's Intelligent Manufacturing Solutions business. The business works with non-standard equipment, so the system must respect practical purchasing workflows, supplier knowledge reuse, and data governance.

## Initial Structure

```text
app/
  backend/
  frontend/
database/
  sqlserver/
    dummy-data/
    migrations/
    scripts/
    seeds/
    views/
data/
  dummy/
  samples/
docs/
  decisions/
  diagrams/
specs/
tests/
```

## Development Principle

Development happens on a personal computer with dummy data. Validation happens later in the company environment with Microsoft SQL Server 2022 Express and SSMS 20.x.

Real company data must not be committed or uploaded from the development environment.
