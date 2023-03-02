import requests
from fastapi import FastAPI

app = FastAPI(title="Trading App")

"""Currency calculator"""


@app.post("/currency_data/")
async def get_currency(sum: float = 100.00, from_in: str = "USD", to: str = "EUR") -> dict:
    from_in = from_in.upper()
    to = to.upper()

    currency_data_file: list[dict] = requests.get(
        "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    ).json()

    from_dict = {"cc": "UAH", "rate": 1.00} if from_in == "UAH" else None
    to_dict = {"cc": "UAH", "rate": 1.00} if to == "UAH" else None

    for item in currency_data_file:
        if item["cc"] == from_in:
            from_dict = {key: value for key, value in item.items() if key in ["cc", "rate"]}
        elif item["cc"] == to:
            to_dict = {key: value for key, value in item.items() if key in ["cc", "rate"]}

    if from_dict and to_dict:
        if "rate" not in from_dict or not isinstance(from_dict["rate"], (int, float)):
            return {"status": 404, "result": "Invalid exchange rate in from_dict"}
        if "rate" not in to_dict or not isinstance(to_dict["rate"], (int, float)):
            return {"status": 404, "result": "Invalid exchange rate in to_dict"}

        conversion_factor = from_dict["rate"] / to_dict["rate"]
        sum *= conversion_factor

    else:
        if from_dict:
            return {"status": 404, "result": f"{to} currency does not exist"}
        return {"status": 404, "result": f"{from_in} currency does not exist"}

    return {"result": f"{round(sum, 2)} {to}", "from": from_dict, "to": to_dict}
