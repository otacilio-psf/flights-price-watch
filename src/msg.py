from datetime import datetime

dt_obj = lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ")

def get_best_price_day_msg(flight_data):

    flight_data.sort(key=lambda x: x["price"])
    flight = flight_data[0]

    price = flight['price']*(1-0.05)

    outbound_from = flight['route'][0]['cityFrom']
    outbound_to = flight['route'][1]['cityTo']

    outbound_departure_date = dt_obj(flight['route'][0]['local_departure']).strftime("%d/%m/%Y")
    outbound_departure_time = dt_obj(flight['route'][0]['local_departure']).strftime("%H:%M")
    outbound_arrival_time = dt_obj(flight['route'][1]['local_arrival']).strftime("%H:%M")

    outbound_flight_duration_sec = flight['duration']['departure']
    outbound_flight_duration_hours = int(outbound_flight_duration_sec // 3600)
    outbound_flight_duration_minutes = int((outbound_flight_duration_sec % 3600) // 60)
    outbound_flight_duration = f"duration {outbound_flight_duration_hours:02d}:{outbound_flight_duration_minutes:02d}"

    inbound_departure_date = dt_obj(flight['route'][2]['local_departure']).strftime("%d/%m/%Y")
    inbound_departure_time = dt_obj(flight['route'][2]['local_departure']).strftime("%H:%M")
    inbound_arrival_time = dt_obj(flight['route'][3]['local_arrival']).strftime("%H:%M")

    inbound_flight_duration_sec = flight['duration']['return']
    inbound_flight_duration_hours = int(inbound_flight_duration_sec // 3600)
    inbound_flight_duration_minutes = int((inbound_flight_duration_sec % 3600) // 60)
    inbound_flight_duration = f"duration {inbound_flight_duration_hours:02d}:{inbound_flight_duration_minutes:02d}"

    msg = f"""*{outbound_from}* ✈️ *{outbound_to}*
{outbound_departure_date} <> {inbound_departure_date}
Departure: {outbound_departure_time} » {outbound_arrival_time} - {outbound_flight_duration}
Return:  {inbound_departure_time} » {inbound_arrival_time} - {inbound_flight_duration}
*Price* 💸: {price} €"""
    
    return msg