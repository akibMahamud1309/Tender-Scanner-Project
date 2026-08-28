# Workflow

## Normal workflow

1.  Load uncertain record and its extracted evidence.
2.  Call the AI classifier with the current prompt/model version.
3.  Persist the structured result with evidence references.

## Failure/retry workflow

-   An AI provider error or timeout is retried under Scheduler-controlled backoff before being flagged for manual review.
-   A response that fails to parse as the expected structured format is treated as a failure, not a silent NOT_RELEVANT.

## Manual-review workflow

Low-confidence or failed classifications are surfaced on the Dashboard for manual bid/no-bid style review.
