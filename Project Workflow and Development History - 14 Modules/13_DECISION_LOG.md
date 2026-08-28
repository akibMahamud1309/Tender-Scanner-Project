# 13 --- DECISION LOG

## Approved decisions

1.  Local-first architecture.
2.  PostgreSQL as primary database.
3.  Start only with the supplied approved source list.
4.  Never bypass website security controls.
5.  Build incrementally and validate early modules before advanced
    intelligence.

Major changes require a documented reason, alternatives, impact,
migration plan, and status.

## 2026-08-28 - Migration history reconciliation

- Decision: reconcile an existing database with Alembic using `stamp` only
  after schema comparison, then apply pending migrations.
- Reason: the local database already contained the initial tables, but had no
  `alembic_version` marker. Re-running the initial migration would fail with
  duplicate-table errors.
- Impact: existing tables and data were preserved; the pending
  `tenders.metadata` migration was applied.
- Status: complete; database verified at revision `20260828_0002`.
