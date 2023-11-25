import uuid

from sqlalchemy import UUID, String, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


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
    first_name:  Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    middle_name: Mapped[str] = mapped_column(String)


class Account(Base):
    __tablename__ = "account"

    profile_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('account_profile.id'))\
    profile = relationship(AccountProfile)

    username: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    access_token: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    is_activated: Mapped[bool] = mapped_column(Boolean)
