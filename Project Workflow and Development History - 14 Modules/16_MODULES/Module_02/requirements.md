# Requirements

## Functional requirements

- Fetch configured HTTP(S) listing pages.
- Extract and normalize tender links and titles.
- Deduplicate links within a scan.
- Persist scan job state and failures.
- Surface blocked, invalid, timeout, and non-HTML responses.

## Non-functional requirements

- Respect source security controls.
- Bound timeout, delay, and result count.
- Avoid executing downloaded HTML or source-provided configuration.

## Inputs

- Active Module 01 `Source` records and JSON configuration.

## Outputs

- `ScanResult` containing normalized `ScanListing` records.
- `JobStatus` persistence for source health.

## Acceptance criteria

- Scanner unit tests pass.
- Successful and failed scans record explicit job states.
- No request bypasses authentication, CAPTCHA, WAF, or rate limits.
