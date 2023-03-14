from apps.db.get_db import get_db
from apps.tickets.models import Ticket
from apps.tickets.schemas import (
    TicketCreateShema,
    TicketPostShema,
    TicketResponseSchema,
    TicketShema,
)
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

tickets_router = APIRouter(prefix="/tickets", tags=["tickets"])


@tickets_router.post("/tickets/", response_model=TicketResponseSchema)
def Post_ticket(ticket_in: TicketPostShema = Body(...), db: Session = Depends(get_db)):
    db_ticket = Ticket(**ticket_in.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    ticket: list[TicketShema] = [TicketShema.from_orm(db_ticket)]
    return TicketResponseSchema(results=ticket)


@tickets_router.get("/tickets/")
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).offset(skip).limit(limit).all()
    if db_ticket is None:
        return JSONResponse(status_code=404, content={"message": "Запрос не найден"})
    tickets: list[TicketShema] = [TicketShema.from_orm(ticket) for ticket in db_ticket]
    return TicketResponseSchema(results=tickets)


@tickets_router.get("/tickets/{ticket_id}", response_model=TicketResponseSchema)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket is None:
        return JSONResponse(status_code=404, content={"message": "Запрос не найден"})
    ticket: list[TicketShema] = [TicketShema.from_orm(db_ticket)]
    return TicketResponseSchema(results=ticket)


@tickets_router.put("/tickets/{ticket_id}", response_model=TicketResponseSchema)
def update_ticket(ticket_id: int, ticket_in: TicketCreateShema = Body(...), db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket is None:
        return JSONResponse(status_code=404, content={"message": "Запрос не найден"})
    db_ticket.title = ticket_in.title  # type: ignore
    db_ticket.description = ticket_in.description  # type: ignore
    db_ticket.status = ticket_in.status  # type: ignore
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    ticket: list[TicketShema] = [TicketShema.from_orm(db_ticket)]
    return TicketResponseSchema(results=ticket)
