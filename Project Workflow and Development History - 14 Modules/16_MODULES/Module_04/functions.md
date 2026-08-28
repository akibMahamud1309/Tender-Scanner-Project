# Functions

  Function   Purpose   Status    File   Tests
  ---------- --------- --------- ------ -------
  normalize_url       Normalize an HTTP(S) listing URL       Implemented  app/deduplication.py  test_deduplication.py
  generate_match_key  Build a stable identifier             Implemented  app/deduplication.py  test_deduplication.py
  classify_change     Determine NEW / UNCHANGED / CHANGED   Implemented  app/deduplication.py  test_deduplication.py
  build_field_diff    Produce a field-level diff            Implemented  app/deduplication.py  test_deduplication.py
  persist_listing     Persist tender and version history   Implemented  app/deduplication.py  test_deduplication.py
