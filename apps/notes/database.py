from os import getenv

from databases import Database
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_session, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base

# SQLAlchemy specific code, as with any other app
# DATABASE_URL = "sqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = getenv("DATABASE_URL")

database = Database(
    # DATABASE_URL
    SQLALCHEMY_DATABASE_URL
)
Base: DeclarativeMeta = declarative_base()
metadata = MetaData()

engine = create_async_engine(
    # DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL
)

async_session_maker = async_session(engine)
