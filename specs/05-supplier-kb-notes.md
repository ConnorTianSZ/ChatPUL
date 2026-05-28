# Supplier Knowledge Base Spec

## Intent

The Supplier Knowledge Base should help procurement users preserve, retrieve, and reuse supplier-related knowledge that is currently scattered across shared drives, email, SAP-related exports, personal memory, and informal team knowledge.

The first version focuses on answering supplier capability questions for Bosch China, Suzhou, Intelligent Manufacturing Solutions procurement users in the non-standard equipment business context.

## First Workflow

The first Supplier Knowledge Base workflow is capability search:

- User input examples: "who can do vacuum piping", "do we have suppliers for visual inspection", "which suppliers can support front-stage pump related work".
- The chatbot interprets the natural-language question and searches the internal supplier knowledge database.
- The answer returns supplier accounts already present in the database, with capability context, represented manufacturer context when relevant, standardization/agreement-price flags where available, authorization validity when relevant, and the responsible buyer.

MPN or Bosch material number lookup remains in scope for the product, but it is not the first MVP workflow. If uploaded supplier records already contain material numbers or MPN values, the first version may support simple exact matching. It does not model full SAP material master data, guarantee complete MPN mapping, or perform real-time SAP lookup.

## MVP Scope

The first version should not assume that one supplier number equals one manufacturer or one technical capability owner.

The first version uses a simple supplier account profile plus optional represented-manufacturer and authorization records:

- One supplier account represents one internal supplier number or procurement-facing supplier record.
- A supplier account may be a manufacturer, distributor, trader, integrator, service provider, or agent.
- One supplier account may represent multiple manufacturers.
- One represented manufacturer may have different strengths, material areas, products, and certificate validity under the same supplier account.
- Multi-value fields may still use commas or semicolons in early uploads where a separate record has not yet been approved.
- The product accepts that early records may be rough, as long as they are useful enough for search and review.
- Data cleanup happens before upload. The Supplier KB tool is not responsible for cleaning, merging, normalizing, or deduplicating uploaded data in the MVP.

The MVP supports:

- Natural-language supplier capability search.
- Direct Excel or CSV upload into approved Supplier KB templates.
- Manual single-record create and edit.
- Supplier profile fields for rough capability, material field, strengths, typical products or services, and application scenarios.
- Representation records for supplier-account-to-manufacturer relationships.
- Authorization certificate records for represented manufacturers, including validity period and status.
- Display of responsible buyer.
- Display of whether the supplier is in the standardization list and whether agreement-price coverage is known.
- Display of represented manufacturer and authorization status when the match depends on a manufacturer relationship.
- Clear marking of information confirmation state.
- AI-assisted answer wording and database-internal candidate ranking, with strict labeling when a result is inferred or uncertain.

The MVP does not support:

- Direct mailbox, shared-drive, SAP, or production-data ingestion.
- AI data cleaning, AI canonical-term generation, AI synonym generation, or AI clarification-question generation.
- Public website or supplier-news extraction.
- A complete material-field taxonomy or graph.
- Automatic identification of manufacturer, brand, or authorization from material descriptions.
- Automatic validation of authorization certificates against external manufacturer websites or portals.
- HOD approval as a routine data maintenance step.
- Default display of supplier contact person, supplier phone number, or supplier email.

## Data Source Strategy

The first version starts from manually maintained supplier capability profiles.

Standardization lists and agreement-price lists are source or validation inputs, not the product's final knowledge shape. They may be cleaned outside this tool and uploaded into the supplier profile fields:

- Standardization list input can populate `is_standardized`.
- Agreement-price list input can populate `has_agreement_price` or related notes.
- Responsible-buyer input can populate `responsible_buyer`.

Agreement-price coverage is commercial evidence. It must not be treated as proof that a supplier has a broad technical capability.

Public website and news extraction are deferred to a later module, primarily for large suppliers, large manufacturers, or important brands. Any public-web extraction must produce candidate information only and require human approval before becoming trusted supplier knowledge.

### Supplier Account, Manufacturer, and Authorization Evidence

Supplier KB must distinguish between the procurement-facing supplier account and the manufacturer whose products or capabilities may be supplied through that account.

