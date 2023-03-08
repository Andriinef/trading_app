from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .currency.router import currency_router
from .fake_user_trades.router import trades_router
from .notes.router import notes_router

# from users.router import users_router

app = FastAPI()


app.include_router(trades_router)
app.include_router(currency_router)
# app.include_router(users_router)
app.include_router(notes_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
