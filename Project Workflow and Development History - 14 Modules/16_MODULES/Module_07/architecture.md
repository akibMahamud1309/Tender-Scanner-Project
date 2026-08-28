# Architecture

## Components

-   Text extractor
-   Quality scorer
-   Normalizer
-   OCR router

## Data flow

``` text
Collected document -> Extract text -> Score quality -> Normalize -> (if quality sufficient) forward to AI Classification, else route to OCR
```

## Interfaces

-   Reads: document files from Module 06.
-   Writes: extracted/normalized text to Module 03.
-   Routes: low-quality documents to Module 08 (OCR).

## Security considerations

-   Document parsing libraries are used defensively; malformed files must not crash the pipeline.
-   Extracted content remains untrusted text passed to AI, not executed.

## Dependencies

-   Module 06 for source documents.
-   Module 08 (OCR) for fallback extraction.
-   Module 03 for persistence.
