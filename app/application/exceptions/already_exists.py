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
        field: str | None = None,
        value: Any | None = None,
        message: str | None = None,
    ):
        self.entity_type = entity_type
        self.field = field
        self.value = value
        self.message = message or self._build_message()

        super().__init__(self.message)

    def _build_message(self) -> str:
        if self.field is not None:
            return (
                f"{self.entity_type.__name__} "
                f"with {self.field}='{self.value}' already exists"
            )

        return f"{self.entity_type.__name__} already exists"

    def to_dict(self) -> dict:
        return {
            "error": "EntityAlreadyExists",
            "entity_type": self.entity_type.__name__,
            "field": self.field,
            "value": self.value,
            "error_message": self.message,
        }

    def __str__(self) -> str:
        return self.message


class UserAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, field: str, value: object):
        super().__init__(User, field, value)


class NodeAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, field: str, value: object):
        super().__init__(Node, field, value)


class RootAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, field: str, value: object):
        super().__init__(Root, field, value)


class SnapshotAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, field: str, value: object):
        super().__init__(Snapshot, field, value)


class SnapshotFileAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, field: str, value: object):
        super().__init__(SnapshotFile, field, value)