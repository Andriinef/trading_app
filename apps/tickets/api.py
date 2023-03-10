from apps.db.db import SessionLocal, get_db
from apps.tickets.models import Ticket
from apps.tickets.schemas import TicketCreateSchema, TicketResponseSchema, TicketSchema
from fastapi import APIRouter, Body, Depends
from sqlalchemy import Result, select
from sqlalchemy.orm import Session

tickets_router = APIRouter(prefix="/tickets", tags=["Tickets"])


@tickets_router.get("", response_model=TicketResponseSchema)
def all():
    session = SessionLocal()
    results: Result = session.execute(select(Ticket))

    tickets_results: list[TicketSchema] = [TicketSchema.from_orm(ticket) for ticket in results.scalars().all()]

    return TicketResponseSchema(results=tickets_results)


# @tickets_router.post("/tickets", response_model=TicketResponseSchema)
# def create(schema: TicketCreateSchema = Body(...), db: Session = Depends(get_db)):
#     db_ticket = Ticket(schema)  # создание объекта модели Ticket на основе данных из схемы TicketSchema
#     db.add(db_ticket)  # добавление объекта в сессию
#     db.commit()  # сохранение изменений в базе данных
#     db.refresh(db_ticket)  # обновление объекта с новым id
#     return db_ticket

# results: Result = db_ticket

# tickets_results: list[TicketSchema] = [
#     TicketSchema.from_orm(ticket) for ticket in results.scalars().all()
# ]

# return TicketsResponseSchema(results=tickets_results)
# возврат созданного билета из базы данных в соответствии с схемой TicketSchema


@tickets_router.post("/api/tickets", response_model=TicketResponseSchema)
def create_tickets(tickets: TicketCreateSchema = Body(...), db: Session = Depends(get_db)):
    db_tickets = Ticket(
        customer_id=tickets.customer_id,
        manager_id=tickets.manager_id,
        header=tickets.header,
        body=tickets.body,
    )
    db.add(db_tickets)
    db.commit()
    db.refresh(db_tickets)

    return db_tickets
