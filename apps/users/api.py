import bcrypt
from apps.db.db import SessionLocal
from apps.users.models import User
from apps.users.shemas import UserCreateSchema, UserPostSchema, UserResponseSchema
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

users_router = APIRouter(prefix="/users", tags=["users"])

# Dependency


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore


@users_router.post("/users/", response_model=UserResponseSchema)
def create_user(user: UserPostSchema, db: Session = Depends(get_db)):
    # Хешируем пароль пользователя
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserResponseSchema(results=[db_user])


@users_router.get("/users/", response_model=UserResponseSchema)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_results = db.query(User).offset(skip).limit(limit).all()
    return UserResponseSchema(results=user_results)  # type: ignore


@users_router.get("/users/{user_id}", response_model=UserResponseSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    return UserResponseSchema(results=[db_user])


@users_router.put("/users/{user_id}", response_model=UserResponseSchema)
def update_user(user_id: int, user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    db_user.username = user.username  # type: ignore
    db_user.email = user.email  # type: ignore
    db.commit()
    db.refresh(db_user)
    return UserResponseSchema(results=[db_user])


@users_router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    db.delete(db_user)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Пользователь удален"})
