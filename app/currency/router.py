import requests
from fastapi import APIRouter

currency_router = APIRouter(prefix="/currency", tags=["currency"])


def update_currency_data_file():
    return requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json").json()


@currency_router.get("/currency_data")
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


@currency_router.get("/currency_price")
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


@currency_router.post("/currency_data")
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
