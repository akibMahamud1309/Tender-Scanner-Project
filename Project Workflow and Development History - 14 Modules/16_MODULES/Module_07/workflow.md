# Workflow

## Normal workflow

1.  Load a collected document.
2.  Attempt text extraction.
3.  Score extraction quality.
4.  Normalize and persist, or route to OCR.

## Failure/retry workflow

-   An unsupported or corrupted file format is flagged for manual review rather than silently skipped.
-   Extraction timeouts are retried once before flagging failure.

## Manual-review workflow

Documents that fail extraction even after OCR are surfaced for manual review.
