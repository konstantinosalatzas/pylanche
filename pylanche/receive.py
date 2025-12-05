import asyncio
import logging

from azure.eventhub.aio import EventHubConsumerClient

from pylanche.process import parse
from pylanche.State import State

async def on_event(partition_context, event):
    message = event.body_as_str(encoding="UTF-8")
    
    # Print the event data.
    print("Received the event: {} from the partition with ID: {}".format(message, partition_context.partition_id))
    logging.info("Received the event: {} from the partition with ID: {}".format(message, partition_context.partition_id))
    
    # Process the event data.
    data = parse(message)
    if data != None:
        print("Parsed the message: {}".format(str(data)))
        logging.info("Parsed the message: {}".format(str(data)))
        
        state = State(id="id")
        print("Created state: {}".format(str(state.events)))
        logging.info("Created state: {}".format(str(state.events)))

        state.pull_from_db()
        print("Pulled state: {}".format(str(state.events)))
        logging.info("Pulled state: {}".format(str(state.events)))

        state.update(data)
        print("Updated state: {}".format(str(state.events)))
        logging.info("Updated state: {}".format(str(state.events)))

        state.push_to_db()
        print("Pushed state.")
        logging.info("Pushed state.")
    
    # Update the checkpoint so that the program doesn't read the events that it has already read when it runs next time.
    await partition_context.update_checkpoint(event)

async def on_error(partition_context, error):
    # partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(partition_context.partition_id, error))
        logging.info("An exception: {} occurred during receiving from Partition: {}.".format(partition_context.partition_id, error))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))
        logging.info("An exception: {} occurred during the load balance process.".format(error))

async def main(consumer: EventHubConsumerClient, RECEIVE_DURATION: str):
    print("Consumer will keep receiving for {} seconds.".format(RECEIVE_DURATION))
    logging.info("Consumer will keep receiving for {} seconds.".format(RECEIVE_DURATION))

    async with consumer:
        task = asyncio.ensure_future(
            consumer.receive(
                on_event=on_event,
                on_error=on_error,
                starting_position="-1",  # "-1" is from the beginning of the partition.
            )
        )
        await asyncio.sleep(int(RECEIVE_DURATION))
    await task

    print("Consumer has stopped receiving.")
    logging.info("Consumer has stopped receiving.")

def receive(consumer: EventHubConsumerClient, RECEIVE_DURATION: str):
    asyncio.run(main(consumer, RECEIVE_DURATION))