from httpx import Client
from .models import DiscordCommand
from loguru import logger
from ..errors.network import DiscordAPIError


class RegisterCommands(object):
    def __init__(self, application_id: str, bot_token: str):
        self.__bot_token = bot_token
        self._application_id = application_id
        self._client = Client(
            base_url=f"https://discord.com/api/v8/applications/{self._application_id}/"
        )

    def register(
        self, command: DiscordCommand, guild_only=False, guild_to_target: int = None
    ):
        if guild_only == True:
            if guild_to_target is None:
                raise TypeError(
                    "if guild_only is set to true, a guild id must be provided."
                )

            logger.info(f"Targeting a specific guild -> {guild_to_target}")
            _request_url = f"guilds/{guild_to_target}/commands"
        else:
            _request_url = f"commands"

        try:
            _command_to_json = command.dict()
            _send_request = self._client.post(
                _request_url, headers=self.request_headers, json=command.dict()
            )
            if _send_request.status_code in [200, 201]:
                return True

            raise DiscordAPIError(_send_request.status_code, _send_request.text)
        except Exception:
            raise

    @property
    def request_headers(self):
        return {"Authorization": f"Bot {self.__bot_token}"}

    @property
    def bot_token(self):
        raise PermissionError("You cannot view the bot token directly.")

    @bot_token.setter
    def bot_token(self, new_bot_token):
        if new_bot_token == self.__bot_token:
            raise TypeError("Bot token already set to that.")
        self.__bot_token = new_bot_token