# Workflow

## Normal workflow

1.  Receive a low-quality document/page.
2.  Run OCR on the affected pages.
3.  Normalize and record output with engine/version metadata.

## Failure/retry workflow

-   An OCR engine crash or timeout on a page is recorded as OCR_FAILED for that page, not skipped silently.
-   Repeated OCR failures on a document are escalated rather than retried indefinitely.

## Manual-review workflow

Documents where OCR still yields unusable text are flagged for manual review.
