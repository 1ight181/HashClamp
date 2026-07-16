from dataclasses import field
from uuid import UUID, uuid4

from pydantic.dataclasses import dataclass


@dataclass(kw_only=True)
class BaseEntity:
    id: UUID = field(
        default_factory=uuid4,
    )