import asyncio
import json
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

async def main(EVENT_HUB_CONNECTION_STR: str, EVENT_HUB_NAME: str):
    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string(
        EVENT_HUB_CONNECTION_STR,
        consumer_group="$Default",
        eventhub_name=EVENT_HUB_NAME
    )
    async with client:
        # Call the receive method. Read from the beginning of the
        # partition (starting_position: "-1")
        await client.receive(on_event=on_event, starting_position="-1")


def receive():
    # Read the configuration file. (TODO: replace with environment variables)
    with open('./pylanche/event_hub.json', 'r') as file:
        event_hub_config = json.load(file)
        EVENT_HUB_CONNECTION_STR = event_hub_config['EVENT_HUB_CONNECTION_STR']
        EVENT_HUB_NAME = event_hub_config['EVENT_HUB_NAME']

    asyncio.run(main(EVENT_HUB_CONNECTION_STR, EVENT_HUB_NAME))