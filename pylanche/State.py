class State:
    def __init__(self, id):
        self.id = id # the id key
        self.events = {}

    def update(self, event: dict):
        state_id = self.id
        state_events = self.events
        if state_id in event:
            state_events[event[state_id]] = event # upsert state
    
    def push_to_db(self):
        pass