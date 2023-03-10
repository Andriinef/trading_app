from apps.db.db import Base
from sqlalchemy import Column, Integer, String


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(
        Integer,
    )
