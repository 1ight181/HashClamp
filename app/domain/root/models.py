from pathlib import Path
from dataclasses import dataclass, field
from typing import TypedDict, Unpack
from uuid import UUID, uuid4
from datetime import datetime, timezone


@dataclass
class Root:
    path: Path
    alias: str

    node_id: UUID

    scan_interval_minutes: int

    id: UUID = field(init=False, default_factory=uuid4())

    created_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))
    updated_at: datetime = field(init=False, default_factory=datetime.now(timezone.utc))

    class RootCreateOptions(TypedDict, total=False):
        scan_interval_minutes: int

    @classmethod
    def create(
            cls,
            path: Path,
            alias: str,
            node_id: UUID,
            **kwargs: Unpack[RootCreateOptions],
    ):
        """
        Creates a new root.

        Args:
            path: Absolute filesystem path.
            alias: Human-readable root alias.
            node_id: Identifier of the owning node.
            **kwargs:
                scan_interval_minutes: Scan interval in minutes.

        Returns:
            A new Root instance.

        Raises:
            TypeError: If an argument has an invalid type.
            ValueError: If an argument has an invalid value.
        """
        if not path.is_absolute():
            raise ValueError(f"Root path {path} is not absolute")

        if not alias.strip():
            raise ValueError(f"Root alias must not be empty")

        if not node_id:
            raise ValueError(f"Root node_id must not be empty")

        scan_interval_minutes = kwargs.get('scan_interval_minutes')
        if scan_interval_minutes is not None:
            if isinstance(scan_interval_minutes, int):
                if scan_interval_minutes <= 0:
                    raise ValueError(f"Scan interval {scan_interval_minutes} must be positive")
            else:
                raise TypeError("Scan_interval_minutes must be positive integer")

        return cls(
            path=path,
            alias=alias,
            node_id=node_id,
            **kwargs,
        )

    class RootUpdateOptions(TypedDict, total=False):
        path: Path
        alias: str
        scan_interval_minutes: int

    def update(self,**kwargs: Unpack[RootUpdateOptions]) -> bool:
        """
            Updates the entity.

            Returns:
                bool: True if at least one field was changed, False otherwise.
        """
        allowed_fields = {
            'alias',
            'scan_interval_minutes',
            'path',
        }

        unknown = set(kwargs) - allowed_fields
        if unknown:
            raise ValueError(f"Unknown fields {unknown}")

        path = kwargs.get('path')
        if path is not None:
            if isinstance(path, Path):
                if not path.is_absolute():
                    raise ValueError(f"Root path {path} is not absolute")
            else:
                raise TypeError("Root path must be a Path")

        scan_interval_minutes = kwargs.get('scan_interval_minutes')
        if scan_interval_minutes is not None:
            if isinstance(scan_interval_minutes, int):
                if scan_interval_minutes <= 0:
                    raise ValueError(f"Scan interval {scan_interval_minutes} must be positive")
            else:
                raise TypeError("Scan interval must be positive integer")

        was_updated = False
        for key, value in kwargs.items():
            setattr(self, key, value)
            was_updated = True

        if was_updated:
            self.updated_at = datetime.now()

        return was_updated
