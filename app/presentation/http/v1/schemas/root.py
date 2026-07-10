from datetime import datetime
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RootCreateRequest(BaseModel):
    path: Path

    alias: str = Field(
        min_length=1,
    )

    node_id: UUID

    scan_interval_minutes: int = Field(
        default=30,
        gt=0,
    )


class RootUpdateRequest(BaseModel):
    path: Path | None = None

    alias: str | None = Field(
        default=None,
        min_length=1,
    )

    scan_interval_minutes: int | None = Field(
        default=None,
        gt=0,
    )


class RootResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    path: Path

    alias: str

    node_id: UUID

    scan_interval_minutes: int

    created_at: datetime

    updated_at: datetime