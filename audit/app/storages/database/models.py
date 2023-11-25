import uuid
from datetime import datetime

from sqlalchemy import UUID, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
        default=uuid.uuid4
    )

    @property
    def fields(self):
        return self.__dict__


class AccountProfile(Base):
    __tablename__ = "account_profile"
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    middle_name: Mapped[str] = mapped_column(String)


class Account(Base):
    __tablename__ = "account"

    profile: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('account_profile.id'))
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    access_token: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    is_activated: Mapped[bool] = mapped_column(Boolean)


class AuditLog(Base):
    __tablename__ = "auditlog"

    type: Mapped[str] = mapped_column(String)
    detail: Mapped[str] = mapped_column(String, nullable=True)
    application: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("account.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    ip_address: Mapped[str] = mapped_column(String)
