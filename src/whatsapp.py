from twilio.rest import Client
import os
import time
from dotenv import load_dotenv
load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
whatsapp_num_from = os.environ["WHATSAPP_NUMBER_FROM"]
whatsapp_num_to = os.environ["WHATSAPP_NUMBER_TO"]

client = Client(account_sid, auth_token)

def send_msg(msg):
    client.messages.create(
        body = msg,
        from_ = f"whatsapp:{whatsapp_num_from}",
        to = f"whatsapp:{whatsapp_num_to}",
    )
    time.sleep(0.5)