from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Callable
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.models import JobStatus, Source
from app.source_scanner import ScanResult, scan_source


class SchedulerError(Exception):
    """Raised when a scheduled job cannot be safely started."""


@dataclass(frozen=True)
class ScheduledJob:
    job_id: UUID
    job_type: str
    source_id: UUID | None
    status: str
    retry_count: int


def apply_backoff(retry_count: int, *, base_seconds: int = 60, max_seconds: int = 3600) -> timedelta:
    if retry_count < 0 or base_seconds <= 0 or max_seconds <= 0:
        raise SchedulerError("Backoff parameters must be positive.")
    return timedelta(seconds=min(max_seconds, base_seconds * (2 ** retry_count)))


def _latest_job(db: Session, source_id: UUID, job_type: str) -> JobStatus | None:
    return db.scalar(
        select(JobStatus)
        .where(JobStatus.source_id == source_id, JobStatus.job_type == job_type)
        .order_by(JobStatus.finished_at.desc().nullslast(), JobStatus.started_at.desc().nullslast())
        .limit(1)
    )


def check_due_jobs(db: Session, sources: list[Source], *, now: datetime | None = None) -> list[Source]:
    current = now or datetime.now(timezone.utc)
    due: list[Source] = []
    for source in sources:
        if not source.active:
            continue
        latest = _latest_job(db, source.id, "SCAN")
        if latest is None or latest.finished_at is None or latest.finished_at + source.scan_frequency <= current:
            due.append(source)
    return due


def trigger_job(
    db: Session,
    *,
    job_type: str,
    source_id: UUID | None = None,
    tender_id: UUID | None = None,
    handler: Callable[[], object],
) -> ScheduledJob:
    running = db.scalar(
        select(JobStatus).where(
            JobStatus.job_type == job_type,
            JobStatus.source_id == source_id,
            JobStatus.tender_id == tender_id,
            JobStatus.status == "RUNNING",
        ).limit(1)
    )
    if running is not None:
        raise SchedulerError(f"{job_type} is already running for the requested target.")
    job = JobStatus(
        job_type=job_type,
        source_id=source_id,
        tender_id=tender_id,
        status="RUNNING",
        started_at=datetime.now(timezone.utc),
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    try:
        handler()
    except Exception as exc:
        job.status = "FAILED"
        job.error_message = str(exc)
        job.finished_at = datetime.now(timezone.utc)
        db.commit()
        raise
    job.status = "SUCCEEDED"
    job.finished_at = datetime.now(timezone.utc)
    db.commit()
    return ScheduledJob(job.id, job.job_type, job.source_id, job.status, job.retry_count)


def record_job_status(
    db: Session,
    job_id: UUID,
    *,
    status: str,
    error_message: str | None = None,
    retry_count: int | None = None,
) -> JobStatus:
    if status not in {"QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "RETRYING"}:
        raise SchedulerError("Invalid job status.")
    job = db.get(JobStatus, job_id)
    if job is None:
        raise SchedulerError(f"Job '{job_id}' was not found.")
    job.status = status
    job.error_message = error_message
    if retry_count is not None:
        job.retry_count = retry_count
    if status in {"SUCCEEDED", "FAILED"}:
        job.finished_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(job)
    return job


def run_due_scans(db: Session, sources: list[Source]) -> list[ScanResult]:
    results: list[ScanResult] = []
    for source in check_due_jobs(db, sources):
        try:
            result = scan_source(db, source)
        except Exception:
            continue
        results.append(result)
    return results
