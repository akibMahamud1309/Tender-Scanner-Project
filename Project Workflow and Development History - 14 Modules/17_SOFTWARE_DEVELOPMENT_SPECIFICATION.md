# 17 --- SOFTWARE DEVELOPMENT SPECIFICATION

This file is the concrete engineering specification for Tender Scanner.
Where `03_SYSTEM_ARCHITECTURE.md` and `16_MODULES/` describe *what* each
module does at a conceptual level, this file defines *exactly how* the
system is built: the database schema, the API contract, the testing
strategy, security/config handling, and how the system actually runs
day-to-day.

Any coding agent implementing a module should treat this file as
authoritative for schema/API shape. If an implementation requires a
change to something defined here, update this file in the same session
and record the change in `14_CHANGE_LOG.md`.

---

## 1. Data Model / Database Schema

Technology: PostgreSQL. ORM: SQLAlchemy. All tables use a surrogate
`id` primary key (`BIGSERIAL` or `UUID` --- UUID recommended for
`tenders` and `documents` since they may be referenced across modules
and eventually synced/exported).

### 1.1 `sources` (Module 01 --- Source Registry)

| Column        | Type         | Notes                                  |
|---------------|--------------|-----------------------------------------|
| id            | UUID PK      | |
| source_id     | TEXT UNIQUE  | Human-readable stable ID (e.g. "gov-procurement-01") |
| organization  | TEXT         | |
| website       | TEXT         | Base URL |
| config        | JSONB        | Scraper-specific config (selectors, auth, pagination rules) |
| scan_frequency| INTERVAL     | e.g. '1 day' |
| active        | BOOLEAN      | Default true |
| created_at    | TIMESTAMPTZ  | |
| updated_at    | TIMESTAMPTZ  | |

### 1.2 `tenders` (Module 04/05 write here via Module 03)

| Column          | Type        | Notes |
|-----------------|-------------|-------|
| id              | UUID PK     | |
| source_id       | UUID FK -> sources.id | |
| match_key       | TEXT        | Stable dedup key (Module 04) |
| title           | TEXT        | |
| reference_number| TEXT NULL   | |
| organization    | TEXT NULL   | Issuing org, if different from source |
| source_url      | TEXT        | Original listing URL |
| relevance_state | TEXT        | RELEVANT / NOT_RELEVANT / UNCERTAIN |
| current_version | INT         | Increments on each material change |
| metadata        | JSONB       | Current listing metadata such as deadline, scope, documents, and status |
| created_at      | TIMESTAMPTZ | |
| updated_at      | TIMESTAMPTZ | |

Unique constraint: `(source_id, match_key)`.

### 1.3 `tender_versions` (Module 04 --- change history, never destroyed)

| Column        | Type        | Notes |
|---------------|-------------|-------|
| id            | UUID PK     | |
| tender_id     | UUID FK -> tenders.id | |
| version_number| INT         | |
| field_diff    | JSONB       | `{"field": {"old": ..., "new": ...}}` |
| detected_at   | TIMESTAMPTZ | |

### 1.4 `documents` (Module 06/07/08)

| Column        | Type        | Notes |
|---------------|-------------|-------|
| id            | UUID PK     | |
| tender_id     | UUID FK -> tenders.id | |
| filename      | TEXT        | |
| source_url    | TEXT        | |
| checksum      | TEXT        | SHA-256 |
| size_bytes    | BIGINT      | |
| content_type  | TEXT        | |
| status        | TEXT        | COLLECTED / FAILED / SKIPPED_DUPLICATE |
| downloaded_at | TIMESTAMPTZ NULL | |

### 1.5 `document_pages` (Module 07/08 --- extracted or OCR'd text)

| Column              | Type        | Notes |
|---------------------|-------------|-------|
| id                  | UUID PK     | |
| document_id         | UUID FK -> documents.id | |
| page_number         | INT         | |
| extracted_text      | TEXT        | |
| extraction_method   | TEXT        | TEXT_EXTRACTION / OCR |
| extraction_quality  | NUMERIC     | 0.0-1.0 score |
| engine_version      | TEXT        | e.g. "pdfminer-2024" or "tesseract-5.3" |
| created_at          | TIMESTAMPTZ | |

### 1.6 `classifications` (Module 05 rules + Module 09 AI)

