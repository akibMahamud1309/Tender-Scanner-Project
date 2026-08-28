# Tender Scanner Project

Automates daily tender/opportunity discovery: monitors approved sources,
detects new and changed tenders, filters for software/IT relevance,
collects and processes documents, classifies and analyzes them with AI,
and presents everything on a local dashboard for bid/no-bid decisions.

## For any coding agent or new collaborator

Start here, in order:

1. **`Project Workflow and Development History - 14 Modules/01_PROJECT_HISTORY.md`**
   — overall development history and current state.
2. **`03_SYSTEM_ARCHITECTURE.md`** and **`04_SYSTEM_WORKFLOW.md`** — how the
   14 modules fit together and the end-to-end pipeline.
3. **`16_MODULES/README.md`** — index of all 14 modules and what each one does.
4. Each module's own folder (`16_MODULES/Module_XX/`) has its own README,
   requirements, architecture, workflow, functions, version, compatibility,
   and error-history files.

## Rule for every agent/session

Before ending a session: update the relevant module's `README.md`
("Current status", "Current active task", "Exact next action") and the
top-level `14_CHANGE_LOG.md` / `13_DECISION_LOG.md` with exactly what was
done and what should happen next. This documentation folder is the
project's persistent memory across sessions and across different coding
agents.

## Build status

- Modules 01–14 have initial implementations, tests, and documentation.
- Backend validation currently passes 58 tests.
- The React/Vite dashboard builds successfully.
- PostgreSQL is running locally and the database is aligned with Alembic
  revision `20260828_0002`.

## Tech direction

Local-first: Python 3.12, FastAPI, PostgreSQL, Playwright (where needed),
local OCR, local document storage.

## Database development

Install runtime and development dependencies with
`python -m pip install -r requirements-dev.txt`. Set `DATABASE_URL` in the
root `.env` file, then run `alembic upgrade head` to apply migrations and
`python -m pytest tests -q` to run the tests.

If the database was created before Alembic tracking was enabled, compare the
existing schema first. When it matches the initial migration, run
`alembic stamp 20260828_0001` followed by `alembic upgrade head`. Never drop
existing tables merely to resolve a migration-history mismatch.

## Dashboard development

Run the FastAPI backend on port 8000, then start the React dashboard:

```text
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

### Start the FastAPI backend

From the project root:

```text
python -m uvicorn app.main:app --reload --port 8000
```

Open `http://127.0.0.1:8000/docs` for the API controls. To scan an approved
source, create it with `POST /api/v1/sources`, then trigger
`POST /api/v1/sources/{source_id}/scan`.

## AI provider switching

Set `AI_PROVIDER` to `terra`, `openai` (or `chatgpt`), or `gemini` in `.env`.
Configure only the matching provider credentials and endpoint. OCR,
classification, and tender analysis use the selected provider without code
changes.