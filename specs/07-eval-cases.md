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
- Supplier account, represented manufacturer, and authorization certificate handling.
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

### EVAL-006: Supplier Capability Search Uses Uploaded Profiles

- Capability area: Supplier Knowledge Base.
- User role: procurement team lead.
- Input or action: ask "who can do vacuum piping" against dummy supplier profiles.
- Dummy data setup: at least one confirmed supplier account profile with "vacuum piping" in a capability field, and at least one unrelated supplier account profile.
- Expected behavior: the confirmed matching supplier is returned with supplier name, capability summary, match reason, standardization flag, agreement-price flag, responsible buyer, verification status, and latest verification date if available.
- Unacceptable behavior: returning suppliers outside the uploaded database, omitting the match reason, or treating agreement-price coverage alone as proof of capability.
- Evidence required: captured query intent, matched dummy records, and rendered answer.

### EVAL-007: LLM Does Not Invent Canonical Supplier Terms

- Capability area: Supplier Knowledge Base LLM boundary.
- User role: procurement team lead.
- Input or action: ask a capability question containing a term that is not present in uploaded canonical, synonym, related, or raw profile fields.
- Dummy data setup: dummy supplier profiles without the queried term or maintained synonym.
- Expected behavior: the LLM may extract literal search terms, but canonical terms, synonyms, related terms, and alternatives only come from uploaded or manually maintained fields.
- Unacceptable behavior: the LLM creates a new canonical term, synonym, related term, or alternative and presents it as maintained knowledge.
- Evidence required: captured LLM intent, database term-resolution output, and answer text.

### EVAL-008: Related Terms Are Not Presented as Alternatives

- Capability area: Supplier Knowledge Base retrieval.
- User role: procurement team lead.
- Input or action: ask for suppliers matching a dummy capability where only related terms exist.
- Dummy data setup: one supplier account profile has a maintained `related_terms` value; no maintained `alternative_supplier_names` or `alternative_terms` exist.
- Expected behavior: the answer may show related areas or related supplier records as exploration candidates, clearly separated from confirmed alternatives.
- Unacceptable behavior: presenting a related supplier or related term as a substitute or alternative without a maintained alternative relationship.
- Evidence required: dummy profile fields and rendered answer grouping.

### EVAL-009: Maintained Alternatives Can Be Displayed

- Capability area: Supplier Knowledge Base retrieval.
- User role: procurement team lead.
- Input or action: ask for alternatives to a dummy supplier or capability.
- Dummy data setup: a dummy supplier profile includes `alternative_supplier_names`, `alternative_reason`, `alternative_source`, and `alternative_verified_at`, using a localization-project example.
- Expected behavior: the maintained alternative is shown separately from confirmed direct matches and related terms, with reason, source, and verification date.
- Unacceptable behavior: hiding maintained alternatives, mixing alternatives with related terms, or generating unmaintained alternatives.
- Evidence required: dummy profile fields and rendered answer grouping.

### EVAL-010: No Confirmed Result Does Not Mean No Supplier Exists

- Capability area: Supplier Knowledge Base uncertainty handling.
- User role: procurement team lead.
- Input or action: ask for a capability with no confirmed matching dummy profile.
- Dummy data setup: no confirmed match; optionally one pending or stale match.
- Expected behavior: the answer states that the current knowledge base has no confirmed match, then shows pending or stale matches separately if present, or says the capability data may need supplementation.
- Unacceptable behavior: saying the company has no such supplier, hiding pending or stale matches without explanation, or fabricating a supplier outside the database.
- Evidence required: matched record set and answer text.

### EVAL-011: Supplier Profile Upload Is Not Data Cleaning

- Capability area: Supplier Knowledge Base maintenance.
- User role: data maintainer.
- Input or action: upload a dummy Excel or CSV supplier profile file containing valid required columns and rough multi-value text fields.
- Dummy data setup: dummy upload file with comma or semicolon separated fields.
- Expected behavior: the system imports rows directly after minimum technical checks for readability and required columns.
- Unacceptable behavior: automatic deduplication, automatic synonym generation, automatic canonical-term generation, automatic related-term generation, or silent modification of uploaded text.
- Evidence required: uploaded file, import log, and stored records.

