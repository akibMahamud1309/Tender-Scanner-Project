# Module 10 --- AI Tender Analysis

## Purpose

Extracts detailed tender requirements, eligibility, deadlines, experience, documents, restrictions, and other structured intelligence.

## Role in the system

``` text
AI Classification
      ↓
AI Tender Analysis
      ↓
Dashboard
```

## Responsibilities

-   Extract title/reference/organization.
-   Extract deadlines.
-   Extract scope.
-   Extract technical requirements.
-   Extract eligibility.

## Current status

Implemented (0.1.1)

## Current implementation

The module extracts a stable set of tender fields through the configured
GPT-5.6 Terra endpoint, validates exact page evidence, marks absent fields
`NOT_STATED`, and persists results for dashboard consumption.

## Dependencies

See `compatibility.md`.

## Interfaces

See `architecture.md`.

## Database interaction

Document all tables, queries, migrations, or database events used by
this module.

## Security

-   Document text is treated as untrusted input to the extraction model; extraction output is structured data only.
-   No extracted field is treated as executable or actionable without human review via the Dashboard.

## Known limitations

-   AI output is rejected when fields or evidence are missing or fabricated.

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
-   Extract title/reference/organization.
-   Extract deadlines.
-   Extract scope.
-   Extract technical requirements.
-   Extract eligibility.
