from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = getenv("DATABASE_URL")
Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(
    # DATABASE_URL
    SQLALCHEMY_DATABASE_URL
)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
