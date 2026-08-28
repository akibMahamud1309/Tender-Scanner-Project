# Module 04 --- Deduplication & Change Detection

## Purpose

Determines whether a collected opportunity is new, duplicate, or materially changed.

## Role in the system

``` text
Source Scanner
      ↓
Deduplication & Change Detection
      ↓
Database
```

## Responsibilities

-   Match by stable identifiers such as source/reference information and normalized URLs where appropriate.
-   Detect materially changed tender fields/documents.
-   Preserve history instead of destroying previous versions.
-   Prevent duplicate records.

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

-   Treats incoming record fields as untrusted text; does not execute or evaluate any content from source records.
-   Match-key generation must not be vulnerable to key-collision manipulation from source content.

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
-   Match by stable identifiers such as source/reference information and normalized URLs where appropriate.
-   Detect materially changed tender fields/documents.
-   Preserve history instead of destroying previous versions.
-   Prevent duplicate records.
