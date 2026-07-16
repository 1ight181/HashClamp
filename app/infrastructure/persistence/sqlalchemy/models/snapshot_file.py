from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base


if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.root import RootModel


class SnapshotFileModel(Base):
    __tablename__ = "file_entries"

    __table_args__ = (
        UniqueConstraint(
            "root_id",
            "relative_path",
            "filename",
            name="unique_file_entry_path",
        ),
    )

    root_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "roots.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    root: Mapped["RootModel"] = relationship(
        back_populates="files",
    )

    relative_path: Mapped[str] = mapped_column(
        String(1024),
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        nullable=False,
    )

    hash_base64: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

