import json

from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.aio import EventHubProducerClient

from pylanche.recv import receive
from pylanche.send import send

class Client:
    def __init__(self, op: str):
        # Read the configuration file.
        with open('./pylanche/event_hub.json', 'r') as file:
            event_hub_config = json.load(file)

        EVENT_HUB_CONN_STR = event_hub_config['EVENT_HUB_CONN_STR']
        EVENT_HUB_NAME = event_hub_config['EVENT_HUB_NAME']
               
        if op == "receive":
            BLOB_STORAGE_CONN_STR = event_hub_config['BLOB_STORAGE_CONN_STR']
            BLOB_CONTAINER_NAME = event_hub_config['BLOB_CONTAINER_NAME']
            # Create an Azure blob checkpoint store to store the checkpoints.
            checkpoint_store = BlobCheckpointStore.from_connection_string(
                BLOB_STORAGE_CONN_STR, BLOB_CONTAINER_NAME
            )

            # Create a consumer client for the event hub.
            self.consumer = EventHubConsumerClient.from_connection_string(
                EVENT_HUB_CONN_STR,
                consumer_group="$Default",
                eventhub_name=EVENT_HUB_NAME,
                checkpoint_store=checkpoint_store
            )

            self.RECEIVE_DURATION = event_hub_config['RECEIVE_DURATION']
        elif op == "send":
            # Create a producer client to send messages to the event hub.
            self.producer = EventHubProducerClient.from_connection_string(
                conn_str=EVENT_HUB_CONN_STR, eventhub_name=EVENT_HUB_NAME
            )

            self.SEND_COUNT = event_hub_config['SEND_COUNT']

    def receive(self):
        receive(self.consumer, self.RECEIVE_DURATION)

    def send(self):
        send(self.producer, self.SEND_COUNT)