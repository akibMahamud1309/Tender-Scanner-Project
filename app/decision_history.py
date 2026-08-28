from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Decision, Tender


class DecisionError(Exception):
    """Raised for invalid or unavailable decision operations."""


@dataclass(frozen=True)
class DecisionInput:
    decision: str
    decline_reason: str | None = None
    category: str | None = None
    comment: str | None = None


def validate_decision(payload: DecisionInput) -> DecisionInput:
    if payload.decision not in {"BID", "NO_BID"}:
        raise DecisionError("decision must be BID or NO_BID.")
    if payload.decision == "NO_BID" and (not payload.decline_reason or not payload.category):
        raise DecisionError("NO_BID requires decline_reason and category.")
    return payload


def record_decision(db: Session, tender_id: UUID, payload: DecisionInput) -> Decision:
    validate_decision(payload)
    if db.get(Tender, tender_id) is None:
        raise DecisionError(f"Tender '{tender_id}' was not found.")
    decision = Decision(tender_id=tender_id, decision=payload.decision, decline_reason=payload.decline_reason, category=payload.category, comment=payload.comment)
    db.add(decision)
    db.commit()
    db.refresh(decision)
    return decision


def get_decision_history(db: Session, tender_id: UUID) -> list[Decision]:
    if db.get(Tender, tender_id) is None:
        raise DecisionError(f"Tender '{tender_id}' was not found.")
    return list(db.scalars(select(Decision).where(Decision.tender_id == tender_id).order_by(Decision.decided_at.asc(), Decision.id.asc())).all())
