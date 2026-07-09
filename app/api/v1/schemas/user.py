from datetime import datetime
from uuid import UUID

from pydantic import Field, BaseModel, EmailStr, ConfigDict


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=4, max_length=20)

    fullname: str | None = None

    should_notify_on_changes: bool = False
    notification_email: EmailStr | None = None

    default_scan_interval_minutes: int = Field(default=30, gt=0)
    max_nodes: int = Field(default=5, gt=0)


class UserUpdateRequest(BaseModel):
    username: str | None = Field(default=None, min_length=3)
    email: EmailStr | None = None

    should_notify_on_changes: bool | None = None
    notification_email: EmailStr | None = None

    default_scan_interval_minutes: int | None = Field(default=None, gt=0)
    max_nodes: int | None = Field(default=None, gt=0)

    is_active: bool | None = None
    is_superuser: bool | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    username: str
    email: EmailStr
    fullname: str | None

    created_at: datetime
    updated_at: datetime

    is_active: bool
    is_superuser: bool

    should_notify_on_changes: bool
    notification_email: EmailStr | None

    default_scan_interval_minutes: int
    max_nodes: int