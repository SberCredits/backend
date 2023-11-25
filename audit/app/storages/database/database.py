from contextlib import contextmanager
from os import getenv

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, Session

from storages.database.models import Base

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
    drivername="postgresql+psycopg2"
)

engine = create_engine(url)
session = sessionmaker(bind=engine)


@contextmanager
def get_session() -> Session:
    with session(expire_on_commit=False) as sess:
        yield sess


Base.metadata.create_all(engine)
