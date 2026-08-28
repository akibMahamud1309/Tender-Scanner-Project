# Module 03 --- Database

## Purpose

Provides the PostgreSQL persistence layer and data-access model for the
application.

## Role in the system

``` text
Previous module
      ↓
Database
      ↓
Next module
```

## Responsibilities

-   Implement only responsibilities belonging to this module.
-   Provide documented inputs and outputs.
-   Report errors without silently hiding them.
-   Maintain its own version and compatibility records.
-   Keep interfaces stable unless an API/architecture change is
    documented.

## Current status

In Progress

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

Document security assumptions and untrusted inputs.

## Known limitations

-   Not yet implemented.

## Current active task

Environment and schema design complete. Writing SQLAlchemy models next.

## Exact next action

Write SQLAlchemy models (starting with `sources`, then `tenders`, `tender_versions`, `documents`, `document_pages`, `classifications`, `tender_analysis`, `decisions`, `job_status`, `notifications`) per 17_SOFTWARE_DEVELOPMENT_SPECIFICATION.md Section 1. Then create the tables in the `tender_scanner` database via SQLAlchemy `create_all()` or Alembic migration.

## Agent continuation rule

Before changing this module, read the module files and the top-level
project history/decision/compatibility files. Before ending a session,
update the module history and the top-level history with the exact work
completed and next action.

## Expected responsibilities
- Define ORM/data-access layer.
- Manage PostgreSQL migrations.
- Persist sources, tenders, documents, analysis, decisions, and history.
- Enforce appropriate keys, constraints, and indexes.

## Database direction
PostgreSQL is the approved primary database direction.
