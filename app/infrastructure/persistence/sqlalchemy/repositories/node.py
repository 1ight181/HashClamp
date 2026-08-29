from uuid import UUID

from sqlalchemy import select

from app.domain.entities.node.models import Node
from app.domain.repositories.node import NodeRepository
from app.infrastructure.persistence.sqlalchemy.constraints.constraint_registry import ConstraintRegistry
from app.infrastructure.persistence.sqlalchemy.models.node import NodeModel
from app.infrastructure.persistence.sqlalchemy.repositories.base import (
    SqlAlchemyBaseRepository, T_orm, T_domain,
)


class SqlAlchemyNodeRepository(
    NodeRepository,
    SqlAlchemyBaseRepository[Node, NodeModel],
):
    def __init__(
        self,
        session,
        constraint_registry: ConstraintRegistry,
    ):
        super().__init__(
            session,
            NodeModel,
            constraint_registry,
        )

    async def get_all_by_user_id(
        self,
        user_id: UUID,
    ) -> list[Node]:
        result = await self.session.execute(
            select(self.orm_model).where(
                self.orm_model.user_id == user_id
            )
        )

        return [
            self._to_domain(orm)
            for orm in result.scalars().all()
        ]

    async def get_by_name(
        self,
        name: str,
    ) -> Node | None:
        result = await self.session.execute(
            select(self.orm_model).where(
                self.orm_model.name == name
            )
        )

        orm = result.scalar_one_or_none()

        return self._to_domain(orm) if orm else None

    @staticmethod
    def _to_domain(
        orm: NodeModel,
    ) -> Node:
        return Node.restore(
            id=orm.id,
            name=orm.name,
            os_type=orm.os_type,
            os_version=orm.os_version,
            user_id=orm.user_id,
            hostname=orm.hostname,
            ip_addresses=orm.ip_addresses,
            port=orm.port,
            max_roots=orm.max_roots,
            default_scan_interval_minutes=orm.default_scan_interval_minutes,
        )

    @staticmethod
    def _from_domain(
        domain: Node,
    ) -> NodeModel:
        return NodeModel(
            id=domain.id,
            name=domain.name,
            os_type=domain.os_type,
            os_version=domain.os_version,
            user_id=domain.user_id,
            hostname=domain.hostname,
            ip_addresses=domain.ip_addresses,
            port=domain.port,
            max_roots=domain.max_roots,
            default_scan_interval_minutes=domain.default_scan_interval_minutes,
        )

    @staticmethod
    def _update_orm_from_domain(orm: NodeModel, domain: Node):
        orm.name = domain.name
        orm.os_type = domain.os_type
        orm.os_version = domain.os_version

        orm.hostname = domain.hostname
        orm.ip_addresses = domain.ip_addresses
        orm.port = domain.port

        orm.default_scan_interval_minutes = domain.default_scan_interval_minutes
        orm.max_roots = domain.max_roots