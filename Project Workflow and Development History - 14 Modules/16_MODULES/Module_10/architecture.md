# Architecture

## Components

-   Field extraction engine
-   Evidence linker
-   Multi-document consolidator

## Data flow

``` text
Relevant tender + document text -> Structured field extraction -> Evidence linking -> Consolidation across documents -> Persist -> Dashboard
```

## Interfaces

-   Reads: classified tenders and document text from Module 09.
-   Writes: structured analysis to Module 03.
-   Feeds: Module 11 (Dashboard).

## Security considerations

-   Document text is treated as untrusted input to the extraction model; extraction output is structured data only.
-   No extracted field is treated as executable or actionable without human review via the Dashboard.

## Dependencies

-   Module 09 for classified tenders and evidence.
-   Module 03 for persistence.
-   Module 11 for presentation.
