import logging

from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.aio import EventHubProducerClient
from azure.storage.blob import BlobServiceClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

from pylanche.utils import get_config_from_environ_or_file
from pylanche.receive import receive
from pylanche.send import send
from pylanche.anonymize import anonymize

class Client:
    def __init__(self, op: str):
        config = get_config_from_environ_or_file()
        (BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME, EVENT_HUB_CONNECTION_STRING, EVENT_HUB_NAME, RECEIVE_DURATION, FILE_NAME, LANGUAGE_KEY, LANGUAGE_ENDPOINT) = config
        logging.info("Got the configuration values.")

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

        if op == "send":
            # Create a producer client to send events to the event hub.
            self.producer = EventHubProducerClient.from_connection_string(
                conn_str=EVENT_HUB_CONNECTION_STRING, eventhub_name=EVENT_HUB_NAME
            )

            # Connect to storage account.
            blob_service_client = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
            # Create container client.
            self.container_client = blob_service_client.get_container_client(container=BLOB_CONTAINER_NAME)
            self.FILE_NAME = FILE_NAME
        
        if op == "anonymize":
            # Create and authenticate client.
            credential = AzureKeyCredential(LANGUAGE_KEY)
            self.text_analytics_client = TextAnalyticsClient(endpoint=LANGUAGE_ENDPOINT, credential=credential)

    def perform(self, op: str, param: None | str) -> None | str:
        if op == "receive":
            return receive(self.consumer, self.RECEIVE_DURATION)
        if op == "send":
            return send(self.producer, self.container_client, self.FILE_NAME, param)
        if op == "anonymize":
             return anonymize(self.text_analytics_client, param)