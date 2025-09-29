import json
import logging

def parse(message: str) -> dict | None:
    try:
        data = json.loads(message)
    except ValueError: # The message is not in JSON format.
        return None
    return data