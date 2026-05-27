# ChatBI Domain Spec

## Intent

ChatBI should help procurement users ask business questions and receive trustworthy, traceable answers from approved data sources.

## Initial User Group

The initial users are procurement leaders and team leads. The first version should support decision review and management visibility before broad self-service analytics.

## Current Decision Boundary

ChatBI implementation is paused until the domain is specified through SDD conversations. The next ChatBI conversations should define:

- Priority questions users want to ask.
- Metrics and definitions users already trust.
- Source systems, files, PowerBI datasets, or reports involved.
- Required answer format.
- Permission and sensitivity boundaries.
- Cases where the assistant should refuse, ask for clarification, or show uncertainty.

## Candidate Question Categories

These are candidate categories, not approved requirements:

- Supplier performance.
- Purchase order status.
- Cost or price trend analysis.
- Project purchasing overview.
- Delivery or quality risk.
- Data quality checks.

## Traceability Requirement

ChatBI answers should eventually explain where the answer came from. At minimum, future specs should decide whether answers cite:

- Database table or view names.
- Report names.
- Source file names.
- Query filters.
- Time range.
- Data refresh time.

## Open Questions

- What are the top five ChatBI questions for procurement leaders?
- Which existing PowerBI report is the best starting reference?
- Should answers be mostly Chinese, English, or bilingual?
- How should the system handle incomplete or stale data?
