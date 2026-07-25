from typing import TypeVar, Type

from app.domain.entities.base import BaseEntity

EntityType = TypeVar("EntityType", bound=BaseEntity)

class DomainInvalidDataError(Exception):
    def __init__(
        self,
        entity_type: Type[EntityType],
        message: str,
    ):
        self.entity_type = entity_type
        self.message = message

    def __str__(self) -> str:
        # Invalid data for User: Username must be at least 3 characters long
        return f'Invalid data for {self.entity_type}{f' :{self.message}' if  self.message else ""}'

