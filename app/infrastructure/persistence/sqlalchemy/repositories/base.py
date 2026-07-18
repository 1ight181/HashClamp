from typing import TypeVar, Generic
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.entities.base import BaseEntity
from app.infrastructure.persistence.sqlalchemy.constraints.constraint_registry import ConstraintRegistry
from app.infrastructure.persistence.sqlalchemy.models.base import Base

from shared.exceptions.already_exists import EntityAlreadyExistsError

T_domain = TypeVar("T_domain", bound=BaseEntity)
T_orm = TypeVar("T_orm", bound=Base)


class SqlAlchemyBaseRepository(Generic[T_domain, T_orm]):

    def __init__(
        self,
        session: AsyncSession,
        orm_model: type[T_orm],
        constraint_registry: ConstraintRegistry,
    ):
        self.session = session
        self.orm_model = orm_model
        self.constraint_registry = constraint_registry

    async def get_by_id(self, entity_id: UUID) -> T_domain | None:
        result = await self.session.execute(
            select(self.orm_model).where(self.orm_model.id == entity_id)
        )

        orm = result.scalar_one_or_none()

        return self._to_domain(orm) if orm else None

    async def save(self, domain_entity: T_domain) -> T_domain:
        orm_entity = await self._get_existing_or_new_orm(domain_entity.id)
        self._update_orm_from_domain(orm_entity, domain_entity)

        self.session.add(orm_entity)
        try:
            await self.session.flush()
        except IntegrityError as exc:
            constraint_name = getattr(exc.orig, "constraint_name", None)
            fields = self.constraint_registry.get_fields_for_unique_constraint(constraint_name)
            fields_with_values = {field: getattr(domain_entity, field) for field in fields}

            raise EntityAlreadyExistsError(type(domain_entity), fields_with_values)


        return domain_entity

    async def get_all(self, limit: int = 50, offset: int = 0) -> list[T_domain]:
        result = await self.session.execute(
            select(self.orm_model).limit(limit).offset(offset)
        )

        return [self._to_domain(orm) for orm in result.scalars().all()]

    async def delete(self, entity_id: UUID) -> bool:
        result = await self.session.execute(
            select(self.orm_model).where(self.orm_model.id == entity_id)
        )

        orm = result.scalar_one_or_none()

        if orm:
            await self.session.delete(orm)
            return True

        return False

    async def exists(self, entity_id: UUID) -> bool:

        result = await self.session.execute(
            select(self.orm_model).where(self.orm_model.id == entity_id)
        )

        orm = result.scalar_one_or_none()

        return orm is not None

    def _to_domain(self, orm: T_orm) -> T_domain:
        raise NotImplementedError

    def _update_orm_from_domain(self, orm: T_orm, domain: T_domain):
        raise NotImplementedError

    async def _get_existing_or_new_orm(self, entity_id: UUID) -> T_orm:
        result = await self.session.execute(
            select(self.orm_model).where(self.orm_model.id == entity_id)
        )

        return result.scalar_one_or_none() or self.orm_model(id=entity_id)