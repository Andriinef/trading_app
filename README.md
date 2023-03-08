# FastApi

## Пример создания модели user в fastapi

Конкретная модель для пользователя может выглядеть по-разному в зависимости от того, какие данные вы хотите хранить. Однако, общая структура модели может выглядеть так:

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = False
```

Здесь мы определяем модель пользователя с помощью базовой модели Pydantic, которая позволяет нам определять поля и их типы. В этой модели мы определяем следующие поля:

* id - идентификатор пользователя, который будет являться уникальным идентификатором пользователя в базе данных;
* username - имя пользователя, которое он будет использовать для входа в систему;
* email - адрес электронной почты пользователя, который будет использоваться для отправки уведомлений и других сообщений;
* password - пароль пользователя, который будет храниться в хэшированном виде в базе данных;
* full_name - полное имя пользователя, которое может быть опциональным;
* disabled - флаг, который указывает, отключен ли пользователь в настоящее время.

Как только вы определили модель пользователя, вы можете использовать ее для создания маршрутов API с помощью FastAPI. Например, вы можете создать маршрут, который позволяет пользователю зарегистрироваться в системе, используя следующий код:

```python
from fastapi import FastAPI
from .models import User

app = FastAPI()

@app.post("/users/")
async def create_user(user: User):
    # Создание пользователя в базе данных
    # Возврат данных пользователя
    return user
```

Здесь мы определяем маршрут POST /users/, который принимает модель пользователя в качестве входных данных и создает нового пользователя в базе данных. Затем мы возвращаем данные пользователя в качестве ответа на запрос.

Это простой пример использования модели пользователя в FastAPI, который может быть адаптирован для вашей конкретной системы.

## пример  создания модели users с помощью sqlalchemy

Конкретная модель для пользователей с помощью SQLAlchemy может выглядеть так:

```python
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from typing import Optional


Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    full_name = Column(String, default="")
    disabled = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    role = relationship("Role", backref="users")


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: str = None
    disabled: bool = False
    role_id: int = None
```

Здесь мы определяем модель пользователя с помощью SQLAlchemy. В этой модели мы определяем следующие поля:

* id - идентификатор пользователя, который будет являться уникальным идентификатором пользователя в базе данных;
* username - имя пользователя, которое он будет использовать для входа в систему;
* email - адрес электронной почты пользователя, который будет использоваться для отправки уведомлений и других сообщений;
* password - пароль пользователя, который будет храниться в базе данных;
* full_name - полное имя пользователя, которое может быть опциональным;
* disabled - флаг, который указывает, отключен ли пользователь в настоящее время.

Здесь мы также определяем таблицу с именем users с помощью атрибута __tablename__. Мы также определяем индексы для полей username и email, чтобы обеспечить быстрый доступ к этим полям в базе данных.

## Базы данных SQLAlchemy

Вот пример модуля database.py, который определяет объект engine для соединения с базой данных и для создания объектов сессии базы данных SQLAlchemy:

```python
from databases import Database
from sqlalchemy import MetaData, create_engine
from os import getenv

# SQLAlchemy specific code, as with any other app
# DATABASE_URL = "sqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = getenv("DATABASE_URL")

database = Database(
    # DATABASE_URL
    SQLALCHEMY_DATABASE_URL
    )

metadata = MetaData()

engine = create_engine(
    # DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL
)
metadata.create_all(engine)
```
