class UnknownInteractionType(BaseException):
    def __init__(self, interaction_type: int):
        """Exception raised internally for when an interaction is recived but it's type is not handled by this library.
        You should never get this.

        Args:
            interaction_type (int): interaction type recieved
        """
        self.interaction_type = interaction_type

    def __str__(self) -> str:
        return f"Unknown type from Discord recieved. ({self.interaction_type}). You shouldn't have recieve this error. Please file a bug with us."