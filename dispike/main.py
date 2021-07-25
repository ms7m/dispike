import inspect
import typing
import warnings
from enum import Enum

from fastapi import FastAPI
from loguru import logger

from dispike.errors.events import InvalidEventType
from dispike.errors.warnings import InsecureBindingWithCustomHostWarning

from .models import IncomingApplicationCommand
from .register import RegisterCommands
from .register.models import DiscordCommand
from .server import DiscordVerificationMiddleware
from .server import interaction as router_interaction
from .server import router
from .interactions import EventCollection, PerCommandRegistrationSettings

import asyncio

import httpx

from .errors.network import DiscordAPIError
from .register.models.permissions import (
    GuildApplicationCommandPermissions,
    NewApplicationPermission,
)

if typing.TYPE_CHECKING:
    from .eventer import EventHandler  # pragma: no cover
    from .models.incoming import IncomingDiscordInteraction  # pragma: no cover
    from .response import DiscordResponse  # pragma: no cover


class EventTypes(str, Enum):
    COMMAND = "command"
    COMPONENT = "component"


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
        self.callbacks = {"command": {}, "component": {}}

        self._cache_router = router

    @logger.catch(reraise=True)
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
        if new_bot_token is None:
            _bot_token = self._bot_token
        else:
            _bot_token = new_bot_token
        if new_application_id is None:
            _application_id = self._application_id
        else:
            _application_id = new_application_id
        self._registrator = RegisterCommands(
            application_id=_application_id, bot_token=_bot_token
        )
        self._bot_token = _bot_token
        self._application_id = _application_id

        return True

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

    @logger.catch(reraise=True, message="Issue with getting commands from Discord")
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
        if guild_only:
            if not guild_id_passed or not isinstance(guild_id_passed, str):
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

    @logger.catch(reraise=True, message="Issue with editing commands from Discord")
    def edit_command(
        self,
        new_command: typing.Union[typing.List[DiscordCommand], DiscordCommand],
        command_id: int = None,
        bulk=False,
        guild_only=False,
        guild_id_passed=False,
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

        if guild_only:
            if not guild_id_passed:
                raise TypeError(
                    "You cannot have guild_only set to True and NOT pass any guild id."
                )
            if bulk:
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

            if bulk:
                return [DiscordCommand(**x) for x in _send_request.json()]
            else:
                return DiscordCommand(**_send_request.json())
        except DiscordAPIError:
            logger.exception("Discord API Failure.")
            return False

    @logger.catch(reraise=True, message="Issue with deleting commands from Discord")
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
        if guild_only:
            if not guild_id_passed:
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

    def set_command_permission(
        self, command_id, guild_id, new_permissions: "NewApplicationPermission"
    ) -> bool:
        """Set a permissions for a command in a specific guild. This function is sync!

        Args:
            command_id (int): Command ID
            guild_id (int): Guild ID
            new_permissions (NewApplicationPermission): Permissions for this command.

        Returns:
            [bool]: True, if the command has been successfully edited.
        """
        with httpx.Client() as client:
            try:

                _set_command_permissions = client.put(
                    f"https://discord.com/api/v8/applications/{self._application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
                    json=new_permissions.dict(),
                    headers={"Authorization": f"Bot {self._bot_token}"},
                )
                _set_command_permissions.raise_for_status()
                return True
            except httpx.HTTPError:
                logger.exception(
                    f"Unable to set permission for command {command_id} for guild {guild_id}"
                )
                logger.debug(
                    f"request: {_set_command_permissions.status_code}: {_set_command_permissions.text}"
                )
                return False

    async def async_set_command_permission(
        self, command_id, guild_id, new_permissions: "NewApplicationPermission"
    ) -> bool:
        """Set a permissions for a command in a specific guild. This function is async!

        Args:
            command_id (int): Command ID
            guild_id (int): Guild ID
            new_permissions (NewApplicationPermission): Permissions for this command.

        Returns:
            [bool]: True, if the command has been successfully edited.
        """
        async with httpx.AsyncClient() as client:
            try:

                _set_command_permissions = await client.put(
                    f"https://discord.com/api/v8/applications/{self._application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
                    data=new_permissions.dict(),
                    headers={"Authorization": f"Bot {self._bot_token}"},
                )
                _set_command_permissions.raise_for_status()
                return True
            except httpx.HTTPError:
                logger.exception(
                    f"Unable to set permission for command {command_id} for guild {guild_id}"
                )
                return False

    async def send_deferred_message(
        self,
        original_context: "IncomingDiscordInteraction",
        new_message: "DiscordResponse",
    ):
        """Send a deferred message.

        Args:
            original_context (IncomingDiscordInteraction): The orginal context of the message.
            new_message (DiscordResponse): Message to send.
        """
        async with httpx.AsyncClient(
            base_url=f"https://discord.com/api/v8/webhooks/{self._application_id}/{original_context.token}/messages/",
            headers={
                "Authorization": f"Bot {self._bot_token}",
                "Content-Type": "application/json",
            },
        ) as client:
            try:
                # TODO: Probably change later to inside the DeferredResponse?
                new_message._switch_to_followup_message()
                response = await client.patch("/@original", json=new_message.response)
                response.raise_for_status()
            except httpx.HTTPError:
                logger.exception(
                    f"Unable to send deferred message with error: {response.text}"
                )

    async def async_get_command_permission_in_guild(
        self, command_id, guild_id
    ) -> GuildApplicationCommandPermissions:
        """Return permissions for a single command in a guild. If no permissions are available, it will return None.

        Args:
            command_id (typing.Union[str, int]): Command ID
            guild_id (typing.Union[str, int]): Guild ID

        Returns:
            GuildApplicationCommandPermissions: Return if permissions exist.
            None: Return if no permissions exist.
        """
        async with httpx.AsyncClient() as client:
            try:
                _request_command_permission = await client.get(
                    f"https://discord.com/api/v8/applications/{self._application_id}/guilds/{guild_id}/commands/{command_id}/permissions"
                )
                if _request_command_permission.status_code == 404:
                    return None
                else:
                    _request_command_permission.raise_for_status()
                return GuildApplicationCommandPermissions(
                    **_request_command_permission.json()
                )
            except httpx.HTTPError:
                logger.exception(
                    f"Unable to get command permission! {_request_command_permission.status_code}"
                )

    async def async_get_all_command_permissions_in_guild(
        self, guild_id
    ) -> typing.List[GuildApplicationCommandPermissions]:
        """Return permissions for all commands in a guild.

        Args:
            guild_id (typing.Union[str, int]): ID of guild.

        Returns:
            typing.List[GuildApplicationCommandPermissions]: Permissions for all commands (if any permissions exist.)
        """
        async with httpx.AsyncClient() as client:
            try:
                _request_command_permission = await client.get(
                    f"https://discord.com/api/v8/applications/{self._application_id}/guilds/{guild_id}/commands/permissions"
                )
                _request_command_permission.raise_for_status()
                return [
                    GuildApplicationCommandPermissions(**x)
                    for x in _request_command_permission.json()
                ]
            except httpx.HTTPError:
                logger.exception(
                    f"Unable to get command permission! {_request_command_permission.status_code}"
                )

    def get_all_command_permissions_in_guild(
        self, guild_id: typing.Union[str, int]
    ) -> typing.List[GuildApplicationCommandPermissions]:
        """Return permissions for all commands in a guild.

        Args:
            guild_id (typing.Union[str, int]): ID of guild.

        Returns:
            typing.List[GuildApplicationCommandPermissions]: Permissions for all commands (if any permissions exist.)
        """
        with httpx.Client() as client:
            try:
                _request_command_permission = client.get(
                    f"https://discord.com/api/v8/applications/{self._application_id}/guilds/{guild_id}/commands/permissions",
                    headers={"Authorization": f"Bot {self._bot_token}"},
                )
                _request_command_permission.raise_for_status()
                return [
                    GuildApplicationCommandPermissions(**x)
                    for x in _request_command_permission.json()
                ]
            except httpx.HTTPError:
                logger.exception(
                    f"Unable to get command permission! {_request_command_permission.status_code}"
                )

    def get_command_permission_in_guild(
        self, command_id: typing.Union[str, int], guild_id: typing.Union[str, int]
    ) -> GuildApplicationCommandPermissions:
        """Return permissions for a single command in a guild. If no permissions are available, it will return None.

        Args:
            command_id (typing.Union[str, int]): Command ID
            guild_id (typing.Union[str, int]): Guild ID

        Returns:
            GuildApplicationCommandPermissions: Return if permissions exist.
            None: Return if no permissions exist.
        """
        with httpx.Client() as client:
            try:
                _request_command_permission = client.get(
                    f"https://discord.com/api/v8/applications/{self._application_id}/guilds/{guild_id}/commands/{command_id}/permissions",
                    headers={"Authorization": f"Bot {self._bot_token}"},
                )
                if _request_command_permission.status_code == 404:
                    return None
                else:
                    _request_command_permission.raise_for_status()
                return GuildApplicationCommandPermissions(
                    **_request_command_permission.json()
                )
            except httpx.HTTPError:
                logger.exception(
                    f"Unable to get command permission! {_request_command_permission.status_code} {_request_command_permission.text}"
                )

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

    def run(
        self,
        port: int = None,
        unix_socket: str = None,
        bind_to_ip_address: str = None,
        supress_insecure_binding_warning: bool = False,
    ):
        """Runs the bot with the already-installed Uvicorn webserver.

        Args:
            port (int, optional): Run the bot on a specific port.
            unix_socket (str, optional): [description]. Run the bot and listen on a specific unix domain socket..

        Raises:
            ArgumentError: [description]
        """
        uvicorn = self._return_uvicorn_run_function()

        if unix_socket and port:
            raise ValueError("You cannot bind to port AND a unix socket")
        else:
            if port:
                if bind_to_ip_address:
                    if supress_insecure_binding_warning == False:
                        warnings.warn(
                            "Binding to a IP Address other than 127.0.0.1 may not be secure! If you are exposing this service to the outside world -- a reverse proxy is strongly recommended.",
                            InsecureBindingWithCustomHostWarning,
                        )
                    uvicorn.run(
                        app=self.referenced_application,
                        host=bind_to_ip_address,
                        port=port,
                    )
                else:
                    uvicorn.run(app=self.referenced_application, port=port)
            elif unix_socket:
                if "unix" not in unix_socket:
                    unix_socket = f"unix:{unix_socket}"
                else:
                    uvicorn.run(self.referenced_application, host=unix_socket)
            if not unix_socket and not port:
                raise ValueError("You must specify a port or unix socket")

    def on(
        self,
        event: str,
        type: EventTypes = EventTypes.COMMAND,
        func: typing.Callable = None,
    ):
        """A wrapper over an async function, registers it in .callbacks.

        Args:
            event (str): Event name
            type (EventTypes): Type of this event.
            func (None, optional): function to wrap around

        Returns:
            <function>: returns the wrapped function
        """

        if not isinstance(type, EventTypes):
            if isinstance(type, str):  # pragma: no cover
                logger.warning(
                    "Passing a unknown EventType, this may cause issues and is unsupported"
                )  # noqa
            else:
                # TODO: Maybe it's not good to overrwrite a default python function. Maybe change type to a different value?
                raise InvalidEventType(type)  # pragma: no cover

        def on(func):
            self._add_function_to_callbacks(event, type, func)
            return func

        return on(func) if func else on

    def check_event_exists(self, event: str, type: str) -> bool:
        """Checks if the event in ``.callbacks``

        Args:
            event (str): event name

        Returns:
            bool: returns if the event is in callbacks.
        """
        return event in self.callbacks[type]

    def return_event_settings(self, event: str, type: str) -> dict:
        if self.check_event_exists(event, type):
            return self.callbacks[type][event]["settings"]
        raise TypeError(
            f"Event {event} is not in callbacks. Did you register this event?"
        )

    def return_event_function(self, event: str, type: str) -> dict:
        if self.check_event_exists(event, type):
            return self.callbacks[type][event]["function"]
        raise TypeError(
            f"Event {event} is not in callbacks. Did you register this event?"
        )

    def view_event_function_return_type(self, event: str, type: str) -> dict:
        """Get type hint for event functions

        Args:
            event (str): Event name

        Returns:
            dict: Returns .get_type_hints for event
        """
        return typing.get_type_hints(self.callbacks[type][event]["function"])

    async def emit(self, event: str, type: str, *args, **kwargs):
        """'Emits' an event. It will basically call the function from .callbacks and return the function result

        Args:
            event (str): Event name
            type (str): Event type
            *args: extra arguments to pass
            **kwargs: extra kwargs to pass

        Returns:
            function result: returns the function result

        Raises:
            TypeError: raises if event is not registered.
        """
        if event not in self.callbacks[type]:
            raise TypeError(
                f"event {event} does not have a corresponding handler. Did you register this function/event?"
            )

        _look_up_function = self.return_event_function(event, type)
        return await _look_up_function(*args, **kwargs)

    def _add_function_to_callbacks(
        self, function_name: str, function_type: EventTypes, function: typing.Callable
    ):
        if not inspect.iscoroutinefunction(function):
            raise TypeError("Passed function is not an asynchronous function.")

        if not isinstance(function_type, (EventTypes, str)):
            raise TypeError(
                f"Passed function is not the correct type. Expected a <str> but received {type(function_type)}"
            )

        if function_name in self.callbacks[function_type]:
            raise TypeError(f"{function_name} ({function_type}) is already registered.")
        else:
            logger.debug(f"Adding {function_name} ({function_type}) to callbacks..")
            self.callbacks[function_type][function_name] = {
                "settings": {},
                "function": function,
            }

    def register_event_command(
        self,
        function_event_name: str,
        function: typing.Callable,
        function_type: EventTypes = None,
        **kwargs,
    ):
        if function_type is None:
            # try to see if the function has a _event_type attribute
            try:
                function_type = function._dispike_event_type
            except AttributeError:
                raise AttributeError(
                    "Unable to find function event type attribute inside function.. Did you add a decorator to this function?"
                )
        else:
            if isinstance(function_type, EventTypes):
                function_type = function_type

        self._add_function_to_callbacks(
            function_name=function_event_name,
            function_type=function_type,
            function=function,
        )

    def register_collection(
        self,
        collection: "EventCollection",
        register_command_with_discord: bool = False,
        initialze_on_load: bool = False,
        initalization_arguments: typing.Dict = None,
    ):
        """Registers a EventCollection.

        Args:
            collection (EventCollection): The collection to register.
        """

        if initialze_on_load:
            collections = collection(**initalization_arguments)

        _load_in_functions = self._detect_functions_with_event_decorator(
            collection=collections,
        )

        # TODO: Maybe re-enable this as a fallback?
        """
        for shallow_function in collections.registered_commands():
            self._add_function_to_callbacks(
                function=shallow_function,
                function_name=shallow_function._dispike_event_name,
                function_type=shallow_function._dispike_event_type,
            )
        """

        for shallow_function in _load_in_functions:
            self._add_function_to_callbacks(
                function=shallow_function,
                function_name=shallow_function._dispike_event_name,
                function_type=shallow_function._dispike_event_type,
            )

        if register_command_with_discord:
            for command in collection.command_schemas():
                if isinstance(command, PerCommandRegistrationSettings):
                    self.register(
                        command=command.schema,
                        guild_only=True,
                        guild_to_target=command.guild_id,
                    )
                else:
                    self.register(command=command)

    def clear_all_event_callbacks(self, event_type: "EventTypes" = None):
        """Clears all event callbacks."""
        if not event_type:
            self.callbacks = {}
        else:
            self.callbacks[event_type] = {}

    @staticmethod
    def _detect_functions_with_event_decorator(collection: EventCollection):
        # check if colleciton inherited from EventCollection
        if isinstance(collection, EventCollection) or issubclass(
            collection, EventCollection
        ):
            _funcs = [
                function
                for function in collection.__dict__.values()
                if hasattr(function, "_dispike_event_type")
            ]

            if len(_funcs) == 0:
                raise ValueError(
                    f"{collection} contains no functions that have the interactions decorator."
                )
            return _funcs
        raise TypeError("Collection passed must subclass EventCollection.")
