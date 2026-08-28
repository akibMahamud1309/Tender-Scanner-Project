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
- `alembic/` provides the migration environment and initial schema revision.
- `tests/unit/test_database.py` verifies registered tables, constraints,
  foreign keys, model registration, and session creation.

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

- The initial Alembic revision is a baseline for fresh databases; an existing
  database created with `create_all()` must be stamped at that revision before
  applying future migrations.
- No repository/data-access helper functions beyond session creation.

## Current active task

Initial schema tests and Alembic migration setup are complete. The next
active task is to implement Module 01 Source Registry.

## Exact next action

Implement Module 01 Source Registry CRUD and validation against the stable
database models and migration workflow.

## Agent continuation rule

Before changing this module, read the module files and the top-level
project history/decision/compatibility files. Before ending a session,
update the module history and the top-level history with the exact work
completed and next action.

## Database direction

PostgreSQL is the approved primary database direction.
