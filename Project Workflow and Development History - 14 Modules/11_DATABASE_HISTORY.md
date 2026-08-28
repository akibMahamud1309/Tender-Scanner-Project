# 11 --- DATABASE HISTORY

PostgreSQL is the primary database direction. Track schema entities,
migrations, indexes, constraints, compatibility, tests, and rollback
plans. Initial planned entities include sources, organizations, tenders,
documents, requirements, eligibility, categories, decisions, processing
history, source health, and AI analysis.

## 2026-08-28 18:50

- Implemented initial SQLAlchemy database layer in `app/database.py`.
- Implemented ORM models in `app/models.py` for `sources`, `tenders`,
  `tender_versions`, `documents`, `document_pages`, `classifications`,
  `tender_analysis`, `decisions`, `job_status`, and `notifications`.
- Added `scripts/create_tables.py` to create registered tables using
  `Base.metadata.create_all()`.
- Created/verified all 10 tables in the local PostgreSQL
  `tender_scanner` database.
- Alembic migrations are not configured yet; next database step is
  focused tests and migration setup before further schema evolution.

## 2026-08-28 21:25

- Added Alembic environment configuration and baseline revision
  `20260828_0001_initial_schema`.
- Added focused metadata, constraint, foreign-key, model-registration, and
  session-factory tests; all five pass.
- Fresh databases can use `alembic upgrade head`. Existing databases created
  by `create_all()` should be stamped at the baseline revision before future
  migrations are applied.
