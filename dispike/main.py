from fastapi import FastAPI
import typing
from loguru import logger
from .server import router, DiscordVerificationMiddleware
from .server import interaction as router_interaction
from .register import RegisterCommands
from .register.models import DiscordCommand
from .models import IncomingApplicationCommand

from .errors.network import DiscordAPIError
import asyncio

if typing.TYPE_CHECKING:
    import httpx  # pragma: no cover
    from .eventer import EventHandler  # pragma: no cover


class Dispike(object):

    """Dispike - python library for interacting with discord slash commands via an independently hosted server.

    *Powered by FastAPI*
    """

    def __init__(
        self, client_public_key: str, bot_token: str, application_id: str, **kwargs
    ):
        """Initialize Dispike Object

        Args:
            client_public_key (str): Discord provided client public key.
            bot_token (str): Discord provided bot token. You must create a bot user to view this!
            application_id (str): Discord provided Client ID
            custom_context_argument_name (str, optional): Change the name of the context arugment when passing to a function. Set to "ctx".
        """
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
        if not kwargs.get("custom_context_argument_name"):
            router._user_defined_setting_ctx_value = "ctx"
        else:
            router._user_defined_setting_ctx_value = kwargs.get(
                "custom_context_argument_name"
            )

        self._cache_router = router

    def reset_registration(self, new_bot_token=None, new_application_id=None):
        """This method resets the built-in RgeisterCommands.
        You should not have to call this method directly.

        Call it only if you change the client id or bot token.

        Args:
            new_bot_token (None, optional): Description
            new_application_id (None, optional): Description

        Returns:
            TYPE: bool
        """
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
            self._bot_token = _bot_token
            self._application_id = _application_id
            return True
        except Exception:
            return False

    @staticmethod
    async def background(function: typing.Callable, *args, **kwargs):
        logger.debug(f"register background to function {function}")
        return asyncio.create_task(function(*args, **kwargs))

    @property
    def interaction(self) -> "EventHandler":
        """Returns an already initialized ``EventHandler`` object.
        You will use this method to handle incoming commands.

        Returns:
            EventHandler: shared EventHandler
        """
        return router_interaction

    @property
    def referenced_application(self) -> FastAPI:
        """Returns the internal FastAPI object that was initialized.
        You are welcome to edit this with the appropriate settings found in
        the FastAPI docs.

        Returns:
            FastAPI: a pre-configured FastAPI object with required middlewares.
        """
        return self._internal_application

    @property
    def register(self) -> RegisterCommands.register:
        """Returns a shortcut the RegisterCommands.register function

        Returns:
            RegisterCommands.register: internal RegisterCommands Object
        """
        return self._registrator.register

    @property
    def shared_client(self) -> "httpx.Client":
        """Returns a pre-initialized ``httpx.Client`` that is used for requests internally.

        Returns:
            httpx.Client: used for network requests to discord.
        """
        return self._registrator._client

    def get_commands(
        self, guild_only=False, guild_id_passed=None
    ) -> typing.List[IncomingApplicationCommand]:
        """Returns a list of ``DiscordCommands`` either globally or for a specific guild.

        Args:
            guild_only (bool, optional): whether to target a guild. Defaults to False.
            guild_id_passed ([type], optional): guild id if guild_only is set to True. Defaults to None.

        Returns:
            typing.List[DiscordCommand]: Array of DiscordCommand

        Raises:
            DiscordAPIError: any Discord returned errors.
        """
        if guild_only == True:
            if guild_id_passed == False or not isinstance(guild_id_passed, str):
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
        new_command: typing.Union[typing.List[DiscordCommand], DiscordCommand],
        command_id: int = None,
        bulk=False,
        guild_only=False,
        guild_id_passed=None,
    ) -> DiscordCommand:
        """Edits a command provided with a command_id and a valid new command.

        Args:
            command_id (int): Command ID
            new_command ([DiscordCommand, List[DiscordCommand]]): A valid DiscordCommand object (or a dict with proper syntax, if a dict is passed no verification will be made and discord will return the syntax error)
            guild_only (bool, optional): whether to target a guild. Defaults to False.
            guild_id_passed (bool, optional): guild id if guild_only is set to True. Defaults to None.
            bulk (bool, optional): Whether to specifiy if this action will be a bulk action.

        Returns:
            DiscordCommand: Returns the DiscordCommand object created. (Will return a DiscordCommand irregardless of new_command)

        Raises:
            TypeError: Invalid types passed.
            DiscordAPIError: any Discord returned errors.
        """

        if not isinstance(new_command, (DiscordCommand, dict, list)):
            raise TypeError("New command must be a DiscordCommand or a valid dict.")

        if guild_only == True:
            if guild_id_passed == False:
                raise TypeError(
                    "You cannot have guild_only set to True and NOT pass any guild id."
                )
            if bulk == True:
                _url = f"/guilds/{guild_id_passed}/commands"
            else:
                _url = f"/guilds/{guild_id_passed}/commands/{command_id}"
        else:
            _url = "/commands"
        if bulk == True and isinstance(new_command, list):
            _new_command = [command.dict() for command in new_command]
            _selected_request_method = "PUT"
        else:
            _new_command = new_command.dict()
            _selected_request_method = "PATCH"
        try:
            _send_request = self._registrator._client.request(
                method=_selected_request_method,
                url=_url,
                headers=self._registrator.request_headers,
                json=_new_command,
            )
            if _send_request.status_code != 200:
                raise DiscordAPIError(_send_request.status_code, _send_request.text)

            if bulk == True:
                return [DiscordCommand(**x) for x in _send_request.json()]
            else:
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

        Returns:
            bool: True if status code is 201, otherwise an error will be raised.

        Raises:
            TypeError: Invalid types passed.
            DiscordAPIError: any Discord returned errors.
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
            raise
        except Exception:
            logger.exception("Unknown exception returned")
            raise

    @staticmethod
    def _return_uvicorn_run_function():
        """Import uvicorn, only exists to make testing easier. You do not need to import this.

        Raises:
            SystemExit: If uvicorn is not installed

        Returns:
            uvicorn: If everything works out.
        """
        try:
            import uvicorn

            return uvicorn
        except Exception:
            raise SystemExit(
                "Uvicorn is not installed. Please use a different webserver pointing to <..>.referenced_application"
            )

    def run(self, port: int = 5000):

        """Runs the bot with the already-installed Uvicorn webserver.

        Args:
            port (int, optional): Port to run the bot over. Defaults to 5000.
        """

        uvicorn = self._return_uvicorn_run_function()
        uvicorn.run(app=self.referenced_application, port=port)