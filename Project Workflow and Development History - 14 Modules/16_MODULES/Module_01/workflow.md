# Workflow

## Normal workflow

1. Validate source payload with Pydantic.
2. Persist or update the `sources` row through the registry service.
3. Return the source or explicit validation/conflict/not-found error.

## Failure/retry workflow

1. Roll back the transaction on database integrity errors.
2. Return HTTP 409 for duplicate/conflicting source data.
3. Return HTTP 404 when the stable source ID does not exist.

## Manual-review workflow

Source configuration is reviewed by the operator before activation.
