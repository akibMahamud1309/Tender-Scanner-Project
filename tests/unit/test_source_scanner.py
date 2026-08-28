from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.source_scanner import ScannerError, SourceBlockedError, fetch_source, parse_listings, scan_source


def test_parse_listings_normalizes_absolute_urls_and_deduplicates() -> None:
    html = '<a href="/one"> First tender </a><a href="/one">Duplicate</a><a href="https://example.gov/two">Second</a>'
    listings = parse_listings(html, "https://example.gov/list")
    assert [(item.title, item.source_url) for item in listings] == [
        ("First tender", "https://example.gov/one"),
        ("Second", "https://example.gov/two"),
    ]


def test_parse_listings_limits_results() -> None:
    assert len(parse_listings('<a href="/1">One</a><a href="/2">Two</a>', "https://example.gov", max_items=1)) == 1


def test_fetch_source_rejects_non_html() -> None:
    response = Mock()
    response.headers.get_content_type.return_value = "application/pdf"
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=None)
    opener = Mock(return_value=response)
    source = SimpleNamespace(website="https://example.gov", config={})
    with pytest.raises(ScannerError, match="text/html"):
        fetch_source(source, opener=opener)


def test_scan_source_records_successful_job() -> None:
    response = Mock()
    response.headers.get_content_type.return_value = "text/html"
    response.headers.get_content_charset.return_value = "utf-8"
    response.read.return_value = b'<a href="/notice">Notice</a>'
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=None)
    db = Mock()
    db.refresh.side_effect = lambda job: setattr(job, "id", uuid4())
    source = SimpleNamespace(id=uuid4(), source_id="gov-01", website="https://example.gov", config={})
    result = scan_source(db, source, opener=Mock(return_value=response))
    assert result.listings[0].title == "Notice"
    assert db.commit.call_count == 2


def test_scan_source_marks_failed_job() -> None:
    db = Mock()
    db.refresh.side_effect = lambda job: setattr(job, "id", uuid4())
    source = SimpleNamespace(id=uuid4(), source_id="gov-01", website="https://example.gov", config={"timeout_seconds": 0})
    with pytest.raises(ScannerError):
        scan_source(db, source, opener=Mock())
    job = db.add.call_args.args[0]
    assert job.status == "FAILED"
    assert db.commit.call_count == 2
