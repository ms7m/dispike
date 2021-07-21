class InvalidComponentError(Exception):
    def __init__(self, type):
        self.message = f"{type} is not a valid component class"

    def __str__(self):
        return self.message


class ComponentCombinationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SelectMenuOptionError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
