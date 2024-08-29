#https://tequila.kiwi.com/portal/docs/tequila_api/search_api

import requests
from datetime import datetime
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
whatsapp_num_from = os.environ["WHATSAPP_NUMBER_FROM"]
whatsapp_num_to = os.environ["WHATSAPP_NUMBER_TO"]
TEQUILA_AUTH_TOKEN = os.environ["TEQUILA_AUTH_TOKEN"]

client = Client(account_sid, auth_token)

def send_msg(msg):
    client.messages.create(
        body = msg,
        from_ = f"whatsapp:{whatsapp_num_from}",
        to = f"whatsapp:{whatsapp_num_to}",
    )

dt_obj = lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")

url = "https://api.tequila.kiwi.com/v2/search"

headers = {
    "apikey": TEQUILA_AUTH_TOKEN
}

params = {
    "fly_from": "BCN",
    "fly_to": "GRU",
    "date_from": "29/11/2024",
    "date_to": "29/11/2024",
    "return_from": "07/01/2025",
    "return_to": "07/01/2025",
    "adults": 1,
    "curr": "EUR",
    "select_airlines": "AZ"
}

response = requests.get(url=url, headers=headers, params=params)
r = response.json()['data']

r.sort(key=lambda x: x["price"])

top_3 = r[0:3]

all_msg = list()

for f in top_3:
    price = f['price']
    outbound_from = f['route'][0]['cityFrom']
    outbound_to = f['route'][1]['cityTo']
    outbound_departure = dt_obj(f['route'][0]['local_departure']).strftime("%d/%m/%Y - %H:%M")
    outbound_arrival = dt_obj(f['route'][1]['local_arrival']).strftime("%d/%m/%Y - %H:%M")
    outbound_flight_duration_obj = dt_obj(f['route'][1]['utc_arrival']) - dt_obj(f['route'][0]['utc_departure'])
    outbound_flight_duration_hours = int(outbound_flight_duration_obj.total_seconds() // 3600)
    outbound_flight_duration_minutes = int((outbound_flight_duration_obj.total_seconds() % 3600) // 60)
    outbound_flight_duration = f"{outbound_flight_duration_hours} hours {outbound_flight_duration_minutes} minutes"
    inbound_from = f['route'][2]['cityFrom']
    inbound_to = f['route'][3]['cityTo']
    inbound_departure = dt_obj(f['route'][2]['local_departure']).strftime("%d/%m/%Y - %H:%M")
    inbound_arrival = dt_obj(f['route'][3]['local_arrival']).strftime("%d/%m/%Y - %H:%M")
    inbound_flight_duration_obj = dt_obj(f['route'][3]['utc_arrival']) - dt_obj(f['route'][2]['utc_departure'])
    inbound_flight_duration_hours = int(inbound_flight_duration_obj.total_seconds() // 3600)
    inbound_flight_duration_minutes = int((inbound_flight_duration_obj.total_seconds() % 3600) // 60)
    inbound_flight_duration = f"{inbound_flight_duration_hours} hours {inbound_flight_duration_minutes} minutes"
    msg = f"""*Price*: {price} €
*{outbound_from} > {outbound_to}*
Departure 🛫: {outbound_departure}
Arraival 🛬: {outbound_arrival}
Duration 🕑: {outbound_flight_duration}
*{inbound_from} > {inbound_to}*
Departure 🛫: {inbound_departure}
Arraival 🛬: {inbound_arrival}
Duration 🕑: {inbound_flight_duration}"""
    
    all_msg.append(msg)


for m in all_msg:
    send_msg(m)


## Need to clean up and refact, better msg, Init and End msg and add ability to track an specific flight based on flight num