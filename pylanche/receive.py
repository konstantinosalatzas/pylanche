import asyncio
import logging

from azure.eventhub.aio import EventHubConsumerClient

from pylanche.process import parse

async def on_event(partition_context, event):
    message = event.body_as_str(encoding="UTF-8")
    
    # Print the event data.
    print('Received the event: "{}" from the partition with ID: "{}"'.format(message, partition_context.partition_id))
    logging.info('Received the event: "{}" from the partition with ID: "{}"'.format(message, partition_context.partition_id))
    
    # Process the event data.
    parse(message)
    
    # Update the checkpoint so that the program doesn't read the events that it has already read when it runs next time.
    await partition_context.update_checkpoint(event)

async def main(consumer: EventHubConsumerClient, RECEIVE_DURATION: float):
    print("Consumer will keep receiving for {} seconds.".format(RECEIVE_DURATION))
    logging.info("Consumer will keep receiving for {} seconds.".format(RECEIVE_DURATION))

    async with consumer:
        task = asyncio.ensure_future(
            consumer.receive(
                on_event=on_event,
                starting_position="-1",  # "-1" is from the beginning of the partition.
            )
        )
        await asyncio.sleep(RECEIVE_DURATION)
    await task

    print("Consumer has stopped receiving.")
    logging.info("Consumer has stopped receiving.")

def receive(consumer: EventHubConsumerClient, RECEIVE_DURATION: float):
    asyncio.run(main(consumer, RECEIVE_DURATION))