# Evaluation Cases

## Purpose

This file will hold concrete cases used to judge whether ChatBI, Supplier Knowledge Base, database behavior, and unified UX behavior are acceptable.

## Evaluation Principle

Each important requirement should become at least one testable case before implementation. Cases should use dummy data in development.

## Case Format

Each case should include:

- Case ID.
- Capability area.
- User role.
- Input or action.
- Dummy data setup.
- Expected behavior.
- Unacceptable behavior.
- Evidence required for pass or fail.

## Initial Eval Areas

The first eval set should cover:

- ChatBI answer correctness.
- ChatBI source traceability.
- ChatBI uncertainty handling.
- Supplier knowledge retrieval.
- Supplier profile update behavior.
- Sensitive data handling.
- PowerBI compatibility views.
- Unified UX handoff between ChatBI and Supplier Knowledge Base.

## Draft Cases

### EVAL-001: Refuse Real Data in Development

- Capability area: data safety.
- User role: developer.
- Input or action: attempt to add real company data into development fixtures.
- Dummy data setup: none.
- Expected behavior: the repo guidance requires synthetic or sanitized data only.
- Unacceptable behavior: committing real supplier names, pricing, project details, or confidential identifiers.
- Evidence required: review of changed files and fixture content.

### EVAL-002: Answer Requires a Source

- Capability area: ChatBI.
- User role: procurement leader.
- Input or action: ask a metric question after approved dummy data exists.
- Dummy data setup: a future dummy dataset with known expected values.
- Expected behavior: answer includes the value and source context required by the ChatBI spec.
- Unacceptable behavior: answer gives a number without traceability.
- Evidence required: comparison with dummy dataset and answer metadata.

## Current Boundary

Detailed eval cases depend on future domain specs. This file currently defines the required evaluation structure and the first safety-oriented cases.
