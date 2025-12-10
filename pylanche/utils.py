import logging
import os
import json

def get_config(config: dict[str, str]) -> tuple[str, ...]  | None:
    try:
        BLOB_STORAGE_CONNECTION_STRING = config['BLOB_STORAGE_CONNECTION_STRING']
        BLOB_CONTAINER_NAME = config['BLOB_CONTAINER_NAME']
        EVENT_HUB_CONNECTION_STRING = config['EVENT_HUB_CONNECTION_STRING']
        EVENT_HUB_NAME = config['EVENT_HUB_NAME']
        RECEIVE_DURATION = config['RECEIVE_DURATION']
        SEND_COUNT = config['SEND_COUNT']
        STATE_ID = config['STATE_ID']
    except Exception as error:
        logging.info(str(error))
        return None
    return (BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME, EVENT_HUB_CONNECTION_STRING, EVENT_HUB_NAME, RECEIVE_DURATION, SEND_COUNT, STATE_ID)

# Call get_config() with input depending on the configuration.
def get_config_from_environ_or_file() -> tuple[str, ...]:
        # Get the environment variables.
        config = get_config(os.environ)
        if config == None:
            logging.info("Failed to get the configuration values from the environment variables.")
            # Read the configuration file.
            with open("./pylanche/config.json", "r") as config_file:
                config = get_config(json.load(config_file))
                if config == None:
                    logging.info("Failed to get the configuration values from the configuration file.")
        return config