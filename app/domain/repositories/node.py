from uuid import UUID

from app.domain.entities.node.models import Node
from app.domain.repositories.base import BaseRepository


class NodeRepository(BaseRepository[Node]):
    async def get_all_by_user_id(self, user_id: UUID) -> list[Node]: ...
