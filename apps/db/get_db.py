# Dependency
from apps.db.db import SessionLocal


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore
