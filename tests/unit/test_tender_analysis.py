import json
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.tender_analysis import ANALYSIS_FIELDS, TenderAnalysisError, analyze_tender


def test_analyze_tender_validates_and_persists_all_fields() -> None:
    document_id = uuid4()
    page = SimpleNamespace(page_number=1, extracted_text="Deadline is 2026-09-01.")
    document = SimpleNamespace(id=document_id, pages=[page])
    tender = SimpleNamespace(id=uuid4(), title="Tender", reference_number=None, documents=[document])
    fields = [
        {"name": name, "value": "2026-09-01" if name == "submission_deadline" else None,
         "status": "STATED" if name == "submission_deadline" else "NOT_STATED",
         "confidence": 0.9 if name == "submission_deadline" else 0.0,
         "evidence": [{"document_id": str(document_id), "page_number": 1, "snippet": "Deadline is 2026-09-01."}] if name == "submission_deadline" else []}
        for name in ANALYSIS_FIELDS
    ]
    response = Mock()
    response.read.return_value = json.dumps({"choices": [{"message": {"content": json.dumps({"fields": fields})}}]}).encode()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=None)
    db = Mock()
    result = analyze_tender(db, tender, api_key="secret", api_base_url="https://terra.example", opener=Mock(return_value=response))
    assert len(result.fields) == len(ANALYSIS_FIELDS)
    assert db.add.call_count == len(ANALYSIS_FIELDS)


def test_analyze_tender_rejects_missing_field() -> None:
    document = SimpleNamespace(id=uuid4(), pages=[])
    tender = SimpleNamespace(id=uuid4(), title="Tender", reference_number=None, documents=[document])
    response = Mock()
    response.read.return_value = b'{"choices":[{"message":{"content":"{\\"fields\\":[]}"}}]}'
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=None)
    with pytest.raises(TenderAnalysisError):
        analyze_tender(Mock(), tender, api_key="secret", api_base_url="https://terra.example", opener=Mock(return_value=response))
