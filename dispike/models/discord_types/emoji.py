from pydantic import BaseModel
from enum import Enum
import dataclasses
import typing

if typing.TYPE_CHECKING:  # pragma: no cover
    static_check_init_args = dataclasses.dataclass
else:

    def static_check_init_args(cls):
        return cls


@static_check_init_args
class PartialEmoji(BaseModel):
    """Parital Emoji type, this is typically used in a Button Component"""

    name: str
    id: str
    animated: bool