from pydantic import BaseModel
import typing

try:
    from typing import Literal  # pragma: no cover
except ImportError:  # pragma: no cover
    # backport
    from typing_extensions import Literal  # pragma: no cover


class User(BaseModel):

    """A representation of a User object from discord. this is not intended for you to edit, and will not
    be accepted as an argument in any function.
    """

    class Config:
        arbitary_types_allowed = True

    id: int
    username: str
    avatar: typing.Union[None, str]
    discriminator: str
    public_flags: int
