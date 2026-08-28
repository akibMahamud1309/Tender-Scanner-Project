# Architecture

## Components

- SQLAlchemy declarative base
- PostgreSQL engine/session factory
- ORM model definitions
- Table creation script

## Data flow

``` text
DATABASE_URL -> SQLAlchemy engine/session -> ORM models -> PostgreSQL tables
```

## Interfaces

- Reads `DATABASE_URL` from root `.env`.
- Exposes `Base`, `engine`, `SessionLocal`, and `get_db()` from
  `app/database.py`.
- Exposes ORM models from `app/models.py`.
- Provides `scripts/create_tables.py` for initial local schema creation.

## Security considerations

- Database credentials are not hardcoded in source code.
- `.env` remains git-ignored.
- `.env.example` contains placeholder credentials only.
- Source website and document content remain untrusted data in downstream
  tables.

## Dependencies

- Python 3.12
- SQLAlchemy
- psycopg2-binary
- python-dotenv
- PostgreSQL
