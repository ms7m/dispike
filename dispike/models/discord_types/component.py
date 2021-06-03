from pydantic import BaseModel, HttpUrl, constr
from enum import Enum
import dataclasses
import typing
from .emoji import PartialEmoji

if typing.TYPE_CHECKING:  # pragma: no cover
    static_check_init_args = dataclasses.dataclass
else:

    def static_check_init_args(cls):
        return cls


try:
    from typing import Literal  # pragma: no cover
except ImportError:  # pragma: no cover
    # backport
    from typing_extensions import Literal  # pragma: no cover


class ComponentType(int, Enum):
    ACTION_ROW = 1
    BUTTON = 2


class Component(BaseModel):
    type: ComponentType
    style: typing.Optional[int]
    label: typing.Optional[constr(max_length=80)]
    emoji: typing.Optional[PartialEmoji]
    custom_id: typing.Optional[str]
    url: typing.Optional[HttpUrl]
    disabled: typing.Optional[bool] = False
