import asyncio

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

async def run(EVENT_HUB_CONNECTION_STR: str, EVENT_HUB_NAME: str, SEND_COUNT: int):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
    )
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        for i in range(1, SEND_COUNT+1):
            event_data_batch.add(EventData(f"Event {str(i)}"))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

def send(EVENT_HUB_CONNECTION_STR: str, EVENT_HUB_NAME: str, SEND_COUNT: int):
    asyncio.run(run(EVENT_HUB_CONNECTION_STR, EVENT_HUB_NAME, SEND_COUNT))