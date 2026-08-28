# Architecture

## Components

-   Match-key generator
-   Lookup/comparison engine
-   Diff generator
-   Change-event writer

## Data flow

``` text
Source Scanner output -> Match-key generation -> Lookup against Database -> Compare -> Classify (NEW/UNCHANGED/CHANGED) -> Diff (if CHANGED) -> Persist via Database
```

## Interfaces

-   Reads: normalized records from Module 02.
-   Reads/writes: Module 03 (Database) for lookups and history writes.
-   Writes: classification result consumed by Module 05 (IT/Software Relevance Filter).

## Security considerations

-   Treats incoming record fields as untrusted text; does not execute or evaluate any content from source records.
-   Match-key generation must not be vulnerable to key-collision manipulation from source content.

## Dependencies

-   Module 02 (Source Scanner) for input records.
-   Module 03 (Database) for persistence and history.
