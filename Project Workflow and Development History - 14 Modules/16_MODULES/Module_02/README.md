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

Planned

## Current implementation

No application implementation has been established yet. Agents must
inspect the repository before updating this statement.

## Dependencies

See `compatibility.md`.

## Interfaces

See `architecture.md`.

## Database interaction

Document all tables, queries, migrations, or database events used by
this module.

## Security

Document security assumptions and untrusted inputs.

## Known limitations

-   Not yet implemented.

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
- Execute HTTP/browser collection for configured sources.
- Extract title, reference number, dates, URLs, and available document links.
- Handle timeouts, HTTP errors, parsing errors, and source health.
- Never bypass CAPTCHA/WAF/authentication/rate-limit controls.

## Does not do
- It does not perform final tender analysis.
- It does not bypass source security.
