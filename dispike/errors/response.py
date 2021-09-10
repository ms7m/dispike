class ContentIsEmpty(Exception):
    def __str__(self) -> str:
        return "No string was passed for content. You must add a text content to a DiscordResponse"

    def __repr__(self) -> str:
        return "No string was passed for content. You must add a text content to a DiscordResponse"


class InvalidDiscordResponse(Exception):
    pass


class NoResolvedInteractions(Exception):
    pass