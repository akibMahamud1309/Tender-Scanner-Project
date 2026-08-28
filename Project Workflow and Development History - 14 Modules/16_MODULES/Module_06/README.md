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

Implemented (0.1.1)

## Current implementation

The collector discovers `document_urls` from tender listing metadata, safely
downloads HTTP(S) content, validates supported file signatures and size,
computes SHA-256 checksums, persists document metadata, and skips collected
duplicates.

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

-   HTML and office formats without recognized signatures are rejected.
-   Storage defaults to `storage/documents/{tender_id}` through the API.

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
