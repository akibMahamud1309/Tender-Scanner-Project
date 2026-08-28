# Workflow

## Normal workflow

1.  Read relevant tender metadata and discover attachment URLs.
2.  Download each new/changed attachment with bounded response size.
3.  Validate content signatures and calculate SHA-256.
4.  Record `COLLECTED`, `FAILED`, or `SKIPPED_DUPLICATE`.

## Failure/retry workflow

-   A failed download is retried under Scheduler-controlled backoff before being marked FAILED.
-   A source that blocks or rejects downloads is logged as a source-health issue, not silently ignored.

## Manual-review workflow

Tenders where no attachments could be discovered despite an expected document set are flagged for manual review.
