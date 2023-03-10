from apps.db.db import SessionLocal, get_db
from fastapi import APIRouter, Body, Depends
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from .models import Person
from .shemas import PersonCreateSchema, PersonResponseSchema

person_router = APIRouter(prefix="/person", tags=["person"])


@person_router.get("/api/users", response_model=PersonResponseSchema)
def get_people(db: Session = Depends(get_db)):
    return db.query(Person).all()


@person_router.get("/api/users/{id}", response_model=PersonResponseSchema)
def get_person(id, db: Session = Depends(get_db)):
    # получаем пользователя по id
    person = db.query(Person).filter(Person.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # если пользователь найден, отправляем его
    return person


@person_router.post("/api/users", response_model=PersonResponseSchema)
def create_person(person: PersonCreateSchema, db: Session = Depends(get_db)):
    db_person = Person(name=person.name, age=person.age)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


@person_router.put("/api/users")
def edit_person(data=Body(), db: Session = Depends(get_db)):

    # получаем пользователя по id
    person = db.query(Person).filter(Person.id == data["id"]).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    person.age = data["age"]
    person.name = data["name"]
    db.commit()  # сохраняем изменения
    db.refresh(person)
    return person


@person_router.delete("/api/users/{id}")
def delete_person(id, db: Session = Depends(get_db)):
    # получаем пользователя по id
    person = db.query(Person).filter(Person.id == id).first()

    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})

    # если пользователь найден, удаляем его
    db.delete(person)  # удаляем объект
    db.commit()  # сохраняем изменения
    return person
