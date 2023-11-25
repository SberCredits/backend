import uuid
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from storages.database.database import get_session
from storages.database.models.application import Application


class ApplicationRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_session)]):
        self.session = session

    async def get(
            self,
            application_id: uuid.UUID = None,
            one: bool = True
    ):
        queries = []
        stmt = select(Application)
        if application_id:
            queries.append(cast(Application.id, String).istartswith(str(application_id)))

        stmt = stmt.where(*queries)
        result = await self.session.execute(stmt)

        scalars = result.scalars()
        if one:
            return scalars.first()

        return scalars.all()


class Service:
    def __init__(
            self, session: Annotated[AsyncSession, Depends(get_session)],
            applications: Annotated[ApplicationRepository, Depends()]
    ):
        self.session = session
        self.applications = applications

    async def get_application(self, application_id: uuid.UUID) -> Application:
        return await self.applications.get(application_id=application_id, one=True)

