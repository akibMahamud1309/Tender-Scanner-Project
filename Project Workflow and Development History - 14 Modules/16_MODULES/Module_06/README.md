# Module 06 --- Document Collector

## Purpose

Finds, downloads, validates, and tracks tender documents associated with relevant opportunities.

## Role in the system

``` text
IT/Software Relevance Filter
      ↓
Document Collector
      ↓
Document Processor
```

## Responsibilities

-   Discover tender attachments.
-   Download accessible documents.
-   Validate and record file metadata.
-   Avoid repeated unnecessary downloads.
-   Treat downloads as untrusted files.

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

-   All downloaded files are treated as untrusted; no automatic execution of macros, scripts, or embedded content.
-   File type is validated by inspecting content, not solely by trusting the file extension.

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
-   Discover tender attachments.
-   Download accessible documents.
-   Validate and record file metadata.
-   Avoid repeated unnecessary downloads.
-   Treat downloads as untrusted files.
