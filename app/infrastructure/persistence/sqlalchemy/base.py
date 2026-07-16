from sqlalchemy.orm import DeclarativeBase, Mapped
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )