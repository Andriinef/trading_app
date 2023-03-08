# from typing import Optional

# import databases
# from pydantic import BaseModel
# from sqlalchemy import (
#     Boolean,
#     Column,
#     ForeignKey,
#     Integer,
#     MetaData,
#     String,
#     create_engine,
# )
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker

# # Создаем объект базы данных SQLAlchemy
# Base = declarative_base()


# # SQLAlchemy specific code, as with any other app
# DATABASE_URL = "sqlite:///./test.db"
# # DATABASE_URL = "postgresql://user:password@postgresserver/db"

# database = databases.Database(DATABASE_URL)

# metadata = MetaData()


# class Role(Base):
#     __tablename__ = "roles"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50), unique=True, index=True, nullable=False)
#     description = Column(String(255), nullable=True)


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(50), unique=True, index=True, nullable=False)
#     email = Column(String(100), unique=True, index=True, nullable=False)
#     password = Column(String(100), nullable=False)
#     full_name = Column(String(100), nullable=True)
#     disabled = Column(Boolean, default=False)
#     role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
#     role = relationship("Role", backref="users")

#     class Config:
#         orm_mode = True


# # Создаем объект базы данных SQLAlchemy
# engine = create_engine(
#     # SQLALCHEMY_DATABASE_URL
#     DATABASE_URL,
#     connect_args={"check_same_thread": False},
# )

# # Создаем объект-фабрику для создания объектов сессии базы данных SQLAlchemy
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Создание таблицы roles в базе данных
# metadata.create_all(bind=engine)


# class RoleCreate(BaseModel):
#     name: str
#     description: Optional[str] = None


# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str
#     full_name: str = None
#     disabled: bool = False
#     role_id: int = None
