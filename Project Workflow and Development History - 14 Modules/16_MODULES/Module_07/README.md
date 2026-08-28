# Module 07 --- Document Processor

## Purpose

Extracts text and metadata from machine-readable tender documents and prepares content for analysis.

## Role in the system

``` text
Document Collector
      ↓
Document Processor
      ↓
OCR (when needed) / AI Classification
```

## Responsibilities

-   Extract text from supported machine-readable PDFs/DOCX and similar formats.
-   Detect extraction quality.
-   Normalize extracted content for downstream AI.
-   Route insufficient extraction to OCR.

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

-   Document parsing libraries are used defensively; malformed files must not crash the pipeline.
-   Extracted content remains untrusted text passed to AI, not executed.

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
-   Extract text from supported machine-readable PDFs/DOCX and similar formats.
-   Detect extraction quality.
-   Normalize extracted content for downstream AI.
-   Route insufficient extraction to OCR.
