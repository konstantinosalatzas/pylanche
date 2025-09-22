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

        if op == "receive":
            # Create an Azure blob checkpoint store to store the checkpoints.
            checkpoint_store = BlobCheckpointStore.from_connection_string(
                event_hub_config['BLOB_STORAGE_CONN_STR'], event_hub_config['BLOB_CONTAINER_NAME']
            )
            # Create a consumer client to receive events from the event hub.
            self.consumer = EventHubConsumerClient.from_connection_string(
                event_hub_config['EVENT_HUB_CONN_STR'],
                consumer_group="$Default",
                eventhub_name=event_hub_config['EVENT_HUB_NAME'],
                checkpoint_store=checkpoint_store
            )
            self.RECEIVE_DURATION = event_hub_config['RECEIVE_DURATION']
        elif op == "send":
            # Create a producer client to send events to the event hub.
            self.producer = EventHubProducerClient.from_connection_string(
                conn_str=event_hub_config['EVENT_HUB_CONN_STR'], eventhub_name=event_hub_config['EVENT_HUB_NAME']
            )
            self.SEND_COUNT = event_hub_config['SEND_COUNT']

    def perform(self, op: str):
        if op == "receive":
            receive(self.consumer, self.RECEIVE_DURATION)
        elif op == "send":
            send(self.producer, self.SEND_COUNT)