This distinction is required because a supplier number may belong to an agent or distributor that represents several manufacturers, and each manufacturer can have different material coverage, technical strengths, application scenarios, and authorization validity.

Authorization evidence should be treated as maintained evidence, not as an AI-inferred fact:

- A supplier account may have zero, one, or many represented manufacturers.
- A supplier-account-to-manufacturer relationship may have zero, one, or many authorization certificate records.
- Authorization certificate validity is specific to the supplier account and manufacturer relationship.
- Expired, missing, or unknown authorization must not be displayed as currently authorized.
- Manufacturer capability context must not be copied into the supplier account's own capability fields unless a maintainer explicitly confirms that the supplier itself provides that capability.
- A historical purchase record or material description may suggest that a supplier has supplied a manufacturer's product, but it does not prove current authorization.

### 2025 Spend-Derived Material Evidence

A proposed Supplier KB enrichment source is the 2025 supplier purchasing detail prepared by interns or procurement maintainers from approved internal sources.

This source should be treated as procurement evidence, not as a replacement for supplier capability profiles:

- The 2025 annual supplier order value may be stored in the database for internal analysis and prioritization.
- The 2025 annual supplier order value is internal-sensitive commercial data and is not displayed by default in Supplier KB answers.
- The annual value should not be sent to an LLM prompt unless a later approved spec defines a controlled ChatBI or analytics use case.
- Historical order value must not be treated as proof that a supplier has a broad technical capability.
- The source export, calculation workbook, import file, and database records must follow the repository data safety rules.

For each supplier, the maintainer may sort 2025 material-level order value in descending order and select the materials whose cumulative order value reaches the first 80% of that supplier's 2025 total order value. These selected material descriptions may be stored as historical material evidence.

The 80% rule is a prioritization rule only. It does not mean low-value materials are unimportant, and it does not mean selected materials are confirmed capability terms.

English material descriptions from 2025 purchasing detail may receive an AI-assisted Chinese translation draft, subject to these limits:

- Real company material descriptions must not be uploaded to public cloud AI services from the development machine.
- AI translation for real data requires an approved internal or company-permitted AI environment.
- AI-translated Chinese descriptions are stored as draft translations until reviewed by a responsible buyer, data owner, or approved maintainer.
- AI translation must not create canonical terms, synonyms, related terms, alternative terms, supplier alternatives, or normalized capability fields in the MVP.
- Exact duplicate English descriptions may be grouped or linked for review and search traceability, but fuzzy deduplication, semantic linking, synonym generation, and AI normalization remain out of MVP scope unless a later approved spec changes this boundary.
- AI must not infer manufacturer identity, brand ownership, or authorization status from material descriptions unless those fields were explicitly provided or human-maintained.

## Supplier Profile Fields

The MVP supplier profile should include these logical fields for the procurement-facing supplier account:

### Supplier Identity

- `supplier_id`: internal stable ID.
- `supplier_number`: internal supplier number when available.
- `supplier_name`: official supplier name.
- `supplier_short_name`: common short name, alias, or spoken name.
- `supplier_type`: optional value such as manufacturer, distributor, trader, integrator, or service provider.
- `supplier_role_note`: optional note clarifying whether the account acts as direct manufacturer, authorized agent, distributor, trader, integrator, or mixed role.

### Capability Description

- `capability_summary`: short free-text summary of what the supplier can do.
- `material_field`: rough material field values, allowing comma or semicolon separated entries.
- `strengths`: supplier strengths, allowing free text or separated values.
- `typical_products_or_services`: typical products or services.
- `application_scenarios`: equipment, industry, or use-case scenarios.
- `origin_or_manufacturing_location`: optional origin or manufacturing location.
- `shipping_location`: optional shipping location.
- `standard_lead_time`: optional standard lead time.

### Procurement Context

- `is_standardized`: yes, no, or unknown. Unknown must not be displayed as no.
- `has_agreement_price`: yes, no, or unknown. Unknown must not be displayed as no.
- `responsible_buyer`: responsible procurement colleague. This is shown by default.
- `commercial_note`: optional internal note. Sensitive content must follow repository data safety rules.

### Maintenance Metadata

