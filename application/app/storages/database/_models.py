import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


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
