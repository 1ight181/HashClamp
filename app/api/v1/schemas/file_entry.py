from datetime import datetime
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FileEntryCreateRequest(BaseModel):
    root_id: UUID

    relative_path: Path

    filename: str = Field(
        min_length=1,
    )

    file_size: int = Field(
        ge=0,
    )

    hash_base64: str = Field(
        min_length=1,
    )


class FileEntryUpdateRequest(BaseModel):
    relative_path: Path | None = None

    filename: str | None = Field(
        default=None,
        min_length=1,
    )

    file_size: int | None = Field(
        default=None,
        ge=0,
    )

    hash_base64: str | None = Field(
        default=None,
        min_length=1,
    )

    scanned_at: datetime | None = None

    is_deleted: bool | None = None


class FileEntryResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    root_id: UUID

    relative_path: Path

    filename: str

    file_size: int

    hash_base64: str

    previous_hash: str | None

    last_modified_at: datetime

    scanned_at: datetime

    is_deleted: bool

    created_at: datetime

    updated_at: datetime