- `source_type`: manual, excel_import, supplier_call, supplier_email_confirmation, internal_list, agreement_price_list, standardization_list, or other.
- `data_owner`: person responsible for maintaining the profile.
- `updated_by`: latest editor.
- `reviewed_by`: person who confirmed the profile information when applicable.
- `last_verified_at`: latest confirmation date.
- `verification_method`: phone confirmation, email confirmation, internal list, procurement experience, or other.
- `profile_verification_status`: confirmed, pending_review, stale, or archived_record.
- `sensitivity_level`: normal or internal_sensitive.
- `raw_notes`: original notes that should be preserved for traceability.

### Optional Human-Maintained Search Helpers

These fields are optional in the MVP. If used, they must be maintained or uploaded by humans before the query runs:

- `canonical_terms`: confirmed standard terms.
- `synonyms`: confirmed synonyms.
- `related_terms`: related areas or adjacent capabilities.
- `alternative_terms`: confirmed alternative terms.
- `alternative_supplier_names`: confirmed alternative supplier relationships.
- `alternative_reason`: reason for the alternative relationship.
- `alternative_source`: source such as localization_project or procurement_confirmation.
- `alternative_verified_at`: date the alternative relationship was confirmed.

## Manufacturer Representation Fields

Manufacturer representation should not be flattened into the supplier account profile row once the relationship needs certificate validity, manufacturer-specific capabilities, or manufacturer-specific material evidence.

### Manufacturer Identity

- `manufacturer_id`: internal stable ID for a manufacturer or brand owner.
- `manufacturer_name`: official manufacturer name.
- `manufacturer_short_name`: common short name, brand name, or spoken name.
- `manufacturer_country_or_region`: optional origin or main manufacturing region.
- `manufacturer_note`: optional maintainer note.
- `manufacturer_verification_status`: confirmed, pending_review, stale, or archived_record.

### Supplier Manufacturer Representation

- `supplier_manufacturer_id`: internal stable ID for the supplier-account-to-manufacturer relationship.
- `supplier_id`: links to the supplier account.
- `manufacturer_id`: links to the represented manufacturer.
- `representation_type`: authorized_agent, distributor, reseller, trader, system_integrator, service_partner, unknown, or other.
- `representation_scope`: optional scope such as product line, material family, region, project type, or application area.
- `manufacturer_capability_summary`: manufacturer-specific capability or product summary for this relationship.
- `manufacturer_material_field`: rough manufacturer-specific material fields.
- `manufacturer_typical_products_or_services`: typical manufacturer products or services supplied through this account.
- `manufacturer_application_scenarios`: manufacturer-specific application scenarios.
- `relationship_verification_status`: confirmed, pending_review, stale, or archived_record.
- `relationship_source_type`: manual, excel_import, supplier_confirmation, manufacturer_certificate, internal_list, agreement_price_list, purchase_history, or other.
- `responsible_buyer`: responsible procurement colleague for this relationship when different from the supplier account owner.
- `data_owner`: person accountable for maintaining this relationship.
- `last_verified_at`: latest relationship confirmation date.
- `raw_notes`: original relationship notes for traceability.

Representation records may support search and display, but relationship fields must make clear whether the match is against the supplier account itself or against a represented manufacturer.

### Authorization Certificate

- `authorization_certificate_id`: internal stable ID.
- `supplier_manufacturer_id`: links to the supplier-account-to-manufacturer relationship.
- `certificate_type`: agency_certificate, distribution_authorization, reseller_authorization, service_authorization, other, or unknown.
- `certificate_number`: optional certificate or authorization reference number.
- `authorized_scope`: product line, material family, region, or business scope covered by the certificate.
- `valid_from`: certificate start date when available.
- `valid_to`: certificate end date when available.
- `authorization_status`: valid, expired, pending_review, unknown, revoked, or not_applicable.
- `issuer_name`: manufacturer or issuer shown on the certificate.
- `certificate_source_type`: uploaded_certificate, supplier_provided, manufacturer_provided, internal_list, manual, or other.
- `certificate_file_reference`: internal file reference or document ID if files are later supported; raw files must not be committed to this repo.
- `reviewed_by`: person who reviewed the certificate.
- `last_reviewed_at`: latest certificate review date.
- `sensitivity_level`: normal or internal_sensitive.

For MVP answer display, the system may show authorization status, validity date range, represented manufacturer, and authorized scope. It should not show raw certificate files by default.

