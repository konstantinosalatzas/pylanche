import asyncio
import logging

from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import (
    BlobCheckpointStore,
)

async def on_event(partition_context, event):
    # Print the event data.
    print(
        'Received the event: "{}" from the partition with ID: "{}"'.format(
            event.body_as_str(encoding="UTF-8"), partition_context.partition_id
        )
    )
    logging.info(
        'Received the event: "{}" from the partition with ID: "{}"'.format(
            event.body_as_str(encoding="UTF-8"), partition_context.partition_id
        )
    )

    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)

async def main(EVENT_HUB_CONNECTION_STR: str, EVENT_HUB_NAME: str, RECEIVE_DURATION: float, BLOB_STORAGE_CONNECTION_STRING: str, BLOB_CONTAINER_NAME: str):
    # Create an Azure blob checkpoint store to store the checkpoints.
    checkpoint_store = BlobCheckpointStore.from_connection_string(
        BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME
    )

    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string(
        EVENT_HUB_CONNECTION_STR,
        consumer_group="$Default",
        eventhub_name=EVENT_HUB_NAME,
        checkpoint_store=checkpoint_store
    )

    print("Consumer will keep receiving for {} seconds.".format(RECEIVE_DURATION))
    logging.info("Consumer will keep receiving for {} seconds.".format(RECEIVE_DURATION))

    async with client:
        task = asyncio.ensure_future(
            client.receive(
                on_event=on_event,
                starting_position="-1",  # "-1" is from the beginning of the partition.
            )
        )
        await asyncio.sleep(RECEIVE_DURATION)
    await task

    print("Consumer has stopped receiving.")
    logging.info("Consumer has stopped receiving.")

def receive(EVENT_HUB_CONNECTION_STR: str, EVENT_HUB_NAME: str, RECEIVE_DURATION: float, BLOB_STORAGE_CONNECTION_STRING: str, BLOB_CONTAINER_NAME: str):
    asyncio.run(main(EVENT_HUB_CONNECTION_STR, EVENT_HUB_NAME, RECEIVE_DURATION, BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME))