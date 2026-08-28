# Module 13 --- Scheduler

## Purpose

Controls automated scan jobs, processing jobs, retry timing, and scheduled maintenance.

## Role in the system

``` text
(cross-cutting, operates across the pipeline)
      ↓
Scheduler
      ↓
(cross-cutting, operates across the pipeline)
```

## Responsibilities

-   Schedule source scans.
-   Schedule document processing.
-   Control retries and backoff.
-   Prevent overlapping duplicate jobs.
-   Record job status and failures.

## Current status

Implemented (0.1.1)

## Current implementation

The scheduler checks due source scans, prevents equivalent running jobs,
records lifecycle statuses, and provides exponential retry backoff helpers.

## Dependencies

See `compatibility.md`.

## Interfaces

See `architecture.md`.

## Database interaction

Document all tables, queries, migrations, or database events used by
this module.

## Security

-   Scheduler only triggers internally defined jobs; it does not execute arbitrary external commands based on source content.

## Known limitations

-   The current implementation is an in-process orchestration layer; an
    external daemon/worker is not included.

## Current active task

None.

## Exact next action

Follow `09_MODULE_VERSION_HISTORY.md` and the latest project-history
handoff to determine the next implementation task.

## Agent continuation rule

Before changing this module, read the module files and the top-level
project history/decision/compatibility files. Before ending a session,
update the module history and the top-level history with the exact work
completed and next action.

## Expected responsibilities
-   Schedule source scans.
-   Schedule document processing.
-   Control retries and backoff.
-   Prevent overlapping duplicate jobs.
-   Record job status and failures.
