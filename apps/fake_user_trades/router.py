from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

fake_user = [
    {"id": 1, "role": "admin", "name": "admin"},
    {"id": 2, "role": "manager", "name": "Bob"},
    {
        "id": 3,
        "role": "user",
        "name": "Meri",
        "degree": [{"id": 1, "create_at": "2022-01-01T00:00:00", "type_degree": "expert"}],
    },
]


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "USD", "side": "sell", "price": 100.00, "amount": 5.0},
    {"id": 2, "user_id": 2, "currency": "USD", "side": "sell", "price": 102.00, "amount": 6.0},
    {"id": 3, "user_id": 3, "currency": "USD", "side": "sell", "price": 105.00, "amount": 15.0},
    {"id": 4, "user_id": 4, "currency": "USD", "side": "sell", "price": 109.99, "amount": 2.5},
]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    create_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[list[Degree]] = []


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    site: str
    price: float = Field(ge=0)
    amount: float


trades_router = APIRouter(prefix="/trades", tags=["trades"])


@trades_router.get("/user/{user_id}", response_model=list[User])
def get_user(user_id: int):
    for user in fake_user:
        if user.get("id") == user_id:
            user_list = []
            user_list.append(user)
            return user_list


@trades_router.post("/user_lambda/{user_id}")
def update_user_name_lambda(user_id: int, new_name: str):
    update_user = list(filter(lambda user: user["id"] == user_id, fake_user))
    if not update_user:
        return {"status": 404, "data": f"User with id {user_id} not found"}

    update_user[0]["name"] = new_name
    return {"status": 200, "data": update_user[0]}


@trades_router.post("/user/{user_id}")
def update_user_name(user_id: int, new_name: str):
    update_user = next((user for user in fake_user if user["id"] == user_id), None)
    if update_user is None:
        return {"status": 404, "data": f"User with id {user_id} not found"}

    update_user["name"] = new_name
    return {"status": 200, "data": update_user}


# @trades_router.post("/tredis")
# def add_tredis(tredis: list[Trade]):
#     fake_trades.extend(tredis)
#     return {"status": 200, "data": fake_trades}
