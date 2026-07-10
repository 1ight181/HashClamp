from pathlib import Path
from dataclasses import dataclass, field
from typing import TypedDict, Unpack
from uuid import UUID, uuid4

from exceptions import (
    InvalidRootDataError,
    InvalidRootUpdateError,
)


@dataclass
class Root:
    path: Path
    alias: str

    node_id: UUID

    scan_interval_minutes: int

    id: UUID = field(
        default_factory=uuid4,
    )

    @classmethod
    def create(
            cls,
            path: Path,
            alias: str,
            node_id: UUID,
            scan_interval_minutes: int,
    ) -> "Root":

        cls._validate(
            path=path,
            alias=alias,
            node_id=node_id,
            scan_interval_minutes=scan_interval_minutes,
        )

        return cls(
            path=path,
            alias=alias,
            node_id=node_id,
            scan_interval_minutes=scan_interval_minutes,
        )

    @classmethod
    def restore(
            cls,
            id: UUID,
            path: Path,
            alias: str,
            node_id: UUID,
            scan_interval_minutes: int,
    ) -> "Root":

        if not id:
            raise InvalidRootDataError(
                "Root id cannot be empty"
            )

        cls._validate(
            path=path,
            alias=alias,
            node_id=node_id,
            scan_interval_minutes=scan_interval_minutes,
        )

        return cls(
            id=id,
            path=path,
            alias=alias,
            node_id=node_id,
            scan_interval_minutes=scan_interval_minutes,
        )


    class RootUpdateOptions(TypedDict, total=False):
        path: Path
        alias: str
        scan_interval_minutes: int


    def update(
            self,
            **kwargs: Unpack[RootUpdateOptions],
    ):

        allowed_fields = {
            "path",
            "alias",
            "scan_interval_minutes",
        }


        unknown_fields = set(kwargs) - allowed_fields

        if unknown_fields:
            raise InvalidRootUpdateError(
                f"Unknown fields: {unknown_fields}"
            )


        path = kwargs.get("path")

        if path is not None:
            self._validate_path(path)


        alias = kwargs.get("alias")

        if alias is not None:
            self._validate_alias(alias)


        scan_interval_minutes = kwargs.get(
            "scan_interval_minutes"
        )

        if scan_interval_minutes is not None:
            self._validate_scan_interval(
                scan_interval_minutes
            )

        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def _validate(
            cls,
            path: Path,
            alias: str,
            node_id: UUID,
            scan_interval_minutes: int,
    ) -> None:

        cls._validate_path(path)

        cls._validate_alias(alias)

        if not node_id:
            raise InvalidRootDataError(
                "Root node id cannot be empty"
            )

        cls._validate_scan_interval(
            scan_interval_minutes
        )

    @staticmethod
    def _validate_path(path: Path) -> None:
        if not path.is_absolute():
            raise InvalidRootDataError(
                f"Root path {path} is not absolute"
            )


    @staticmethod
    def _validate_alias(alias: str) -> None:
        if not alias.strip():
            raise InvalidRootDataError(
                "Root alias cannot be empty"
            )


    @staticmethod
    def _validate_scan_interval(
            scan_interval_minutes: int,
    ) -> None:

        if scan_interval_minutes <= 0:
            raise InvalidRootDataError(
                "Scan interval must be positive"
            )