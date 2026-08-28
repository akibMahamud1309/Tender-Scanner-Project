# Workflow

## Normal workflow

1.  Receive a decision action from the Dashboard.
2.  Validate required fields for the decision type.
3.  Persist as a new, timestamped history entry.

## Failure/retry workflow

-   A decision missing required fields (e.g., no-bid without reason) is rejected back to the Dashboard with a clear validation message rather than partially saved.

## Manual-review workflow

Not applicable; this module records human decisions rather than generating ones requiring review.
