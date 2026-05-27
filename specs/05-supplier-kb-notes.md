# Supplier Knowledge Base Spec

## Intent

The Supplier Knowledge Base should help procurement users preserve, retrieve, and reuse supplier-related knowledge that is currently scattered across shared drives, email, SAP-related exports, personal memory, and informal team knowledge.

The first version focuses on answering supplier capability questions for Bosch China, Suzhou, Intelligent Manufacturing Solutions procurement users in the non-standard equipment business context.

## First Workflow

The first Supplier Knowledge Base workflow is capability search:

- User input examples: "who can do vacuum piping", "do we have suppliers for visual inspection", "which suppliers can support front-stage pump related work".
- The chatbot interprets the natural-language question and searches the internal supplier knowledge database.
- The answer returns suppliers already present in the database, with capability context, standardization/agreement-price flags where available, and the responsible buyer.

MPN or Bosch material number lookup remains in scope for the product, but it is not the first MVP workflow. If uploaded supplier records already contain material numbers or MPN values, the first version may support simple exact matching. It does not model full SAP material master data, guarantee complete MPN mapping, or perform real-time SAP lookup.

## MVP Scope

The first version uses a flat supplier-level capability profile:

- One row represents one supplier profile.
- Multi-value fields may use commas or semicolons.
- The product accepts that early records may be rough, as long as they are useful enough for search and review.
- Data cleanup happens before upload. The Supplier KB tool is not responsible for cleaning, merging, normalizing, or deduplicating uploaded data in the MVP.

The MVP supports:

- Natural-language supplier capability search.
- Direct Excel or CSV upload into the supplier profile table.
- Manual single-record create and edit.
- Supplier profile fields for rough capability, material field, strengths, typical products or services, and application scenarios.
- Display of responsible buyer.
- Display of whether the supplier is in the standardization list and whether agreement-price coverage is known.
- Clear marking of information confirmation state.
- AI-assisted answer wording and database-internal candidate ranking, with strict labeling when a result is inferred or uncertain.

The MVP does not support:

- Direct mailbox, shared-drive, SAP, or production-data ingestion.
- AI data cleaning, AI canonical-term generation, AI synonym generation, or AI clarification-question generation.
- Public website or supplier-news extraction.
- A complete material-field taxonomy or graph.
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

## Supplier Profile Fields

The MVP supplier profile should include these logical fields:

### Supplier Identity

- `supplier_id`: internal stable ID.
- `supplier_name`: official supplier name.
- `supplier_short_name`: common short name, alias, or spoken name.
- `supplier_type`: optional value such as manufacturer, distributor, trader, integrator, or service provider.

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

## Maintenance Model

Daily maintenance can be done by the product owner, interns, or responsible buyers.

HOD is not part of routine data maintenance or approval. The goal is traceable responsibility, not a heavy approval chain.

Interns may call or email suppliers to confirm supplier-shareable information such as capability, lead time, origin, or shipping location. They must not disclose internal agreement prices, internal evaluations, project details, or other sensitive Bosch information to suppliers.

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

Data cleanup, deduplication, and field standardization happen outside the tool before upload.

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
    "agreement_price_required": null
  }
}
```

Canonical terms, synonyms, related terms, and alternatives must come from uploaded or manually maintained database fields. If those fields are empty, the search should rely on the raw supplier profile text fields.

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

Agreement-price and standardization fields may be used for display, filtering, and ranking, but they must not alone prove supplier capability.

## Result Ranking and Display

Result ranking should prefer:

1. `confirmed` profiles.
2. Direct matches in capability, material field, strengths, products/services, or scenarios.
3. Matches in human-maintained canonical terms or synonyms.
4. Multiple-field matches.
5. Standardized suppliers.
6. Suppliers with known agreement-price coverage.
7. More recently verified profiles.

Each supplier result should show:

- supplier name;
- capability summary;
- match reason;
- standardization flag;
- agreement-price flag;
- responsible buyer;
- profile verification status;
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
- create or persist canonical terms, synonyms, related terms, or alternatives in the MVP.

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

A later spec should define the material and MPN workflow separately.

## Future Modules

Future Supplier Knowledge Base work may include:

- material field dictionary and taxonomy;
- synonym and canonical-term governance;
- supplier capability detail records below the supplier-profile level;
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
