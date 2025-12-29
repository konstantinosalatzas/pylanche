import asyncio
import logging
import json
import csv

from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from azure.storage.blob import ContainerClient

async def main(producer: EventHubProducerClient, container_client: ContainerClient, FILE_NAME: str, count: str):
    # Download file from container.
    with open(file="/tmp/pylanche_data_to_send.csv", mode="wb") as tmp_file:
        tmp_file.write(container_client.download_blob(FILE_NAME).readall())
        print("Downloaded file from container.")
        logging.info("Downloaded file from container.")

    print("Producer will send events.")
    logging.info("Producer will send events.")

    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        with open("/tmp/pylanche_data_to_send.csv") as tmp_file: # Read downloaded file.
            reader = csv.DictReader(tmp_file)
            for row in reader:
                event_data_str = json.dumps(row)
                event_data_batch.add(EventData(event_data_str))

        # Add events to the batch.
        for i in range(0, int(count)):
            event_data_dict = {"id": str(i+1)}
            event_data_str = json.dumps(event_data_dict)
            event_data_batch.add(EventData(event_data_str))
        
        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

    print("Producer sent events.")
    logging.info("Producer sent events.")

def send(producer: EventHubProducerClient, container_client: ContainerClient, FILE_NAME: str, count: str):
    asyncio.run(main(producer, container_client, FILE_NAME, count))