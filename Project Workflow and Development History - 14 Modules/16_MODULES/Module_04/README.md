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

Implemented - initial deduplication and change detection

## Current implementation

Implemented in `app/deduplication.py`, with scanner listing input from Module
02 and persistence through the Module 03 ORM models.

## Dependencies

Depends on Module 02 `ScanListing` and Module 03 `Tender` /
`TenderVersion` models.

## Interfaces

Provides reusable deduplication functions and the
`POST /api/v1/sources/{source_id}/deduplicate` batch endpoint.

## Database interaction

Reads and writes `tenders`; changed records update current values and append
`tender_versions`. Current listing metadata is stored in the `tenders.metadata`
JSONB column.

## Security

-   Treats incoming record fields as untrusted text; does not execute or evaluate any content from source records.
-   Match-key generation must not be vulnerable to key-collision manipulation from source content.

## Known limitations

-   Relevance classification remains `UNCERTAIN` until Module 05 processes
    the tender.

## Current active task

Add Module 05 deterministic IT/software relevance filtering.

## Exact next action

Connect deduplicated tenders to the relevance filter pipeline.

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
