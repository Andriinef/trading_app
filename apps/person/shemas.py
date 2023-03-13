from pydantic import BaseModel, Field


class PersonCreateSchema(BaseModel):
    name: str
    age: int


class PersonSchema(PersonCreateSchema):
    id: int

    class Config:
        orm_mode = True


class PersonResponseSchema(BaseModel):
    results: list[PersonSchema] = Field(
        description="Includes the list of Person response schema",
        default_factory=list,
    )
