from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .currency_data import update_currency_data_file

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


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


@app.get("/user/{user_id}", response_model=list[User])
def get_user(user_id: int):
    for user in fake_user:
        if user.get("id") == user_id:
            user_list = []
            user_list.append(user)
            return user_list


@app.post("/user_/{user_id}", deprecated=True)
def update_user_name_(user_id: int, new_name: str):
    update_user = list(filter(lambda user: user.get("id") == user_id, fake_user))[0]
    update_user["name"] = new_name
    return {"status": 200, "data": update_user}


@app.post("/user/{user_id}", response_model=list[User])
async def update_user_name(user_id: int, new_name: str):
    for user in fake_user:
        if user.get("id") == user_id:
            update_user = user
            update_user["name"] = new_name
            return {"status": 200, "data": update_user}

    return {"status": 404, "data": f"User with id {user_id} not found"}


@app.get("/currency_data")
async def get_currency_data(limit: int = 1, offset: int = 24):
    currency_data_file = update_currency_data_file()
    # currency_data = currency_data_file[offset:][:limit]
    # new_currency_data = []
    # for item in currency_data:
    #     dict_currency_data = {}
    #     for key, value in item.items():
    #         if key=="txt" or key=="currency_data":
    #             dict_currency_data[key] = value
    #     new_currency_data.append(dict_currency_data)
    new_currency_data = [
        {key: value for key, value in item.items() if key == "cc" or key == "rate" or key == "exchangedate"}
        for item in currency_data_file[offset:][:limit]
    ]
    return new_currency_data


@app.get("/currency_price")
async def get_price(from_in: str = "USD", to: str = "EUR"):
    from_in = from_in.upper()
    to = to.upper()
    currency_data_file: list[dict] = update_currency_data_file()
    new_currency_data = []
    if from_in == "UAH" or to == "UAH":
        new_currency_data.append({"cc": "UAH", "rate": 1.00})
    for item in currency_data_file:
        dict_currency_data = {}
        for key, value in item.items():
            if value == from_in or value == to:
                dict_currency_data[key] = value
                for key, value in item.items():
                    if key == "rate":
                        dict_currency_data[key] = value
        if dict_currency_data:
            new_currency_data.append(dict_currency_data)
    return new_currency_data


"""Currency calculator"""


@app.post("/currency_data")
async def get_currency(sum: float = 100.00, from_in: str = "USD", to: str = "EUR") -> dict:
    from_in = from_in.upper()
    to = to.upper()

    currency_data_file: list[dict] = update_currency_data_file()

    from_dict = {"cc": "UAH", "rate": 1.00} if from_in == "UAH" else None
    to_dict = {"cc": "UAH", "rate": 1.00} if to == "UAH" else None

    for item in currency_data_file:
        if item["cc"] == from_in:
            from_dict = {key: value for key, value in item.items() if key in ["cc", "rate"]}
        elif item["cc"] == to:
            to_dict = {key: value for key, value in item.items() if key in ["cc", "rate"]}

    if from_dict and to_dict:
        if "rate" not in from_dict or not isinstance(from_dict["rate"], (int, float)):
            return {"status": 503, "result": "Invalid exchange rate in from_dict"}
        if "rate" not in to_dict or not isinstance(to_dict["rate"], (int, float)):
            return {"status": 504, "result": "Invalid exchange rate in to_dict"}

        conversion_factor = from_dict["rate"] / to_dict["rate"]
        sum *= conversion_factor

    else:
        if from_dict:
            return {"status": 404, "result": f"{to} currency does not exist"}
        return {"status": 404, "result": f"{from_in} currency does not exist"}

    return {"result": f"{round(sum, 2)} {to}", "from": from_dict, "to": to_dict}


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "USD", "side": "sell", "price": 100.00, "amount": 5.0},
    {"id": 2, "user_id": 2, "currency": "USD", "side": "sell", "price": 102.00, "amount": 6.0},
    {"id": 3, "user_id": 3, "currency": "USD", "side": "sell", "price": 105.00, "amount": 15.0},
    {"id": 4, "user_id": 4, "currency": "USD", "side": "sell", "price": 109.99, "amount": 2.5},
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    site: str
    price: float = Field(ge=0)
    amount: float


# @app.post("/tredis")
# def add_tredis(tredis: list[Trade]):
#     fake_trades.extend(tredis)
#     return {"status": 200, "data": fake_trades}
