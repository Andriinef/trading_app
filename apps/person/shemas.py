from pydantic import BaseModel


class PersonCreateSchema(BaseModel):
    name: str
    age: int


class PersonResponseSchema(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        orm_mode = True
