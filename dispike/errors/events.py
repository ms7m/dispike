class InvalidEventType(Exception):
    def __init__(self, event_type_passed):
        self._event_type_value = type(event_type_passed)

    def __str__(self):
        return f"An invalid event type: {self._event_type_value} was passed. An event type must be a string!"
