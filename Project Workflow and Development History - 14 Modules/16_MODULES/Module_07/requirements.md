# Requirements

## Functional requirements

-   Accept collected documents from Module 06.
-   Extract text and structural metadata (page count, sections where detectable) from supported formats.
-   Score extraction quality (e.g., proportion of pages yielding usable text).
-   Normalize extracted text (encoding, whitespace, page markers) into a consistent format for AI consumption.
-   Route documents below the extraction-quality threshold to Module 08 (OCR).

## Non-functional requirements

-   Must clearly distinguish 'no text extracted' from 'extraction not yet attempted'.
-   Normalization must not lose page/document traceability needed to cite evidence later.
-   Should support the range of formats actually returned by approved sources (PDF, DOCX, and similar).

## Inputs

-   Collected document files and metadata from Module 06.

## Outputs

-   Extracted, normalized text per document.
-   Extraction-quality score per document.
-   Documents routed to OCR when quality is insufficient.

## Acceptance criteria

-   A machine-readable PDF yields extracted text without requiring OCR.
-   A scanned/image-only PDF is correctly routed to OCR rather than treated as empty.
-   Extracted text retains a mapping back to page numbers for traceability.
