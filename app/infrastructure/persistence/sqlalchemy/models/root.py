from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.node import NodeModel
    from app.infrastructure.persistence.sqlalchemy.models.snapshot_file import SnapshotFileModel


class RootModel(Base):
    __tablename__ = "roots"

    __table_args__ = (
        UniqueConstraint(
            "node_id",
            "path",
            name="uq_root_node_id_path",
        ),

        UniqueConstraint(
            "node_id",
            "alias",
            name="uq_root_node_id_alias",
        )
    )

    path: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
        index=True,
    )

    alias: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
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

    snapshot_files: Mapped[list[SnapshotFileModel]] = relationship(
        back_populates="root",
        cascade="all, delete-orphan",
        passive_deletes=True
    )