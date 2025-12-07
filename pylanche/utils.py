import logging

def get_config(config: dict[str, str]) -> tuple[str, ...]  | None:
    try:
        BLOB_STORAGE_CONNECTION_STRING = config['BLOB_STORAGE_CONNECTION_STRING']
        BLOB_CONTAINER_NAME = config['BLOB_CONTAINER_NAME']
        EVENT_HUB_CONNECTION_STRING = config['EVENT_HUB_CONNECTION_STRING']
        EVENT_HUB_NAME = config['EVENT_HUB_NAME']
        RECEIVE_DURATION = config['RECEIVE_DURATION']
        SEND_COUNT = config['SEND_COUNT']
    except Exception as error:
        logging.info(str(error))
        return None
    return (BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME, EVENT_HUB_CONNECTION_STRING, EVENT_HUB_NAME, RECEIVE_DURATION, SEND_COUNT)