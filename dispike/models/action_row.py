from .discord_types.component import Component, ComponentType
from pydantic import BaseModel
from enum import Enum
import dataclasses
import typing

if typing.TYPE_CHECKING:  # pragma: no cover
    static_check_init_args = dataclasses.dataclass
else:

    def static_check_init_args(cls):
        return cls


class ActionRowComponents(Component):
    components: typing.List[Component]


class ActionRow(Component):
    type = ComponentType.ACTION_ROW
    components: typing.List[ActionRowComponents]