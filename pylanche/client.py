import json

from pylanche.recv import receive
from pylanche.send import send

class client:
    def __init__(self):
        # Read the configuration file.
        with open('./pylanche/event_hub.json', 'r') as file:
            event_hub_config = json.load(file)
            self.EVENT_HUB_CONNECTION_STR = event_hub_config['EVENT_HUB_CONNECTION_STR']
            self.EVENT_HUB_NAME = event_hub_config['EVENT_HUB_NAME']

    def receive(self):
        receive(self.EVENT_HUB_CONNECTION_STR, self.EVENT_HUB_NAME)

    def send(self):
        send(self.EVENT_HUB_CONNECTION_STR, self.EVENT_HUB_NAME)
