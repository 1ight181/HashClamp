from typing import Optional, Any, TypeVar, Type
from uuid import UUID

from app.domain.entities.base import BaseEntity
from app.domain.entities.node.models import Node
from app.domain.entities.root.models import Root
from app.domain.entities.snapshot.models import Snapshot
from app.domain.entities.snapshot_file.models import SnapshotFile
from app.domain.entities.user.models import User

EntityType = TypeVar("EntityType", bound=BaseEntity)

class EntityNotFoundError(Exception):

    def __init__(
        self,
        entity_type: Type[EntityType],
        entity_id: UUID | None = None,
        message: str | None = None,
    ):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.message = message if message else self._build_message()
        super().__init__(self.message)

    def _build_message(self) -> str:
        if self.entity_id is not None:
            return f"{self.entity_type} with id '{self.entity_id}' not found"
        return f"{self.entity_type} not found"

    def to_dict(self) -> dict:
        return {
            "error": "EntityNotFound",
            "entity_id": self.entity_id,
            "entity_type": self.entity_type.__name__,
            "error_message": self.message,
        }

    def __str__(self) -> str:
        return self.message


class UserNotFoundError(EntityNotFoundError):
    def __init__(self, user_id: UUID):
        super().__init__(User, user_id)


class NodeNotFoundError(EntityNotFoundError):
    def __init__(self, node_id: UUID):
        super().__init__(Node, node_id)


class RootNotFoundError(EntityNotFoundError):
    def __init__(self, root_id: UUID):
        super().__init__(Root, root_id)

class SnapshotNotFoundError(EntityNotFoundError):
    def __init__(self, snapshot_id: UUID):
        super().__init__(Snapshot, snapshot_id)

class SnapshotFileNotFoundError(EntityNotFoundError):
    def __init__(self, file_id: UUID):
        super().__init__(SnapshotFile, file_id)

