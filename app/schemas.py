from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator


class SourceCreate(BaseModel):
    source_id: str = Field(min_length=1, max_length=200)
    organization: str = Field(min_length=1, max_length=500)
    website: AnyHttpUrl
    config: dict[str, Any] = Field(default_factory=dict)
    scan_frequency: timedelta = Field(default=timedelta(days=1), gt=timedelta(0))
    active: bool = True

    @field_validator("source_id", "organization")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("value must not be blank")
        return value


class SourceUpdate(BaseModel):
    organization: str | None = Field(default=None, min_length=1, max_length=500)
    website: AnyHttpUrl | None = None
    config: dict[str, Any] | None = None
    scan_frequency: timedelta | None = Field(default=None, gt=timedelta(0))
    active: bool | None = None

    @field_validator("organization")
    @classmethod
    def strip_organization(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("organization must not be blank")
        return value


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_id: str
    organization: str
    website: AnyHttpUrl
    config: dict[str, Any]
    scan_frequency: timedelta
    active: bool
    created_at: datetime
    updated_at: datetime


class SourceHealth(BaseModel):
    source_id: str
    last_scan_started_at: datetime | None
    last_scan_finished_at: datetime | None
    recent_failures: int


class ListingInput(BaseModel):
    title: str = Field(min_length=1)
    source_url: AnyHttpUrl
    reference_number: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class DecisionCreate(BaseModel):
    decision: str
    decline_reason: str | None = None
    category: str | None = None
    comment: str | None = None
