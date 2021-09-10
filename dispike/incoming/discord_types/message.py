from pydantic import BaseModel

import typing

try:
    from typing import Literal  # pragma: no cover
except ImportError:  # pragma: no cover
    # backport
    from typing_extensions import Literal  # pragma: no cover

from .user import User


class MessageAttachment(BaseModel):
    """
    A message attachment
    """

    id: str
    filename: str
    content_type: str
    size: int
    url: str
    proxy_url: str
    height: int = None
    width: int = None


class Message(BaseModel):

    """A representation of a discord message, intended for you to easily access attributes. this is not intended for you to edit, and will not
    be accepted as an argument in any function.
    """

    class Config:
        arbitrary_types_allowed = True

    # TODO: Make this a lot better, there is lots of unimplemented stuff here...

    attachments: typing.List[MessageAttachment]
    author: User
    channel_id: str
    # components:
    content: str
    edited_timestamp: str = None
    # embeds
    flags: int
    id: int
    mention_everyone: bool
    # mention_roles:
    # mentsions
    pinned: bool
    timestamp: str
    tts: bool
    type: int
