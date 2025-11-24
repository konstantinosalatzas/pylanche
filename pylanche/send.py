import asyncio
import logging

from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

async def main(producer: EventHubProducerClient, SEND_COUNT: str):
    print("Producer will send {} events.".format(SEND_COUNT))
    logging.info("Producer will send {} events.".format(SEND_COUNT))

    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        for i in range(0, int(SEND_COUNT)):
            event_data_str = '{"id": "'+str(i+1)+'"}'
            event_data_batch.add(EventData(event_data_str))
        
        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

    print("Producer sent {} events.".format(SEND_COUNT))
    logging.info("Producer sent {} events.".format(SEND_COUNT))

def send(producer: EventHubProducerClient, SEND_COUNT: str):
    asyncio.run(main(producer, SEND_COUNT))