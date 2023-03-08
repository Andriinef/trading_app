from os import getenv

from databases import Database
from sqlalchemy import MetaData, create_engine

# SQLAlchemy specific code, as with any other app
# DATABASE_URL = "sqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = getenv("DATABASE_URL")

database = Database(
    # DATABASE_URL
    SQLALCHEMY_DATABASE_URL
)

metadata = MetaData()

engine = create_engine(
    # DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL
)
metadata.create_all(engine)
