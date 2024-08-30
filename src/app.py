from datetime import datetime

from whatsapp import send_msg
from flights import get_flight_data
from msg import get_best_price_day_msg

fly_from = "BCN"
fly_to = "GRU"
departure_date = "29/11/2024"
return_dates_list = ["07/01/2025", "08/01/2025", "09/01/2025", "10/01/2025"]

all_msg = []

for r_date in return_dates_list:
    flight_data = get_flight_data(fly_from, fly_to, departure_date, r_date, airlines="AZ")
    m = get_best_price_day_msg(flight_data)
    all_msg.append(m)


send_msg(f"Best {fly_from} > {fly_to} prices\n{str(datetime.now())}")
for m in all_msg:
    send_msg(m)

## Need to clean up and refact, better msg, Init and End msg and add ability to track an specific flight based on flight num