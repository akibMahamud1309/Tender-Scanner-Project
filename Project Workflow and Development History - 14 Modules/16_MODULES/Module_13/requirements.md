# Requirements

## Functional requirements

-   Trigger Module 02 (Source Scanner) scans on a configured schedule per source.
-   Trigger downstream processing jobs (Modules 04-10) as new/changed data becomes available.
-   Apply retry/backoff policy to failed jobs across modules rather than each module implementing its own.
-   Prevent a job from starting if an equivalent job for the same source/tender is already running.
-   Record job status (queued, running, succeeded, failed, retrying) for visibility on the Dashboard.

## Non-functional requirements

-   Scheduling must be resilient to the local process restarting (no permanently stuck 'running' jobs after a crash).
-   Backoff policy must avoid hammering a source that is failing.
-   Job status must be queryable in near-real-time for the Dashboard's source-health view.

## Inputs

-   Source configuration (scan frequency) from Module 01.
-   Job completion/failure signals from all pipeline modules.

## Outputs

-   Triggered job executions across the pipeline.
-   Job status records for Dashboard source-health view.

## Acceptance criteria

-   A source scans on its configured schedule without manual intervention.
-   A failed job retries according to the configured backoff policy and eventually surfaces as a failure if retries are exhausted.
-   No two overlapping jobs run for the same source at the same time.
