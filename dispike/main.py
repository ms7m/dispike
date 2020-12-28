from fastapi import FastAPI
import typing
from loguru import logger
from .server import router, DiscordVerificationMiddleware
from .server import interaction as router_interaction
from .register import RegisterCommands
from .register.models import DiscordCommand
from .models import IncomingApplicationCommand

from .errors.network import DiscordAPIError

import uvicorn

if typing.TYPE_CHECKING:
    import httpx


class Dispike(object):
    def __init__(self, client_public_key: str, bot_token: str, application_id: str):

        self._bot_token = bot_token
        self._application_id = application_id
        self._registrator = RegisterCommands(
            application_id=self._application_id, bot_token=self._bot_token
        )
        self._internal_application = FastAPI()
        self._internal_application.add_middleware(
            DiscordVerificationMiddleware, client_public_key=client_public_key
        )
        self._internal_application.include_router(router=router)

    def reset_registration(self, new_bot_token=None, new_application_id=None):
        try:
            if new_bot_token == None:
                _bot_token = self._bot_token
            else:
                _bot_token = new_bot_token

            if new_application_id == None:
                _application_id = self._application_id
            else:
                _application_id = new_application_id
            self._registrator = RegisterCommands(
                application_id=_application_id, bot_token=_bot_token
            )
            return True
        except Exception:
            return False

    @property
    def interaction(self):
        return router_interaction

    @property
    def referenced_application(self):
        return self._internal_application

    @property
    def register(self) -> RegisterCommands.register:
        return self._registrator.register

    @property
    def shared_client(self) -> "httpx.Client":
        return self._registrator._client

    def get_commands(
        self, guild_only=False, guild_id_passed=None
    ) -> typing.List[IncomingApplicationCommand]:
        """Returns a list of ``DiscordCommands`` either globally or for a specific guild.

        Args:
            guild_only (bool, optional): whether to target a guild. Defaults to False.
            guild_id_passed ([type], optional): guild id if guild_only is set to True. Defaults to None.

        Raises:
            DiscordAPIError: any Discord returned errors.

        Returns:
            typing.List[DiscordCommand]: Array of DiscordCommand
        """
        if guild_only == True:
            if guild_id_passed == False:
                raise TypeError(
                    "You cannot have guild_only == True and NOT pass any guild id."
                )
            _url = f"/guilds/{guild_id_passed}/commands"
        else:
            _url = f"/commands"

        try:
            _send_request = self._registrator._client.get(
                _url, headers=self._registrator.request_headers
            )
            if _send_request.status_code == 200:
                return [IncomingApplicationCommand(**x) for x in _send_request.json()]

            raise DiscordAPIError(_send_request.status_code, _send_request.text)
        except DiscordAPIError:
            logger.exception("Discord API Failure.")
            raise
        except Exception:
            logger.exception("Unknown exception returned")
            raise

    def edit_command(
        self,
        command_id: int,
        new_command: DiscordCommand,
        guild_only=False,
        guild_id_passed=None,
    ) -> DiscordCommand:
        """Edits a command provided with a command_id and a valid new command.

        Args:
            command_id (int): Command ID
            new_command (DiscordCommand): A valid DiscordCommand object (or a dict with proper syntax, if a dict is passed no verification will be made and discord will return the syntax error)
            guild_only (bool, optional): whether to target a guild. Defaults to False.
            guild_id_passed ([type], optional): guild id if guild_only is set to True. Defaults to None.

        Raises:
            TypeError: Invalid types passed.
            DiscordAPIError: any Discord returned errors.

        Returns:
            DiscordCommand: Returns the DiscordCommand object created. (Will return a DiscordCommand irregardless of new_command)
        """
        if not isinstance(new_command, (DiscordCommand, dict)):
            raise TypeError("New command must be a DiscordCommand or a valid dict.")

        if guild_only == True:
            if guild_id_passed == False:
                raise TypeError(
                    "You cannot have guild_only == True and NOT pass any guild id."
                )
            _url = f"/guilds/{guild_id_passed}/commands/{command_id}"
        else:
            _url = f"/commands/{command_id}"

        _new_command = new_command.dict()
        try:
            _send_request = self._registrator._client.patch(
                _url, headers=self._registrator.request_headers, json=_new_command
            )
            if _send_request.status_code != 200:
                raise DiscordAPIError(_send_request.status_code, _send_request.text)
            return DiscordCommand(**_send_request.json())
        except DiscordAPIError:
            logger.exception("Discord API Failure.")
            return False
        except Exception:
            logger.exception("Unknown exception returned")
            return False

    def delete_command(
        self, command_id: int, guild_only=False, guild_id_passed=None
    ) -> bool:
        """Deletes a command, provided with a command_id

        Args:
            command_id (int): Command ID required
            guild_only (bool, optional): Whether to be a global action or target a guild. Defaults to False.
            guild_id_passed ([type], optional): Guild ID if guild_only is set to True. Defaults to None.

        Raises:
            TypeError: Invalid types passed.
            DiscordAPIError: any Discord returned errors.

        Returns:
            bool: True if status code is 201, otherwise will LOG exception and return False.
        """
        if guild_only == True:
            if guild_id_passed == False:
                raise TypeError(
                    "You cannot have guild_only == True and NOT pass any guild id."
                )
            _url = f"/guilds/{guild_id_passed}/commands/{command_id}"
        else:
            _url = f"/commands/{command_id}"

        try:
            _send_request = self._registrator._client.delete(
                _url, headers=self._registrator.request_headers
            )
            if _send_request.status_code != 204:
                raise DiscordAPIError(_send_request.status_code, _send_request.text)
            return True
        except DiscordAPIError:
            logger.exception("Discord API Failure.")
            return False
        except Exception:
            logger.exception("Unknown exception returned")
            return False

    def run(self, port: int = 5000):
        uvicorn.run(app=self.referenced_application, port=port)