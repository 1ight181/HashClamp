from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, TypedDict, Unpack
from uuid import UUID, uuid4

import re

from app.domain.base.base import BaseEntity
from exceptions import (
    InvalidUserDataError,
    InvalidUserUpdateError,
)


EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)


@dataclass
class User(BaseEntity):
    username: str
    email: str

    password_hash: str

    fullname: Optional[str] = None

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

        cls._validate_username(username)

        cls._validate_email(email)

        cls._validate_password_hash(password_hash)


        notification_email = kwargs.get(
            "notification_email"
        )

        if notification_email is not None:
            cls._validate_email(
                notification_email,
                notification=True,
            )


        scan_interval = kwargs.get(
            "default_scan_interval_minutes"
        )

        if scan_interval is not None:
            cls._validate_scan_interval(scan_interval)


        max_nodes = kwargs.get(
            "max_nodes"
        )

        if max_nodes is not None:
            cls._validate_max_nodes(max_nodes)


        should_notify = kwargs.get(
            "should_notify_on_changes",
            False,
        )

        cls._validate_notifications(
            should_notify,
            notification_email,
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
    ):

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


        try:
            username = kwargs.get("username")

            if username is not None:
                self._validate_username(username)


            email = kwargs.get("email")

            if email is not None:
                self._validate_email(email)


            notification_email = kwargs.get(
                "notification_email"
            )

            if notification_email is not None:
                self._validate_email(
                    notification_email,
                    notification=True,
                )


            should_notify = kwargs.get(
                "should_notify_on_changes"
            )

            if should_notify is not None:
                self._validate_notifications(
                    should_notify,
                    notification_email
                    if notification_email is not None
                    else self.notification_email,
                )


            scan_interval = kwargs.get(
                "default_scan_interval_minutes"
            )

            if scan_interval is not None:
                self._validate_scan_interval(
                    scan_interval
                )


            max_nodes = kwargs.get(
                "max_nodes"
            )

            if max_nodes is not None:
                self._validate_max_nodes(
                    max_nodes
                )


        except InvalidUserDataError as error:
            raise InvalidUserUpdateError(
                str(error)
            )

        for key, value in kwargs.items():
            setattr(self, key, value)

    class UserRestoreOptions(TypedDict, total=False):
        fullname: str
        notification_email: str
        should_notify_on_changes: bool
        default_scan_interval_minutes: int
        max_nodes: int
        is_active: bool
        is_superuser: bool

    @classmethod
    def restore(
            cls,
            id: UUID,
            username: str,
            email: str,
            password_hash: str,
            **kwargs: Unpack[UserRestoreOptions],
    ) -> "User":

        if not id:
            raise InvalidUserDataError(
                "User id cannot be empty"
            )

        cls._validate_username(username)

        cls._validate_email(email)

        cls._validate_password_hash(password_hash)

        notification_email = kwargs.get(
            "notification_email"
        )

        if notification_email is not None:
            cls._validate_email(
                notification_email,
                notification=True,
            )

        scan_interval = kwargs.get(
            "default_scan_interval_minutes"
        )

        if scan_interval is not None:
            cls._validate_scan_interval(
                scan_interval
            )

        max_nodes = kwargs.get(
            "max_nodes"
        )

        if max_nodes is not None:
            cls._validate_max_nodes(
                max_nodes
            )

        should_notify = kwargs.get(
            "should_notify_on_changes",
            False,
        )

        cls._validate_notifications(
            should_notify,
            notification_email,
        )

        fullname = kwargs.get(
            "fullname",
            username,
        )

        user = cls(
            id=id,
            username=username,
            email=email,
            fullname=fullname,
            password_hash=password_hash,
            **kwargs,
        )

        return user

    @staticmethod
    def _validate_username(
            username: str,
    ) -> None:

        if len(username.strip()) < 3:
            raise InvalidUserDataError(
                "Username must be at least 3 characters long"
            )


    @staticmethod
    def _validate_email(
            email: str,
            notification: bool = False,
    ) -> None:

        if not EMAIL_REGEX.match(
            email.strip()
        ):
            if notification:
                raise InvalidUserDataError(
                    "Notification email address is invalid"
                )

            raise InvalidUserDataError(
                "Email address is invalid"
            )


    @staticmethod
    def _validate_password_hash(
            password_hash: str,
    ) -> None:

        if not password_hash.strip():
            raise InvalidUserDataError(
                "Password hash cannot be empty"
            )


    @staticmethod
    def _validate_scan_interval(
            scan_interval_minutes: int,
    ) -> None:

        if scan_interval_minutes <= 0:
            raise InvalidUserDataError(
                "Default scan interval minutes must be positive"
            )


    @staticmethod
    def _validate_max_nodes(
            max_nodes: int,
    ) -> None:

        if max_nodes <= 0:
            raise InvalidUserDataError(
                "Max nodes must be positive"
            )


    @staticmethod
    def _validate_notifications(
            should_notify: bool,
            notification_email: Optional[str],
    ) -> None:

        if should_notify and not notification_email:
            raise InvalidUserDataError(
                "Notification email is required when notifications are enabled"
            )
