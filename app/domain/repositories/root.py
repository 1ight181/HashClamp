from pathlib import Path
from uuid import UUID

from app.domain.entities.root.models import Root
from app.domain.repositories.base import BaseRepository


class RootRepository(BaseRepository[Root]):
    async def get_all_by_node_id(self, node_id: UUID) -> list[Root]: ...
    async def get_by_path_by_node_id(self, path: Path, node_id: UUID) -> Root | None: ...
    async def get_by_alias_by_node_id(self, alias: str, node_id: UUID) -> Root | None: ...