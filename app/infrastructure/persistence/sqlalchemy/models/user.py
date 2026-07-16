from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.sqlalchemy.models.base import Base


if TYPE_CHECKING:
    from app.infrastructure.persistence.sqlalchemy.models.node import NodeModel


class UserModel(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        unique=True,
        index=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        nullable=False,
    )

    fullname: Mapped[str | None] = mapped_column(
        nullable=True,
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

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    default_scan_interval_minutes: Mapped[int] = mapped_column(
        default=30,
        nullable=False,
    )

    max_nodes: Mapped[int] = mapped_column(
        default=5,
        nullable=False,
    )

    should_notify_on_changes: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    notification_email: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    nodes: Mapped[list["NodeModel"]] = relationship(
        back_populates="user",
        passive_deletes=True,
    )