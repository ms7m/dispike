from dispike.eventer import EventTypes
from dispike.errors.events import InvalidEventType
from loguru import logger
import inspect

import typing

if typing.TYPE_CHECKING:
    from .main import Dispike  # pragma: no cover
    from dispike.creating.models.options import DiscordCommand  # pragma: no cover


def on(
    event: str,
    type: EventTypes = EventTypes.COMMAND,
    func: typing.Callable = None,
):
    """A proxy decorator for registering commands. This decorator will add a number of attributes within the object.
    You can use this decorator to register commands with ``.register_command`` function on the main Dispike object.

    Args:
        event (str): Event callback name, usually the discord command name.
        type (EventTypes, optional): The event type. Defaults to EventTypes.COMMAND.
        func (typing.Callable, optional): Function, will automatically be added if a decorator..

    Raises:
        InvalidEventType: If invalid EventType. Will not raise if it's a string.

    Returns:
        typing.Callable: A function with the attributes added.
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
        if not inspect.iscoroutinefunction(func):
            pass
            # raise TypeError("Function must be a async function.")
        func._dispike_event_type = type
        func._dispike_event_name = event
        return func

    return on(func) if func else on


class PerCommandRegistrationSettings(object):
    """Allows for per-basis configuration of a command."""

    def __init__(self, schema: "DiscordCommand", guild_id: str = None):
        self.schema = schema
        self.guild_id = guild_id


class EventCollection(object):
    """Base object to inherit to help developers keep similar commands in a group."""

    @staticmethod
    def command_schemas() -> typing.List[
        typing.Union[PerCommandRegistrationSettings, "DiscordCommand"]
    ]:
        """Function to return list of DiscordCommands or PerCommandRegistrationSettings objects.

            Returns:
                List[
            typing.Union[PerCommandRegistrationSettings, "DiscordCommand"]
        ]: ...
        """
        return []

    @staticmethod
    def registered_commands() -> typing.List[typing.Callable]:
        """Function to return list of event callbacks. Usually not used, Dispike will automatically find functions with the interactions decorator.

        Returns:
            typing.List[typing.Callable]: Functions.
        """
        return []
