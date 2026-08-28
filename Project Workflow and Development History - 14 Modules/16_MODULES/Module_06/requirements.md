# Requirements

## Functional requirements

-   For each RELEVANT (and UNCERTAIN pending review) record, discover linked attachment URLs from the source page/listing.
-   Download each discovered document to local storage.
-   Validate file type, size, and integrity (checksum) before marking a document collected.
-   Record file metadata: filename, source URL, checksum, size, content type, download timestamp.
-   Skip re-downloading a document already collected for a given tender unless the source indicates it changed.

## Non-functional requirements

-   Downloads must not execute or open documents in a way that runs embedded content.
-   Must handle partial/failed downloads without leaving corrupt files marked as collected.
-   Should respect reasonable rate limits per source to avoid overloading source websites.

## Inputs

-   RELEVANT/UNCERTAIN tender records with source page references from Module 05 / Module 03.

## Outputs

-   Downloaded document files in local storage.
-   Document metadata records linked to the parent tender.
-   Collection status per document (COLLECTED / FAILED / SKIPPED_DUPLICATE).

## Acceptance criteria

-   A tender with attached files results in those files being downloaded and recorded.
-   Re-scanning the same tender does not re-download an unchanged attachment.
-   A corrupted or partial download is not marked COLLECTED.
-   Every collected document has a recorded checksum and source URL.
