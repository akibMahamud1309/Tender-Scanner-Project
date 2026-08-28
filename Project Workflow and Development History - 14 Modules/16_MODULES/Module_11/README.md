# Module 11 --- Dashboard

## Purpose

Provides the local user interface for reviewing tenders, documents, analysis, source health, and decisions.

## Role in the system

``` text
AI Tender Analysis
      ↓
Dashboard
      ↓
Decision History
```

## Responsibilities

-   Show new/relevant tenders.
-   Show analysis and source evidence.
-   Show document status.
-   Show source health.
-   Allow review and decision actions.
-   Provide filtering/search/sorting.

## Current status

Implemented (0.1.1)

## Current implementation

The React dashboard provides a local tender review queue with search,
relevance filters, summary metrics, source links, and a selected-tender detail
panel backed by the FastAPI tender list endpoint.

## Dependencies

See `compatibility.md`.

## Interfaces

See `architecture.md`.

## Database interaction

Document all tables, queries, migrations, or database events used by
this module.

## Security

-   Local-only interface; no assumption of remote/multi-user access unless explicitly documented.
-   Displayed source content remains clearly attributed to its source, not presented as verified fact.

## Known limitations

-   Decision actions remain pending Module 12.
-   Detailed analysis/document status panels will expand as their read APIs are added.

## Current active task

None.

## Exact next action

Follow `09_MODULE_VERSION_HISTORY.md` and the latest project-history
handoff to determine the next implementation task.

## Agent continuation rule

Before changing this module, read the module files and the top-level
project history/decision/compatibility files. Before ending a session,
update the module history and the top-level history with the exact work
completed and next action.

## Expected responsibilities
-   Show new/relevant tenders.
-   Show analysis and source evidence.
-   Show document status.
-   Show source health.
-   Allow review and decision actions.
-   Provide filtering/search/sorting.
