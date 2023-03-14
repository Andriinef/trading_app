from typing import Optional

from pydantic import BaseModel, Field


class TicketCreateShema(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "publ"


class TicketPostShema(TicketCreateShema):
    owner_id: int = 2


class TicketShema(TicketPostShema):
    id: int

    class Config:
        orm_mode = True


class TicketResponseSchema(BaseModel):
    results: list[TicketShema] = Field(
        description="Includes the list of Ticket response schema",
        default_factory=list,
    )
