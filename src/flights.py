#https://tequila.kiwi.com/portal/docs/tequila_api/search_api
import requests
import os
from dotenv import load_dotenv
load_dotenv()

tequila_auth_token = os.environ["TEQUILA_AUTH_TOKEN"]

def get_flight_data(fly_from, fly_to, departure_date, return_date, airlines=False):

    url = "https://api.tequila.kiwi.com/v2/search"

    headers = {
        "apikey": tequila_auth_token
    }

    params = {
        "fly_from": fly_from,
        "fly_to": fly_to,
        "date_from": departure_date,
        "date_to": departure_date,
        "return_from": return_date,
        "return_to": return_date,
        "adults": 1,
        "curr": "EUR"
    }

    if airlines:
        params['select_airlines'] = airlines

    response = requests.get(url=url, headers=headers, params=params)
    return response.json()['data']


if __name__ == "__main__":
    print(get_flight_data("BCN", "GRU", "29/11/2024", "07/01/2025", airlines="AZ")[0])