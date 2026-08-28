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

Implemented (0.1.1)

## Current implementation

The notification service creates durable unread event records, deduplicates
events by key, exposes unread retrieval and read acknowledgement, and reports
delivery failures explicitly.

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

-   Delivery is currently represented by the local database/in-process adapter;
    email or chat channels can be added later.

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
