# Environment Strategy

## Development Environment

Development happens on a personal computer through Codex with dummy data only.

Rules:

- Do not use real company datasets.
- Do not upload company data to cloud tools.
- Do not store production credentials.
- Keep `.env` local and untracked.
- Keep `.env.example` limited to variable names and safe example values.

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

- Which local backend runtime is preferred for development?
- Which frontend runtime is acceptable on the company machine?
- Are there company restrictions on installing packages or running local services?
- Should the first company test use a local SQL Server database name reserved for this project?