## Spend-Derived Evidence Fields

2025 spend-derived evidence should not be flattened into the main supplier profile row. When schema design is approved, it should use separate logical records so that commercial evidence, material evidence, and confirmed supplier capability remain distinguishable.

### Supplier Annual Spend Summary

- `supplier_id`: links to the supplier profile.
- `spend_year`: initially 2025.
- `annual_order_value`: total order value for the supplier in the spend year.
- `currency`: currency for the annual value.
- `source_type`: approved internal export, PowerBI-derived source, SAP-related export, or other approved source.
- `source_snapshot_at`: date when the source extract was produced.
- `prepared_by`: person who prepared the import file.
- `data_owner`: person accountable for the data after import.
- `sensitivity_level`: normally `internal_sensitive`.
- `display_by_default`: false for the MVP.

### Supplier Material Spend Evidence

- `supplier_id`: links to the supplier profile.
- `supplier_manufacturer_id`: optional link to a represented manufacturer relationship when the source explicitly provides manufacturer or brand information, or when a maintainer has reviewed the mapping.
- `spend_year`: initially 2025.
- `material_identifier`: optional Bosch material number, MPN, or source material key when available and allowed.
- `manufacturer_part_number`: optional manufacturer part number when available and allowed.
- `manufacturer_name_from_source`: optional manufacturer or brand name exactly as shown in the approved source.
- `manufacturer_mapping_status`: not_provided, source_provided, human_reviewed, or rejected.
- `material_description_en`: original English material description from the approved source.
- `material_description_zh_ai_draft`: AI-assisted Chinese translation draft, when allowed.
- `translation_status`: `not_translated`, `ai_draft`, or `human_reviewed`.
- `translation_reviewed_by`: reviewer for human-reviewed translations, when applicable.
- `included_by_pareto_80`: true when selected by the first-80%-of-order-value rule.
- `pareto_rank`: descending order-value rank within the supplier and year, when available.
- `cumulative_order_value_share`: cumulative share at selection time, when available.
- `evidence_note`: optional maintainer note.
- `source_snapshot_at`: date when the source extract was produced.
- `sensitivity_level`: normally `internal_sensitive`.

Spend-derived material descriptions may support search as historical purchase evidence after import, but answer wording must label the match reason clearly, for example:

- "Matched historical 2025 material description."
- "Matched manufacturer-specific historical material evidence."
- "AI Chinese translation draft; needs review."
- "This is historical purchase evidence, not a confirmed broad capability statement."
- "Manufacturer mapping is source-provided or human-reviewed; current authorization still depends on certificate status."

## Maintenance Model

Daily maintenance can be done by the product owner, interns, or responsible buyers.

HOD is not part of routine data maintenance or approval. The goal is traceable responsibility, not a heavy approval chain.

Interns may call or email suppliers to confirm supplier-shareable information such as capability, lead time, origin, or shipping location. They must not disclose internal agreement prices, internal evaluations, project details, or other sensitive Bosch information to suppliers.

Interns may also prepare 2025 supplier purchasing detail only from approved internal sources on approved company equipment. That work is a data preparation workflow outside the Supplier KB application:

1. Export or receive the approved 2025 detail source.
2. Calculate supplier-level 2025 annual order value.
3. Preserve supplier number, supplier name, manufacturer or brand fields if the approved source contains them.
4. Select material descriptions covering the first 80% of each supplier's 2025 order value.
5. Add AI-assisted Chinese translation drafts only in an approved internal or company-permitted AI environment.
6. Submit the prepared import file for review or upload by the data owner.

The application must preserve who prepared the data, which source snapshot was used, and whether translations are AI drafts or human-reviewed.

Interns or maintainers may also collect supplier-manufacturer authorization certificate information. Certificate maintenance must preserve represented manufacturer, authorized scope, validity dates, review status, and source. Certificate files or scans must not be committed to this repo; only dummy or sanitized structural samples may be used for development.

## Upload Behavior

The MVP upload flow is intentionally simple:

1. Upload an Excel or CSV file.
2. The system checks only minimum technical requirements:
   - file can be read;
   - required columns exist;
   - column names match the expected template.
3. The system imports rows directly.

The MVP upload tool must not:

