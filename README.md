# FastApi

## пример  создания модели users с помощью sqlalchemy

Конкретная модель для пользователей с помощью SQLAlchemy может выглядеть так:

```python
from sqlalchemy import Column, Integer, String, Boolean


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
from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = getenv("DATABASE_URL")
Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(
    # DATABASE_URL
    SQLALCHEMY_DATABASE_URL
)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

## Alembic для миграции базы данных

Чтобы использовать Alembic для миграции базы данных в FastAPI, нужно выполнить несколько шагов:

1. Установите alembic и SQLAlchemy:

    ```code
    pipenv install alembic sqlalchemy
    ```

2. Инициализируйте Alembic:

    ```code
    alembic init ./migration/
    ```

3. Сделайте в корневом каталоге вашего проекта файл alembic.ini следующие изменения:

    ```code
    [alembic]
    script_location = alembic
    sqlalchemy.url = driver://user:pass@localhost/dbname
    ```

    необходимо заменить driver://user:pass@localhost/dbname на URL вашей базы данных, например postgresql://user:password@localhost:port/mydatabase.

4. Создайте модель базы данных с помощью SQLAlchemy в вашем приложении FastAPI.

5. В файле migration/env.py сделайте изменение в строке target_metadata = None:

    ```python
    from db.db import DATABASE_URL, Base

    target_metadata = Base.metadata
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
    ```

6. Сгенерируйте начальную миграцию Alembic:

    ```code
    alembic revision --autogenerate -m "Initial migration"
    ```

7. Примените миграцию к базе данных:

    ```code
    alembic upgrade head
    ```

8. Добавьте миграцию в систему контроля версий и повторите шаги 5-7 при каждом изменении модели базы данных.
