# Module 12 --- Decision History

## Purpose

Stores bid/no-bid decisions, decline reasons, categories, comments, and decision history.

## Role in the system

``` text
Dashboard
      ↓
Decision History
      ↓
(terminal / feeds reporting)
```

## Responsibilities

-   Store bid/no-bid decisions.
-   Store decline reason and category.
-   Store user comments and timestamps.
-   Preserve historical decisions.
-   Provide data for future reporting/learning.

## Current status

Implemented (0.1.1)

## Current implementation

The module validates and appends bid/no-bid decisions, requires reason and
category for no-bid entries, and exposes chronological decision history.

## Dependencies

See `compatibility.md`.

## Interfaces

See `architecture.md`.

## Database interaction

Document all tables, queries, migrations, or database events used by
this module.

## Security

-   Decision comments are stored as plain user-entered text; no execution of comment content anywhere in the system.

## Known limitations

-   Decision categories remain free text until a maintained taxonomy is introduced.

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
-   Store bid/no-bid decisions.
-   Store decline reason and category.
-   Store user comments and timestamps.
-   Preserve historical decisions.
-   Provide data for future reporting/learning.
