# Functions

  Function   Purpose   Status    File   Tests
  ---------- --------- --------- ------ -------
  handle_event   Receive, deduplicate, and record an event   Done    app/notifications.py    test_notifications.py
  check_duplicate   Check whether this event was already notified   Done    app/notifications.py    test_notifications.py
  deliver_notification   Invoke the configured delivery callback   Done    app/notifications.py    test_notifications.py
  record_notification_status   Persist unread/failed status   Done    app/notifications.py    test_notifications.py
