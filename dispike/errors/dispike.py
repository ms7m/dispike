class BotTokenNotProvided(Exception):
    """Exception that is raised when you attempt to use a certain
    function, method or class without providing a bot token.
    """

    def __init__(self, functionality_name: str = "unknown"):
        self.func_name = functionality_name

    def __str__(self) -> str:
        return f"This functionality ({self.func_name}) cannot be used without supplying a bot token to Dispike"

    def __repr__(self) -> str:
        return f"This functionality ({self.func_name}) cannot be used without supplying a bot token to Dispike"