# Architecture

## Components

-   Job queue/trigger
-   Retry/backoff controller
-   Overlap guard
-   Job status recorder

## Data flow

``` text
Schedule config -> Trigger job -> Execute (Scanner/Processor/etc.) -> Success or Failure -> Retry per backoff policy or record final status
```

## Interfaces

-   Reads: schedule configuration from Module 01.
-   Triggers: Modules 02, 04-10 as applicable.
-   Writes: job status to Module 03, visible via Module 11.

## Security considerations

-   Scheduler only triggers internally defined jobs; it does not execute arbitrary external commands based on source content.

## Dependencies

-   Module 01 for schedule configuration.
-   All pipeline modules as job targets.
-   Module 03 for job status persistence.