| Column          | Type        | Notes |
|-----------------|-------------|-------|
| id              | UUID PK     | |
| tender_id       | UUID FK -> tenders.id | |
| method          | TEXT        | RULE / AI |
| label           | TEXT        | RELEVANT / NOT_RELEVANT |
| confidence      | NUMERIC NULL| Null for deterministic rule matches |
| rule_id         | TEXT NULL   | Which rule fired (method=RULE) |
| model_version   | TEXT NULL   | Model/prompt version (method=AI) |
| evidence_ref    | JSONB NULL  | `{"document_id": ..., "page": ..., "snippet": ...}` |
| created_at      | TIMESTAMPTZ | |

### 1.7 `tender_analysis` (Module 10)

| Column        | Type        | Notes |
|---------------|-------------|-------|
| id            | UUID PK     | |
| tender_id     | UUID FK -> tenders.id | |
| field_name    | TEXT        | deadline / scope / eligibility / technical_requirements / restrictions / experience_required / documents_required |
| field_value   | TEXT NULL   | NULL + status=NOT_STATED if absent |
| status        | TEXT        | EXTRACTED / NOT_STATED / CONFLICTING |
| confidence    | NUMERIC NULL| |
| evidence_ref  | JSONB NULL  | |
| created_at    | TIMESTAMPTZ | |

### 1.8 `decisions` (Module 12)

| Column          | Type        | Notes |
|-----------------|-------------|-------|
| id              | UUID PK     | |
| tender_id       | UUID FK -> tenders.id | |
| decision        | TEXT        | BID / NO_BID |
| decline_reason  | TEXT NULL   | Required if decision=NO_BID |
| category        | TEXT NULL   | Required if decision=NO_BID |
| comment         | TEXT NULL   | |
| decided_at      | TIMESTAMPTZ | |

Decisions are append-only. A revised decision inserts a new row; the
latest row per `tender_id` (by `decided_at`) is the current decision.

### 1.9 `job_status` (Module 13 --- Scheduler)

| Column        | Type        | Notes |
|---------------|-------------|-------|
| id            | UUID PK     | |
| job_type      | TEXT        | SCAN / DOCUMENT_PROCESS / OCR / AI_CLASSIFY / AI_ANALYZE |
| source_id     | UUID NULL FK -> sources.id | |
| tender_id     | UUID NULL FK -> tenders.id | |
| status        | TEXT        | QUEUED / RUNNING / SUCCEEDED / FAILED / RETRYING |
| retry_count   | INT         | Default 0 |
| error_message | TEXT NULL   | |
| started_at    | TIMESTAMPTZ NULL | |
| finished_at   | TIMESTAMPTZ NULL | |

Partial unique index: only one `RUNNING` row per `(job_type, source_id)`
at a time --- this is the overlap guard.

### 1.10 `notifications` (Module 14)

| Column        | Type        | Notes |
|---------------|-------------|-------|
| id            | UUID PK     | |
| event_type    | TEXT        | NEW_RELEVANT_TENDER / DEADLINE_APPROACHING / SOURCE_FAILURE |
| tender_id     | UUID NULL FK -> tenders.id | |
| dedup_key     | TEXT        | Prevents duplicate sends for the same event |
| status        | TEXT        | SENT / FAILED |
| created_at    | TIMESTAMPTZ | |

Unique constraint: `dedup_key`.

---

## 2. API Contract

Framework: FastAPI. All endpoints under `/api/v1`. This is the surface
Module 11 (Dashboard) consumes; it also gives every other module a
stable, testable interface.

### Sources (Module 01)
- `GET /api/v1/sources` --- list all sources
- `POST /api/v1/sources` --- add a source
- `PATCH /api/v1/sources/{source_id}` --- update config/active flag
- `GET /api/v1/sources/{source_id}/health` --- last scan time, recent failures

### Tenders (Modules 03/04/05)
- `GET /api/v1/tenders` --- list, filterable by `relevance_state`, `source_id`, `deadline_before`
- `GET /api/v1/tenders/{tender_id}` --- full detail incl. current version
- `GET /api/v1/tenders/{tender_id}/versions` --- change history

### Documents (Modules 06/07/08)
- `GET /api/v1/tenders/{tender_id}/documents` --- list with status
- `GET /api/v1/documents/{document_id}/pages` --- extracted text per page

### Classification & Analysis (Modules 09/10)
- `GET /api/v1/tenders/{tender_id}/classifications`
- `GET /api/v1/tenders/{tender_id}/analysis`

