from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import DecisionCreate, ListingInput, SourceCreate, SourceHealth, SourceRead, SourceUpdate
from app.source_registry import (
    DuplicateSourceError,
    SourceNotFoundError,
    create_source,
    get_source_health,
    list_sources,
    update_source,
)
from app.source_scanner import ScannerError, ScanResult, scan_source
from app.source_scanner import ScanListing
from app.deduplication import DeduplicationError, persist_listing
from app.relevance_filter import RelevanceFilterError, classify_tender_by_id
from app.models import Tender
from app.ocr import OCRError, process_document_with_ocr
from app.ai_classification import AIClassificationError, classify_tender_with_ai
from app.tender_analysis import TenderAnalysisError, analyze_tender
from app.decision_history import DecisionError, DecisionInput, get_decision_history, record_decision
from app.scheduler import SchedulerError, check_due_jobs
from app.notifications import NotificationError, NotificationEvent, get_notifications, handle_event, mark_notification_read
from uuid import UUID
from pathlib import Path
from app.document_collector import DocumentCollectorError, collect_documents


app = FastAPI(title="Tender Scanner")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/tenders")
def read_tenders(db: Session = Depends(get_db)) -> list[dict[str, object]]:
    tenders = db.scalars(select(Tender).order_by(Tender.updated_at.desc())).all()
    return [
        {
            "id": str(tender.id),
            "title": tender.title,
            "reference_number": tender.reference_number,
            "organization": tender.organization,
            "source_url": tender.source_url,
            "relevance_state": tender.relevance_state,
            "current_version": tender.current_version,
            "listing_metadata": tender.listing_metadata,
        }
        for tender in tenders
    ]


@app.get("/api/v1/sources", response_model=list[SourceRead])
def read_sources(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[SourceRead]:
    return list(list_sources(db, limit=limit, offset=offset))


@app.post("/api/v1/sources", response_model=SourceRead, status_code=status.HTTP_201_CREATED)
def add_source(payload: SourceCreate, db: Session = Depends(get_db)) -> SourceRead:
    try:
        return create_source(db, payload)
    except DuplicateSourceError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": str(exc), "code": "SOURCE_ALREADY_EXISTS"},
        ) from exc


@app.patch("/api/v1/sources/{source_id}", response_model=SourceRead)
def edit_source(
    source_id: str, payload: SourceUpdate, db: Session = Depends(get_db)
) -> SourceRead:
    try:
        return update_source(db, source_id, payload)
    except SourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": str(exc), "code": "SOURCE_NOT_FOUND"},
        ) from exc
    except DuplicateSourceError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": str(exc), "code": "SOURCE_UPDATE_CONFLICT"},
        ) from exc


@app.get("/api/v1/sources/{source_id}/health", response_model=SourceHealth)
def source_health(source_id: str, db: Session = Depends(get_db)) -> SourceHealth:
    try:
        return get_source_health(db, source_id)
    except SourceNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": str(exc), "code": "SOURCE_NOT_FOUND"},
        ) from exc


@app.post("/api/v1/sources/{source_id}/scan")
def trigger_source_scan(source_id: str, db: Session = Depends(get_db)) -> dict[str, object]:
    from app.source_registry import get_source

    try:
        source = get_source(db, source_id)
        result: ScanResult = scan_source(db, source)
        return {
            "source_id": result.source_id,
            "job_id": str(result.job_id),
            "listing_count": len(result.listings),
            "listings": [listing.__dict__ for listing in result.listings],
        }
    except SourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str(exc), "code": "SOURCE_NOT_FOUND"}) from exc
    except ScannerError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail={"error": str(exc), "code": "SOURCE_SCAN_FAILED"}) from exc


@app.post("/api/v1/sources/{source_id}/deduplicate")
def deduplicate_listings(
    source_id: str, listings: list[ListingInput], db: Session = Depends(get_db)
) -> list[dict[str, object]]:
    from app.source_registry import get_source

    try:
        source = get_source(db, source_id)
        results = [
            persist_listing(
                db,
                source,
                ScanListing(
                    title=item.title,
                    source_url=str(item.source_url),
                    reference_number=item.reference_number,
                    metadata=item.metadata,
                ),
            )
            for item in listings
        ]
        return [
            {
                "state": result.state,
                "tender_id": str(result.tender.id),
                "match_key": result.tender.match_key,
                "field_diff": result.field_diff,
            }
            for result in results
        ]
    except SourceNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str(exc), "code": "SOURCE_NOT_FOUND"}) from exc
    except DeduplicationError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"error": str(exc), "code": "DEDUPLICATION_FAILED"}) from exc


@app.post("/api/v1/tenders/{tender_id}/relevance")
def classify_tender_relevance(tender_id: UUID, db: Session = Depends(get_db)) -> dict[str, object]:
    try:
        result = classify_tender_by_id(db, tender_id)
        return {
            "tender_id": str(tender_id),
            "label": result.label,
            "confidence": result.confidence,
            "rule_ids": list(result.rule_ids),
            "evidence": list(result.evidence),
        }
    except RelevanceFilterError as exc:
        status_code = status.HTTP_404_NOT_FOUND if "was not found" in str(exc) else status.HTTP_422_UNPROCESSABLE_ENTITY
        raise HTTPException(
            status_code=status_code,
            detail={"error": str(exc), "code": "RELEVANCE_FILTER_FAILED"},
        ) from exc


