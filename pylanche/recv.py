import asyncio
import logging

from azure.eventhub.aio import EventHubConsumerClient

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

async def main(EVENT_HUB_CONNECTION_STR: str, EVENT_HUB_NAME: str, RECEIVE_DURATION: float):
    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string(
        EVENT_HUB_CONNECTION_STR,
        consumer_group="$Default",
        eventhub_name=EVENT_HUB_NAME
    )
    async with client:
        # Call the receive method. Read from the beginning of the
        # partition (starting_position: "-1")
        #await client.receive(on_event=on_event, starting_position="-1")

        # The receive method is a coroutine which will be blocking when awaited.
        # It can be executed in an async task for non-blocking behavior, and combined with the 'close' method.

        recv_task = asyncio.ensure_future(client.receive(on_event=on_event, starting_position="-1"))
        await asyncio.sleep(RECEIVE_DURATION)  # keep receiving for 3 seconds
        recv_task.cancel()  # stop receiving

def receive(EVENT_HUB_CONNECTION_STR: str, EVENT_HUB_NAME: str, RECEIVE_DURATION: float):
    asyncio.run(main(EVENT_HUB_CONNECTION_STR, EVENT_HUB_NAME, RECEIVE_DURATION))