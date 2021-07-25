from dispike.errors.events import InvalidEventType
import typing
from loguru import logger
import inspect
from enum import Enum


class EventTypes(str, Enum):
    COMMAND = "command"
    COMPONENT = "component"
