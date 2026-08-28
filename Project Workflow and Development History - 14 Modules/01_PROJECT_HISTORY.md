# 01 --- PROJECT HISTORY

This is the permanent multi-agent project memory. Every session must
record agent, date, system version, active module, task, completed work,
files changed, tests, errors, active file/function, what was about to be
done, and the exact next action.

## Initial state

System version: 0.1.0. Application implementation is not yet
established. The next implementation milestone is Module 01 Source
Registry followed by Module 02 Source Scanner and Module 03 Database.

## Agent rule

A new agent must be able to continue without access to the previous
conversation. Never leave a vague handoff.

## 2026-08-28 - Module 06

- Implemented safe attachment discovery, bounded HTTP(S) downloads, content
  signature validation, SHA-256 deduplication, and document status persistence.
- Added `/api/v1/tenders/{tender_id}/documents` and five focused tests.
- Next action: implement Module 07 Document Processor.

## 2026-08-28 - Module 08 OCR

- Added GPT-5.6 Terra OpenAI-compatible OCR adapter, strict page-aware output
  validation, normalization, persistence, failure status, and API route.
- Next action: implement Module 07 Document Processor integration with OCR.

## 2026-08-28 - Module 09 AI Classification

- Added versioned Terra classification prompts, structured output validation,
  evidence verification, persistence, manual-review flagging, and API route.
- Next action: implement Module 10 AI Tender Analysis.

## 2026-08-28 - Module 10 AI Tender Analysis

- Added Terra structured field extraction, multi-document consolidation,
  exact evidence validation, `NOT_STATED` handling, persistence, and API route.
- Next action: implement Module 11 Dashboard.

## 2026-08-28 - Module 11 Dashboard

- Added React/Vite dashboard with tender metrics, search, relevance filters,
  responsive list/detail views, and FastAPI tender list endpoint with CORS.
- Decision actions remain pending Module 12; next action is Module 12.

## 2026-08-28 - Module 12 Decision History

- Added validated append-only bid/no-bid decisions, chronological history API,
  and React dashboard decision actions.
- Next action: implement Module 13 Scheduler.

## 2026-08-28 - Module 13 Scheduler

- Added due-source detection, overlap prevention, retry backoff, lifecycle
  persistence, and scheduler API visibility.
- Next action: implement Module 14 Notifications.

## 2026-08-28 - Module 14 Notifications

- Added deduplicated durable notification events, delivery failure handling,
  unread/read APIs, dashboard unread metrics, tests, and documentation.
- All 14 planned modules now have initial implementations; next action is
  integration hardening and end-to-end validation.

## 2026-08-28 - Database migration reconciliation

- Verified the local PostgreSQL server accepts connections on port 5432.
- Confirmed the existing database contained all expected application tables.
- Compared the live schema with the ORM models and found only the
  `tenders.metadata` column missing.
- Safely stamped the existing initial schema at Alembic revision
  `20260828_0001`, then applied revision `20260828_0002`.
- Verified the database is now at revision `20260828_0002` with no missing
  expected tables or columns.
- Exact next action: use the API documentation at
  `http://127.0.0.1:8000/docs` to create an approved source and trigger its
  scan.

## 2026-08-28 17:05 (Session 2)

- Set up local development environment: Python 3.12.10 installed via `py install manager` (alongside 3.13.5, 3.14.7), venv created in project root.
- Installed core packages: fastapi, uvicorn, sqlalchemy, psycopg2-binary, python-dotenv.
- Installed PostgreSQL 17 locally, created `tender_scanner` database via pgAdmin.
- Connected project to GitHub: https://github.com/akibMahamud1309/Tender-Scanner-Project (main branch).
- Added root README.md with agent onboarding instructions.
- Added 17_SOFTWARE_DEVELOPMENT_SPECIFICATION.md: concrete schema (10 tables), API contract, testing strategy, security/config rules, deployment/ops notes.
- Created .env at project root with DATABASE_URL (Postgres connection string, password URL-encoded). Verified it loads correctly via python-dotenv. Confirmed .env is excluded from git via .gitignore; only .env.example is committed.

Exact next action: write SQLAlchemy models for Module 03 matching schema in 17_SOFTWARE_DEVELOPMENT_SPECIFICATION.md Section 1, then create the tables in tender_scanner.

## 2026-08-28 18:50 (Session 3)

