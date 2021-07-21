class DiscordAPIError(Exception):
    # TODO: Add detection for more distinct exceptions based on api codes.
    def __init__(self, status_code, request_text):
        self.message = f"Discord API returned an unexpected response back [{status_code}]: {request_text}"

    def __str__(self):
        return self.message