### Decisions (Module 12)
- `GET /api/v1/tenders/{tender_id}/decisions`
- `POST /api/v1/tenders/{tender_id}/decisions` --- body: `{decision, decline_reason?, category?, comment?}`; server validates decline_reason/category required when decision=NO_BID

### Jobs (Module 13)
- `GET /api/v1/jobs?status=RUNNING|FAILED` --- for Dashboard source-health view
- `POST /api/v1/jobs/{job_type}/trigger` --- manual trigger (admin use)

### Notifications (Module 14)
- `GET /api/v1/notifications?status=FAILED` --- for troubleshooting

All list endpoints support `?limit=&offset=` pagination. All responses
use Pydantic models defined in `app/schemas/`. Errors return
`{"error": "message", "code": "MACHINE_READABLE_CODE"}` with an
appropriate HTTP status (400/404/409/500).

---

## 3. Testing Strategy

Framework: `pytest`, with `pytest-asyncio` for FastAPI async routes and
a dedicated test PostgreSQL database (`tender_scanner_test`) reset
between test runs.

- **Unit tests** (per module, in `tests/unit/test_module_XX.py`): test
  pure functions in isolation --- e.g. `generate_match_key`,
  `evaluate_relevance`, `build_field_diff` --- with mocked inputs, no DB.
- **Integration tests** (`tests/integration/`): test a module against
  a real test database --- e.g. Module 04 correctly classifies
  NEW/UNCHANGED/CHANGED against seeded `tenders` rows.
- **Pipeline tests** (`tests/pipeline/`): run a small fixture "fake
  source" through Modules 01→02→04→03→05 end-to-end and assert the
  final DB state.
- **Fixtures**: sample HTML pages for 2-3 real approved sources, sample
  PDFs (one clean text PDF, one scanned/image PDF) checked into
  `tests/fixtures/` for Module 06/07/08 tests.
- Every new function added to a module's `functions.md` table must have
  a corresponding test before its status moves from `Planned` to
  `Implemented`.
- Target: meaningful coverage of business logic (match-key generation,
  relevance rules, diffing, decision validation), not 100% line coverage
  for its own sake.

---

## 4. Security & Configuration Management

- All secrets (DB password, AI provider API key) live in a `.env` file
  at the project root, loaded via `python-dotenv`. **`.env` must be in
  `.gitignore` and never committed.** Commit a `.env.example` with keys
  but placeholder values instead.
- Database credentials are never hardcoded in source files.
- All content from source websites and downloaded documents is treated
  as untrusted: no `eval`, no automatic execution of downloaded files,
  file type validated by content inspection (not extension) before
  processing.
- AI classification/analysis prompts must be structured so that text
  extracted from tender documents cannot be interpreted as instructions
  to the model (prompt-injection resistance) --- evidence text is passed
  as clearly delimited data, not concatenated into the instruction itself.
- Rate limiting per source in Module 02/06 to avoid overloading or
  getting blocked by source websites.
- pgAdmin/Postgres superuser account is for local admin only; the
  application connects with a separate, least-privilege database role
  once the schema is stable.

---

## 5. Deployment & Operations

- **Environment**: local Windows PC, Python 3.12 virtual environment,
  local PostgreSQL instance. No cloud dependency required for core
  operation.
- **Scheduling**: Module 13 runs as a long-lived local process (e.g.
  `apscheduler` inside the FastAPI app, or a separate worker process)
  rather than relying solely on Windows Task Scheduler, so retry/backoff
  and overlap-guard logic in the spec above can run in-process.
- **Running the app**: `uvicorn app.main:app --reload` for development;
  a Windows service or scheduled startup task for persistent local
  operation.
- **Backups**: nightly `pg_dump` of `tender_scanner` to a local backups
  folder (outside the repo), retained on a rolling window (e.g. 14 days).
- **Monitoring**: the Dashboard's source-health view (Module 11, backed
  by `job_status`) is the primary day-to-day monitoring surface; no
  external monitoring service required at this stage.
- **Logging**: structured logs (module name, job id, level) written to a
  local log file per run, rotated to avoid unbounded growth.

---

## 6. Change Control

Any change to the schema (Section 1) or API contract (Section 2) must:
1. Be reflected in this file first.
2. Be recorded in `14_CHANGE_LOG.md` and, if it reflects a deliberate
   trade-off, in `13_DECISION_LOG.md`.
3. Update the affected module's `README.md` (Interfaces/Database
   interaction sections) and `functions.md`.
