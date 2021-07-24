from dispike.eventer import EventTypes
from dispike.errors.events import InvalidEventType
from loguru import logger
import inspect

import typing

if typing.TYPE_CHECKING:
    from .main import Dispike
    from dispike.register.models.options import DiscordCommand


def _shallow_on(
    event: str,
    type: EventTypes = EventTypes.COMMAND,
    guild_id: str = None,
    func: typing.Callable = None,
):
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


on = _shallow_on


class PerCommandRegistrationSettings(object):
    def __init__(self, schema: "DiscordCommand", guild_id: str):
        self.schema = schema
        self.guild_id = guild_id


class EventCollection(object):
    @staticmethod
    def command_schemas() -> typing.List[
        typing.Union[PerCommandRegistrationSettings, "DiscordCommand"]
    ]:
        return []

    @staticmethod
    def registered_commands(self) -> typing.List[typing.Callable]:
        return []
