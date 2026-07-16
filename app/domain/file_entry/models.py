import base64
import re

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, TypedDict, Unpack
from uuid import UUID, uuid4

from app.domain.base.base import BaseEntity
from exceptions import (
    InvalidFileEntryDataError,
    InvalidFileEntryUpdateError,
)


FILENAME_REGEX = re.compile(
    r'^[^\\/:*?"<>|]+$'
)


@dataclass
class FileEntry(BaseEntity):
    root_id: UUID

    relative_path: Path
    filename: str

    file_size: int
    hash_base64: str

    last_modified_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    scanned_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    is_deleted: bool = False

    class FileEntryUpdateOptions(TypedDict, total=False):
        relative_path: Path
        filename: str
        file_size: int
        hash_base64: str
        scanned_at: datetime
        is_deleted: bool

    class FileEntryRestoreOptions(TypedDict, total=False):
        last_modified_at: datetime
        scanned_at: datetime
        is_deleted: bool

    @classmethod
    def create(
            cls,
            root_id: UUID,
            relative_path: Path,
            filename: str,
            file_size: int,
            hash_base64: str,
    ) -> "FileEntry":

        cls._validate(
            root_id=root_id,
            relative_path=relative_path,
            filename=filename,
            file_size=file_size,
            hash_base64=hash_base64,
        )

        return cls(
            root_id=root_id,
            relative_path=relative_path,
            filename=filename,
            file_size=file_size,
            hash_base64=hash_base64,
        )

    @classmethod
    def restore(
            cls,
            id: UUID,
            root_id: UUID,
            relative_path: Path,
            filename: str,
            file_size: int,
            hash_base64: str,
            **kwargs: Unpack[FileEntryRestoreOptions],
    ) -> "FileEntry":

        if not id:
            raise InvalidFileEntryDataError(
                "File entry id cannot be empty"
            )

        cls._validate(
            root_id=root_id,
            relative_path=relative_path,
            filename=filename,
            file_size=file_size,
            hash_base64=hash_base64,
        )

        return cls(
            id=id,
            root_id=root_id,
            relative_path=relative_path,
            filename=filename,
            file_size=file_size,
            hash_base64=hash_base64,
            **kwargs,
        )

    def update(
            self,
            **kwargs: Unpack[FileEntryUpdateOptions],
    ) -> bool:

        allowed_fields = {
            "relative_path",
            "filename",
            "file_size",
            "hash_base64",
            "scanned_at",
            "is_deleted",
        }


        unknown_fields = set(kwargs) - allowed_fields

        if unknown_fields:
            raise InvalidFileEntryUpdateError(
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


        if not kwargs:
            return False


        for key, value in kwargs.items():

            if key == "hash_base64":
                self.previous_hash = self.hash_base64
                self.last_modified_at = datetime.now(
                    timezone.utc
                )

            setattr(
                self,
                key,
                value,
            )


        self.updated_at = datetime.now(
            timezone.utc
        )

        return True

    @classmethod
    def _validate(
            cls,
            root_id: UUID,
            relative_path: Path,
            filename: str,
            file_size: int,
            hash_base64: str,
    ) -> None:

        if not root_id:
            raise InvalidFileEntryDataError(
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
            raise InvalidFileEntryDataError(
                "Relative path must be non-absolute"
            )


    @staticmethod
    def _validate_filename(
            filename: str,
    ) -> None:

        if not FILENAME_REGEX.match(filename):
            raise InvalidFileEntryDataError(
                "Filename is invalid"
            )


    @staticmethod
    def _validate_file_size(
            file_size: int,
    ) -> None:

        if file_size < 0:
            raise InvalidFileEntryDataError(
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
            raise InvalidFileEntryDataError(
                "Hash is not a valid base64 string"
            )