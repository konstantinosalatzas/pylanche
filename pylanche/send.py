import asyncio

from azure.eventhub import EventData

async def run(producer, SEND_COUNT: int):
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        for i in range(0, SEND_COUNT):
            event_data_batch.add(EventData(f"Event {str(i+1)}"))
        
        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

def send(producer, SEND_COUNT: int):
    asyncio.run(run(producer, SEND_COUNT))