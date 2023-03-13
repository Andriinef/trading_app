from apps.db.get_db import get_db
from apps.tickets.models import Ticket
from apps.tickets.schemas import TicketBase, TicketCreate, TicketResponseSchema
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

tickets_router = APIRouter(prefix="/tickets", tags=["tickets"])


@tickets_router.post("/tickets/")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = Ticket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@tickets_router.get("/tickets/")
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).offset(skip).limit(limit).all()
    return tickets


@tickets_router.get("/tickets/{ticket_id}", response_model=TicketResponseSchema)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    return db_ticket


@tickets_router.put("/tickets/{ticket_id}", response_model=TicketResponseSchema)
def update_ticket(ticket_id: int, ticket: TicketBase, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if db_ticket is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
