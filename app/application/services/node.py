from uuid import UUID

from app.application.exceptions.not_found import NodeNotFoundError
from app.domain.entities.node.models import Node
from app.domain.repositories.node import NodeRepository

from shared.exceptions.already_exists import EntityAlreadyExistsError


class NodeService:
    def __init__(
        self,
        repo: NodeRepository,
    ):
        self._repo = repo

    async def get_node(
        self,
        node_id: UUID,
    ) -> Node:
        node = await self._repo.get_by_id(node_id)

        if not node:
            raise NodeNotFoundError(node_id)

        return node

    async def create_node(
        self,
        node: Node,
    ) -> Node:
        try:
            await self._repo.save(node)
        except EntityAlreadyExistsError:
            raise

        return node

    async def update_node(
        self,
        node: Node,
    ) -> Node:
        try:
            await self._repo.save(node)
        except EntityAlreadyExistsError:
            raise

        return node

    async def delete_node(
        self,
        node_id: UUID,
    ) -> None:
        if not await self._repo.delete(node_id):
            raise NodeNotFoundError(node_id)