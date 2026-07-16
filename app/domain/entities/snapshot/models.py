from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import TypedDict, Unpack
from uuid import UUID

from app.domain.entities.base import BaseEntity
from exceptions import (
    InvalidSnapshotDataError,
    InvalidSnapshotUpdateError,
)


class SnapshotStatus(str, Enum):
    CREATED = "created"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Snapshot(BaseEntity):
    root_id: UUID

    status: SnapshotStatus

    created_at: datetime

    @classmethod
    def create(
            cls,
            root_id: UUID,
    ) -> "Snapshot":

        cls._validate(
            root_id=root_id,
        )

        return cls(
            root_id=root_id,
            status=SnapshotStatus.CREATED,
            created_at=datetime.now(timezone.utc),
        )


    @classmethod
    def restore(
            cls,
            id: UUID,
            root_id: UUID,
            status: SnapshotStatus,
            created_at: datetime,
    ) -> "Snapshot":

        if not id:
            raise InvalidSnapshotDataError(
                "Snapshot id cannot be empty"
            )

        cls._validate(
            root_id=root_id,
            status=status,
            created_at=created_at,
        )

        return cls(
            id=id,
            root_id=root_id,
            status=status,
            created_at=created_at,
        )

    class SnapshotUpdateOptions(TypedDict, total=False):
        status: SnapshotStatus

    def update(
            self,
            **kwargs: Unpack[SnapshotUpdateOptions],
    ):

        allowed_fields = {
            "status",
        }

        unknown_fields = set(kwargs) - allowed_fields

        if unknown_fields:
            raise InvalidSnapshotUpdateError(
                f"Unknown fields: {unknown_fields}"
            )


        status = kwargs.get("status")

        if status is not None:
            self._validate_status(status)

        for key, value in kwargs.items():
            setattr(
                self,
                key,
                value,
            )


    @classmethod
    def _validate(
            cls,
            root_id: UUID,
            status: SnapshotStatus = SnapshotStatus.CREATED,
            created_at: datetime | None = None,
    ) -> None:

        if not root_id:
            raise InvalidSnapshotDataError(
                "Snapshot root id cannot be empty"
            )

        cls._validate_status(
            status
        )

        if created_at is not None:
            cls._validate_created_at(
                created_at
            )

    @staticmethod
    def _validate_status(
            status: SnapshotStatus,
    ) -> None:

        if not isinstance(status, SnapshotStatus):
            raise InvalidSnapshotDataError(
                "Snapshot status is invalid"
            )


    @staticmethod
    def _validate_created_at(
            created_at: datetime,
    ) -> None:

        if created_at.tzinfo is None:
            raise InvalidSnapshotDataError(
                "Created at must contain timezone information"
            )