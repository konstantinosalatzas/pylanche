import os
import json
import logging

from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.aio import EventHubProducerClient

from pylanche.receive import receive
from pylanche.send import send

def get_config(config: dict[str, str]) -> tuple[str, ...]  | None:
    try:
        BLOB_STORAGE_CONNECTION_STRING = config['BLOB_STORAGE_CONNECTION_STRING']
        BLOB_CONTAINER_NAME = config['BLOB_CONTAINER_NAME']
        EVENT_HUB_CONNECTION_STRING = config['EVENT_HUB_CONNECTION_STRING']
        EVENT_HUB_NAME = config['EVENT_HUB_NAME']
        RECEIVE_DURATION = config['RECEIVE_DURATION']
        SEND_COUNT = config['SEND_COUNT']
        return (BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME, EVENT_HUB_CONNECTION_STRING, EVENT_HUB_NAME, RECEIVE_DURATION, SEND_COUNT)
    except Exception as exception:
        logging.info(str(exception))
        return None

class Client:
    def __init__(self, op: str):
        # Get the environment variables.
        config = get_config(os.environ)
        if config != None:
            (BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME, EVENT_HUB_CONNECTION_STRING, EVENT_HUB_NAME, RECEIVE_DURATION, SEND_COUNT) = config
            logging.info("Got the configuration values from the environment variables.")
        else:
            logging.info("Failed to get the configuration values from the environment variables.")
            # Read the configuration file.
            with open("./pylanche/config.json", "r") as config_file:
                config = json.load(config_file)
                try:
                    (BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME, EVENT_HUB_CONNECTION_STRING, EVENT_HUB_NAME, RECEIVE_DURATION, SEND_COUNT) = get_config(config)
                    logging.info("Read the configuration file.")
                except Exception as error:
                    logging.error(str(error))
                    logging.info("Failed to get the configuration values from the configuration file.")

        if op == "receive":
            # Create an Azure blob checkpoint store to store the checkpoints.
            checkpoint_store = BlobCheckpointStore.from_connection_string(
                BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME
            )
            # Create a consumer client to receive events from the event hub.
            self.consumer = EventHubConsumerClient.from_connection_string(
                EVENT_HUB_CONNECTION_STRING,
                consumer_group="$Default",
                eventhub_name=EVENT_HUB_NAME,
                checkpoint_store=checkpoint_store
            )
            self.RECEIVE_DURATION = RECEIVE_DURATION
        elif op == "send":
            # Create a producer client to send events to the event hub.
            self.producer = EventHubProducerClient.from_connection_string(
                conn_str=EVENT_HUB_CONNECTION_STRING, eventhub_name=EVENT_HUB_NAME
            )
            self.SEND_COUNT = SEND_COUNT

    def perform(self, op: str):
        if op == "receive":
            receive(self.consumer, self.RECEIVE_DURATION)
        elif op == "send":
            send(self.producer, self.SEND_COUNT)