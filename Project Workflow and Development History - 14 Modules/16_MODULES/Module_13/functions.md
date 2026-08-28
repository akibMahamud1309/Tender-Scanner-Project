# Functions

  Function   Purpose   Status    File   Tests
  ---------- --------- --------- ------ -------
  check_due_jobs   Determine which source scans are due   Done    app/scheduler.py    test_scheduler.py
  trigger_job   Start a job if no overlap exists   Done    app/scheduler.py    test_scheduler.py
  apply_backoff   Compute exponential retry delay   Done    app/scheduler.py    test_scheduler.py
  record_job_status   Persist job lifecycle status   Done    app/scheduler.py    test_scheduler.py
