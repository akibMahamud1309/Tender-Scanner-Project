from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Document, Tender


class DocumentCollectorError(Exception):
    """Base exception for document collection failures."""


@dataclass(frozen=True)
class DocumentCandidate:
    filename: str
    source_url: str


@dataclass(frozen=True)
class CollectedDocument:
    document_id: UUID
    filename: str
    source_url: str
    checksum: str
    status: str


def discover_attachments(tender: Tender) -> tuple[DocumentCandidate, ...]:
    metadata = tender.listing_metadata or {}
    raw_urls = metadata.get("document_urls", [])
    if not isinstance(raw_urls, list) or not all(isinstance(url, str) for url in raw_urls):
        raise DocumentCollectorError("document_urls must be a list of strings.")
    candidates: list[DocumentCandidate] = []
    seen: set[str] = set()
    for raw_url in raw_urls:
        url = urljoin(tender.source_url, raw_url)
        if not url.startswith(("http://", "https://")) or url in seen:
            continue
        seen.add(url)
        filename = Path(url.split("?", 1)[0]).name or "document"
        candidates.append(DocumentCandidate(filename=filename[:255], source_url=url))
    return tuple(candidates)


def validate_document(content: bytes, content_type: str, *, max_size_bytes: int = 25_000_000) -> str:
    if not content:
        raise DocumentCollectorError("Downloaded document is empty.")
    if len(content) > max_size_bytes:
        raise DocumentCollectorError("Downloaded document exceeds the configured size limit.")
    normalized_type = content_type.split(";", 1)[0].strip().lower()
    if content.startswith(b"%PDF-"):
        return "application/pdf"
    if content.startswith(b"PK\x03\x04") and normalized_type in {
        "application/zip",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/octet-stream",
    }:
        return normalized_type
    raise DocumentCollectorError("Downloaded content is not a supported document type.")


def download_document(
    candidate: DocumentCandidate,
    *,
    opener: Any = urlopen,
    timeout: float = 30,
    max_size_bytes: int = 25_000_000,
) -> tuple[bytes, str]:
    if timeout <= 0 or timeout > 120:
        raise DocumentCollectorError("timeout must be greater than 0 and at most 120 seconds.")
    request = Request(candidate.source_url, headers={"User-Agent": "TenderScanner/0.1"})
    try:
        with opener(request, timeout=timeout) as response:
            content_type = response.headers.get("Content-Type", "application/octet-stream")
            content_length = response.headers.get("Content-Length")
            if content_length:
                try:
                    declared_size = int(content_length)
                except (TypeError, ValueError) as exc:
                    raise DocumentCollectorError("Document response has an invalid size header.") from exc
                if declared_size > max_size_bytes:
                    raise DocumentCollectorError("Document exceeds the configured size limit.")
            content = response.read(max_size_bytes + 1)
    except HTTPError as exc:
        raise DocumentCollectorError(f"Document request returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise DocumentCollectorError(f"Document request failed: {exc.reason}.") from exc
    return content, validate_document(content, content_type, max_size_bytes=max_size_bytes)


def collect_documents(
    db: Session,
    tender: Tender,
    *,
    storage_root: Path,
    opener: Any = urlopen,
) -> tuple[CollectedDocument, ...]:
    storage_dir = storage_root / str(tender.id)
    results: list[CollectedDocument] = []
    for candidate in discover_attachments(tender):
        try:
            content, content_type = download_document(candidate, opener=opener)
            checksum = hashlib.sha256(content).hexdigest()
            existing = db.scalar(
                select(Document).where(
                    Document.tender_id == tender.id,
                    Document.checksum == checksum,
                    Document.status == "COLLECTED",
                )
            )
            if existing is not None:
                results.append(
                    CollectedDocument(existing.id, existing.filename, existing.source_url, checksum, "SKIPPED_DUPLICATE")
                )
                continue
            storage_dir.mkdir(parents=True, exist_ok=True)
            target = storage_dir / f"{checksum}-{candidate.filename}"
            target.write_bytes(content)
            document = Document(
                tender_id=tender.id,
                filename=str(target),
                source_url=candidate.source_url,
                checksum=checksum,
                size_bytes=len(content),
                content_type=content_type,
                status="COLLECTED",
                downloaded_at=datetime.now(timezone.utc),
            )
            db.add(document)
            db.commit()
            db.refresh(document)
            results.append(CollectedDocument(document.id, document.filename, document.source_url, checksum, document.status))
        except DocumentCollectorError as exc:
            failed = Document(
                tender_id=tender.id,
                filename=candidate.filename,
                source_url=candidate.source_url,
                checksum="",
                size_bytes=0,
                content_type="",
                status="FAILED",
            )
            db.add(failed)
            db.commit()
            results.append(CollectedDocument(failed.id, failed.filename, failed.source_url, "", "FAILED"))
    return tuple(results)
