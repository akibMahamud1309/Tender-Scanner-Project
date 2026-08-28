from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.document_collector import (
    DocumentCollectorError,
    DocumentCandidate,
    collect_documents,
    discover_attachments,
    validate_document,
)


def test_discover_attachments_normalizes_and_deduplicates_urls() -> None:
    tender = SimpleNamespace(
        source_url="https://example.gov/notices/1",
        listing_metadata={"document_urls": ["/files/spec.pdf", "https://example.gov/files/spec.pdf"]},
    )
    candidates = discover_attachments(tender)
    assert len(candidates) == 1
    assert candidates[0].filename == "spec.pdf"


def test_validate_document_requires_content_signature() -> None:
    assert validate_document(b"%PDF-1.7 data", "application/pdf") == "application/pdf"
    with pytest.raises(DocumentCollectorError):
        validate_document(b"not a pdf", "application/pdf")


def test_validate_document_rejects_oversized_content() -> None:
    with pytest.raises(DocumentCollectorError):
        validate_document(b"%PDF-", "application/pdf", max_size_bytes=4)


def test_collect_documents_persists_document(tmp_path: Path) -> None:
    response = Mock()
    response.headers = {"Content-Type": "application/pdf"}
    response.read.return_value = b"%PDF-1.7 tender"
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=None)
    db = Mock()
    db.scalar.return_value = None
    db.refresh.side_effect = lambda document: setattr(document, "id", uuid4())
    tender = SimpleNamespace(
        id=uuid4(),
        source_url="https://example.gov/notice",
        listing_metadata={"document_urls": ["/files/spec.pdf"]},
    )
    result = collect_documents(db, tender, storage_root=tmp_path, opener=Mock(return_value=response))
    assert result[0].status == "COLLECTED"
    assert list(tmp_path.rglob("*.pdf"))


def test_collect_documents_records_failed_download(tmp_path: Path) -> None:
    db = Mock()
    db.refresh.side_effect = lambda document: setattr(document, "id", uuid4())
    tender = SimpleNamespace(
        id=uuid4(),
        source_url="https://example.gov/notice",
        listing_metadata={"document_urls": ["/files/spec.pdf"]},
    )
    response = Mock()
    response.headers = {"Content-Type": "text/html"}
    response.read.return_value = b"<html>blocked</html>"
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=None)
    result = collect_documents(db, tender, storage_root=tmp_path, opener=Mock(return_value=response))
    assert result[0].status == "FAILED"
