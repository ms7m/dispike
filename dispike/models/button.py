from pydantic import BaseModel
from enum import Enum
import dataclasses
import typing

if typing.TYPE_CHECKING:  # pragma: no cover
    static_check_init_args = dataclasses.dataclass
else:

    def static_check_init_args(cls):
        return cls


from .discord_types.component import Component, ComponentType


class ButtonStyle(int, Enum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


class Button(Component):
    type = ComponentType.BUTTON
    style: ButtonStyle = ButtonStyle.PRIMARY
    components: typing.Optional[Component] = []