- Clean data.
- Merge duplicate suppliers.
- Normalize multi-value fields.
- Generate canonical terms.
- Generate synonyms.
- Generate related terms.
- Generate clarification questions.
- Automatically infer alternatives.
- Automatically infer represented manufacturers from free-text material descriptions.
- Automatically infer valid authorization from purchase history, agreement-price coverage, or material descriptions.

Data cleanup, deduplication, and field standardization happen outside the tool before upload.

Supplier account upload, manufacturer representation upload, authorization certificate upload, and 2025 spend-derived evidence upload are separate workflows. A valid spend-derived evidence upload must not silently modify the supplier account's confirmed capability fields, manufacturer representation fields, or authorization certificate fields. If a maintainer wants a material description to become a confirmed capability term, that confirmation must happen through a separate profile or representation edit.

## Query Understanding

The LLM may extract the user's intent and literal search terms, but it must not decide official canonical terms by itself.

Example intent:

```json
{
  "query_type": "supplier_capability_search",
  "original_user_text": "有没有做真空管路的供应商",
  "extracted_terms": ["真空管路"],
  "filters": {
    "profile_verification_status": ["confirmed", "pending_review", "stale"],
    "standardized_only": null,
    "agreement_price_required": null,
    "authorization_required": null,
    "manufacturer_name": null
  }
}
```

Canonical terms, synonyms, related terms, and alternatives must come from uploaded or manually maintained database fields. If those fields are empty, the search should rely on the raw supplier profile text fields.
Manufacturer names, represented-manufacturer relationships, and authorization status must come from uploaded or manually maintained fields. The LLM must not infer current authorization from material descriptions or purchase history.

The first-version matching fields are:

- `capability_summary`
- `material_field`
- `strengths`
- `typical_products_or_services`
- `application_scenarios`
- optional human-maintained `canonical_terms`
- optional human-maintained `synonyms`
- optional human-maintained `related_terms`
- optional human-maintained `alternative_terms` and `alternative_supplier_names`
- represented manufacturer fields such as `manufacturer_name`, `manufacturer_short_name`, `manufacturer_capability_summary`, `manufacturer_material_field`, `manufacturer_typical_products_or_services`, and `manufacturer_application_scenarios`
- authorization fields such as `authorization_status`, `authorized_scope`, `valid_from`, and `valid_to` when the user asks about authorized agents or current representation
- imported 2025 `material_description_en` and `material_description_zh_ai_draft` as historical material evidence, if the spend-derived evidence module is approved and populated

Agreement-price and standardization fields may be used for display, filtering, and ranking, but they must not alone prove supplier capability.
Spend-derived order value may be used for internal prioritization only after an approved spec defines the behavior. It must not be displayed by default or used as standalone proof of capability.
Authorization certificate fields may be used for display, filtering, and ranking, but expired, missing, or unknown authorization must be labeled clearly.

## Result Ranking and Display

Result ranking should prefer:

1. `confirmed` profiles.
2. Direct matches in the correct entity context: supplier account fields for supplier capability questions, represented manufacturer fields for manufacturer or brand questions.
3. Valid authorization certificate records when the user asks for authorized agents, distributors, or current representation.
4. Matches in human-maintained canonical terms or synonyms.
5. Multiple-field matches.
6. Standardized suppliers.
7. Suppliers with known agreement-price coverage.
8. More recently verified profiles, relationships, and certificates.

If spend-derived material evidence is enabled, exact matches in human-confirmed supplier profile fields should rank above matches found only in historical material descriptions. AI-translated Chinese descriptions should rank below original English descriptions and human-reviewed translations unless a later evaluation proves otherwise.
If the query is about a manufacturer or brand, a supplier account with a valid matching representation should rank above a supplier account that only has historical purchase evidence for that manufacturer.

Each supplier result should show:

- supplier name;
- supplier number when available;
- supplier type or role when relevant;
- capability summary;
- match reason;
- represented manufacturer when the match depends on a manufacturer relationship;
- authorization status, valid date range, and authorized scope when the match depends on authorization;
- standardization flag;
- agreement-price flag;
- responsible buyer;
- profile verification status;
- relationship and certificate verification status when relevant;
- latest verification date when available;
- important uncertainty or clarification notes.

