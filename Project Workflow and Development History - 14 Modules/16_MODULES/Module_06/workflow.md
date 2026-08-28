# Workflow

## Normal workflow

1.  Read relevant tender's source page.
2.  Discover attachment links.
3.  Download each new/changed attachment.
4.  Validate and record metadata.

## Failure/retry workflow

-   A failed download is retried under Scheduler-controlled backoff before being marked FAILED.
-   A source that blocks or rejects downloads is logged as a source-health issue, not silently ignored.

## Manual-review workflow

Tenders where no attachments could be discovered despite an expected document set are flagged for manual review.
