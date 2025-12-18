import asyncio
import logging
import json

from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from azure.storage.blob import ContainerClient

async def main(producer: EventHubProducerClient, container_client: ContainerClient, SEND_COUNT: str):
    # Download file from container.
    with open(file="/tmp/pylanche.csv", mode="wb") as tmp_file:
        tmp_file.write(container_client.download_blob("data.csv").readall())
        print("Downloaded file from container.")
        logging.info("Downloaded file from container.")

    print("Producer will send {} events.".format(SEND_COUNT))
    logging.info("Producer will send {} events.".format(SEND_COUNT))

    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        for i in range(0, int(SEND_COUNT)):
            #event_data_str = '{"id": "'+str(i+1)+'"}'
            event_data_dict = {"id": str(i+1)}
            event_data_str = json.dumps(event_data_dict)
            event_data_batch.add(EventData(event_data_str))
        
        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

    print("Producer sent {} events.".format(SEND_COUNT))
    logging.info("Producer sent {} events.".format(SEND_COUNT))

def send(producer: EventHubProducerClient, container_client: ContainerClient, SEND_COUNT: str):
    asyncio.run(main(producer, container_client, SEND_COUNT))