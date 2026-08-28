from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Classification, Tender


class RelevanceFilterError(Exception):
    """Base exception for relevance filtering failures."""


@dataclass(frozen=True)
class RuleSet:
    include_keywords: tuple[str, ...]
    exclude_keywords: tuple[str, ...]
    uncertain_keywords: tuple[str, ...]

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> RuleSet:
        raw = config.get("relevance_rules", config)
        if not isinstance(raw, dict):
            raise RelevanceFilterError("relevance_rules must be an object.")

        def values(name: str) -> tuple[str, ...]:
            value = raw.get(name, ())
            if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
                raise RelevanceFilterError(f"{name} must be a list of strings.")
            normalized = tuple(" ".join(item.split()).casefold() for item in value if item.strip())
            return normalized

        rules = cls(values("include_keywords"), values("exclude_keywords"), values("uncertain_keywords"))
        if not rules.include_keywords:
            raise RelevanceFilterError("At least one include keyword is required.")
        return rules


@dataclass(frozen=True)
class RelevanceResult:
    label: str
    confidence: float
    rule_ids: tuple[str, ...]
    evidence: tuple[str, ...]


def evaluate_relevance(
    text: str, rules: RuleSet, *, rule_prefix: str = "default"
) -> RelevanceResult:
    normalized_text = " ".join(text.split()).casefold()
    if not normalized_text:
        return RelevanceResult("UNCERTAIN", 0.0, ("empty-text",), ())
    included = tuple(
        (f"{rule_prefix}:include:{index}", keyword)
        for index, keyword in enumerate(rules.include_keywords, start=1)
        if keyword in normalized_text
    )
    excluded = tuple(
        (f"{rule_prefix}:exclude:{index}", keyword)
        for index, keyword in enumerate(rules.exclude_keywords, start=1)
        if keyword in normalized_text
    )
    uncertain = tuple(
        (f"{rule_prefix}:uncertain:{index}", keyword)
        for index, keyword in enumerate(rules.uncertain_keywords, start=1)
        if keyword in normalized_text
    )
    if included and not excluded and not uncertain:
        return RelevanceResult(
            "RELEVANT",
            min(1.0, 0.7 + 0.1 * len(included)),
            tuple(rule_id for rule_id, _ in included),
            tuple(keyword for _, keyword in included),
        )
    if excluded and not included:
        return RelevanceResult(
            "NOT_RELEVANT",
            min(1.0, 0.7 + 0.1 * len(excluded)),
            tuple(rule_id for rule_id, _ in excluded),
            tuple(keyword for _, keyword in excluded),
        )
    rule_ids = tuple(rule_id for rule_id, _ in included + excluded + uncertain)
    evidence = tuple(keyword for _, keyword in included + excluded + uncertain)
    return RelevanceResult("UNCERTAIN", 0.5, rule_ids or ("ambiguous",), evidence)


def classify_tender(db: Session, tender: Tender, source_config: dict[str, Any]) -> RelevanceResult:
    rules = RuleSet.from_config(source_config)
    metadata = tender.listing_metadata or {}
    text = " ".join(
        str(value)
        for value in (tender.title, tender.reference_number or "", *metadata.values())
        if value is not None
    )
    result = evaluate_relevance(text, rules, rule_prefix=str(source_config.get("rule_set_id", "source")))
    tender.relevance_state = result.label
    db.add(
        Classification(
            tender_id=tender.id,
            method="RULE",
            label=result.label,
            confidence=result.confidence,
            rule_id=",".join(result.rule_ids),
            evidence_ref={"keywords": list(result.evidence)},
        )
    )
    db.commit()
    return result


def classify_tender_by_id(db: Session, tender_id: UUID) -> RelevanceResult:
    tender = db.get(Tender, tender_id)
    if tender is None:
        raise RelevanceFilterError(f"Tender '{tender_id}' was not found.")
    if tender.source is None:
        raise RelevanceFilterError(f"Tender '{tender_id}' has no source configuration.")
    return classify_tender(db, tender, tender.source.config)
