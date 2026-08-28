from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Notification, Tender


class NotificationError(Exception):
    """Raised for invalid notification operations."""


@dataclass(frozen=True)
class NotificationEvent:
    event_type: str
    dedup_key: str
    message: str
    tender_id: UUID | None = None


def check_duplicate(db: Session, dedup_key: str) -> bool:
    return db.scalar(select(Notification.id).where(Notification.dedup_key == dedup_key)) is not None


def handle_event(
    db: Session,
    event: NotificationEvent,
    *,
    deliver_notification: Callable[[str], None] | None = None,
) -> Notification:
    if not event.event_type.strip() or not event.dedup_key.strip() or not event.message.strip():
        raise NotificationError("event_type, dedup_key, and message are required.")
    if event.tender_id is not None and db.get(Tender, event.tender_id) is None:
        raise NotificationError(f"Tender '{event.tender_id}' was not found.")
    existing = db.scalar(select(Notification).where(Notification.dedup_key == event.dedup_key))
    if existing is not None:
        return existing
    notification = Notification(
        event_type=event.event_type,
        tender_id=event.tender_id,
        dedup_key=event.dedup_key,
        status="UNREAD",
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    if deliver_notification is not None:
        try:
            deliver_notification(event.message)
        except Exception as exc:
            notification.status = "FAILED"
            db.commit()
            raise NotificationError("Notification delivery failed.") from exc
    return notification


def get_notifications(db: Session, *, unread_only: bool = False) -> list[Notification]:
    query = select(Notification).order_by(Notification.created_at.desc(), Notification.id.desc())
    if unread_only:
        query = query.where(Notification.status == "UNREAD")
    return list(db.scalars(query).all())


def mark_notification_read(db: Session, notification_id: UUID) -> Notification:
    notification = db.get(Notification, notification_id)
    if notification is None:
        raise NotificationError(f"Notification '{notification_id}' was not found.")
    notification.status = "READ"
    db.commit()
    db.refresh(notification)
    return notification
