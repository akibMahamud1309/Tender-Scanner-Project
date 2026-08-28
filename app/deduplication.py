from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Source, Tender, TenderVersion
from app.source_scanner import ScanListing


class DeduplicationError(Exception):
    """Base exception for deduplication failures."""


class MatchKeyError(DeduplicationError):
    """Raised when a stable match key cannot be generated."""


class DuplicateMatchError(DeduplicationError):
    """Raised when persistence detects a conflicting match key."""


@dataclass(frozen=True)
class DeduplicationResult:
    state: str
    tender: Tender
    field_diff: dict[str, dict[str, Any]]


def normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    if parts.scheme.lower() not in {"http", "https"} or not parts.netloc:
        raise MatchKeyError("Listing URL must be an absolute HTTP or HTTPS URL.")
    hostname = (parts.hostname or "").lower()
    port = parts.port
    netloc = hostname
    if port and not ((parts.scheme.lower() == "http" and port == 80) or (parts.scheme.lower() == "https" and port == 443)):
        netloc = f"{hostname}:{port}"
    query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))
    path = parts.path or "/"
    return urlunsplit((parts.scheme.lower(), netloc, path, query, ""))


def generate_match_key(source_id: str, listing: ScanListing) -> str:
    source = source_id.strip().lower()
    if not source:
        raise MatchKeyError("Source ID is required to generate a match key.")
    if listing.reference_number and listing.reference_number.strip():
        reference = " ".join(listing.reference_number.split()).casefold()
        return f"{source}:reference:{reference}"
    if not listing.title.strip():
        raise MatchKeyError("Listing title is required when reference number is absent.")
    normalized_url = normalize_url(listing.source_url)
    title_hash = hashlib.sha256(" ".join(listing.title.split()).casefold().encode()).hexdigest()
    return f"{source}:url-title:{normalized_url}:{title_hash}"


def _snapshot(listing: ScanListing) -> dict[str, Any]:
    metadata = listing.metadata or {}
    json.dumps(metadata, sort_keys=True)
    return {
        "title": " ".join(listing.title.split()),
        "reference_number": listing.reference_number.strip() if listing.reference_number else None,
        "source_url": normalize_url(listing.source_url),
        "metadata": metadata,
    }


def build_field_diff(old: dict[str, Any], new: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        field: {"old": old.get(field), "new": new.get(field)}
        for field in sorted(set(old) | set(new))
        if old.get(field) != new.get(field)
    }


def classify_change(existing: Tender | None, incoming: dict[str, Any]) -> str:
    if existing is None:
        return "NEW"
    current = {
        "title": existing.title,
        "reference_number": existing.reference_number,
        "source_url": normalize_url(existing.source_url),
        "metadata": existing.listing_metadata or {},
    }
    return "UNCHANGED" if not build_field_diff(current, incoming) else "CHANGED"


def persist_listing(db: Session, source: Source, listing: ScanListing) -> DeduplicationResult:
    match_key = generate_match_key(source.source_id, listing)
    incoming = _snapshot(listing)
    existing = db.scalar(
        select(Tender).where(Tender.source_id == source.id, Tender.match_key == match_key)
    )
    state = classify_change(existing, incoming)
    if existing is None:
        tender = Tender(
            source_id=source.id,
            match_key=match_key,
            title=incoming["title"],
            reference_number=incoming["reference_number"],
            organization=None,
            source_url=incoming["source_url"],
            relevance_state="UNCERTAIN",
            listing_metadata=incoming["metadata"],
        )
        db.add(tender)
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise DuplicateMatchError(f"Match key '{match_key}' already exists.") from exc
        db.refresh(tender)
        return DeduplicationResult(state=state, tender=tender, field_diff={})
    field_diff = build_field_diff(
        {
            "title": existing.title,
            "reference_number": existing.reference_number,
            "source_url": normalize_url(existing.source_url),
            "metadata": existing.listing_metadata or {},
        },
        incoming,
    )
    if field_diff:
        next_version = existing.current_version + 1
        for field in ("title", "reference_number", "source_url"):
            if field in incoming:
                setattr(existing, field, incoming[field])
        if "metadata" in incoming:
            existing.listing_metadata = incoming["metadata"]
        existing.current_version = next_version
        db.add(TenderVersion(tender_id=existing.id, version_number=next_version, field_diff=field_diff))
        db.commit()
        db.refresh(existing)
    return DeduplicationResult(state=state, tender=existing, field_diff=field_diff)
