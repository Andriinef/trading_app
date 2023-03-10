from pydantic import BaseModel


class TicketCreateSchema(BaseModel):
    customer_id: int
    manager_id: int
    header: str
    body: str


class TicketSchema(TicketCreateSchema):
    id: int


class TicketResponseSchema(BaseModel):
    id: int
    customer_id: int
    manager_id: int
    header: str
    body: str

    class Config:
        orm_mode = True
