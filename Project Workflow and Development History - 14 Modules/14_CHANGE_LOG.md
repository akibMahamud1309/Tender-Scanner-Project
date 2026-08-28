# 14 --- CHANGE LOG

## 2026-08-28 - Module 06 Document Collector

- Added attachment discovery, safe document download and validation.
- Added checksum-based duplicate avoidance and document status persistence.
- Added document collection API and unit coverage.

## 2026-08-28 - Module 08 OCR

- Added configurable GPT-5.6 Terra OCR integration and page-level persistence.
- Added strict response validation, explicit failure status, API route, and tests.

## 2026-08-28 - Module 09 AI Classification

- Added GPT-5.6 Terra classification adapter with validated labels,
  confidence, page evidence, and model/prompt traceability.
- Added persistence, manual-review handling, API route, and tests.

## 2026-08-28 - Module 10 AI Tender Analysis

- Added GPT-5.6 Terra tender field analysis with stable structured output,
  evidence traceability, persistence, API integration, and tests.

## 2026-08-28 - Module 11 Dashboard

- Added React/Vite frontend dashboard and responsive tender review views.
- Added search/filter interactions, source links, API proxy, CORS, and tender list endpoint.

## 2026-08-28 - Module 12 Decision History

- Added decision validation, append-only persistence, history retrieval, API
  endpoints, dashboard actions, tests, and documentation.

## 2026-08-28 18:50

- Implemented Module 03 initial database schema code:
  `app/database.py`, `app/models.py`, and `scripts/create_tables.py`.
- Created/verified the 10-table PostgreSQL schema specified in
  `17_SOFTWARE_DEVELOPMENT_SPECIFICATION.md` Section 1.
- Updated `.env.example` to use placeholder credentials only.
- Updated `.gitignore` to ignore Python `__pycache__/` directories.
- Updated Module 03 README, architecture, workflow, functions,
  compatibility, and version docs.

## 2026-08-28 21:25

- Added pinned `requirements.txt` and `requirements-dev.txt`.
- Added Alembic configuration and the initial 10-table schema migration.
- Added focused Module 03 database tests; all five tests pass.
- Updated root and Module 03 documentation with migration/test commands and
  the next implementation task.

## 2026-08-28 21:30

- Implemented Module 01 Source Registry CRUD, validation, API routes, and
  source scan-health lookup.
- Added source schemas and five focused unit tests; full available suite
  passes with 10 tests.
- Updated Module 01 documentation and version history.

## 2026-08-28 21:34

- Implemented Module 02 safe HTTP source scanner, HTML listing parser,
  bounded request handling, and scan job persistence.
- Added source scan trigger route and five scanner unit tests; full suite
  passes with 15 tests.
- Updated Module 02 documentation and version history.

## 2026-08-28 21:35

- Implemented Module 04 deduplication and change detection.
- Added deterministic match keys, field diffs, tender version history, and
  current JSONB listing metadata.
- Added batch deduplication API and seven tests; full suite passes with
  22 tests.
- Updated Module 04 documentation and the authoritative specification.

## 2026-08-28 21:40

- Implemented Module 05 deterministic IT/software relevance filtering.
- Added source-configured rules, traceable classifications, relevance API
  endpoint, and six tests; full suite passes with 28 tests.
- Updated Module 05 documentation and version history.

## 2026-08-28

- Populated real (non-template) documentation for Modules 04-14:
  README.md, requirements.md, architecture.md, workflow.md, and
  functions.md now contain module-specific purpose, responsibilities,
  data flow, interfaces, security notes, and function stubs derived
  from 03_SYSTEM_ARCHITECTURE.md and 04_SYSTEM_WORKFLOW.md.
- version.md, compatibility.md, and error_history.md for Modules
  04-14 remain on the standard template, since there is no real
  version/dependency/error history until implementation begins.
- Modules 01-03 were already substantively documented and were not
  changed in this pass.

## 0.1.0 --- Initial project documentation

## 2026-08-28 - Module 13 Scheduler

- Added in-process scheduler helpers for due scans, overlap prevention,
  exponential backoff, lifecycle status recording, tests, and API visibility.

## 2026-08-28 - Module 14 Notifications

- Added notification event deduplication, durable statuses, delivery failure
  handling, unread/read APIs, dashboard metrics, tests, and documentation.

Created the complete 14-module documentation framework and multi-agent
continuation rules. Application implementation has not yet started.

## 2026-08-28 17:05

- Added 17_SOFTWARE_DEVELOPMENT_SPECIFICATION.md (schema, API contract, testing, security, ops)
- Added root README.md
- Environment setup: Python 3.12.10, PostgreSQL 17, venv, core packages installed
- Connected repo to GitHub
- Added .env / .env.example, verified DATABASE_URL loads correctly
