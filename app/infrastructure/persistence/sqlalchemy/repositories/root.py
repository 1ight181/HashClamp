from pathlib import Path
from uuid import UUID

from sqlalchemy import select

from app.domain.entities.root.models import Root
from app.domain.repositories.root import RootRepository
from app.infrastructure.persistence.sqlalchemy.constraints.constraint_registry import ConstraintRegistry
from app.infrastructure.persistence.sqlalchemy.models.root import RootModel
from app.infrastructure.persistence.sqlalchemy.repositories.base import (
    SqlAlchemyBaseRepository, T_orm, T_domain,
)


class SqlAlchemyRootRepository(
    RootRepository,
    SqlAlchemyBaseRepository[Root, RootModel],
):
    def __init__(
        self,
        session,
        constraint_registry: ConstraintRegistry,
    ):
        super().__init__(
            session,
            RootModel,
            constraint_registry,
        )

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

    @staticmethod
    def _to_domain(
        orm: RootModel,
    ) -> Root:
        return Root.restore(
            id=orm.id,
            path=Path(orm.path),
            alias=orm.alias,
            node_id=orm.node_id,
            scan_interval_minutes=orm.scan_interval_minutes,
        )

    @staticmethod
    def _from_domain(
        domain: Root,
    ) -> RootModel:
        return RootModel(
            id=domain.id,
            path=domain.path,
            alias=domain.alias,
            node_id=domain.node_id,
            scan_interval_minutes=domain.scan_interval_minutes,
        )

    @staticmethod
    def _update_orm_from_domain(orm: RootModel, domain: Root):
        orm.path = str(domain.path)
        orm.alias = orm.alias
        orm.scan_interval_minutes = orm.scan_interval_minutes
