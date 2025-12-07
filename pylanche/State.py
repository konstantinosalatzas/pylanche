import sqlite3
import json
import logging

from pylanche.utils import get_config_from_environ_or_file

# Holds the event processing state of the execution.
class State:
    def __init__(self):
        config = get_config_from_environ_or_file()
        (BLOB_STORAGE_CONNECTION_STRING, BLOB_CONTAINER_NAME, EVENT_HUB_CONNECTION_STRING, EVENT_HUB_NAME, RECEIVE_DURATION, SEND_COUNT, STATE_ID) = config
        logging.info("Got the configuration values.")

        self.id = STATE_ID
        self.events = {} # {'0': {'id': '0', 'key': 'value', ...}, ...}
        self.connection = sqlite3.connect("./pylanche/state.db")
        self.cursor = self.connection.cursor()

    def update(self, event: dict):
        state_id = self.id
        state_events = self.events

        if state_id in event:
            state_events[event[state_id]] = event # upsert state
    
    def pull_from_db(self):
        table = self.cursor.execute("SELECT * FROM state").fetchall()

        events = {}
        for row in table:
            events[str(row[0])] = json.loads(row[1])
        
        self.events = events
    
    def push_to_db(self):
        events = self.events
        
        rows = []
        for id in events:
            rows.append((id, json.dumps(events[id])))
        
        # TODO
        self.cursor.execute("DELETE FROM state")
        self.cursor.executemany("INSERT INTO state VALUES (?, ?)", rows)
        self.connection.commit()
    
    def clean_up(self):
        self.cursor.execute("DELETE FROM state")
        self.connection.commit()