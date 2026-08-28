# Workflow

## Normal workflow

1. Load database settings from `.env`.
2. Import `app.models` so all ORM models register with `Base.metadata`.
3. Open sessions through `SessionLocal` / `get_db()`.
4. Persist and query pipeline records through the ORM models.

## Failure/retry workflow

1. Missing `DATABASE_URL` raises a startup/runtime error immediately.
2. Database connection failures surface through SQLAlchemy and should be
   recorded by the calling module/job.
3. Schema changes should move to Alembic before production-style
   migrations.

## Manual-review workflow

Not applicable for this module directly; manual review happens in
pipeline/dashboard modules using records stored by this module.
