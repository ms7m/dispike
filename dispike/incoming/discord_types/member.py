from pydantic import BaseModel

from datetime import datetime

import typing

try:
    from typing import Literal  # pragma: no cover
except ImportError:  # pragma: no cover
    # backport
    from typing_extensions import Literal  # pragma: no cover

from .user import User


class Member(BaseModel):

    """A representation of a discord member, intended for you to easily access attributes. this is not intended for you to edit, and will not
    be accepted as an argument in any function.
    """

    class Config:
        arbitrary_types_allowed = True

    user: User
    roles: typing.List[str]
    premium_since: typing.Union[
        None, str, int
    ]  # ? Discord docs doesn't talk about this so..
    permissions: str
    pending: bool
    nick: typing.Union[None, str]
    mute: bool
    joined_at: datetime
    deaf: bool