### EVAL-012: Responsible Buyer Is Shown Instead of Supplier Contact

- Capability area: Supplier Knowledge Base UX and data safety.
- User role: procurement team lead.
- Input or action: view supplier capability search results.
- Dummy data setup: supplier profile includes responsible buyer; supplier contact fields are absent or not enabled for display.
- Expected behavior: the result displays responsible buyer and does not display supplier contact person, phone number, or email by default.
- Unacceptable behavior: displaying supplier contact details by default or omitting responsible buyer from a supplier result.
- Evidence required: rendered answer or frontend inspection.

### EVAL-013: 2025 Spend Value Is Stored But Not Displayed By Default

- Capability area: Supplier Knowledge Base data safety.
- User role: procurement team lead.
- Input or action: ask a supplier capability question against dummy records that include a 2025 annual supplier order value.
- Dummy data setup: one dummy supplier account profile linked to a synthetic 2025 annual spend summary.
- Expected behavior: the answer may use supplier profile and approved material evidence for matching, but it does not display the 2025 annual order value by default and does not send that value to the LLM prompt.
- Unacceptable behavior: showing annual order value in the default Supplier KB answer, using the annual value as proof of capability, or sending the annual value to an LLM prompt without a later approved spec.
- Evidence required: rendered answer, matched record metadata, and prompt payload inspection.

### EVAL-014: Pareto Material Descriptions Stay Evidence, Not Normalized Terms

- Capability area: Supplier Knowledge Base maintenance and LLM boundary.
- User role: data maintainer.
- Input or action: import dummy 2025 material descriptions selected by the first-80%-of-order-value rule, including repeated English descriptions and AI Chinese translation drafts.
- Dummy data setup: synthetic supplier spend-derived evidence with duplicate descriptions, `included_by_pareto_80`, `pareto_rank`, `cumulative_order_value_share`, and `translation_status`.
- Expected behavior: original descriptions and AI translation drafts are preserved as evidence fields. Exact duplicates may be linked or grouped for traceability, but no canonical terms, synonyms, related terms, alternatives, or normalized capability fields are generated automatically.
- Unacceptable behavior: automatic fuzzy deduplication, AI synonym generation, AI related-term generation, AI normalization, or silent promotion of AI translation drafts into confirmed capability fields.
- Evidence required: uploaded dummy file, import log, stored records, and comparison showing no unapproved generated terms.

### EVAL-015: Agent Supplier Can Represent Multiple Manufacturers

- Capability area: Supplier Knowledge Base retrieval.
- User role: procurement team lead.
- Input or action: ask which supplier can provide a dummy manufacturer or product family represented by an agent supplier.
- Dummy data setup: one synthetic supplier account with `supplier_type` = distributor or authorized_agent, linked to two synthetic represented manufacturers with different material fields and product summaries.
- Expected behavior: the answer returns the supplier account and clearly labels the represented manufacturer that matched, without mixing the two manufacturers' capabilities or presenting manufacturer capability as the supplier account's own manufacturing capability.
- Unacceptable behavior: flattening all manufacturer capabilities into the supplier account, hiding which manufacturer matched, or returning the wrong manufacturer relationship.
- Evidence required: supplier account record, representation records, captured query intent, matched relationship, and rendered answer.

### EVAL-016: Authorization Validity Is Relationship-Specific

- Capability area: Supplier Knowledge Base authorization handling.
- User role: procurement team lead.
- Input or action: ask for an authorized agent for a dummy manufacturer.
- Dummy data setup: one synthetic supplier account linked to two manufacturers; one relationship has a valid authorization certificate, and the other has an expired or unknown certificate.
- Expected behavior: the result shows authorization status and validity date range for the matching supplier-manufacturer relationship. Valid authorization is preferred when the user asks for authorized agents. Expired or unknown authorization is clearly labeled and not displayed as currently authorized.
- Unacceptable behavior: treating supplier-level authorization as valid for all represented manufacturers, omitting expiry status, or inferring valid authorization from purchase history, agreement-price coverage, or material descriptions.
- Evidence required: certificate records, matched relationship, ranking output, and rendered answer.

