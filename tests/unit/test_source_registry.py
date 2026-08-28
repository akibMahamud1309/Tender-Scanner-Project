from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.schemas import SourceCreate, SourceUpdate
from app.source_registry import (
    SourceNotFoundError,
    create_source,
    get_source,
    update_source,
)


def source_payload() -> SourceCreate:
    return SourceCreate(
        source_id="gov-01",
        organization="Public Procurement",
        website="https://example.gov",
        scan_frequency=timedelta(days=1),
    )


def test_source_create_validates_url_and_positive_frequency() -> None:
    with pytest.raises(ValidationError):
        SourceCreate(
            source_id="gov-01",
            organization="Public Procurement",
            website="not-a-url",
            scan_frequency=timedelta(0),
        )


def test_source_update_rejects_blank_organization() -> None:
    with pytest.raises(ValidationError):
        SourceUpdate(organization="  ")


def test_create_source_persists_normalized_payload() -> None:
    db = Mock()
    db.refresh.side_effect = lambda source: setattr(source, "id", uuid4())
    source = create_source(db, source_payload())
    assert source.source_id == "gov-01"
    assert source.website == "https://example.gov/"
    db.commit.assert_called_once()


def test_get_source_raises_for_missing_source() -> None:
    db = Mock()
    db.scalar.return_value = None
    with pytest.raises(SourceNotFoundError):
        get_source(db, "missing")


def test_update_source_only_changes_supplied_fields() -> None:
    existing = SimpleNamespace(
        source_id="gov-01",
        organization="Old",
        website="https://old.example",
        active=True,
    )
    db = Mock()
    db.scalar.return_value = existing
    db.refresh.side_effect = lambda source: None
    updated = update_source(db, "gov-01", SourceUpdate(active=False))
    assert updated.organization == "Old"
    assert updated.active is False
    db.commit.assert_called_once()
