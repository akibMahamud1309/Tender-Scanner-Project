# Module 01 --- Source Registry

## Purpose

Owns the approved list of tender/notice sources and source-specific
configuration.

## Role in the system

``` text
Previous module
      ↓
Source Registry
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
- Maintain source ID, organization, URLs, source type, scanning method, active state, and notes.
- Define source-specific parser/adapter configuration.
- Provide the scanner with approved source definitions.
- Track source configuration changes.

## Does not do
- It does not perform the actual web scan.
- It does not decide whether a tender is relevant.
