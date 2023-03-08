from app.database.database import metadata
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, Table

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String(255)),
    Column("completed", Boolean),
)


class NoteIn(BaseModel):
    text: str
    completed: bool


class Note(BaseModel):
    id: int
    text: str
    completed: bool