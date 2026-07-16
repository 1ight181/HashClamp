from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.base import Base

if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.node import NodeModel
    from app.infrastructure.persistence.sqlalchemy.models.file_entry import FileEntryModel


class RootModel(Base):
    __tablename__ = "roots"

    path: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
        index=True,
        unique=True,
    )

    alias: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        unique=True,
    )

    node_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "nodes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    node: Mapped["NodeModel"] = relationship(
        back_populates="roots",
    )

    scan_interval_minutes: Mapped[int] = mapped_column(
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    file_entries: Mapped[list[FileEntryModel]] = relationship(
        back_populates="root",
        passive_deletes=True
    )