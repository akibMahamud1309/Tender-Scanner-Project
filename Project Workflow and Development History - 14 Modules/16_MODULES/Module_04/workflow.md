# Workflow

## Normal workflow

1. Receive a batch of normalized records from a scan.
2. Generate a match key for each record.
3. Look up each match key in the Database.
4. Classify NEW / UNCHANGED / CHANGED and persist accordingly.

## Failure/retry workflow

-   If the Database lookup fails, retry the batch under Scheduler-controlled backoff.
-   If a match key cannot be generated (missing identifiers), route the record to manual review instead of guessing.

## Manual-review workflow

Records with ambiguous or colliding match keys are held for manual review rather than auto-merged or auto-split.
