# Product Scope

## One Entry, Two Capabilities

The product should provide one unified entry point with two main capabilities:

1. ChatBI
2. Supplier Knowledge Base

The entry point should make the relationship between both capabilities clear. Users should not feel they are switching between unrelated tools.

## Initial Users

The first users are procurement leaders and team leads. The first version should optimize for review, decision support, and knowledge lookup rather than broad self-service configuration.

## ChatBI Scope

ChatBI will eventually help users ask questions about procurement-related data. The exact data domains, metrics, and question types will be specified in `specs/04-chatbi-domain-spec.md`.

Current boundary: ChatBI behavior is not implemented until data sources, trusted metrics, permission boundaries, and answer evaluation cases are specified.

## Supplier Knowledge Base Scope

The Supplier Knowledge Base will eventually help users maintain and retrieve supplier-related knowledge. The exact entities, workflows, and source documents will be specified in `specs/05-supplier-kb-notes.md`.

Current boundary: Supplier knowledge behavior is not implemented until core supplier objects, update ownership, search expectations, and data sensitivity rules are specified.

## Shared UX Scope

The unified navigation and orchestration between ChatBI and Supplier Knowledge Base is specified in `specs/06-unified-ux-orchestration.md`.

## Evaluation Scope

Expected behavior will be validated through concrete cases in `specs/07-eval-cases.md` before implementation.
