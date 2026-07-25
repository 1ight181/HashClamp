from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserCommand:
    username: str
    email: str
    password: str
    fullname: str | None = None
    should_notify_on_changes: bool = False
    notification_email: str | None = None
    default_scan_interval_minutes: int = 30
    max_nodes: int = 5
