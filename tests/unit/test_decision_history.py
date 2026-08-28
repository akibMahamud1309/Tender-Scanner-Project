from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.decision_history import DecisionError, DecisionInput, record_decision, validate_decision


def test_no_bid_requires_reason_and_category() -> None:
    with pytest.raises(DecisionError):
        validate_decision(DecisionInput("NO_BID"))


def test_bid_is_valid_without_decline_fields() -> None:
    assert validate_decision(DecisionInput("BID")).decision == "BID"


def test_record_decision_creates_append_only_entry() -> None:
    tender_id = uuid4()
    db = Mock()
    db.get.return_value = object()
    db.refresh.side_effect = lambda decision: setattr(decision, "id", uuid4())
    decision = record_decision(db, tender_id, DecisionInput("NO_BID", "Budget", "Commercial", "Too expensive"))
    assert decision.decision == "NO_BID"
    assert db.add.call_count == 1
    assert db.commit.call_count == 1
