import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional, TypedDict, Unpack
import base64

from pathlib import Path

FILENAME_REGEX = re.compile(
    r'^[^\\/:*?"<>|]+$'
)

@dataclass
class FileEntry:
    root_id: UUID

    relative_path: Path
    filename: str

    file_size: int
    hash_base64: str

    id: UUID = field(init=False, default_factory=uuid4())

    last_modified_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))
    scanned_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))

    is_deleted: bool = field(init=False, default=False)
    previous_hash: Optional[str] = field(init=False, default=None)

    created_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))
    updated_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))

    class FileEntryUpdateOptions(TypedDict, total=False):
        relative_path: Path
        filename: str
        file_size: int
        hash_base64: str
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
    ):
        """
        Creates a new file entry.

        Args:
            root_id: Identifier of the root containing the file.
            relative_path: Relative path to the parent directory.
            filename: Name of the file.
            file_size: File size in bytes.
            hash_base64: Base64-encoded file hash.

        Returns:
            A new FileEntry instance.

        Raises:
            ValueError: If any argument is invalid.
        """
        if not root_id:
            raise ValueError("Root id cannot be empty")

        if relative_path.is_absolute():
            raise ValueError("Relative path is required must be non-absolute")

        if not FILENAME_REGEX.match(str(filename)):
            raise ValueError("Filename must be a valid filename (filename.ext)")

        if file_size < 0:
            raise ValueError(f"File size {file_size} must be non-negative")

        try:
            base64.b64decode(hash_base64, validate=True)
        except Exception:
            raise ValueError("Hash base64 is not a valid base64 string")

        return cls(
            root_id=root_id,
            relative_path=relative_path,
            filename=filename,
            file_size=file_size,
            hash_base64=hash_base64,
        )

    def update(self, **kwargs: Unpack[FileEntryUpdateOptions]) -> bool:
        """
            Updates the entity.

            Returns:
                bool: True if at least one field was changed, False otherwise.
        """
        allowed_fields = {
            "relative_path",
            "filename",
            "file_size",
            "hash_base64",
            "scanned_at",
            "is_deleted",
        }

        unknown = set(kwargs) - allowed_fields
        if unknown:
            raise ValueError(f"Unknown fields {unknown}")

        relative_path = kwargs.get("relative_path")
        if relative_path is not None:
            if not isinstance(relative_path, Path):
                raise TypeError("Relative path must be a Path")
            if relative_path.is_absolute():
                raise ValueError("Relative path is required must be non-absolute")

        filename = kwargs.get("filename")
        if filename is not None:
            if not FILENAME_REGEX.match(str(filename)):
                raise ValueError("Filename must be a valid filename (filename.ext)")

        file_size = kwargs.get("file_size")
        if file_size is not None:
            if isinstance(file_size, int):
                if file_size < 0:
                    raise ValueError(f"File size {file_size} must be positive integer")
            else:
                raise TypeError("File_size must be an positive integer")

        hash_base64 = kwargs.get("hash_base64")
        if hash_base64 is not None:
            try:
                base64.b64decode(str(hash_base64), validate=True)
            except Exception:
                raise ValueError("Hash base64 is not a valid base64 string")

        scanned_at = kwargs.get("scanned_at")
        if scanned_at is not None:
            if not isinstance(scanned_at, datetime):
                raise ValueError("Scanned at must be a datetime")

        is_deleted = kwargs.get("is_deleted")
        if is_deleted is not None:
            if not isinstance(is_deleted, bool):
                raise ValueError("Is deleted must be a boolean")

        was_updated = False
        for key, value in kwargs.items():
            if key == "hash_base64":
                self.last_modified_at = datetime.now()
                self.previous_hash = self.hash_base64

            setattr(self, key, value)
            was_updated = True

        if was_updated:
            self.updated_at = datetime.now()

        return was_updated