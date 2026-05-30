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

These are candidate flows, not approved requirements. Each flow is anchored to the first approved ChatBI tools in `specs/08-chatbi-tool-schemas.md` so the UX surface stays inside the approved analytics scope.

- A user reviews a `supplier_dimension_summary` result and opens the related Supplier Knowledge Base profile from a row in that result.
- A user reviews a `manufacturer_dimension_summary` row (including the `<BLANK>` manufacturer bucket) and either opens the related manufacturer record in Supplier KB or files a data quality note when no Supplier KB record exists.
- A user reviews a `lead_time_summary` bucket (`>7days`, `no order confirmation`, or `Delivered without OC`) and opens the responsible buyer or the related supplier profile to investigate.
- A user reviews an `auto_po_ratio_summary` group and saves a follow-up question or supplier note for later review.
- A user reads a supplier profile and asks ChatBI for recent purchase context, which is answered through one of the four approved tools above, not a free-form query.

## Cross-Feature Identifier Boundary

ChatBI analytical supplier and manufacturer dimensions are not the same objects as Supplier Knowledge Base profiles. ChatBI tools work from PO-item source identifiers (`Vendor`, `Name 1`, `Manufactur`). Supplier KB profiles use their own `supplier_id` and represented-manufacturer records.

Cross-feature navigation must therefore go through an explicit mapping rather than a silent join. The first version should keep this boundary visible in the UI, for example by labeling whether a result row links to a confirmed Supplier KB profile or only to a procurement-source identifier.

## UX Constraints

- Initial users are procurement leaders and team leads, so the interface should prioritize clarity, trust, and review.
- The UI should expose data source and freshness information when analytics are involved.
- The UI should avoid making generated answers look more certain than the underlying data supports.

## Open Questions

- Should the first version start with a chat-first entry or a dashboard/search-first entry?
- Should ChatBI and Supplier Knowledge Base share one conversation context?
- What actions should be available from a ChatBI answer? At minimum, the four approved tools in `specs/08-chatbi-tool-schemas.md` should each have a defined set of available actions before backend implementation.
- What actions should be available from a supplier profile?
- How should `Vendor` / `Name 1` from ChatBI tools map to Supplier Knowledge Base `supplier_id`? Who owns and maintains that mapping, and how is an unmapped procurement-source supplier shown in the UI?
- How should `Manufactur` from ChatBI tools (including the `<BLANK>` bucket) map to Supplier KB represented-manufacturer records, and how should a blank or unmapped manufacturer be labeled in cross-feature navigation?
