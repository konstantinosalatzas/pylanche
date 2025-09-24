import json
import logging

def parse(message: str) -> dict | None:
    try:
        data = json.loads(message)
    except ValueError: # The message is not in JSON format.
        print("Failed to parse the message as JSON.")
        logging.info("Failed to parse the message as JSON.")
        return None
    
    print('Parsed the message: "{}"'.format(str(data)))
    logging.info('Parsed the message: "{}"'.format(str(data)))
    
    return data