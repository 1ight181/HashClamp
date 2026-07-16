from pathlib import Path
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.root.models import Root
from app.domain.repositories.root import RootRepository
from app.infrastructure.persistence.sqlalchemy.models.root import RootModel
from app.infrastructure.persistence.sqlalchemy.repositories.base import (
    SqlAlchemyBaseRepository,
)


class SqlAlchemyRootRepository(
    RootRepository,
    SqlAlchemyBaseRepository[Root, RootModel],
):
    def __init__(self, session):
        super().__init__(session, RootModel)

    async def get_all_by_node_id(
        self,
        node_id: UUID,
    ) -> list[Root]:
        result = await self.session.execute(
            select(self.orm_model).where(
                self.orm_model.node_id == node_id
            )
        )

        return [
            self._to_domain(orm)
            for orm in result.scalars().all()
        ]

    async def get_by_path_by_node_id(
        self,
        path: Path,
        node_id: UUID,
    ) -> Root | None:
        result = await self.session.execute(
            select(self.orm_model).where(
                self.orm_model.path == str(path),
                self.orm_model.node_id == node_id,
            )
        )

        orm = result.scalar_one_or_none()

        return self._to_domain(orm) if orm else None

    async def get_by_alias_by_node_id(
        self,
        alias: str,
        node_id: UUID,
    ) -> Root | None:
        result = await self.session.execute(
            select(self.orm_model).where(
                self.orm_model.alias == alias,
                self.orm_model.node_id == node_id,
            )
        )

        orm = result.scalar_one_or_none()

        return self._to_domain(orm) if orm else None

    def _to_domain(
        self,
        root_orm: RootModel,
    ) -> Root:
        return Root.restore(
            id=root_orm.id,
            path=Path(root_orm.path),
            alias=root_orm.alias,
            node_id=root_orm.node_id,
            scan_interval_minutes=root_orm.scan_interval_minutes,
        )

    def _update_orm_from_domain(
        self,
        orm: RootModel,
        domain: Root,
    ):
        orm.id = domain.id
        orm.path = str(domain.path)
        orm.alias = domain.alias
        orm.node_id = domain.node_id
        orm.scan_interval_minutes = domain.scan_interval_minutes