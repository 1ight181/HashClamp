from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.base import Base


if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.root import RootModel


class FileEntryModel(Base):
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

    last_modified_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    scanned_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    is_deleted: Mapped[bool] = mapped_column(
        default=False,
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