- Implemented Module 03 initial database layer.
- Added `app/database.py` with `.env` loading, SQLAlchemy engine,
  declarative `Base`, session factory, and `get_db()` helper.
- Added `app/models.py` with ORM models for the 10 tables specified in
  `17_SOFTWARE_DEVELOPMENT_SPECIFICATION.md` Section 1.
- Added `scripts/create_tables.py` and ran it successfully against the
  configured local PostgreSQL `tender_scanner` database.
- Verified PostgreSQL contains: `sources`, `tenders`,
  `tender_versions`, `documents`, `document_pages`, `classifications`,
  `tender_analysis`, `decisions`, `job_status`, and `notifications`.
- Updated `.env.example` so committed config uses placeholder
  credentials only.
- Updated `.gitignore` to ignore Python `__pycache__/` directories.
- Tests run: `python -m compileall app scripts`; metadata import check
  confirmed 10 registered tables; SQLAlchemy inspector confirmed 10
  tables exist in PostgreSQL.

Exact next action: add focused database tests for model metadata,
constraints, and session creation, then decide whether to add Alembic
migrations before implementing Module 01/02 write paths.

## 2026-08-28 21:25 (Session 4)

- Added pinned runtime and development dependency manifests:
  `requirements.txt` and `requirements-dev.txt`.
- Added Alembic configuration, environment integration with root
  `DATABASE_URL`, and baseline revision
  `alembic/versions/20260828_0001_initial_schema.py` for the 10-table schema.
- Added five focused database unit tests in
  `tests/unit/test_database.py`.
- Validation: `python -m pytest tests\\unit\\test_database.py -q` passed
  (5 tests); Python compileall passed; `alembic heads` reports
  `20260828_0001` as the head.
- No root `.env` is present in this worktree; migration commands require
  `DATABASE_URL` to be supplied through `.env` or the process environment.

Exact next action: implement Module 01 Source Registry CRUD and validation.

## 2026-08-28 21:30 (Session 5)

- Implemented Module 01 Source Registry schemas, CRUD service, validation,
  FastAPI routes, and scan-health lookup.
- Added `app/schemas.py`, `app/source_registry.py`, `app/main.py`, and
  `tests/unit/test_source_registry.py`.
- Validation: full available test suite passed (10 tests); Python compileall
  passed.
- Updated Module 01 documentation and version to 0.1.1.

Exact next action: implement Module 02 Source Scanner with one safe source
adapter and persisted scan job/source health results.

## 2026-08-28 21:34 (Session 6)

- Implemented Module 02 safe HTTP source scanning in
  `app/source_scanner.py`.
- Added HTML link parsing, URL normalization, in-scan deduplication,
  bounded timeout/item/delay configuration, blocked-source handling, and
  persisted `SCAN` job status.
- Added `POST /api/v1/sources/{source_id}/scan` and five scanner tests.
- Validation: full available test suite passes (15 tests); compileall and
  FastAPI route smoke test pass.
- Updated Module 02 documentation and version to 0.1.1.

Exact next action: add an approved source configuration and connect scan
listings to Module 04 deduplication.

## 2026-08-28 21:35 (Session 7)

- Implemented Module 04 in `app/deduplication.py` with URL normalization,
  deterministic match keys, NEW/UNCHANGED/CHANGED classification, field
  diffs, and append-only tender version persistence.
- Added JSONB current listing metadata and Alembic revision
  `20260828_0002_tender_metadata` for deadline/scope/documents/status data.
- Added `POST /api/v1/sources/{source_id}/deduplicate`, input schema, and
  seven focused tests.
- Validation: full available test suite passes (22 tests); compileall,
  migration-chain validation, and git diff checks pass.
- Updated Module 04 and specification documentation.

Exact next action: implement Module 05 deterministic IT/software relevance
filtering.

## 2026-08-28 21:40 (Session 8)

- Implemented Module 05 deterministic relevance filtering in
  `app/relevance_filter.py`.
- Added configurable include, exclude, and uncertain keyword rules,
  explicit malformed-rule errors, confidence/evidence output, and persisted
  `classifications` rows.
- Added `POST /api/v1/tenders/{tender_id}/relevance` and six focused tests.
- Validation: full available test suite passes (28 tests); compileall,
  route smoke test, and diff checks pass.
- Updated Module 05 documentation and version to 0.1.1.

Exact next action: implement Module 06 Document Collector.
