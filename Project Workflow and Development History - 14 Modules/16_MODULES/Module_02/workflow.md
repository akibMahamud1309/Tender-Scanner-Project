# Workflow

## Normal workflow

1. Load an active source and validate its listing configuration.
2. Fetch the HTML page within bounded limits.
3. Parse normalized, deduplicated listing links and persist job success.

## Failure/retry workflow

1. Mark the scan job `FAILED` with an error message.
2. Surface blocked access and invalid responses without retry bypasses.
3. Let the scheduler decide future retry timing.

## Manual-review workflow

Blocked or repeatedly failing sources remain available for operator review;
the scanner does not attempt alternate access methods automatically.
