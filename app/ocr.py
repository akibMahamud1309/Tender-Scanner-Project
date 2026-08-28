from __future__ import annotations

from dataclasses import dataclass
import base64
import json
import os
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import Document, DocumentPage
from app.ai_provider import chat_completions_url, resolve_ai_provider


class OCRError(Exception):
    """Base exception for OCR failures."""


@dataclass(frozen=True)
class OCRPage:
    page_number: int
    text: str
    quality: float


@dataclass(frozen=True)
class OCRResult:
    document_id: UUID
    status: str
    pages: tuple[OCRPage, ...]
    engine_version: str


def detect_scanned_pages(document: Document, *, quality_threshold: float = 0.6) -> tuple[int, ...]:
    if not 0 <= quality_threshold <= 1:
        raise OCRError("quality_threshold must be between 0 and 1.")
    pages = document.pages
    if not pages:
        return (1,)
    return tuple(
        page.page_number
        for page in pages
        if not page.extracted_text.strip() or float(page.extraction_quality) < quality_threshold
    )


def normalize_ocr_output(text: str) -> str:
    if not isinstance(text, str):
        raise OCRError("OCR page text must be a string.")
    return "\n".join(line.strip() for line in text.replace("\r\n", "\n").splitlines() if line.strip()).strip()


def _parse_response(payload: dict[str, Any]) -> tuple[OCRPage, ...]:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise OCRError("Terra OCR response did not contain choices.")
    content = choices[0].get("message", {}).get("content")
    if not isinstance(content, str):
        raise OCRError("Terra OCR response did not contain text content.")
    try:
        result = json.loads(content)
    except json.JSONDecodeError as exc:
        raise OCRError("Terra OCR response content was not valid JSON.") from exc
    raw_pages = result.get("pages")
    if not isinstance(raw_pages, list) or not raw_pages:
        raise OCRError("Terra OCR response did not contain page results.")
    pages: list[OCRPage] = []
    for raw_page in raw_pages:
        if not isinstance(raw_page, dict) or not isinstance(raw_page.get("page_number"), int):
            raise OCRError("Terra OCR returned an invalid page number.")
        text = normalize_ocr_output(raw_page.get("text", ""))
        if not text:
            raise OCRError(f"Terra OCR returned empty text for page {raw_page['page_number']}.")
        pages.append(OCRPage(raw_page["page_number"], text, min(1.0, max(0.0, len(text) / 1000))))
    return tuple(pages)


def run_ocr(
    file_path: Path,
    *,
    api_key: str,
    api_base_url: str,
    model: str = "gpt-5.6-terra",
    opener: Any = urlopen,
    timeout: float = 120,
    max_size_bytes: int = 25_000_000,
) -> tuple[OCRPage, ...]:
    if not api_key.strip():
        raise OCRError("OCR API key is not configured.")
    if not api_base_url.startswith(("http://", "https://")):
        raise OCRError("OCR API base URL must use HTTP or HTTPS.")
    if not file_path.is_file():
        raise OCRError("Document file does not exist.")
    content = file_path.read_bytes()
    if not content or len(content) > max_size_bytes:
        raise OCRError("Document is empty or exceeds the OCR size limit.")
    payload = {
        "model": model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": "Extract all readable text. Return JSON exactly as {\"pages\":[{\"page_number\":1,\"text\":\"...\"}]}.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Transcribe this document: {file_path.name}"},
                    {
                        "type": "input_file",
                        "filename": file_path.name,
                        "file_data": base64.b64encode(content).decode("ascii"),
                    },
                ],
            },
        ],
    }
    request = Request(
        chat_completions_url(api_base_url),
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with opener(request, timeout=timeout) as response:
            response_body = response.read()
    except HTTPError as exc:
        raise OCRError(f"Terra OCR request returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise OCRError(f"Terra OCR request failed: {exc.reason}.") from exc
    try:
        response_payload = json.loads(response_body)
    except json.JSONDecodeError as exc:
        raise OCRError("Terra OCR response was not valid JSON.") from exc
    return _parse_response(response_payload)


def process_document_with_ocr(
    db: Session,
    document: Document,
    *,
    api_key: str | None = None,
    api_base_url: str | None = None,
    model: str | None = None,
    opener: Any = urlopen,
) -> OCRResult:
    provider = resolve_ai_provider() if api_key is None or api_base_url is None else None
    document.status = "OCR_PROCESSING"
    db.commit()
    try:
        pages = run_ocr(
            Path(document.filename),
            api_key=api_key if api_key is not None else provider.api_key,
            api_base_url=api_base_url if api_base_url is not None else provider.base_url,
            model=model or (provider.model if provider else os.getenv("TERRA_MODEL", "gpt-5.6-terra")),
            opener=opener,
        )
        db.execute(delete(DocumentPage).where(DocumentPage.document_id == document.id))
        for page in pages:
            db.add(
                DocumentPage(
                    document_id=document.id,
                    page_number=page.page_number,
                    extracted_text=page.text,
                    extraction_method="OCR",
                    extraction_quality=page.quality,
                    engine_version=model or os.getenv("TERRA_MODEL", "gpt-5.6-terra"),
                )
            )
        document.status = "OCR_COMPLETE"
        db.commit()
        return OCRResult(document.id, document.status, pages, model or os.getenv("TERRA_MODEL", "gpt-5.6-terra"))
    except OCRError:
        document.status = "OCR_FAILED"
        db.commit()
        raise
