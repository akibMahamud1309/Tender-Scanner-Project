# Workflow

## Normal workflow

1.  Receive an event.
2.  Check dedup tracker for prior notification on this event.
3.  Deliver notification and record status.

## Failure/retry workflow

-   A failed delivery is retried a limited number of times, then recorded as failed without blocking pipeline processing.

## Manual-review workflow

Not applicable; failures are recorded for review but do not block other modules.
