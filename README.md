# ChatPUL

Spec-first repository for a procurement-oriented internal tool that combines ChatBI and a Supplier Knowledge Base under one entry point.

## Current Status

This repository has moved from SDD bootstrap into the first backend implementation slice.

Implemented so far:

- ChatBI backend tool execution against synthetic PO-item dummy data.
- Strict structured validation for the four approved ChatBI MVP tools.
- Minimal ChatBI field dictionary metadata for labels, future tooltips, and source traceability.
- SQL Server dummy reporting assets for the approved ChatBI PO-item shape.
- Optional DeepSeek V4 Flash intent parsing for dummy-data local testing.
- Pytest coverage for fixture generation, tool validation, calculations, API behavior, and source trace structure.

No frontend UI, Supplier Knowledge Base implementation, production SQL import path, or real company data handling has been implemented yet.

## Confirmed Technical Stack

The approved backend stack is Python + FastAPI + pytest.

- FastAPI is the default framework for future backend APIs.
- pytest is the default test runner for backend code, fixture generators, and evaluation harnesses.
- SQL Server remains the target database platform for company-environment validation.

The first approved backend endpoints are `POST /api/chatbi/tools/execute` and `POST /api/chatbi/ask`, scoped by `specs/09-chatbi-backend-tool-slice.md` and `specs/10-chatbi-sqlserver-and-llm-milestone.md`.

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
