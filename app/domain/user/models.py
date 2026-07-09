from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, TypedDict, Unpack
from uuid import UUID, uuid4

import re

from exceptions import (
    InvalidUserDataError,
    InvalidUserUpdateError,
)


EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)


@dataclass
class User:
    username: str
    email: str

    password_hash: str

    fullname: Optional[str] = None

    id: UUID = field(init=False, default_factory=uuid4)

    created_at: datetime = field(
        init=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )

    updated_at: datetime = field(
        init=False,
        default_factory=lambda: datetime.now(timezone.utc),
    )

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
    ) -> "User":

        if len(username.strip()) < 3:
            raise InvalidUserDataError(
                "Username must be at least 3 characters long"
            )

        if not EMAIL_REGEX.match(email):
            raise InvalidUserDataError(
                "Email address is invalid"
            )

        if not password_hash.strip():
            raise InvalidUserDataError(
                "Password hash cannot be empty"
            )

        notification_email = kwargs.get("notification_email")

        if notification_email is not None:
            if not EMAIL_REGEX.match(notification_email):
                raise InvalidUserDataError(
                    "Notification email address is invalid"
                )

        default_scan_interval_minutes = kwargs.get(
            "default_scan_interval_minutes"
        )

        if default_scan_interval_minutes is not None:
            if default_scan_interval_minutes <= 0:
                raise InvalidUserDataError(
                    "Default scan interval minutes must be positive"
                )

        max_nodes = kwargs.get("max_nodes")

        if max_nodes is not None:
            if max_nodes <= 0:
                raise InvalidUserDataError(
                    "Max nodes must be positive"
                )

        should_notify_on_changes = kwargs.get(
            "should_notify_on_changes",
            False,
        )

        if should_notify_on_changes and not notification_email:
            raise InvalidUserDataError(
                "Notification email is required when notifications are enabled"
            )

        fullname = kwargs.get(
            "fullname",
            username,
        )

        return cls(
            username=username,
            email=email,
            fullname=fullname,
            password_hash=password_hash,
            **kwargs,
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


    def update(
            self,
            **kwargs: Unpack[UserUpdateOptions],
    ) -> bool:

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

        unknown_fields = set(kwargs) - allowed_fields

        if unknown_fields:
            raise InvalidUserUpdateError(
                f"Unknown fields: {unknown_fields}"
            )

        email = kwargs.get("email")

        if email is not None:
            if not EMAIL_REGEX.match(email.strip()):
                raise InvalidUserUpdateError(
                    "Email address is invalid"
                )

        username = kwargs.get("username")

        if username is not None:
            if len(username.strip()) < 3:
                raise InvalidUserUpdateError(
                    "Username must be at least 3 characters long"
                )

        should_notify_on_changes = kwargs.get(
            "should_notify_on_changes"
        )

        notification_email = kwargs.get(
            "notification_email"
        )

        if should_notify_on_changes is True:
            if not notification_email:
                raise InvalidUserUpdateError(
                    "Notification email is required when notifications are enabled"
                )

            if not EMAIL_REGEX.match(notification_email):
                raise InvalidUserUpdateError(
                    "Notification email address is invalid"
                )

        default_scan_interval_minutes = kwargs.get(
            "default_scan_interval_minutes"
        )

        if default_scan_interval_minutes is not None:
            if default_scan_interval_minutes <= 0:
                raise InvalidUserUpdateError(
                    "Default scan interval minutes must be positive"
                )

        max_nodes = kwargs.get("max_nodes")

        if max_nodes is not None:
            if max_nodes <= 0:
                raise InvalidUserUpdateError(
                    "Max nodes must be positive"
                )

        if not kwargs:
            return False

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.updated_at = datetime.now(timezone.utc)

        return True