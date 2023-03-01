from fake_rate import fake_rate_NBU
from fastapi import FastAPI

app = FastAPI(title="Trading App")


fake_user = [
    {"id": 1, "role": "admin", "name": "admin"},
    {"id": 2, "role": "manager", "name": "Bob"},
    {"id": 3, "role": "user", "name": "Meri"},
]


@app.get("/user/{user_id}")
def get_user(user_id: int):
    for user in fake_user:
        if user.get("id") == user_id:
            return user.get("name")
    return "No user"


@app.post("/user/{user_id}")
def update_user_name(user_id: int, new_name: str):
    update_user = list(filter(lambda user: user.get("id") == user_id, fake_user))[0]
    update_user["name"] = new_name
    return {"status": 200, "data": update_user}


@app.get("/rate")
async def get_rate(limit: int = 5, offset: int = 0):
    return fake_rate_NBU[offset:][:limit]
