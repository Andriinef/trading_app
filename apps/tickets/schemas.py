from typing import Optional

from pydantic import BaseModel


class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None


class TicketCreate(TicketBase):
    pass


class TicketResponseSchema(TicketBase):
    id: int
    status: str
    owner_id: int

    class Config:
        orm_mode = True
