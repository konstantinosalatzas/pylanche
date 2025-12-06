import sqlite3
import json

class State:
    def __init__(self, id: str):
        self.id = id # the id key
        self.events = {}
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