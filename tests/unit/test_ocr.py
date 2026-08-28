import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.ocr import OCRError, detect_scanned_pages, normalize_ocr_output, process_document_with_ocr, run_ocr


def test_normalize_ocr_output_removes_blank_lines_and_normalizes_spacing() -> None:
    assert normalize_ocr_output("  Tender  \r\n\r\n  Notice ") == "Tender\nNotice"


def test_detect_scanned_pages_returns_empty_or_low_quality_pages() -> None:
    document = Mock(
        pages=[
            SimpleNamespace(page_number=1, extracted_text="Readable", extraction_quality=0.9),
            SimpleNamespace(page_number=2, extracted_text="", extraction_quality=0.0),
        ]
    )
    assert detect_scanned_pages(document) == (2,)


def test_run_ocr_sends_file_and_parses_page_results(tmp_path: Path) -> None:
    document = tmp_path / "scan.pdf"
    document.write_bytes(b"%PDF-test")
    response = Mock()
    response.read.return_value = json.dumps(
        {"choices": [{"message": {"content": '{"pages":[{"page_number":1,"text":"  Tender notice  "}]}'}}]}
    ).encode()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=None)
    opener = Mock(return_value=response)
    pages = run_ocr(document, api_key="secret", api_base_url="https://terra.example", opener=opener)
    assert pages[0].text == "Tender notice"
    request = opener.call_args.args[0]
    assert request.full_url.endswith("/v1/chat/completions")
    assert b"gpt-5.6-terra" in request.data


def test_run_ocr_rejects_invalid_provider_response(tmp_path: Path) -> None:
    document = tmp_path / "scan.pdf"
    document.write_bytes(b"%PDF-test")
    response = Mock()
    response.read.return_value = b'{"choices":[]}'
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=None)
    with pytest.raises(OCRError):
        run_ocr(document, api_key="secret", api_base_url="https://terra.example", opener=Mock(return_value=response))


def test_process_document_persists_ocr_pages(tmp_path: Path) -> None:
    document_path = tmp_path / "scan.pdf"
    document_path.write_bytes(b"%PDF-test")
    document = Mock(id=uuid4(), filename=str(document_path), status="OCR_REQUIRED")
    response = Mock()
    response.read.return_value = json.dumps(
        {"choices": [{"message": {"content": '{"pages":[{"page_number":1,"text":"Tender notice"}]}'}}]}
    ).encode()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=None)
    db = Mock()
    result = process_document_with_ocr(
        db, document, api_key="secret", api_base_url="https://terra.example", opener=Mock(return_value=response)
    )
    assert result.status == "OCR_COMPLETE"
    assert db.add.call_count == 1


def test_process_document_marks_provider_failure(tmp_path: Path) -> None:
    document_path = tmp_path / "scan.pdf"
    document_path.write_bytes(b"%PDF-test")
    document = Mock(id=uuid4(), filename=str(document_path), status="OCR_REQUIRED")
    db = Mock()
    with pytest.raises(OCRError):
        process_document_with_ocr(db, document, api_key="", api_base_url="https://terra.example")
    assert document.status == "OCR_FAILED"
