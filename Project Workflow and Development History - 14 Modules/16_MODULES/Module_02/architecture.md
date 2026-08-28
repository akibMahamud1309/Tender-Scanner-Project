# Architecture

## Components

- HTTP(S) fetcher using the Python standard library
- HTML link parser and URL normalizer
- Scan result and job-status persistence
- FastAPI manual scan trigger

## Data flow

``` text
Source config → bounded HTTP request → HTML listings → normalized scan result
```

## Interfaces

- `POST /api/v1/sources/{source_id}/scan`
- `parse_listings(html, base_url)`
- `fetch_source(source)`
- `scan_source(db, source)`

## Security considerations

- Only HTTP(S) listing URLs are accepted.
- Timeout, item-count, and request-delay limits prevent unbounded work.
- HTTP 401/403/429 responses are surfaced as blocked-source failures.
- The scanner never attempts to bypass source controls.

## Dependencies

- Python standard library
- SQLAlchemy
- FastAPI
- PostgreSQL
