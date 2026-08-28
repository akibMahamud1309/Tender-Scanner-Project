# Module 02 --- Source Scanner

## Purpose

Connects to configured sources and collects tender/notice listings and
metadata.

## Role in the system

``` text
Previous module
      ↓
Source Scanner
      ↓
Next module
```

## Responsibilities

-   Implement only responsibilities belonging to this module.
-   Provide documented inputs and outputs.
-   Report errors without silently hiding them.
-   Maintain its own version and compatibility records.
-   Keep interfaces stable unless an API/architecture change is
    documented.

## Current status

Implemented - initial safe HTTP scanner

## Current implementation

The scanner is implemented in `app/source_scanner.py`. It fetches configured
HTML listing pages, normalizes links, deduplicates URLs, and records scan
jobs in `job_status`.

## Dependencies

Uses Module 01 source definitions and Module 03 `Source` / `JobStatus` models.

## Interfaces

Provides `POST /api/v1/sources/{source_id}/scan` plus reusable
`fetch_source`, `parse_listings`, and `scan_source` functions.

## Database interaction

Creates `SCAN` rows in `job_status`, marking them `RUNNING`, `SUCCEEDED`, or
`FAILED` with timestamps and error messages.

## Security

Uses explicit HTTP(S) URLs, bounded timeout/item/delay settings, a descriptive
user agent, and does not bypass authentication, CAPTCHA, WAF, or rate limits.

## Known limitations

-   The initial parser supports generic HTML links; source-specific selectors
    and browser automation will be added only when an approved source requires
    them.

## Current active task

Implement source-specific listing adapters only where the approved source
configuration requires them.

## Exact next action

Add the first approved source configuration and connect scan listings to
Module 04 deduplication.

## Agent continuation rule

Before changing this module, read the module files and the top-level
project history/decision/compatibility files. Before ending a session,
update the module history and the top-level history with the exact work
completed and next action.

## Expected responsibilities
- Execute HTTP/browser collection for configured sources.
- Extract title, reference number, dates, URLs, and available document links.
- Handle timeouts, HTTP errors, parsing errors, and source health.
- Never bypass CAPTCHA/WAF/authentication/rate-limit controls.

## Does not do
- It does not perform final tender analysis.
- It does not bypass source security.
