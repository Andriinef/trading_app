from pydantic import BaseModel, EmailStr, Field


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr


class UserPostSchema(UserCreateSchema):
    password: str


class UserSchema(UserCreateSchema):
    id: int

    class Config:
        orm_mode = True


class UserResponseSchema(BaseModel):
    results: list[UserSchema] = Field(
        description="Includes the list of User response schema",
        default_factory=list,
    )
