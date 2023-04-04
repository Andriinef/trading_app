from apps.db.db import Base
from apps.users.models import User
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    title = Column(String(150), index=True)
    description = Column(Text, index=True)
    status = Column(String(50), index=True)

    owner_id = Column(Integer, ForeignKey(User.id))

    owner = relationship("User", back_populates="tickets")
