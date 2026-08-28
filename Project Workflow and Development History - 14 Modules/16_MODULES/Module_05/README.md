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

Planned

## Current implementation

No application implementation has been established yet. Agents must
inspect the repository before updating this statement.

## Dependencies

See `compatibility.md`.

## Interfaces

See `architecture.md`.

## Database interaction

Document all tables, queries, migrations, or database events used by
this module.

## Security

-   Rule/keyword configuration is treated as trusted internal configuration, not user/source-supplied content.
-   Record text from sources is treated as untrusted input to the rule engine, never executed.

## Known limitations

-   Not yet implemented.

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
-   Apply deterministic keyword/rule filters.
-   Identify software/IT/digital/technology relevance.
-   Use confidence/uncertainty states where classification is not clear.
-   Pass uncertain cases to later AI classification or manual review.
