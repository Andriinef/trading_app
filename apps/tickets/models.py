from apps.db.db import Base
from apps.users.models import User
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(String, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship(User, back_populates="tickets")