Supplier contact person, phone number, and email are not displayed by default in the MVP. Future display of supplier contact details requires explicit data ownership, verification date, and access-control decisions.

## AI Candidate Behavior

AI may help rank or phrase candidate results, but every returned supplier must already exist in the database.

AI candidate output must be separated from confirmed matches and clearly labeled, for example:

- "AI candidate from database records."
- "Needs confirmation."
- "Matched because application scenario contains high-vacuum equipment, but the profile does not explicitly say vacuum piping."

AI must not:

- recommend suppliers that are not in the database;
- turn a related term into an alternative;
- state an inferred relationship as a confirmed fact;
- create or persist canonical terms, synonyms, related terms, or alternatives in the MVP;
- use AI translation drafts to create or persist normalized capability fields without human review;
- infer that a supplier is an authorized agent, distributor, or representative from purchase history, agreement-price coverage, material descriptions, or AI translation;
- infer that a manufacturer capability belongs to the supplier account itself unless a human-maintained field says so.

## Related vs Alternative

`related_terms` and alternatives have different meanings.

`related_terms` are adjacent, upstream, downstream, or semantically related areas. They support exploration and clarification, but they do not mean one term or supplier can replace another.

Alternatives are confirmed substitution relationships. They may be maintained in the MVP, but most records are expected to have empty alternative fields. Alternative relationships should come from localization projects, procurement confirmation, or another explicit source.

The chatbot may display:

- confirmed matches;
- maintained alternatives;
- related areas to continue searching.

It must not display related areas as substitutes unless a maintained alternative relationship exists.

## No-Result Behavior

When no confirmed result is found, the chatbot must not say "we do not have this kind of supplier" unless data coverage has been explicitly proven.

It should say:

- "The current knowledge base has no confirmed supplier matching this query."

Then it should:

- show `pending_review` or `stale` matches separately if they exist;
- show related-area matches separately if maintained `related_terms` exist;
- ask a clarification question if the user term is broad or ambiguous;
- suggest that the capability data may need to be supplemented if no relevant data exists.

## MPN and Bosch Material Number Boundary

MPN and Bosch material number search is a future important workflow.

The MVP may perform simple exact matching only when uploaded supplier profiles already contain material number or MPN fields. It does not define:

- a complete material master data model;
- SAP integration;
- real-time SAP lookup;
- complete Bosch material number to MPN mapping;
- agreement-price detail lookup by material.

If uploaded spend-derived evidence or representation records include manufacturer part numbers or source-provided manufacturer names, the MVP may use simple exact matching with clear labels. It must not infer manufacturer part numbers, manufacturer names, or brand ownership from free-text descriptions.

A later spec should define the material and MPN workflow separately.

## Future Modules

Future Supplier Knowledge Base work may include:

- material field dictionary and taxonomy;
- synonym and canonical-term governance;
- supplier capability detail records below the supplier-profile level;
- manufacturer master-data governance;
- authorization certificate file storage, expiry alerts, and renewal workflow;
- richer supplier spend and material evidence workflows beyond the 2025 first-80%-order-value dataset;
- AI-assisted data normalization with human confirmation;
- public supplier website extraction for large suppliers;
- supplier news monitoring and push alerts for events such as local factory setup, acquisition, capacity expansion, discontinuation, or major quality issues;
- supplier contact display with verification and access-control rules;
- direct integration with approved internal data sources.

## Current Open Questions

- What is the exact Excel/CSV template for the first supplier profile upload?
- Which fields are required versus optional in the first upload template?
- How old can a confirmed profile be before it becomes stale?
- Which MPN or Bosch material number fields, if any, should be included in the first supplier profile template?
- What dummy supplier dataset should be created for development evaluation?
- What is the approved internal source for 2025 supplier purchasing detail?
- Which currency and exchange-rate rule should be used for 2025 annual order value?
- Does "annual order value" mean PO value, invoice value, goods-receipt value, or another approved procurement metric?
- Who is allowed to review and promote AI Chinese translation drafts to human-reviewed translations?
- What is the exact upload template for supplier-account-to-manufacturer representation records?
- What certificate fields are available from existing authorization documents?
- Should Supplier KB show expired authorization records by default as warnings, or only when the user asks for historical/expired relationships?
- Who owns certificate review and renewal-date maintenance?
