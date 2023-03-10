from typing import List

from fastapi import APIRouter

from .database import database
from .models import Note, NoteIn, notes

notes_router = APIRouter(prefix="/notes", tags=["notes"])


@notes_router.on_event("startup")
async def startup():
    await database.connect()


@notes_router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@notes_router.get("/notes/", response_model=List[Note])
async def read_notes():
    query = notes.select()
    return await database.fetch_all(query)


@notes_router.post("/notes/", response_model=Note)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}
