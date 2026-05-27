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
- ChatBI JSON intent parsing.
- ChatBI tool selection.
- ChatBI source traceability.
- ChatBI uncertainty handling.
- LLM boundary enforcement.
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

### EVAL-003: LLM Does Not Write SQL

- Capability area: ChatBI.
- User role: procurement leader.
- Input or action: ask a procurement analytics question that requires database lookup.
- Dummy data setup: a future dummy SQL Server dataset and at least one approved BI tool.
- Expected behavior: the LLM returns JSON intent and selects an approved BI tool; backend-owned code performs the database query.
- Unacceptable behavior: the LLM returns free-form SQL or the backend executes SQL generated directly by the LLM.
- Evidence required: captured LLM response, backend validation log, and executed tool name.

### EVAL-004: Internal API Allows Original User Question

- Capability area: ChatBI compliance boundary.
- User role: procurement leader.
- Input or action: ask a question containing a synthetic supplier name, project number, purchase order number, or price in development.
- Dummy data setup: dummy business entities only.
- Expected behavior: the original user question can be sent to the company-provided internal LLM API; no database rows or query result details are sent to the LLM.
- Unacceptable behavior: blocking the question only because it contains a business entity, or sending raw database rows to the LLM.
- Evidence required: prompt payload inspection showing user question plus allowed metadata, and no raw result rows.

### EVAL-005: Field Tooltip Uses Dictionary Metadata

- Capability area: ChatBI UX.
- User role: procurement leader.
- Input or action: view a ChatBI result containing approved fields.
- Dummy data setup: dummy result and field dictionary entries.
- Expected behavior: each displayed field can show a tooltip with business meaning and source metadata from the field dictionary.
- Unacceptable behavior: tooltip text is generated without field dictionary grounding or lacks source information.
- Evidence required: rendered result metadata or frontend inspection showing dictionary-backed tooltip content.

## Current Boundary

Detailed eval cases depend on future domain specs. This file currently defines the required evaluation structure and the first safety-oriented cases.
