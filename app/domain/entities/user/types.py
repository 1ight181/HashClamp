from typing import TypedDict


class UserCreateOptions(TypedDict, total=False):
    fullname: str | None
    notification_email: str
    should_notify_on_changes: bool
    default_scan_interval_minutes: int
    max_nodes: int


class UserUpdateOptions(TypedDict, total=False):
    username: str
    email: str
    default_scan_interval_minutes: int
    fullname: str | None
    max_nodes: int
    should_notify_on_changes: bool
    notification_email: str | None
    is_active: bool
    is_superuser: bool


class UserRestoreOptions(TypedDict, total=False):
    fullname: str | None
    notification_email: str | None
    should_notify_on_changes: bool
    default_scan_interval_minutes: int
    max_nodes: int
    is_active: bool
    is_superuser: bool