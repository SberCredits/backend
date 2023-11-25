import hashlib
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from storages.database.database import get_session
from storages.database.models import Account


class AccountRepository:
    def __init__(
            self,
            session: Annotated[AsyncSession, Depends(get_session)],
    ):
        self.session = session

    async def hash_password(self, password: str) -> str:
        return hashlib.sha256("123".encode() + password.encode()).hexdigest()

    async def get(
            self,
            username: str = None,
            password: str = None,
            access_token: str = None
    ):
        queries = []
        if username:
            queries.append(Account.username == username)

        if password:
            queries.append(Account.password == password)

        if access_token:
            queries.append(Account.access_token == access_token)

        stmt = select(Account).where(*queries)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def authenticate(self, username: str, password: str):
        hash_password = await self.hash_password(password)
        return await self.get(username=username, password=hash_password)


class Service:
    def __init__(
            self,
            session: Annotated[AsyncSession, Depends(get_session)],
            account_repository: Annotated[AccountRepository, Depends()]
    ):
        self.session = session
        self.account_repository = account_repository

    async def get_user(self, username, password):
        result = await self.account_repository.authenticate(username, password)
        if not result:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Account not found")

        return result

