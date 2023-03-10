from pydantic import BaseModel, Field


class TicketCreateSchema(BaseModel):
    customer_id: int
    manager_id: int
    header: str
    body: str


class TicketSchema(TicketCreateSchema):
    id: int

    class Config:
        orm_mode = True


class TicketsResponseSchema(BaseModel):
    results: list[TicketSchema] = Field(
        description="Includes the list of Ticket response schema",
        default_factory=list,
    )
