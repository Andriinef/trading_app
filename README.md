# FastAPI framework

FastAPI - это современный веб-фреймворк для создания веб-приложений на языке Python, который известен своей скоростью, производительностью и простотой использования. Он основывается на типизации данных и асинхронности, что позволяет создавать масштабируемые и быстрые приложения.

Основные преимущества FastAPI:

* Скорость и производительность: FastAPI является одним из самых быстрых фреймворков на рынке Python. Он использует современные технологии, такие как ASGI (Asynchronous Server Gateway Interface) и Starlette, для обеспечения быстрой обработки запросов и масштабируемости приложений.
* Простота использования: FastAPI имеет простой и интуитивно понятный синтаксис, основанный на типизации данных и асинхронности. Он также предоставляет множество полезных инструментов, таких как автоматическая документация API и встроенный клиент для тестирования запросов.
* Поддержка стандартов: FastAPI полностью совместим с OpenAPI и JSON Schema, что позволяет легко создавать и документировать API.
* Активное сообщество: FastAPI имеет активное сообщество разработчиков и пользователей, которые постоянно работают над улучшением фреймворка и созданием новых инструментов и расширений.

FastAPI рекомендуется для создания масштабируемых веб-приложений на Python, особенно для приложений, где важна производительность и быстродействие.

## Тухнологии и библиотеки FastAPI

FastAPI основывается на нескольких технологиях и библиотеках Python, включая:

1. Starlette - это быстрый и легкий фреймворк для веб-приложений на Python, который используется в FastAPI для обработки запросов и маршрутизации.

2. Pydantic - это библиотека для валидации данных и сериализации объектов, которая используется в FastAPI для определения моделей данных и автоматической генерации документации.

3. OpenAPI - это стандарт для описания RESTful API, который используется в FastAPI для автоматической генерации документации API и клиентских библиотек.

4. JSON Schema - это язык для описания JSON-данных, который используется в FastAPI для валидации входных данных и определения типов данных.

5. ASGI - это интерфейс сервера для Python, который используется в FastAPI для обработки запросов асинхронно и обеспечения масштабируемости приложений.

6. Uvicorn - это ASGI-сервер, который используется в FastAPI для обработки запросов и управления соединениями.

FastAPI также использует нативную поддержку асинхронности в Python, что позволяет приложениям работать более эффективно и быстро обрабатывать большое количество запросов.

Перед тем как начать, убедитесь, что вы установили с помощью pipenv:

```code
pipenv install fastapi uvicorn sqlalchemy alembic psycopg2-binary
```

## Docker Compose для запуска PostgreSQL и FastAPI

Конфигурация Docker Compose для запуска PostgreSQL и FastAPI может выглядеть следующим образом:

```yaml
version: "3.9"

services:
  db:
    image: postgres
    container_name: "tickets_postgres"
    restart: always
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydatabase
    volumes:
      - postgres_data:/var/lib/postgresql/data


  app:
    build:
      context: .
      dockerfile: Dockerfile
    image: "tickets_app"
    container_name: "ttickets_app"
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://myuser:mypassword@db:5432/mydatabase
```

В этом файле мы создаем два сервиса: db и app. Сервис db использует официальный образ PostgreSQL и настраивает некоторые переменные среды для создания пользователя, пароля и базы данных. Сервис app использует наш собственный образ, который мы можем создать с помощью Dockerfile.

В сервисе app мы настраиваем команду запуска и пробрасываем порт 8000 для доступа к нашему FastAPI приложению. Мы также настраиваем зависимость от сервиса db, чтобы убедиться, что база данных будет запущена до того, как наше приложение начнет работу.

Наконец, мы настраиваем переменную среды DATABASE_URL, которая будет использоваться в нашем FastAPI приложении для подключения к базе данных. В этом примере мы используем имя пользователя, пароль и название базы данных, которые мы указали в сервисе db.

После того, как мы создали файл docker-compose.yml, мы можем запустить наше приложение с помощью команды:

```css
docker-compose up -d --build
```

Эта команда соберет наш образ приложения и запустит все сервисы, включая PostgreSQL и FastAPI. Теперь мы можем использовать наше приложение, доступное по адресу:

```http
http://localhost:8000/
```

## База данных PostgreSQL в FastAP

Вот пример файла database.py, который можно использовать для настройки подключения к базе данных PostgreSQL в FastAPI, используя библиотеку SQLAlchemy:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@db:5432/mydatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

В этом примере мы создаем экземпляр SQLAlchemy engine, который использует URL для подключения к базе данных PostgreSQL. Мы также создаем экземпляр sessionmaker, который будет использоваться для создания сессий базы данных в нашем приложении. Мы также определяем базовый класс declarative_base, который будет использоваться для создания моделей базы данных.

