# Module 08 --- OCR

## Purpose

Processes scanned/image-only document pages when normal text extraction is insufficient.

## Role in the system

``` text
Document Processor
      ↓
OCR
      ↓
AI Classification
```

## Responsibilities

-   Detect image-only/scanned pages.
-   OCR only when required.
-   Preserve page/document traceability.
-   Record OCR engine/version and processing results.

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

-   OCR engine runs against untrusted document images; must be sandboxed/resourced to avoid resource-exhaustion from malicious files.
-   OCR output is treated as untrusted extracted text, same as regular extraction.

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
-   Detect image-only/scanned pages.
-   OCR only when required.
-   Preserve page/document traceability.
-   Record OCR engine/version and processing results.
