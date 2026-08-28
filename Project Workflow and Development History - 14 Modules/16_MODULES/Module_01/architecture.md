# Architecture

## Components

- Pydantic source request/response schemas
- SQLAlchemy-backed source registry service
- FastAPI `/api/v1/sources` routes

## Data flow

``` text
HTTP request → Pydantic validation → Source ORM service → PostgreSQL
```

## Interfaces

- `GET /api/v1/sources`
- `POST /api/v1/sources`
- `PATCH /api/v1/sources/{source_id}`
- `GET /api/v1/sources/{source_id}/health`

## Security considerations

- URLs and configuration are validated as data and are never executed.
- The application remains local-only until authentication is implemented.

## Dependencies

- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
