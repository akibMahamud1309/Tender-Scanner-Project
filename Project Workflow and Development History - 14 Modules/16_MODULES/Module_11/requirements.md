# Requirements

## Functional requirements

-   Display a list of tenders filtered by relevance state, deadline, and source.
-   Show the structured analysis (Module 10 output) for a selected tender with links to supporting evidence.
-   Show document collection/processing status per tender.
-   Show source health (last scan time, failures) sourced from the Scheduler/Scanner.
-   Provide filtering, search, and sorting across tenders.
-   Allow the user to record a bid/no-bid decision, which is handed to Module 12 (Decision History).

## Non-functional requirements

-   Must run locally, consistent with the project's local-first direction.
-   Should remain responsive with the expected local data volume without requiring pagination workarounds for normal use.
-   Read-only views must not allow accidental data modification outside explicit decision actions.

## Inputs

-   Tender records, analysis, document status, and source health from Module 03 (populated by Modules 04-10 and 13).

## Outputs

-   User-facing views.
-   Bid/no-bid decision actions forwarded to Module 12.

## Acceptance criteria

-   A relevant tender and its analysis are viewable with evidence links that resolve to the source document/page.
-   Source health for a failing source is visible without needing to inspect logs directly.
-   Recording a decision updates Module 12 and is reflected immediately in the Dashboard.
