from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ListingInput, SourceCreate, SourceHealth, SourceRead, SourceUpdate
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
from uuid import UUID
from pathlib import Path
from app.document_collector import DocumentCollectorError, collect_documents


app = FastAPI(title="Tender Scanner")


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
