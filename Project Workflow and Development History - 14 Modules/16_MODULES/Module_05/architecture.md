# Architecture

## Components

-   Keyword/rule store
-   Rule evaluation engine
-   Relevance state writer

## Data flow

``` text
Deduplicated record -> Rule evaluation -> Relevance state (RELEVANT / NOT_RELEVANT / UNCERTAIN) -> RELEVANT/UNCERTAIN continue downstream, NOT_RELEVANT retained but excluded from active pipeline
```

## Interfaces

-   Reads: Module 04 classification output / Module 03 records.
-   Writes: relevance state to Module 03.
-   Forwards: UNCERTAIN records to Module 09 (AI Classification).

## Security considerations

-   Rule/keyword configuration is treated as trusted internal configuration, not user/source-supplied content.
-   Record text from sources is treated as untrusted input to the rule engine, never executed.

## Dependencies

-   Module 03 (Database) for reading/writing state.
-   Module 04 for upstream classification.
-   Module 09 for UNCERTAIN escalation.
