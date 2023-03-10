from apps.db.db import SessionLocal
from apps.tickets.models import Ticket
from apps.tickets.schemas import TicketSchema, TicketsResponseSchema
from fastapi import APIRouter
from sqlalchemy import Result, select

tickets_router = APIRouter(prefix="/tickets", tags=["Tickets"])

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


@tickets_router.get("", response_model=TicketsResponseSchema)
def all():
    session = SessionLocal()
    results: Result = session.execute(select(Ticket))

    tickets_results: list[TicketSchema] = [TicketSchema.from_orm(ticket) for ticket in results.scalars().all()]

    return TicketsResponseSchema(results=tickets_results)


# @tickets_router.post("/tickets", response_model=TicketsResponseSchema)
# def create_ticket(db_ticket: TicketCreateSchema):
#     db = SessionLocal()
#     db_ticket = TicketCreateSchema(
#         **db_ticket.dict()
#     )  # создание объекта модели Ticket на основе данных из схемы TicketSchema
#     db.add(db_ticket)  # добавление объекта в сессию
#     db.commit()  # сохранение изменений в базе данных
#     db.refresh(db_ticket)  # обновление объекта с новым id
#     qeury = insert(db_ticket)
#     results: Result = db.execute(qeury)

#     tickets_results: list[TicketSchema] = [TicketSchema.from_orm(ticket) for ticket in results.scalars().all()]

#     TicketsResponseSchema(
#         results=tickets_results
#     )  # возврат созданного билета из базы данных в соответствии с схемой TicketSchema
