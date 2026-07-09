from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress


class NodeCreateRequest(BaseModel):
    name: str = Field(
        min_length=3,
    )

    os_type: str = Field(
        min_length=1,
    )

    os_version: str = Field(
        min_length=1,
    )

    hostname: str | None = None

    ip_addresses: list[IPvAnyAddress] | None = None

    port: int | None = Field(
        default=None,
        ge=1,
        le=65535,
    )

    max_roots: int = Field(
        default=50,
        gt=0,
    )

    default_scan_interval_minutes: int = Field(
        default=30,
        gt=0,
    )


class NodeUpdateRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
    )

    os_type: str | None = Field(
        default=None,
        min_length=1,
    )

    os_version: str | None = Field(
        default=None,
        min_length=1,
    )

    hostname: str | None = None

    ip_addresses: list[IPvAnyAddress] | None = None

    port: int | None = Field(
        default=None,
        ge=1,
        le=65535,
    )

    max_roots: int | None = Field(
        default=None,
        gt=0,
    )

    default_scan_interval_minutes: int | None = Field(
        default=None,
        gt=0,
    )


class NodeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    user_id: UUID

    name: str

    os_type: str

    os_version: str

    hostname: str | None

    ip_addresses: list[str] | None

    port: int | None

    max_roots: int

    default_scan_interval_minutes: int

    created_at: datetime

    updated_at: datetime