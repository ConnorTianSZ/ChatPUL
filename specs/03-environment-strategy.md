# Environment Strategy

## Development Environment

Development happens on a personal computer through Codex with dummy data only.

Rules:

- Do not use real company datasets.
- Do not upload company data to cloud tools.
- Do not store production credentials.
- Keep `.env` local and untracked.
- Keep `.env.example` limited to variable names and safe example values.

## Backend Development Stack

The approved backend stack is:

- Runtime language: Python.
- Web API framework: FastAPI.
- Test runner: pytest.

FastAPI is the default backend framework for future ChatBI and Supplier Knowledge Base API work. pytest is the default automated test runner for backend code, fixture generators, and evaluation harnesses.

Backend implementation remains gated by approved specs and small implementation plans. This stack decision does not approve application endpoints, database schemas, SQL views, or production data ingestion by itself.

Recommended future supporting libraries, subject to implementation-plan approval:

- Pydantic for request, response, and BI-tool argument validation.
- SQLAlchemy Core or `pyodbc` for SQL Server access after schema work is approved.
- Alembic for migrations after a physical schema is approved.

## Company Test Environment

The company computer has:

- Microsoft SQL Server 2022 Express.
- Microsoft SQL Server Management Studio 20.x.

The company environment is the target for database validation after development.

## Data Movement Principle

The development environment should simulate structure and behavior, not copy real data. If real data is needed to understand fields, create sanitized field descriptions or synthetic samples.

## Expected Repo Behavior

- `data/dummy/` stores non-database dummy files.
- `database/sqlserver/dummy-data/` stores SQL Server dummy data scripts or data files.
- `database/sqlserver/migrations/` stores schema changes after schema approval.
- `database/sqlserver/scripts/` stores operational SQL scripts after use cases are approved.

## Open Environment Questions

- Which frontend runtime is acceptable on the company machine?
- Are there company restrictions on installing packages or running local services?
- Should the first company test use a local SQL Server database name reserved for this project?
