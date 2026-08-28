# Architecture

## Components

-   Attachment discoverer
-   Downloader
-   File validator
-   Metadata recorder

## Data flow

``` text
Relevant tender record -> Discover attachment links -> Download -> Validate (type/size/checksum) -> Record metadata -> Hand off file references to Document Processor
```

## Interfaces

-   Reads: tender records from Module 05/03.
-   Writes: document files to local storage; document metadata to Module 03.
-   Hands off: collected documents to Module 07 (Document Processor).

## Security considerations

-   All downloaded files are treated as untrusted; no automatic execution of macros, scripts, or embedded content.
-   File type is validated by inspecting content, not solely by trusting the file extension.

## Dependencies

-   Module 05 for the list of relevant tenders.
-   Module 03 (Database) for metadata persistence.
-   Local document storage.
