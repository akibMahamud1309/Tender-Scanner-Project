# Requirements

## Functional requirements

-   Accept RELEVANT tenders (with extracted document text) from Module 09.
-   Extract structured fields: title, reference number, issuing organization, submission deadline, scope of work, technical requirements, eligibility criteria, required experience, required documents, and restrictions.
-   Represent each extracted field with a confidence indicator and a reference back to the supporting evidence.
-   Handle tenders where a field is genuinely absent by marking it NOT_STATED rather than guessing.
-   Persist the structured analysis for Dashboard consumption.

## Non-functional requirements

-   Extraction must not fabricate values for fields not actually present in the source documents.
-   Should handle multi-document tenders, consolidating fields that may be spread across several files.
-   Analysis output format must remain stable for the Dashboard, versioned if changed.

## Inputs

-   RELEVANT tender records and their extracted document text from Module 09.

## Outputs

-   Structured tender analysis (deadlines, scope, requirements, eligibility, restrictions, etc.) with evidence references.

## Acceptance criteria

-   A tender's submission deadline is extracted correctly when present in the documents.
-   A field with no supporting evidence is marked NOT_STATED, not fabricated.
-   Every extracted field links back to the document/page it came from.
