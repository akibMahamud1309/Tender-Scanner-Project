from __future__ import annotations

from html.parser import HTMLParser
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from uuid import UUID
from collections.abc import Iterable

from sqlalchemy.orm import Session

from app.models import JobStatus, Source


class ScannerError(Exception):
    """Base exception for safe source scanning failures."""


class SourceBlockedError(ScannerError):
    """Raised when a source explicitly blocks automated access."""


@dataclass(frozen=True)
class ScanListing:
    title: str
    source_url: str
    reference_number: str | None = None
    metadata: dict[str, Any] | None = None


@dataclass(frozen=True)
class ScanResult:
    source_id: str
    listings: tuple[ScanListing, ...]
    job_id: UUID


class _ListingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.listings: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            attributes = dict(attrs)
            href = attributes.get("href")
            if href:
                self._href = href
                self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href is not None:
            title = " ".join("".join(self._text).split())
            if title:
                self.listings.append((title, self._href))
            self._href = None
            self._text = []


def _get_scan_url(source: Source) -> str:
    configured_url = source.config.get("listing_url", source.website)
    if not isinstance(configured_url, str) or not configured_url.startswith(("http://", "https://")):
        raise ScannerError("Source listing_url must be an HTTP or HTTPS URL.")
    return configured_url


def parse_listings(html: str, base_url: str, *, max_items: int = 100) -> tuple[ScanListing, ...]:
    parser = _ListingParser()
    parser.feed(html)
    listings: list[ScanListing] = []
    seen_urls: set[str] = set()
    for title, href in parser.listings:
        absolute_url = urljoin(base_url, href)
        if absolute_url in seen_urls:
            continue
        seen_urls.add(absolute_url)
        listings.append(ScanListing(title=title, source_url=absolute_url))
        if len(listings) >= max_items:
            break
    return tuple(listings)


def fetch_source(source: Source, *, opener: Any = urlopen) -> tuple[ScanListing, ...]:
    url = _get_scan_url(source)
    config = source.config
    timeout = float(config.get("timeout_seconds", 30))
    if timeout <= 0 or timeout > 120:
        raise ScannerError("timeout_seconds must be greater than 0 and at most 120.")
    request = Request(
        url,
        headers={"User-Agent": str(config.get("user_agent", "TenderScanner/0.1"))},
    )
    try:
        with opener(request, timeout=timeout) as response:
            content_type = response.headers.get_content_type()
            if content_type != "text/html":
                raise ScannerError(f"Expected text/html response, got {content_type}.")
            html = response.read().decode(response.headers.get_content_charset() or "utf-8", errors="replace")
    except HTTPError as exc:
        if exc.code in {401, 403, 429}:
            raise SourceBlockedError(f"Source denied automated access with HTTP {exc.code}.") from exc
        raise ScannerError(f"Source returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise ScannerError(f"Source request failed: {exc.reason}.") from exc
    max_items = int(config.get("max_items", 100))
    if max_items <= 0 or max_items > 1000:
        raise ScannerError("max_items must be between 1 and 1000.")
    return parse_listings(html, url, max_items=max_items)


def scan_source(db: Session, source: Source, *, opener: Any = urlopen) -> ScanResult:
    job = JobStatus(job_type="SCAN", source_id=source.id, status="RUNNING", started_at=datetime.now(timezone.utc))
    db.add(job)
    db.commit()
    db.refresh(job)
    try:
        delay = float(source.config.get("request_delay_seconds", 0))
        if delay < 0 or delay > 60:
            raise ScannerError("request_delay_seconds must be between 0 and 60.")
        if delay:
            time.sleep(delay)
        listings = fetch_source(source, opener=opener)
        job.status = "SUCCEEDED"
        job.finished_at = datetime.now(timezone.utc)
        db.commit()
        return ScanResult(source_id=source.source_id, listings=listings, job_id=job.id)
    except (ScannerError, OSError, TypeError, ValueError, UnicodeError) as exc:
        job.status = "FAILED"
        job.error_message = str(exc)
        job.finished_at = datetime.now(timezone.utc)
        db.commit()
        if isinstance(exc, ScannerError):
            raise
        raise ScannerError("Source scan failed.") from exc


def scan_active_sources(db: Session, sources: Iterable[Source]) -> list[ScanResult]:
    return [scan_source(db, source) for source in sources if source.active]
