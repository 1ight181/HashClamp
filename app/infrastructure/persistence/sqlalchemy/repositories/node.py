from uuid import UUID

from sqlalchemy import select

from app.domain.entities.node.models import Node
from app.domain.repositories.node import NodeRepository
from app.infrastructure.persistence.sqlalchemy.models.node import NodeModel
from app.infrastructure.persistence.sqlalchemy.repositories.base import (
    SqlAlchemyBaseRepository,
)


class SqlAlchemyNodeRepository(
    NodeRepository,
    SqlAlchemyBaseRepository[Node, NodeModel],
):
    def __init__(self, session):
        super().__init__(session, NodeModel)

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

    def _to_domain(
        self,
        node_orm: NodeModel,
    ) -> Node:
        return Node.restore(
            id=node_orm.id,
            name=node_orm.name,
            os_type=node_orm.os_type,
            os_version=node_orm.os_version,
            user_id=node_orm.user_id,
            hostname=node_orm.hostname,
            ip_addresses=node_orm.ip_addresses,
            port=node_orm.port,
            max_roots=node_orm.max_roots,
            default_scan_interval_minutes=node_orm.default_scan_interval_minutes,
        )

    def _update_orm_from_domain(
        self,
        orm: NodeModel,
        domain: Node,
    ) -> None:
        orm.id = domain.id
        orm.name = domain.name
        orm.os_type = domain.os_type
        orm.os_version = domain.os_version
        orm.user_id = domain.user_id
        orm.hostname = domain.hostname
        orm.ip_addresses = domain.ip_addresses
        orm.port = domain.port
        orm.max_roots = domain.max_roots
        orm.default_scan_interval_minutes = domain.default_scan_interval_minutes