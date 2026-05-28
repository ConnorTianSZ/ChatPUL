# Project Brief

## Purpose

Build a spec-first internal tool for procurement colleagues that combines ChatBI and a Supplier Knowledge Base into one entry point.

## Organization Context

- Company context: Bosch China, Suzhou.
- Business context: Intelligent Manufacturing Solutions.
- Work type: non-standard equipment.
- Initial users: procurement leaders and team leads.
- Broader future users: procurement colleagues who need business insight, supplier knowledge, or both.

## Product Thesis

Procurement users should be able to enter one tool, ask business/data questions through ChatBI, and access structured supplier knowledge without switching between disconnected workflows.

## Current Scope Boundary

This repo is only the project skeleton and spec base. Application code, database schema, and production data handling are intentionally outside the current step.

## Durable Constraints

- Database-backed data management is a core requirement.
- Backend development uses Python + FastAPI + pytest unless a later approved spec changes the stack.
- Existing PowerBI assets should remain useful.
- Development must use dummy data to prevent accidental company data upload.
- Company-environment testing targets SQL Server 2022 Express and SSMS 20.x.

## Open Product Questions

- Which procurement decisions should ChatBI support first?
- Which supplier knowledge objects matter most in the first version?
- Which PowerBI datasets or reports are most important to preserve or connect?
- Which user roles need different access permissions?
