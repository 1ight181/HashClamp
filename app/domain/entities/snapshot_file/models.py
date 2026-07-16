import base64
import re

from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict, Unpack
from uuid import UUID

from app.domain.entities.base import BaseEntity
from exceptions import (
    InvalidSnapshotFileDataError,
    InvalidSnapshotFileUpdateError,
)


FILENAME_REGEX = re.compile(
    r'^[^\\/:*?"<>|]+$'
)


@dataclass
class SnapshotFile(BaseEntity):
    snapshot_id: UUID

    relative_path: Path
    filename: str

    file_size: int
    hash_base64: str

    class FileEntryUpdateOptions(TypedDict, total=False):
        relative_path: Path
        filename: str
        file_size: int
        hash_base64: str

    @classmethod
    def create(
            cls,
            snapshot_id: UUID,
            relative_path: Path,
            filename: str,
            file_size: int,
            hash_base64: str,
    ) -> "SnapshotFile":

        cls._validate(
            snapshot_id=snapshot_id,
            relative_path=relative_path,
            filename=filename,
            file_size=file_size,
            hash_base64=hash_base64,
        )

        return cls(
            snapshot_id=snapshot_id,
            relative_path=relative_path,
            filename=filename,
            file_size=file_size,
            hash_base64=hash_base64,
        )

    @classmethod
    def restore(
            cls,
            id: UUID,
            snapshot_id: UUID,
            relative_path: Path,
            filename: str,
            file_size: int,
            hash_base64: str,
    ) -> "SnapshotFile":

        if not id:
            raise InvalidSnapshotFileDataError(
                "File entry id cannot be empty"
            )

        cls._validate(
            snapshot_id=snapshot_id,
            relative_path=relative_path,
            filename=filename,
            file_size=file_size,
            hash_base64=hash_base64,
        )

        return cls(
            id=id,
            snapshot_id=snapshot_id,
            relative_path=relative_path,
            filename=filename,
            file_size=file_size,
            hash_base64=hash_base64,
        )

    def update(
            self,
            **kwargs: Unpack[FileEntryUpdateOptions],
    ):

        allowed_fields = {
            "relative_path",
            "filename",
            "file_size",
            "hash_base64",
        }


        unknown_fields = set(kwargs) - allowed_fields

        if unknown_fields:
            raise InvalidSnapshotFileUpdateError(
                f"Unknown fields: {unknown_fields}"
            )


        relative_path = kwargs.get("relative_path")

        if relative_path is not None:
            self._validate_relative_path(relative_path)


        filename = kwargs.get("filename")

        if filename is not None:
            self._validate_filename(filename)


        file_size = kwargs.get("file_size")

        if file_size is not None:
            self._validate_file_size(file_size)


        hash_base64 = kwargs.get("hash_base64")

        if hash_base64 is not None:
            self._validate_hash(hash_base64)

        for key, value in kwargs.items():
            if key == "hash_base64":
                setattr(
                    self,
                    key,
                    value,
                )

    @classmethod
    def _validate(
            cls,
            snapshot_id: UUID,
            relative_path: Path,
            filename: str,
            file_size: int,
            hash_base64: str,
    ) -> None:

        if not snapshot_id:
            raise InvalidSnapshotFileDataError(
                "Root id cannot be empty"
            )

        cls._validate_relative_path(
            relative_path
        )

        cls._validate_filename(
            filename
        )

        cls._validate_file_size(
            file_size
        )

        cls._validate_hash(
            hash_base64
        )

    @staticmethod
    def _validate_relative_path(
            path: Path,
    ) -> None:

        if path.is_absolute():
            raise InvalidSnapshotFileDataError(
                "Relative path must be non-absolute"
            )


    @staticmethod
    def _validate_filename(
            filename: str,
    ) -> None:

        if not FILENAME_REGEX.match(filename):
            raise InvalidSnapshotFileDataError(
                "Filename is invalid"
            )


    @staticmethod
    def _validate_file_size(
            file_size: int,
    ) -> None:

        if file_size < 0:
            raise InvalidSnapshotFileDataError(
                "File size must be non-negative"
            )


    @staticmethod
    def _validate_hash(
            hash_base64: str,
    ) -> None:

        try:
            base64.b64decode(
                hash_base64,
                validate=True,
            )
        except Exception:
            raise InvalidSnapshotFileDataError(
                "Hash is not a valid base64 string"
            )