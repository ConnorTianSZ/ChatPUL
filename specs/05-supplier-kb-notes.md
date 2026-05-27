# Supplier Knowledge Base Notes

## Intent

The Supplier Knowledge Base should help procurement users preserve, retrieve, and reuse supplier-related knowledge.

## Current Decision Boundary

Supplier Knowledge Base implementation is paused until core knowledge objects and workflows are specified through SDD conversations.

## Candidate Knowledge Objects

These are candidate objects, not approved requirements:

- Supplier profile.
- Contact information.
- Capability description.
- Equipment or process coverage.
- Project history.
- Commercial notes.
- Risk notes.
- Quality or delivery notes.
- Internal evaluation summary.
- Related documents.

## Ownership Questions

Future specs should define:

- Who can create supplier knowledge.
- Who can edit or approve supplier knowledge.
- Which fields are factual versus judgment-based.
- Which fields require audit history.
- Which fields are sensitive.

## Retrieval Questions

Future specs should define:

- Whether users search by supplier, category, capability, project, or issue.
- Whether answers should quote source documents or summarize structured fields.
- Whether ChatBI can reference supplier knowledge in the same conversation.

## Open Questions

- What is the first supplier knowledge workflow to support?
- Which supplier fields are already available in existing files or reports?
- Which supplier knowledge is sensitive enough to require restricted access?
- Should the knowledge base prioritize structured records, document search, or both?
