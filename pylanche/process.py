import json
import logging

def process(message: str) -> dict | None:
    try:
        data = json.loads(message)
    except ValueError: # The message is not in JSON format.
        print("Failed to parse the message as JSON.")
        logging.info("Failed to parse the message as JSON.")
        return None
    
    print('Processed the event: "{}"'.format(str(data)))
    logging.info('Processed the event: "{}"'.format(str(data)))
    
    return data