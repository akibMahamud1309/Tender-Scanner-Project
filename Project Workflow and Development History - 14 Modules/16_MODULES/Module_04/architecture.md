# Architecture

## Components

-   Match-key generator
-   Lookup/comparison engine
-   Diff generator
-   Change-event writer
-   Batch API adapter

## Data flow

``` text
Source Scanner output -> Match-key generation -> Lookup against Database -> Compare -> Classify (NEW/UNCHANGED/CHANGED) -> Diff (if CHANGED) -> Persist via Database
```

## Interfaces

-   Reads: normalized records from Module 02.
-   Reads/writes: Module 03 (Database) for lookups and history writes.
-   Writes: classification result consumed by Module 05 (IT/Software Relevance Filter).
-   Batch endpoint: `POST /api/v1/sources/{source_id}/deduplicate`.

## Security considerations

-   Treats incoming record fields as untrusted text; does not execute or evaluate any content from source records.
-   Match-key generation must not be vulnerable to key-collision manipulation from source content.
-   Listing metadata is validated as JSON data and never executed.

## Dependencies

-   Module 02 (Source Scanner) for input records.
-   Module 03 (Database) for persistence and history.
