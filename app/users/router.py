# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from .models import Role, RoleCreate, SessionLocal, User, UserCreate, database

# users_router = APIRouter(prefix="/users", tags=["users"])


# # Зависимость для создания объекта сессии базы данных SQLAlchemy


# def get_database():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @users_router.on_event("startup")
# async def startup():
#     await database.connect()


# @users_router.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


# # Обработчик маршрута для создания новой роли


# @users_router.post("/roles/")
# def create_role(role: RoleCreate, db: Session = Depends(get_database)):
#     db_role = Role(name=role.name, description=role.description)
#     db.add(db_role)
#     db.commit()
#     db.refresh(db_role)
#     return db_role


# # Обработчик маршрута для создания нового пользователя


# @users_router.post("/users/")
# def create_user(user: UserCreate, db: Session = Depends(get_database)):
#     db_user = User(
#         email=user.email,
#         hashed_password=user.hashed_password,
#         is_active=user.is_active,
#         role_id=user.role_id,
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# # Обработчик маршрута для добавления первой записи в таблицу ролей и пользователей


# @users_router.post("/init")
# async def init_database(db: Session = Depends(get_database)):
#     # Создаем роль "admin"
#     admin_role = Role(name="admin", description="Administrator")
#     db.add(admin_role)
#     db.commit()
#     db.refresh(admin_role)

#     # Создаем пользователя с ролью "admin"
#     admin_user = User(
#         email="admin@example.com",
#         hashed_password="password",
#         is_active=True,
#         role_id=admin_role.id,
#     )
#     db.add(admin_user)
#     db.commit()
#     db.refresh(admin_user)

#     return {"message": "Database initialized successfully."}