@app.post("/api/v1/tenders/{tender_id}/documents")
def collect_tender_documents(tender_id: UUID, db: Session = Depends(get_db)) -> list[dict[str, object]]:
    tender = db.get(Tender, tender_id)
    if tender is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Tender not found.", "code": "TENDER_NOT_FOUND"})
    try:
        documents = collect_documents(db, tender, storage_root=Path("storage") / "documents")
        return [document.__dict__ for document in documents]
    except DocumentCollectorError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail={"error": str(exc), "code": "DOCUMENT_COLLECTION_FAILED"}) from exc


@app.post("/api/v1/documents/{document_id}/ocr")
def run_document_ocr(document_id: UUID, db: Session = Depends(get_db)) -> dict[str, object]:
    from app.models import Document

    document = db.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Document not found.", "code": "DOCUMENT_NOT_FOUND"})
    try:
        result = process_document_with_ocr(db, document)
        return {
            "document_id": str(result.document_id),
            "status": result.status,
            "engine_version": result.engine_version,
            "pages": [{"page_number": page.page_number, "quality": page.quality} for page in result.pages],
        }
    except OCRError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail={"error": str(exc), "code": "OCR_FAILED"}) from exc


@app.post("/api/v1/tenders/{tender_id}/ai-classification")
def classify_tender_ai(tender_id: UUID, db: Session = Depends(get_db)) -> dict[str, object]:
    tender = db.get(Tender, tender_id)
    if tender is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Tender not found.", "code": "TENDER_NOT_FOUND"})
    try:
        result = classify_tender_with_ai(db, tender)
        return {
            "tender_id": str(tender_id),
            "label": result.label,
            "confidence": result.confidence,
            "model_version": result.model_version,
            "prompt_version": result.prompt_version,
            "manual_review": result.manual_review,
            "evidence": list(result.evidence),
        }
    except AIClassificationError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail={"error": str(exc), "code": "AI_CLASSIFICATION_FAILED"}) from exc


@app.post("/api/v1/tenders/{tender_id}/analysis")
def analyze_tender_route(tender_id: UUID, db: Session = Depends(get_db)) -> dict[str, object]:
    tender = db.get(Tender, tender_id)
    if tender is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Tender not found.", "code": "TENDER_NOT_FOUND"})
    try:
        result = analyze_tender(db, tender)
        return {"tender_id": str(result.tender_id), "model_version": result.model_version, "prompt_version": result.prompt_version, "fields": [field.__dict__ for field in result.fields]}
    except TenderAnalysisError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail={"error": str(exc), "code": "TENDER_ANALYSIS_FAILED"}) from exc


@app.get("/api/v1/tenders/{tender_id}/decisions")
def read_decisions(tender_id: UUID, db: Session = Depends(get_db)) -> list[dict[str, object]]:
    try:
        return [
            {"id": str(item.id), "decision": item.decision, "decline_reason": item.decline_reason, "category": item.category, "comment": item.comment, "decided_at": item.decided_at}
            for item in get_decision_history(db, tender_id)
        ]
    except DecisionError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str(exc), "code": "TENDER_NOT_FOUND"}) from exc


@app.post("/api/v1/tenders/{tender_id}/decisions", status_code=status.HTTP_201_CREATED)
def add_decision(tender_id: UUID, payload: DecisionCreate, db: Session = Depends(get_db)) -> dict[str, object]:
    try:
        item = record_decision(db, tender_id, DecisionInput(**payload.model_dump()))
        return {"id": str(item.id), "decision": item.decision, "decline_reason": item.decline_reason, "category": item.category, "comment": item.comment, "decided_at": item.decided_at}
    except DecisionError as exc:
        code = "TENDER_NOT_FOUND" if "not found" in str(exc) else "INVALID_DECISION"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND if code == "TENDER_NOT_FOUND" else status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"error": str(exc), "code": code}) from exc


@app.get("/api/v1/scheduler/due")
def scheduler_due_sources(db: Session = Depends(get_db)) -> list[str]:
    from app.source_registry import list_sources

    try:
        return [source.source_id for source in check_due_jobs(db, list(list_sources(db, limit=500, offset=0)))]
    except SchedulerError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"error": str(exc), "code": "SCHEDULER_FAILED"}) from exc


@app.get("/api/v1/notifications")
def read_notifications(unread_only: bool = False, db: Session = Depends(get_db)) -> list[dict[str, object]]:
    return [
        {"id": str(item.id), "event_type": item.event_type, "tender_id": str(item.tender_id) if item.tender_id else None, "status": item.status, "created_at": item.created_at}
        for item in get_notifications(db, unread_only=unread_only)
    ]


@app.post("/api/v1/notifications")
def create_notification(event: NotificationEvent, db: Session = Depends(get_db)) -> dict[str, object]:
    try:
        item = handle_event(db, event)
        return {"id": str(item.id), "event_type": item.event_type, "status": item.status}
    except NotificationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={"error": str(exc), "code": "NOTIFICATION_FAILED"}) from exc


@app.post("/api/v1/notifications/{notification_id}/read")
def read_notification(notification_id: UUID, db: Session = Depends(get_db)) -> dict[str, object]:
    try:
        item = mark_notification_read(db, notification_id)
        return {"id": str(item.id), "status": item.status}
    except NotificationError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": str(exc), "code": "NOTIFICATION_NOT_FOUND"}) from exc
