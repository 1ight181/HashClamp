from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, TypedDict, Unpack
from uuid import UUID, uuid4

import re

EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

@dataclass
class User:
    username: str
    email: str

    password_hash: str

    fullname: Optional[str] = None

    id: UUID = field(init=False, default_factory=uuid4())

    created_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))
    updated_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))

    is_active: bool = True
    is_superuser: bool = False

    default_scan_interval_minutes: int = 30
    max_nodes: int = 5
    should_notify_on_changes: bool = False
    notification_email: Optional[str] = None

    class UserCreateOptions(TypedDict, total=False):
        fullname: str
        notification_email: str
        should_notify_on_changes: bool
        default_scan_interval_minutes: int
        max_nodes: int

    @classmethod
    def create(
            cls,
            username: str,
            email: str,
            password_hash: str,
            **kwargs: Unpack[UserCreateOptions],
    ):
        """
        Creates a new user.

        Args:
            username: Unique username.
            email: User email address.
            password_hash: Password hash.
            **kwargs:
                fullname: User full name. Defaults to username.
                notification_email: Email address for change notifications.
                should_notify_on_changes: Whether change notifications are enabled.
                default_scan_interval_minutes: Default scan interval in minutes.
                max_nodes: Maximum number of nodes allowed.

        Returns:
            A new User instance.

        Raises:
            TypeError: If an argument has an invalid type.
            ValueError: If an argument has an invalid value.
        """
        if len(username.strip()) < 3:
            raise ValueError("Username is required and must be at least 3 characters long")

        if not EMAIL_REGEX.match(email):
            raise ValueError("Email address is invalid")

        if not password_hash.strip():
            raise ValueError("Password is required and cannot be empty")

        notification_email = kwargs.get("notification_email")
        if notification_email is not None:
            if not EMAIL_REGEX.match(str(notification_email)):
                raise ValueError("Email address for notifications is invalid")

        should_notify_on_changes = kwargs.get("should_notify_on_changes")
        if should_notify_on_changes is not None:
            if not isinstance(should_notify_on_changes, bool):
                raise TypeError("Should notify on changes must be a boolean value")


        default_scan_interval_minutes = kwargs.get("default_scan_interval_minutes")
        if default_scan_interval_minutes is not None:
            if isinstance(default_scan_interval_minutes, int):
                if default_scan_interval_minutes <= 0:
                    raise ValueError(f"Default scan interval minutes {default_scan_interval_minutes} must be positive")
            else:
                raise TypeError("Default scan interval minutes must be a positive integer")

        max_nodes = kwargs.get("max_nodes")
        if max_nodes is not None:
            if isinstance(max_nodes, int):
                if max_nodes <= 0:
                    raise ValueError(f"Max nodes {max_nodes} must be positive")
            else:
                raise TypeError("Max nodes must be a positive integer")

        fullname = kwargs.get("fullname", username)

        return cls(
            username=username,
            email=email,

            fullname=fullname,

            password_hash=password_hash,

            **kwargs
        )

    class UserUpdateOptions(TypedDict, total=False):
        username: str
        email: str
        default_scan_interval_minutes: int
        max_nodes: int
        should_notify_on_changes: bool
        notification_email: str
        is_active: bool
        is_superuser: bool

    def update(self, **kwargs: Unpack[UserUpdateOptions]) -> bool:
        """
            Updates the entity.

            Returns:
                bool: True if at least one field was changed, False otherwise.
        """
        allowed_fields = {
            "username",
            "email",
            "default_scan_interval_minutes",
            "max_nodes",
            "should_notify_on_changes",
            "notification_email",
            "is_active",
            "is_superuser",
        }

        unknown = set(kwargs) - allowed_fields
        if unknown:
            raise ValueError(f"Unknown fields {unknown}")

        email = kwargs.get("email")
        if email is not None:
            if not EMAIL_REGEX.match(str(email).strip()):
                raise ValueError("Email address is invalid")

        username = kwargs.get("username")
        if username is not None:
            if len(str(username).strip()) < 3:
                raise ValueError("Username must be at least 3 characters long")

        if kwargs.get("should_notify_on_changes") is True:
            notification_email = kwargs.get("notification_email")
            if not notification_email:
                raise ValueError("Notifications are enabled but notification_email is not set")

            if not EMAIL_REGEX.match(str(notification_email)):
                raise ValueError("Email address for notifications is invalid")

        default_scan_interval_minutes = kwargs.get("default_scan_interval_minutes")
        if default_scan_interval_minutes is not None:
            if isinstance(default_scan_interval_minutes, int):
                if default_scan_interval_minutes <= 0:
                    raise ValueError(f"Default scan interval minutes {default_scan_interval_minutes} must be positive")
            else:
                raise TypeError("Default scan interval minutes must be a positive integer")

        max_nodes = kwargs.get("max_nodes")
        if max_nodes is not None:
            if isinstance(max_nodes, int):
                if max_nodes <= 0:
                    raise ValueError(f"Max nodes {max_nodes} must be positive")
            else:
                raise TypeError("Max nodes must be a positive integer")

        was_updated = False
        for key, value in kwargs.items():
            setattr(self, key, value)
            was_updated = True

        if was_updated:
            self.updated_at = datetime.now()

        return was_updated