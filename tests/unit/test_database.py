from sqlalchemy.orm import Session

from app.database import Base, SessionLocal
from app import models


EXPECTED_TABLES = {
    "sources",
    "tenders",
    "tender_versions",
    "documents",
    "document_pages",
    "classifications",
    "tender_analysis",
    "decisions",
    "job_status",
    "notifications",
}


def test_all_specified_tables_are_registered() -> None:
    assert set(Base.metadata.tables) == EXPECTED_TABLES


def test_required_constraints_are_registered() -> None:
    tenders = Base.metadata.tables["tenders"]
    decisions = Base.metadata.tables["decisions"]
    job_status = Base.metadata.tables["job_status"]

    assert any(
        constraint.name == "uq_tenders_source_match_key"
        for constraint in tenders.constraints
    )
    assert any(
        constraint.name == "ck_no_bid_requires_reason_category"
        for constraint in decisions.constraints
    )
    assert Base.metadata.tables["notifications"].c.dedup_key.unique
    assert any(
        index.name == "ix_job_status_one_running_per_type_source"
        and index.unique
        for index in job_status.indexes
    )


def test_foreign_key_relationships_match_schema() -> None:
    assert {
        (foreign_key.parent.table.name, foreign_key.target_fullname)
        for foreign_key in Base.metadata.tables["tenders"].foreign_keys
    } == {("tenders", "sources.id")}
    assert {
        foreign_key.target_fullname
        for foreign_key in Base.metadata.tables["documents"].foreign_keys
    } == {"tenders.id"}


def test_session_factory_creates_sqlalchemy_session_without_connecting() -> None:
    session = SessionLocal()
    try:
        assert isinstance(session, Session)
    finally:
        session.close()


def test_models_are_registered_with_expected_classes() -> None:
    assert models.Source.__tablename__ == "sources"
    assert models.Notification.__tablename__ == "notifications"
