from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.notifications import NotificationError, NotificationEvent, handle_event


def test_handle_event_deduplicates_by_key() -> None:
    db = Mock()
    db.get.return_value = object()
    db.scalar.side_effect = [None, None]
    db.refresh.side_effect = lambda notification: setattr(notification, "id", uuid4())
    first = handle_event(db, NotificationEvent("NEW_TENDER", "tender:1", "New tender"), deliver_notification=Mock())
    assert first.status == "UNREAD"
    assert db.add.call_count == 1


def test_handle_event_returns_existing_notification() -> None:
    existing = object()
    db = Mock()
    db.scalar.return_value = existing
    assert handle_event(db, NotificationEvent("NEW_TENDER", "same", "New tender")) is existing
    db.add.assert_not_called()


def test_delivery_failure_is_explicit() -> None:
    db = Mock()
    db.scalar.return_value = None
    db.get.return_value = object()
    db.refresh.side_effect = lambda notification: setattr(notification, "id", uuid4())
    with pytest.raises(NotificationError):
        handle_event(db, NotificationEvent("FAILURE", "job:1", "Job failed"), deliver_notification=Mock(side_effect=RuntimeError()))
