from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.relevance_filter import RelevanceFilterError, RuleSet, classify_tender, evaluate_relevance


def rules() -> RuleSet:
    return RuleSet(("software", "cloud", "cybersecurity"), ("construction", "catering"), ("digital transformation",))


def test_relevant_keyword_is_classified() -> None:
    result = evaluate_relevance("Cloud software platform", rules())
    assert result.label == "RELEVANT"
    assert "software" in result.evidence


def test_out_of_scope_keyword_is_not_relevant() -> None:
    assert evaluate_relevance("Catering services", rules()).label == "NOT_RELEVANT"


def test_ambiguous_or_conflicting_text_is_uncertain() -> None:
    assert evaluate_relevance("Digital transformation services", rules()).label == "UNCERTAIN"
    assert evaluate_relevance("Software for construction", rules()).label == "UNCERTAIN"


def test_empty_text_is_uncertain() -> None:
    assert evaluate_relevance("", rules()).label == "UNCERTAIN"


def test_invalid_rules_fail_explicitly() -> None:
    with pytest.raises(RelevanceFilterError):
        RuleSet.from_config({"relevance_rules": {"include_keywords": "software"}})


def test_classify_tender_persists_rule_classification() -> None:
    db = Mock()
    tender = SimpleNamespace(
        id=uuid4(),
        title="Cloud platform",
        reference_number=None,
        listing_metadata={"scope": "software"},
        relevance_state="UNCERTAIN",
    )
    result = classify_tender(db, tender, {"relevance_rules": {"include_keywords": ["software", "cloud"], "exclude_keywords": [], "uncertain_keywords": []}})
    assert result.label == "RELEVANT"
    assert tender.relevance_state == "RELEVANT"
    db.commit.assert_called_once()
