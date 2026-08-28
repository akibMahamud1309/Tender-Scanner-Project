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

- Modules 01–03 (Source Registry, Source Scanner, Database): documented,
  implementation in progress.
- Modules 04–14: documented (purpose, requirements, architecture, workflow),
  not yet implemented.

## Tech direction

Local-first: Python 3.12, FastAPI, PostgreSQL, Playwright (where needed),
local OCR, local document storage.