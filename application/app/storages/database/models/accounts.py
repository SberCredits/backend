import uuid

from sqlalchemy import String, ForeignKey, UUID, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from storages.database._models import Base


class AccountProfile(Base):
    __tablename__ = "account_profile"

    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    middle_name: Mapped[str] = mapped_column(String)


class Account(Base):
    __tablename__ = "account"

    profile_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('account_profile.id'))
    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    access_token: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    is_activated: Mapped[bool] = mapped_column(Boolean)
