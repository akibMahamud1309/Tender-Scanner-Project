import json
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.ai_classification import AIClassificationError, classify_tender_with_ai, parse_classification_result


def test_parse_classification_validates_evidence_against_page_text() -> None:
    result = parse_classification_result(
        {"choices": [{"message": {"content": '{"label":"RELEVANT","confidence":0.9,"evidence":[{"page_number":1,"snippet":"network"}]}'}}]},
        source_text_by_page={1: "Tender includes network infrastructure."},
        model_version="gpt-5.6-terra",
        prompt_version="classification-v1",
    )
    assert result.label == "RELEVANT"
    assert not result.manual_review


def test_parse_classification_rejects_fabricated_evidence() -> None:
    with pytest.raises(AIClassificationError):
        parse_classification_result(
            {"choices": [{"message": {"content": '{"label":"RELEVANT","confidence":0.9,"evidence":[{"page_number":1,"snippet":"fabricated"}]}'}}]},
            source_text_by_page={1: "Tender text."},
            model_version="model",
            prompt_version="prompt",
        )


def test_classify_tender_with_ai_persists_model_and_prompt_metadata() -> None:
    page = SimpleNamespace(page_number=1, extracted_text="Tender includes software.")
    document = SimpleNamespace(pages=[page])
    tender = SimpleNamespace(id=uuid4(), title="Tender", reference_number=None, listing_metadata={}, documents=[document])
    response = Mock()
    response.read.return_value = json.dumps({"choices": [{"message": {"content": '{"label":"RELEVANT","confidence":0.8,"evidence":[{"page_number":1,"snippet":"software"}]}'}}]}).encode()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=None)
    db = Mock()
    result = classify_tender_with_ai(db, tender, api_key="secret", api_base_url="https://terra.example", opener=Mock(return_value=response))
    assert result.model_version == "gpt-5.6-terra"
    assert db.add.call_count == 1
