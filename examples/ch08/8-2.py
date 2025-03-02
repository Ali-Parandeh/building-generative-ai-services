# entities.py

import uuid
from datetime import UTC, datetime

from sqlalchemy import Index, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(length=255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=255))
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(default="USER")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )

    __table_args__ = (Index("ix_users_email", "email"),)
