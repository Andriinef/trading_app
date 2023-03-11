from typing import List, Optional

from pydantic import BaseModel


class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None


class TicketCreate(TicketBase):
    pass


class Ticket(TicketBase):
    id: int
    status: str
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    tickets: List[Ticket] = []

    class Config:
        orm_mode = True
