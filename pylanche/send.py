import asyncio
import json

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

async def run():
    # Read the configuration file
    with open("./pylanche/event_hub.json", 'r') as file:
        event_hub_config = json.load(file)
        EVENT_HUB_CONNECTION_STR = event_hub_config['EVENT_HUB_CONNECTION_STR']
        EVENT_HUB_NAME = event_hub_config['EVENT_HUB_NAME']

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
        event_data_batch.add(EventData("First event "))
        event_data_batch.add(EventData("Second event"))
        event_data_batch.add(EventData("Third event"))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

def send():
    asyncio.run(run())