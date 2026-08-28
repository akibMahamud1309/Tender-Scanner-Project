# Module 05 --- IT/Software Relevance Filter

## Purpose

Filters collected opportunities to identify software, IT, digital, technology, and related tenders.

## Role in the system

``` text
Deduplication & Change Detection / Database
      ↓
IT/Software Relevance Filter
      ↓
Document Collector
```

## Responsibilities

-   Apply deterministic keyword/rule filters.
-   Identify software/IT/digital/technology relevance.
-   Use confidence/uncertainty states where classification is not clear.
-   Pass uncertain cases to later AI classification or manual review.

## Current status

Implemented - initial deterministic relevance filter

## Current implementation

Implemented in `app/relevance_filter.py`, using source-configured keyword
rules and persisting traceable `Classification` rows.

## Dependencies

Depends on Module 03 `Tender` and `Classification` models and Module 01 source
configuration.

## Interfaces

Provides `POST /api/v1/tenders/{tender_id}/relevance` and reusable rule
evaluation functions.

## Database interaction

Updates `tenders.relevance_state` and appends a rule-based row to
`classifications` with rule IDs and matched-keyword evidence.

## Security

-   Rule/keyword configuration is treated as trusted internal configuration, not user/source-supplied content.
-   Record text from sources is treated as untrusted input to the rule engine, never executed.

## Known limitations

-   Keyword matching is deterministic substring matching.

## Current active task

Implement Module 06 Document Collector for relevant tenders.

## Exact next action

Forward `RELEVANT` and `UNCERTAIN` tenders to document collection while
retaining `NOT_RELEVANT` records for auditability.

## Agent continuation rule

Before changing this module, read the module files and the top-level
project history/decision/compatibility files. Before ending a session,
update the module history and the top-level history with the exact work
completed and next action.

## Expected responsibilities
-   Apply deterministic keyword/rule filters.
-   Identify software/IT/digital/technology relevance.
-   Use confidence/uncertainty states where classification is not clear.
-   Pass uncertain cases to later AI classification or manual review.
