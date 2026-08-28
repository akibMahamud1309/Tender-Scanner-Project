# Workflow

## Normal workflow

1.  Load current keyword/rule set.
2.  Evaluate each new/changed record against the rule set.
3.  Persist RELEVANT / NOT_RELEVANT / UNCERTAIN with triggering rule(s).

## Failure/retry workflow

-   If the rule set fails to load, halt filtering for the batch and alert rather than defaulting all records to RELEVANT or NOT_RELEVANT.
-   Malformed record fields are marked UNCERTAIN, not skipped.

## Manual-review workflow

Records the rule engine cannot confidently classify, and that AI classification (Module 09) also leaves uncertain, are surfaced on the Dashboard for manual review.
