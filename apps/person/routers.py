from apps.db.db import SessionLocal
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .models import Person
from .shemas import PersonCreateSchema, PersonResponseSchema, PersonSchema

person_router = APIRouter(prefix="/person", tags=["person"])

# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@person_router.get("/api/users", response_model=PersonResponseSchema)
def get_people(db: Session = Depends(get_db)):
    # получаем пользователей
    person_results = db.query(Person).all()
    if person_results is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    person: list[PersonSchema] = [PersonSchema.from_orm(person) for person in person_results]
    return PersonResponseSchema(results=person)


@person_router.get("/api/users/{id}", response_model=PersonResponseSchema)
def get_person(id, db: Session = Depends(get_db)):
    # получаем пользователя по id
    person_results = db.query(Person).filter(Person.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person_results == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # если пользователь найден, отправляем его
    return PersonResponseSchema(results=[person_results])


@person_router.post("/api/users", response_model=PersonResponseSchema)
def create_person(person: PersonCreateSchema = Body(...), db: Session = Depends(get_db)):
    person_results = Person(name=person.name, age=person.age)
    db.add(person_results)
    db.commit()
    db.refresh(person_results)
    return PersonResponseSchema(results=[person_results])


@person_router.put("/api/users", response_model=PersonSchema)
def edit_person(id: int, data: PersonCreateSchema = Body(...), db: Session = Depends(get_db)):

    # получаем пользователя по id
    person = db.query(Person).filter(Person.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if person == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    person.age = data.age  # type: ignore
    person.name = data.name  # type: ignore
    db.commit()  # сохраняем изменения
    db.refresh(person)  # обновляем объект в базе данных.
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
    return JSONResponse(status_code=200, content={"message": "Пользователь удален"})
