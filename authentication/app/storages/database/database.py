from os import getenv

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

user = getenv("POSTGRES_USER")
password = getenv("POSTGRES_PASSWORD")
host = getenv("POSTGRES_HOST")
db_name = getenv("POSTGRES_NAME")

url = URL(
    username=user,
    password=password,
    database=db_name,
    host=host,
    port=5432,
    query={},
    drivername="postgresql+asyncpg"
)

engine = create_async_engine(echo=False, url=url)
session = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_session() -> AsyncSession:
    async with session(expire_on_commit=False) as sess:
        yield sess
