# Architecture

## Components

-   Tender list view
-   Tender detail/analysis view
-   Source health view
-   Decision action handler (Module 12 integration pending)

## Data flow

``` text
Database (tenders, analysis, document status, source health) -> Dashboard views -> User review -> Decision action -> Decision History
```

## Interfaces

-   Reads: FastAPI tender list endpoint backed by Module 03.
-   Writes: decision actions to Module 12.

## Security considerations

-   Local-only interface; no assumption of remote/multi-user access unless explicitly documented.
-   Displayed source content remains clearly attributed to its source, not presented as verified fact.

## Dependencies

-   Module 03 for all displayed data.
-   Module 10 for analysis.
-   Module 12 for decision recording.
-   Module 13 for source health data.