Этот файл можно использовать в других файлах FastAPI, чтобы получить доступ к базе данных. Например, в файле main.py можно импортировать объект SessionLocal и использовать его для создания сессий базы данных:

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import database, models
from .tickets.routers import tickets_router

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(tickets_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(database.SessionLocal)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return {"item_id": db_item.id, "item_name": db_item.name}
```

В этом примере мы определяем два маршрута FastAPI и используем параметр db для зависимости от сессии базы данных. Мы можем использовать эту сессию для выполнения запросов к базе данных и получения данных из таблицы Item.

## Models in FastAPI

Вот пример файла models.py для создания модели данных для системы управления билетами (tickets):

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    tickets = relationship("Ticket", back_populates="owner")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(String, index=True)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tickets")
```

В этом примере мы создаем две модели данных: User и Ticket. Модель User представляет пользователя системы управления билетами, которая имеет поля id, username, email и password. Мы также определяем отношение между моделями User и Ticket с помощью relationship, которое позволяет связать одного пользователя с несколькими билетами.

Модель Ticket представляет билет в системе управления билетами, которая имеет поля id, title, description и status. Мы также определяем отношение между моделями Ticket и User с помощью ForeignKey, который позволяет связать каждый билет с конкретным пользователем.

Обе модели данных наследуются от базового класса Base, который мы определили в файле database.py. Это позволяет нам использовать SQLAlchemy для создания таблиц в базе данных на основе этих моделей данных.

Мы можем использовать эти модели данных в других файлах FastAPI для выполнения операций с базой данных, таких как добавление новых пользователей и билетов, получение списка пользователей и билетов и т. д.

## Schemas in FastAPI

Вот пример файла schemas.py, который можно использовать для создания схем данных (data schemas) для системы управления билетами (tickets) в FastAPI:

```python
from typing import List, Optional
from pydantic import BaseModel

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int
    status: str
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    tickets: List[Ticket] = []

    class Config:
        orm_mode = True
```

В этом примере мы определяем четыре схемы данных: TicketBase, TicketCreate, Ticket и User. Схема TicketBase используется для определения общих полей для создания и обновления билетов, таких как title и description.

Схема TicketCreate наследует поля из TicketBase и используется для создания новых билетов.

Схема Ticket также наследует поля из TicketBase, но также добавляет дополнительные поля, такие как id, status и owner_id. Эта схема используется для возвращения данных о билете в ответах на запросы.

Схема UserBase используется для определения общих полей для создания и обновления пользователей, таких как username и email.

Схема UserCreate наследует поля из UserBase и добавляет поле password для создания новых пользователей.

Схема User также наследует поля из UserBase, но также добавляет дополнительное поле tickets, которое является списком билетов, принадлежащих пользователю. Эта схема используется для возвращения данных о пользователе в ответах на запросы.

Мы можем использовать эти схемы данных в других файлах FastAPI для проверки данных, передаваемых в запросах, и для сериализации данных, возвращаемых в ответах. Например, в файле routers.py мы можем использовать схему Ticket для возвращения списка всех билетов в системе.

## Управление миграциями базы данных в SQLAlchemy с использованием инструмента Alembic

Alembic - это инструмент для управления миграциями базы данных в SQLAlchemy. Он может использоваться для создания и применения миграций, которые изменяют схему базы данных, а также для генерации скриптов для отката миграций.
Вот пример файла миграций с использованием Alembic и изменениями в файле migration/env.py.

Чтобы использовать Alembic для миграции базы данных в FastAPI, нужно выполнить несколько шагов:

1. Инициализация проекта Alembic
Сначала мы инициализируем проект Alembic, создав файл alembic.ini и директорию migrations:

    ```code
    alembic init ./migration/
    ```

    Эта команда создаст файл alembic.ini и директорию migrations с файлом env.py внутри.

2. Настройка подключения к базе данных
Откройте файл alembic.ini и при необходимости укажите параметры подключения к вашей базе данных:

    ```code
    [alembic]
    # path to migration scripts
    script_location = ./migration/
    ....
    sqlalchemy.url = driver://user:pass@localhost/dbname
    ```

    При необходимости замените driver://user:pass@localhost/dbname на URL вашей базы данных, например postgresql://myuser:mypassword@db:5432/mydatabase.

3. В файле migration/env.py сделайте изменение в строке target_metadata = None:

    ```python
     from .database import DATABASE_URL, Base
     from .tickets.models import Ticket, User

    target_metadata = Base.metadata
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
    ```

    В этом примере мы к target_metadata подключает базу данных из файла database.py и указываем модели для создания таблиц: __tablename__ = "users" и __tablename__ = "ticket"

4. Создание первой миграции

    Создайте первую миграцию с помощью команды:

    ```code
    alembic revision --autogenerate -m "Initial table tickets and users"
    ```

    Эта команда создаст новый файл миграции в директории migrations с именем, содержащим временную метку и описание миграции.

5. Применение миграции

    Примените миграцию с помощью команды:

    ```code
    alembic upgrade head
    ```

    Эта команда применит все миграции, которые еще не были применены.

6. При внесении изменений или добавлении таблиц в models.py добавьте миграцию в систему контроля версий и повторите шаги 3-5 при каждом изменении модели базы данных.

## Примеры функций использующие FastAPI

Вот примеры функций get, post, put, delete в routers.py:

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Ticket as DBTicket, User as DBUser
from schemas import Ticket as TicketSchema, User as UserSchema

tickets_router = APIRouter(prefix="/tickets", tags=["Tickets"])

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@tickets_router.post("/users/")
def create_user(user: UserSchema, db: Session = Depends(get_db)):
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
def update_user(user_id: int, user: UserSchema, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
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
def create_ticket(ticket: TicketSchema, db: Session = Depends(get_db)):
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
```