### EVAL-017: ChatBI Manufacturer Blank Bucket Is Explicit

- Capability area: ChatBI manufacturer analytics.
- User role: procurement leader.
- Input or action: ask for PO item counts or auto PO ratio by manufacturer.
- Dummy data setup: dummy PO item rows with at least one populated manufacturer and at least one blank manufacturer.
- Expected behavior: the result includes a clearly labeled blank or unknown manufacturer bucket, or explicitly states that blank manufacturers were excluded because the user asked for that filter.
- Unacceptable behavior: dropping blank manufacturer rows silently, inferring manufacturer from material description or Supplier KB records, or treating blank manufacturer as an ingestion failure.
- Evidence required: dummy source rows, executed ChatBI tool parameters, result table, and answer explanation.

### EVAL-018: ChatBI WBS Blank Rows Are Allowed

- Capability area: ChatBI PO item analytics.
- User role: procurement team lead.
- Input or action: ask for PO counts or lead-time metrics with and without project/WBS filtering.
- Dummy data setup: dummy PO item rows with project WBS values and rows where `WBS element` is blank for non-project PO.
- Expected behavior: blank-WBS rows remain queryable and are labeled as non-project or blank WBS according to the approved field dictionary.
- Unacceptable behavior: rejecting blank-WBS rows, classifying them as data corruption, or forcing them into a fake project.
- Evidence required: dummy source rows, field dictionary entry, executed tool filter, and rendered answer.

### EVAL-019: Auto PO Ratio Uses UC4CPIC Over All PO Items

- Capability area: ChatBI auto PO ratio.
- User role: procurement leader.
- Input or action: ask for auto PO ratio by buyer and by manufacturer.
- Dummy data setup: dummy PO item rows with `PO created by = UC4CPIC` on some rows and other creator values on other rows, across at least two buyers and two manufacturers.
- Expected behavior: the numerator is the count of filtered PO item rows created by `UC4CPIC`; the denominator is the count of all filtered PO item rows at PO-item grain.
- Unacceptable behavior: using PO header count when item grain is required, using order value weighting without an approved spec, excluding non-UC4 rows from the denominator, or sending raw rows to the LLM.
- Evidence required: dummy expected-ratio calculation, executed backend tool or SQL view result, captured LLM payload showing no raw rows, and rendered answer.

### EVAL-020: Lead Time Metrics Identify PR Versus OC Logic

- Capability area: ChatBI lead-time reporting.
- User role: procurement leader.
- Input or action: ask for lead-time performance by buyer or manufacturer.
- Dummy data setup: dummy PO item rows with `PR Date`, `Doc. Date`, `order confirmatioin date`, missing confirmation dates, and delivered-without-OC examples.
- Expected behavior: ChatBI states whether the answer uses PR lead time, OC lead time, or both. PR lead time uses working days from PR date to PO document date minus one. OC lead time uses working days from PO document date to order confirmation date minus one. Missing dates are classified according to the ChatBI spec.
- Unacceptable behavior: mixing PR and OC lead-time definitions without labeling, counting missing PR dates as zero, dropping missing OC rows silently, or asking the LLM to calculate lead time from raw rows.
- Evidence required: dummy expected calculation, backend result, answer text, and source traceability metadata.

### EVAL-021: ChatBI And Supplier KB Databases Are Isolated

- Capability area: data architecture and safety.
- User role: developer.
- Input or action: inspect the schema, migrations, connection configuration, or query code after database work begins.
- Dummy data setup: separate dummy ChatBI and Supplier KB datasets.
- Expected behavior: ChatBI reporting tables/views and Supplier KB knowledge tables are in separate database boundaries or equivalent isolated schemas with no shared mutable business tables. Any cross-capability link is absent unless a later approved bridge spec exists.
- Unacceptable behavior: joining ChatBI supplier dimensions directly to Supplier KB profiles in the MVP, writing ChatBI imports into Supplier KB tables, or using Supplier KB manufacturer records to fill blank ChatBI manufacturer fields.
- Evidence required: schema files, migration scripts, connection configuration, and query/tool implementation review.

### EVAL-022: Canonical ChatBI Excel Imports Without Excel Recalculation

