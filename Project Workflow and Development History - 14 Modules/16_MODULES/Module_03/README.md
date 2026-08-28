# Module 03 --- Database

## Purpose

Provides the PostgreSQL persistence layer and data-access model for the
application.

## Role in the system

``` text
Source Registry / Source Scanner / Pipeline modules
      ->
Database
      ->
API / Dashboard / downstream modules
```

## Responsibilities

- Implement only responsibilities belonging to this module.
- Provide documented inputs and outputs.
- Report errors without silently hiding them.
- Maintain its own version and compatibility records.
- Keep interfaces stable unless an API/architecture change is documented.
- Define ORM/data-access layer.
- Manage PostgreSQL schema creation and future migrations.
- Persist sources, tenders, documents, analysis, decisions, and history.
- Enforce appropriate keys, constraints, and indexes.

## Current status

Implemented - initial schema

## Current implementation

Initial SQLAlchemy persistence layer is implemented:

- `app/database.py` loads `DATABASE_URL`, creates the SQLAlchemy engine,
  defines `Base`, and provides `SessionLocal` / `get_db()`.
- `app/models.py` defines the 10 PostgreSQL tables from
  `17_SOFTWARE_DEVELOPMENT_SPECIFICATION.md` Section 1.
- `scripts/create_tables.py` imports the models and runs
  `Base.metadata.create_all()` against the configured local database.

## Dependencies

See `compatibility.md`.

## Interfaces

See `architecture.md`.

## Database interaction

Implemented ORM tables:

- `sources`
- `tenders`
- `tender_versions`
- `documents`
- `document_pages`
- `classifications`
- `tender_analysis`
- `decisions`
- `job_status`
- `notifications`

Tables were created/verified in the local `tender_scanner` PostgreSQL
database on 2026-08-28.

## Security

Secrets are loaded from the root `.env` file via `python-dotenv`.
`.env` remains ignored by git. `.env.example` contains placeholder
credentials only.

## Known limitations

- No Alembic migration setup yet; current table creation uses SQLAlchemy
  `create_all()`.
- No repository/data-access helper functions beyond session creation.
- No tests have been added yet.

## Current active task

Initial schema implementation complete. Next active task is to add tests
and decide whether to introduce Alembic before further schema changes.

## Exact next action

Add focused database tests that verify model metadata, required
constraints, and session creation. Then choose Alembic migration setup
before building Module 01/02 write paths against these models.

## Agent continuation rule

Before changing this module, read the module files and the top-level
project history/decision/compatibility files. Before ending a session,
update the module history and the top-level history with the exact work
completed and next action.

## Database direction

PostgreSQL is the approved primary database direction.
