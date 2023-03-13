from typing import List

from apps.db.db import SessionLocal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .models import Ticket as DBTicket
from .models import User as DBUser
from .schemas import Ticket as TicketSchema
from .schemas import TicketCreate
from .schemas import User as UserSchema
from .schemas import UserBase, UserCreate

tickets_router = APIRouter(prefix="/tickets", tags=["Tickets"])


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@tickets_router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = DBUser(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@tickets_router.get("/users/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(DBUser).offset(skip).limit(limit).all()
    return users


@tickets_router.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@tickets_router.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(UserBase).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user


@tickets_router.delete("/users/{user_id}", response_model=UserSchema)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


@tickets_router.post("/tickets/")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = DBTicket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


@tickets_router.get("/tickets/", response_model=List[TicketSchema])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tickets = db.query(DBTicket).offset(skip).limit(limit).all()
    return tickets


@tickets_router.get("/tickets/{ticket_id}", response_model=TicketSchema)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(DBTicket).filter(DBTicket.id == ticket_id).first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@tickets_router.put("/tickets/{ticket_id}", response_model=TicketSchema)
def update_ticket(ticket_id: int, ticket: TicketSchema, db: Session = Depends(get_db)):
    db_ticket = db.query(DBTicket).filter(DBTicket.id == ticket_id).first()
    if db_ticket is None:
        raise HTTPException
