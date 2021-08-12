from dispike.errors.events import InvalidEventType
import typing
from loguru import logger
import inspect
from enum import Enum


class EventTypes(str, Enum):
    COMMAND = "command"
    COMPONENT = "component"
    MESSAGE_COMMAND = "message_command"
    USER_COMMAND = "user_command"
