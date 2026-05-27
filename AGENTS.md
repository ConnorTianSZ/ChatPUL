# Agent Operating Guide

This repository is developed with SDD: spec-driven development first, implementation second.

## Project Context

- The product is for procurement colleagues, initially leaders and team leads.
- The business context is Bosch China, Suzhou, Intelligent Manufacturing Solutions, non-standard equipment.
- The product will provide one unified entry point for two capabilities:
  - ChatBI
  - Supplier Knowledge Base
- Microsoft SQL Server 2022 Express and SQL Server Management Studio 20.x are available in the company test environment.
- Existing PowerBI assets should not be discarded. The database strategy must preserve a migration path where existing PowerBI data sources can inform the database model, and future database data can serve PowerBI.

## Required Workflow

1. Capture user ideas in `specs/` before implementation.
2. Update `AGENTS.md` when durable agent behavior, safety rules, or workflow rules change.
3. Do not write application code before the relevant spec is explicit enough to test.
4. Keep implementation plans small and reviewable.
5. Prefer dummy data on the development machine.
6. Treat real company data, supplier data, pricing data, purchasing data, and internal reports as sensitive by default.
7. For Supplier Knowledge Base MVP work, keep direct profile upload separate from data cleaning. Do not add automatic deduplication, canonical-term generation, synonym generation, related-term generation, or AI normalization unless a later approved spec explicitly changes that boundary.

## Data Safety Rules

- Never upload real company data to cloud services from the development machine.
- Never commit real company data to this repo.
- Use `data/dummy/` and `database/sqlserver/dummy-data/` for development fixtures.
- Use sanitized samples only when field structure is needed.
- If a requirement depends on real data behavior, write the requirement in specs and test with representative dummy data.
- Supplier contact details should not be displayed by default in Supplier Knowledge Base MVP work. Prefer responsible buyer as the internal contact point unless a later approved spec defines contact-data ownership, verification, and access control.

## Environment Rules

- Personal computer: development with dummy data only.
- Company computer: validation against Microsoft SQL Server 2022 Express and approved local data sources.
- Database scripts should target SQL Server unless a later spec explicitly changes this.
- Keep environment-specific values out of source control. Document required variables in `.env.example`.

## Repository Structure

- `specs/`: Product, domain, data, UX, and evaluation specs.
- `app/backend/`: Future backend application code.
- `app/frontend/`: Future frontend application code.
- `database/sqlserver/migrations/`: Future schema migration scripts.
- `database/sqlserver/views/`: Future SQL views for app and PowerBI consumption.
- `database/sqlserver/scripts/`: Future operational or inspection SQL scripts.
- `database/sqlserver/seeds/`: Future non-sensitive seed data.
- `database/sqlserver/dummy-data/`: SQL Server dummy data for local development.
- `data/dummy/`: Non-database dummy datasets.
- `data/samples/`: Sanitized structural samples only.
- `tests/`: Future automated tests and evaluation harnesses.
- `docs/decisions/`: Architecture decision records.
- `docs/diagrams/`: Text or image diagrams produced from approved specs.

## Spec Writing Rules

- Prefer concrete decisions over vague notes.
- If a detail is not known yet, state the current decision boundary instead of inventing behavior.
- Record open questions as questions, not as hidden assumptions.
- Keep ChatBI, Supplier Knowledge Base, shared UX, data strategy, and eval cases in separate specs unless a change explicitly crosses boundaries.

## Current Implementation Boundary

This repo currently contains documentation and placeholders only. Application code, database schema, and SQL scripts should be added only after the corresponding spec is approved.
