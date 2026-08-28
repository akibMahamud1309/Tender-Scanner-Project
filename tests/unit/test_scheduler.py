from datetime import datetime, timedelta, timezone
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.scheduler import SchedulerError, apply_backoff, check_due_jobs, trigger_job


def test_apply_backoff_is_exponential_and_capped() -> None:
    assert apply_backoff(2, base_seconds=10, max_seconds=30) == timedelta(seconds=30)


def test_check_due_jobs_skips_inactive_and_recent_sources() -> None:
    now = datetime.now(timezone.utc)
    recent = Mock(id=uuid4(), active=True, scan_frequency=timedelta(hours=1))
    inactive = Mock(id=uuid4(), active=False, scan_frequency=timedelta(hours=1))
    db = Mock()
    db.scalar.return_value = Mock(finished_at=now - timedelta(minutes=5), started_at=now - timedelta(minutes=6))
    assert check_due_jobs(db, [recent, inactive], now=now) == []


def test_trigger_job_rejects_existing_running_job() -> None:
    db = Mock()
    db.scalar.return_value = object()
    with pytest.raises(SchedulerError):
        trigger_job(db, job_type="SCAN", source_id=uuid4(), handler=lambda: None)


def test_trigger_job_records_success() -> None:
    db = Mock()
    db.scalar.return_value = None
    db.refresh.side_effect = lambda job: setattr(job, "id", uuid4())
    result = trigger_job(db, job_type="PROCESS", handler=lambda: None)
    assert result.status == "SUCCEEDED"
    assert db.commit.call_count == 2
