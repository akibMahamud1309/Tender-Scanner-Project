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

Implemented (0.1.1)

## Current implementation

The OCR adapter sends low-quality documents to the configured
OpenAI-compatible GPT-5.6 Terra endpoint, validates page-aware JSON output,
normalizes text, and persists page-level OCR results.

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

-   Requires `TERRA_API_KEY` and `TERRA_API_BASE_URL`.
-   Provider responses must contain non-empty page results.

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
