from pydantic import BaseModel

from datetime import datetime

import typing

try:
    from typing import Literal
except ImportError:
    # backport
    from typing_extensions import Literal

from .user import User


class Member(BaseModel):
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
