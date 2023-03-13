from pydantic import BaseModel, EmailStr, Field


class UserPostSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr


class UserSchema(UserCreateSchema):
    id: int

    class Config:
        orm_mode = True


class UserResponseSchema(BaseModel):
    results: list[UserSchema] = Field(
        description="Includes the list of User response schema",
        default_factory=list,
    )
