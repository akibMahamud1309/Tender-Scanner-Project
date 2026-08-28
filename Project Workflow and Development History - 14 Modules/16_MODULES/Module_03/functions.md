# Functions

  Function   Purpose   Status    File   Tests
  ---------- --------- --------- ------ -------
  Base   Declarative base for ORM models   Implemented   app/database.py   Pending
  engine   SQLAlchemy engine using DATABASE_URL   Implemented   app/database.py   Pending
  SessionLocal   Session factory for database access   Implemented   app/database.py   Pending
  get_db   Yield/close database sessions for app dependencies   Implemented   app/database.py   Pending
  Source   ORM model for approved tender sources   Implemented   app/models.py   Pending
  Tender   ORM model for current tender records   Implemented   app/models.py   Pending
  TenderVersion   ORM model for append-only tender change history   Implemented   app/models.py   Pending
  Document   ORM model for collected document metadata   Implemented   app/models.py   Pending
  DocumentPage   ORM model for extracted/OCR page text   Implemented   app/models.py   Pending
  Classification   ORM model for rule/AI relevance classifications   Implemented   app/models.py   Pending
  TenderAnalysis   ORM model for structured extracted tender fields   Implemented   app/models.py   Pending
  Decision   ORM model for append-only bid/no-bid decisions   Implemented   app/models.py   Pending
  JobStatus   ORM model for scheduler/job state   Implemented   app/models.py   Pending
  Notification   ORM model for notification delivery tracking   Implemented   app/models.py   Pending
  main   Create all registered tables in the configured database   Implemented   scripts/create_tables.py   Manual
