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

Implemented - initial CRUD and validation

## Current implementation

Source Registry is implemented in `app/source_registry.py`, with typed
Pydantic models in `app/schemas.py` and FastAPI routes in `app/main.py`.

## Dependencies

Uses SQLAlchemy `Source` and `JobStatus` models from Module 03.

## Interfaces

Provides `GET /api/v1/sources`, `POST /api/v1/sources`,
`PATCH /api/v1/sources/{source_id}`, and
`GET /api/v1/sources/{source_id}/health`.

## Database interaction

Reads and writes `sources`. The health endpoint reads `job_status` scan
records and counts failed scan jobs.

## Security

Document security assumptions and untrusted inputs.

## Known limitations

-   No authentication or authorization layer exists yet; routes are intended
    for the local-only deployment.

## Current active task

Implement Module 02 Source Scanner against the approved source definitions.

## Exact next action

Add the first safe source adapter and persist scan job/source health results.

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

## Validation rules

- `source_id` and `organization` must be non-blank.
- `website` must be an HTTP or HTTPS URL.
- `scan_frequency` must be positive.
- Duplicate `source_id` values return HTTP 409.
- Missing sources return HTTP 404.

## Does not do
- It does not perform the actual web scan.
- It does not decide whether a tender is relevant.
