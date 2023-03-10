from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .currency.router import currency_router
from .fake_user_trades.router import trades_router
from .person.routers import person_router
from .tickets.api import tickets_router

app = FastAPI()


app.include_router(trades_router)
app.include_router(currency_router)
app.include_router(tickets_router)
app.include_router(person_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
