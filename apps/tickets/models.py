from apps.db.db import Base
from sqlalchemy import Column, Integer, String, Text


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer)
    manager_id = Column(Integer)

    header = Column(String)
    body = Column(Text)
