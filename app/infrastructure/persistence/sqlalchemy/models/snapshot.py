from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    String,
    func, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base


if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.root import RootModel
    from app.infrastructure.persistence.sqlalchemy.models.snapshot_file import SnapshotFileModel


class SnapshotModel(Base):
    __tablename__ = "snapshots"

    root_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "roots.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    root: Mapped["RootModel"] = relationship(
        back_populates="snapshots",
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    snapshot_files: Mapped[list["SnapshotFileModel"]] = relationship(
        back_populates="snapshot",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )