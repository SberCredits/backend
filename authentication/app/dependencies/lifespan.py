from contextlib import asynccontextmanager

from storages.database.database import engine
from storages.database.models import Base


@asynccontextmanager
async def lifespan(_):
    await create_database()
    yield


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
