# Unified UX Orchestration

## Intent

The product should feel like one procurement workbench, not two unrelated tools.

## Entry Point

The first screen should eventually provide access to:

- ChatBI conversations.
- Supplier Knowledge Base search or browsing.
- Shared context when a user moves from one capability to the other.

## Orchestration Principle

ChatBI and Supplier Knowledge Base should stay distinct enough to maintain data trust, but connected enough that users can move naturally between analysis and supplier knowledge.

## Candidate Cross-Feature Flows

These are candidate flows, not approved requirements:

- A user asks ChatBI about supplier performance and opens the related supplier profile.
- A user reads a supplier profile and asks ChatBI for recent purchase or project context.
- A user finds missing supplier data and triggers a data quality note.
- A leader reviews a ChatBI answer and saves a follow-up question or supplier note.

## UX Constraints

- Initial users are procurement leaders and team leads, so the interface should prioritize clarity, trust, and review.
- The UI should expose data source and freshness information when analytics are involved.
- The UI should avoid making generated answers look more certain than the underlying data supports.

## Open Questions

- Should the first version start with a chat-first entry or a dashboard/search-first entry?
- Should ChatBI and Supplier Knowledge Base share one conversation context?
- What actions should be available from a ChatBI answer?
- What actions should be available from a supplier profile?
