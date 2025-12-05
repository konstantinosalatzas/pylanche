import sqlite3

class State:
    def __init__(self, id: str):
        self.id = id # the id key
        self.events = {}

    def update(self, event: dict):
        state_id = self.id
        state_events = self.events
        if state_id in event:
            state_events[event[state_id]] = event # upsert state
    
    def pull_from_db(self):
        connection = sqlite3.connect("./pylanche/state.db")
        cursor = connection.cursor()

        table = cursor.execute("SELECT * FROM state").fetchall()

        events = {}
        for row in table:
            events[row[0]] = row[1]
        
        self.events = events
    
    def push_to_db(self):
        events = self.events
        
        rows = []
        for id in events:
            rows.append((id, events[id]))
        
        connection = sqlite3.connect("./pylanche/state.db")
        cursor = connection.cursor()
        cursor.executemany("INSERT INTO state VALUES (?, ?)", rows)
        connection.commit()