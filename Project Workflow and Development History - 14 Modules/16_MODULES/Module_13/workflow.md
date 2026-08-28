# Workflow

## Normal workflow

1.  Check schedule for due jobs.
2.  Trigger the job if no overlapping instance is running.
3.  Record status on completion or failure.

## Failure/retry workflow

-   A job that fails is retried per backoff policy up to a configured limit, then marked FAILED and surfaced on the Dashboard.
-   A crash mid-job is detected on restart and the stale 'running' status is corrected, not left stuck.

## Manual-review workflow

Jobs that exhaust retries are surfaced on the Dashboard as source-health issues for manual attention.
