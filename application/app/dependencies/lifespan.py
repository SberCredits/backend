from contextlib import asynccontextmanager

from storages.database.database import engine
from storages.database._models import Base
from storages.database.models import accounts, application, bki  # noqa
from storages.s3 import get_minio


@asynccontextmanager
async def lifespan(_):
    await create_database()
    yield


async def create_minio():
    minio = get_minio()
    if not minio.bucket_exists("attachments"):
        minio.make_bucket("attachments")


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
