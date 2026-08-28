# Module 14 --- Notifications

## Purpose

Delivers local/configured notifications about new relevant tenders, deadlines, failures, and other events.

## Role in the system

``` text
(cross-cutting, operates across the pipeline)
      ↓
Notifications
      ↓
(terminal)
```

## Responsibilities

-   Notify about newly relevant tenders.
-   Notify about approaching deadlines where configured.
-   Notify about important source failures.
-   Avoid duplicate notification spam.
-   Record notification status.

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

-   Notification content is derived from already-validated internal data, not raw untrusted source text, to avoid delivering unsanitized content.

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
-   Notify about newly relevant tenders.
-   Notify about approaching deadlines where configured.
-   Notify about important source failures.
-   Avoid duplicate notification spam.
-   Record notification status.
