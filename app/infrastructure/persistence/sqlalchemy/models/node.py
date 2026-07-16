from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import (
    ForeignKey,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.root import RootModel
    from app.infrastructure.persistence.sqlalchemy.models.user import UserModel


class NodeModel(Base):
    __tablename__ = "nodes"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    os_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    os_version: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    user: Mapped["UserModel"] = relationship(
        back_populates="nodes",
    )

    hostname: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    ip_addresses: Mapped[list[str] | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    port: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    max_roots: Mapped[int] = mapped_column(
        default=50,
        nullable=False,
    )

    default_scan_interval_minutes: Mapped[int] = mapped_column(
        default=30,
        nullable=False,
    )

    roots: Mapped[list["RootModel"]] = relationship(
        back_populates="node",
        cascade="all, delete-orphan",
        passive_deletes=True
    )