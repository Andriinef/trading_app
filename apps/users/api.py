import bcrypt
from apps.db.get_db import get_db
from apps.users.models import User
from apps.users.shemas import (
    UserCreateSchema,
    UserPostSchema,
    UserResponseSchema,
    UserSchema,
)
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

app = APIRouter(prefix="/users", tags=["users"])


@app.post("/users/", response_model=UserResponseSchema)
def create_user(user: UserPostSchema = Body(...), db: Session = Depends(get_db)):
    # Хешируем пароль пользователя
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponseSchema(results=[db_user])


@app.get("/users/", response_model=UserResponseSchema)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_results = db.query(User).offset(skip).limit(limit).all()
    if user_results is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    user: list[UserSchema] = [UserSchema.from_orm(user) for user in user_results]
    return UserResponseSchema(results=user)


@app.get("/users/{user_id}", response_model=UserResponseSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user_results = db.query(User).filter(User.id == user_id).first()
    if user_results is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    user: list[UserSchema] = [UserSchema.from_orm(user_results)]
    return UserResponseSchema(results=user)


@app.put("/users/{user_id}", response_model=UserResponseSchema)
def update_user(user_id: int, user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    # db_user.username = user.username
    # db_user.email = user.email
    update_user = user.dict(exclude_unset=True)
    for key, value in update_user.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return UserResponseSchema(results=[db_user])


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    db.delete(db_user)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Пользователь удален"})
