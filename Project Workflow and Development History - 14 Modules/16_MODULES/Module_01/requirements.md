# Requirements

## Functional requirements

- Create approved source records.
- List sources with pagination.
- Update source configuration and active state.
- Report source scan health.
- Reject invalid URLs, blank text, and non-positive scan intervals.

## Non-functional requirements

- Preserve unique stable source IDs.
- Surface duplicate and missing-source errors explicitly.

## Inputs

- `SourceCreate` and `SourceUpdate` Pydantic payloads.

## Outputs

- `SourceRead` and `SourceHealth` response models.

## Acceptance criteria

- All Module 01 unit tests pass.
- API routes use the `/api/v1` contract.
