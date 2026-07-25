from typing import TypeVar, Type, Any

from app.domain.entities.base import BaseEntity
from app.domain.entities.node.models import Node
from app.domain.entities.root.models import Root
from app.domain.entities.snapshot.models import Snapshot
from app.domain.entities.snapshot_file.models import SnapshotFile
from app.domain.entities.user.models import User


EntityType = TypeVar("EntityType", bound=BaseEntity)

class EntityAlreadyExistsError(Exception):
    def __init__(
        self,
        entity_type: Type[EntityType],
        fields: dict[str, Any] | None = None,
        message: str | None = None,
    ):
        self.entity_type = entity_type
        self.fields = fields
        self.message = message or self._build_message()

        super().__init__(self.message)

    def _build_message(self) -> str:
        if self.fields is not None:
            values = ", ".join(
                f"{field}={value}"
                for field, value in self.fields
            )

            return (
                # "User with email=jane@gmail.com, username=jane already exists"
                f"{self.entity_type.__name__} "
                f"with {values} already exists"
            )

        return f"{self.entity_type.__name__} already exists"

    def to_dict(self) -> dict:
        return {
            "error": "EntityAlreadyExists",
            "entity_type": self.entity_type.__name__,
            "fields": self.fields,
            "error_message": self.message,
        }

    def __str__(self) -> str:
        return self.message


class UserAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, fields: dict[str, Any]):
        super().__init__(User, fields)


class NodeAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, fields: dict[str, Any]):
        super().__init__(Node, fields)


class RootAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, fields: dict[str, Any]):
        super().__init__(Root, fields)


class SnapshotAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, fields: dict[str, Any]):
        super().__init__(Snapshot, fields)


class SnapshotFileAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, field: dict[str, Any]):
        super().__init__(SnapshotFile, field)