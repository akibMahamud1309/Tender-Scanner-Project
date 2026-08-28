from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import JobStatus, Source
from app.schemas import SourceCreate, SourceHealth, SourceUpdate


class SourceRegistryError(Exception):
    """Base exception for source registry operations."""


class SourceNotFoundError(SourceRegistryError):
    pass


class DuplicateSourceError(SourceRegistryError):
    pass


def list_sources(db: Session, *, limit: int = 100, offset: int = 0) -> Sequence[Source]:
    return db.scalars(
        select(Source).order_by(Source.source_id).limit(limit).offset(offset)
    ).all()


def get_source(db: Session, source_id: str) -> Source:
    source = db.scalar(select(Source).where(Source.source_id == source_id))
    if source is None:
        raise SourceNotFoundError(f"Source '{source_id}' was not found.")
    return source


def create_source(db: Session, payload: SourceCreate) -> Source:
    source = Source(
        source_id=payload.source_id,
        organization=payload.organization,
        website=str(payload.website),
        config=payload.config,
        scan_frequency=payload.scan_frequency,
        active=payload.active,
    )
    db.add(source)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateSourceError(
            f"Source '{payload.source_id}' already exists."
        ) from exc
    db.refresh(source)
    return source


def update_source(db: Session, source_id: str, payload: SourceUpdate) -> Source:
    source = get_source(db, source_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "website" and value is not None:
            value = str(value)
        setattr(source, field, value)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateSourceError(f"Source '{source_id}' could not be updated.") from exc
    db.refresh(source)
    return source


def get_source_health(db: Session, source_id: str) -> SourceHealth:
    source = get_source(db, source_id)
    latest = db.execute(
        select(JobStatus.started_at, JobStatus.finished_at)
        .where(JobStatus.source_id == source.id, JobStatus.job_type == "SCAN")
        .order_by(JobStatus.started_at.desc())
        .limit(1)
    ).one_or_none()
    failures = db.scalar(
        select(func.count())
        .select_from(JobStatus)
        .where(
            JobStatus.source_id == source.id,
            JobStatus.job_type == "SCAN",
            JobStatus.status == "FAILED",
        )
    )
    return SourceHealth(
        source_id=source.source_id,
        last_scan_started_at=latest.started_at if latest else None,
        last_scan_finished_at=latest.finished_at if latest else None,
        recent_failures=failures or 0,
    )
