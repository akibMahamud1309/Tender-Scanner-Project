from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.deduplication import (
    MatchKeyError,
    build_field_diff,
    classify_change,
    generate_match_key,
    normalize_url,
    persist_listing,
)
from app.source_scanner import ScanListing


def test_normalize_url_removes_fragment_and_default_port() -> None:
    assert normalize_url("HTTPS://Example.gov:443/notices?id=2#page") == "https://example.gov/notices?id=2"


def test_generate_match_key_prefers_reference_number() -> None:
    listing = ScanListing("Tender", "https://example.gov/a", " REF-22 ")
    assert generate_match_key(" GOV-01 ", listing) == "gov-01:reference:ref-22"


def test_generate_match_key_falls_back_to_url_and_title_hash() -> None:
    listing = ScanListing("Tender", "https://example.gov/a")
    assert generate_match_key("gov-01", listing).startswith("gov-01:url-title:https://example.gov/a:")


def test_generate_match_key_rejects_missing_title() -> None:
    with pytest.raises(MatchKeyError):
        generate_match_key("gov-01", ScanListing(" ", "https://example.gov/a"))


def test_build_field_diff_is_deterministic() -> None:
    assert build_field_diff({"scope": "old", "deadline": "today"}, {"scope": "new", "deadline": "today"}) == {
        "scope": {"old": "old", "new": "new"}
    }


def test_classify_change_detects_metadata_change() -> None:
    existing = SimpleNamespace(title="Tender", reference_number=None, source_url="https://example.gov/a", listing_metadata={"scope": "old"})
    assert classify_change(existing, {"title": "Tender", "reference_number": None, "source_url": "https://example.gov/a", "metadata": {"scope": "new"}}) == "CHANGED"


def test_persist_listing_creates_new_tender() -> None:
    db = Mock()
    db.scalar.return_value = None
    db.refresh.side_effect = lambda tender: setattr(tender, "id", uuid4())
    source = SimpleNamespace(id=uuid4(), source_id="gov-01")
    result = persist_listing(db, source, ScanListing("Tender", "https://example.gov/a", metadata={"status": "open"}))
    assert result.state == "NEW"
    assert result.tender.listing_metadata == {"status": "open"}
    db.commit.assert_called_once()