- Capability area: ChatBI data ingestion.
- User role: developer.
- Input or action: import a dummy canonical ChatBI Excel workbook into SQL Server staging.
- Dummy data setup: dummy workbook shaped like the current `PO List` source, with calculated compatibility values for `Combine`, reporting month, department, PR lead time, PR classification, OC lead time, and OC classification.
- Expected behavior: the import script reads stored workbook values and loads them into SQL staging with import batch metadata. It does not require opening Excel or recalculating formulas during import.
- Unacceptable behavior: depending on Excel desktop automation for formula recalculation during import, importing stale formula text as official values, or failing when formula cells are stored as values.
- Evidence required: dummy workbook, import log, staging row count, imported compatibility values, and import batch metadata.

### EVAL-023: SQL Reporting Layer Owns Official Formula Logic

- Capability area: ChatBI reporting correctness.
- User role: procurement leader.
- Input or action: ask for lead-time classification or auto PO ratio after dummy data is imported.
- Dummy data setup: dummy SQL staging rows imported from canonical ChatBI Excel, including compatibility formula-column values for reconciliation.
- Expected behavior: ChatBI uses SQL views, stored procedures, or backend-owned query logic for official lead-time classifications and auto PO ratio. Compatibility values may be compared for validation but are not blindly trusted as the only source of truth.
- Unacceptable behavior: ChatBI answers directly from arbitrary Excel formula columns without SQL/backend validation, recalculates metrics in the LLM, or lets PowerBI-only formulas define untested ChatBI behavior.
- Evidence required: executed ChatBI tool name, SQL/backend logic reference, expected dummy calculation, answer text, and reconciliation output when available.

### EVAL-024: ChatBI Tool Schema Is Strictly Enforced

- Capability area: ChatBI BI tool boundary.
- User role: developer.
- Input or action: submit tool calls that (a) name a tool not listed in `specs/08-chatbi-tool-schemas.md`, (b) include a top-level property other than `tool` and `arguments`, (c) include an argument key that is not in the selected tool's JSON Schema, or (d) pass an enum value (such as `group_by`, `wbs_scope`, `lead_time_type`, or `date_field`) that is not in the approved enum list.
- Dummy data setup: any approved tool's dummy fixture; no fixture-shape dependency.
- Expected behavior: each call is rejected by backend schema validation before any data access. The rejection states which rule failed (unknown tool, unknown property, or unknown enum value).
- Unacceptable behavior: silently dropping unknown properties, coercing an unknown enum to a default, executing the tool with partial arguments, or letting the LLM smuggle extra fields into `arguments`.
- Evidence required: captured tool-call payloads, backend validation log, and rejection response.

### EVAL-025: ChatBI Rejects Unsupported Metric Requests

- Capability area: ChatBI scope boundary.
- User role: procurement leader.
- Input or action: ask a question that requires an unsupported metric, such as price trend, value-weighted automation ratio, quality risk, or delivery risk.
- Dummy data setup: dummy PO-item fixture only; no price-trend or risk fields are available.
- Expected behavior: the backend rejects the call or returns a structured error indicating the metric is not supported, without synthesizing an answer.
- Unacceptable behavior: returning a fabricated price-trend, value-weighted, quality-risk, or delivery-risk result; silently substituting PO item count for an unrelated measure.
- Evidence required: captured tool-call payload, backend rejection or error response, and backend validation log.

### EVAL-026: ChatBI Result Includes Structured Source Trace

- Capability area: ChatBI traceability.
- User role: procurement leader.
- Input or action: run any approved ChatBI tool against the dummy PO-item fixture.
- Dummy data setup: `data/dummy/dummy_po_items.csv` and `data/dummy/dummy_po_items_expected.json`.
- Expected behavior: the result payload includes `source_trace` with at least dataset identifier, dataset version or refresh marker, tool name, filters applied, and time range applied.
- Unacceptable behavior: omitting `source_trace`, populating it with free-form text.
- Evidence required: result JSON payload and backend log of the tool call.

## Current Boundary

Additional eval cases depend on future domain specs. This file currently defines the required evaluation structure, the first safety-oriented cases, Supplier KB MVP cases, and the first ChatBI PO-item analytics cases.
