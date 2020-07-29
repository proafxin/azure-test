from azure.servicebus import Message
from datetime import datetime

def form_message(payload):
    message = {}
    message['payload'] = payload
    now = datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    message['timestamp'] = now

    return Message(message)