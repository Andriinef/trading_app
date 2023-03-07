import requests


def update_currency_data_file():
    return requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json").json()
