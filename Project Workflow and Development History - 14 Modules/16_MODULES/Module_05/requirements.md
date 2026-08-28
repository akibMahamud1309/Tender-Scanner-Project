# Requirements

## Functional requirements

-   Read NEW and CHANGED records from Module 04 / Module 03.
-   Apply a maintained set of deterministic keyword and rule-based filters against title, category, and summary fields.
-   Assign a relevance state of RELEVANT, NOT_RELEVANT, or UNCERTAIN.
-   Route UNCERTAIN records to Module 09 (AI Classification) for further evaluation rather than discarding them.
-   Persist the relevance state and the rule(s) that produced it for traceability.

## Non-functional requirements

-   Filter rules must be maintainable without code changes where practical (e.g., an editable keyword/rule list).
-   Must never silently discard a record; NOT_RELEVANT records remain in the database with their classification, not deleted.
-   False negatives (missed relevant tenders) are treated as more costly than false positives that reach manual/AI review.

## Inputs

-   NEW/CHANGED records from Module 04.
-   Current keyword/rule configuration.

## Outputs

-   Relevance classification (RELEVANT / NOT_RELEVANT / UNCERTAIN) per record.
-   UNCERTAIN records forwarded to Module 09.

## Acceptance criteria

-   A tender clearly matching configured IT/software keywords is marked RELEVANT.
-   A tender clearly outside scope (e.g., construction, catering) is marked NOT_RELEVANT.
-   A tender with ambiguous wording is marked UNCERTAIN and forwarded, not dropped.
-   Every classification records which rule(s) triggered it.
