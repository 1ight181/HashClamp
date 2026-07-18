from uuid import UUID

from app.application.exceptions.not_found import RootNotFoundError
from app.domain.entities.root.models import Root
from app.domain.repositories.root import RootRepository

from shared.exceptions.already_exists import EntityAlreadyExistsError


class RootService:
    def __init__(
        self,
        repo: RootRepository,
    ):
        self._repo = repo

    async def get_root(
        self,
        root_id: UUID,
    ) -> Root:
        root = await self._repo.get_by_id(root_id)

        if not root:
            raise RootNotFoundError(root_id)

        return root

    async def create_root(
        self,
        root: Root,
    ) -> Root:
        try:
            await self._repo.save(root)
        except EntityAlreadyExistsError:
            raise

        return root

    async def update_root(
        self,
        root: Root,
    ) -> Root:
        try:
            await self._repo.save(root)
        except EntityAlreadyExistsError:
            raise

        return root

    async def delete_root(
        self,
        root_id: UUID,
    ) -> None:
        if not await self._repo.delete(root_id):
            raise RootNotFoundError(root_id)